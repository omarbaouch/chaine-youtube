#!/usr/bin/env python3
"""Fabrique un YouTube Short vertical (1080x1920) autonome à partir d'une fiche JSON.

    python3 scripts/short_vertical.py videos/_shorts/lot1/01-plein.json [--test]

Fiche :
  id, titre (YouTube), accroche (bandeau du haut, visible tout le Short),
  plans: [{texte, recherche: [mots-clés anglais...], chiffre?: "≈ 50 €", pixabay_id?: [...]}],
  fin (phrase d'abonnement, lue), description, commentaire, sources.

Chaîne : voix Edge Vivienne lue d'un seul souffle (minutage mot à mot) → rushes Pixabay plein écran (un plan toutes
les ~3 s, léger zoom) → sous-titres mot à mot, chiffre choc, bandeau → bruitages + musique → -14 LUFS.
--test : sans réseau (voix muette, faux rushes) pour vérifier la mise en page.
"""
import json, os, re, subprocess, sys, tempfile, random, math, shutil, urllib.parse
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
W, H, FPS = 1080, 1920, 30
VOIX = "fr-FR-VivienneMultilingualNeural"
POLICE = "Poppins"
DOSSIER_POLICES = RACINE / "fonts"
MAX_PLAN = 3.4  # secondes max sur un même rush

TEST = "--test" in sys.argv
fiche_chemin = Path([a for a in sys.argv[1:] if not a.startswith("--")][0])
fiche = json.loads(fiche_chemin.read_text(encoding="utf-8"))
sortie_dir = RACINE / "out" / "shorts"
sortie_dir.mkdir(parents=True, exist_ok=True)
SORTIE = sortie_dir / f"{fiche['id']}.mp4"
tmp = Path(tempfile.mkdtemp(prefix=f"short-{fiche['id']}-"))


def sh(*cmd):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"{cmd[0]} a échoué :\n{r.stderr[-3000:]}")
    return r.stdout


def duree(f):
    return float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f).strip())


def _norm(t):
    return re.sub(r"[\W_]+", "", t.lower())


# ---------- 1. Voix ----------
morceaux = [p["texte"] for p in fiche["plans"]] + ([fiche["fin"]] if fiche.get("fin") else [])
texte_complet = " ".join(morceaux)
voix_mp3 = tmp / "voix.mp3"
if TEST:
    mots, t = [], 0.15
    for w in texte_complet.split():
        d = 0.12 + 0.045 * len(w)
        mots.append({"texte": w, "debut": t, "fin": t + d}); t += d + 0.05
    sh("ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", f"{t + 0.3:.2f}", voix_mp3)
else:
    sys.path.insert(0, str(RACINE / "scripts"))
    from voix_edge import dire_avec_mots
    mots = dire_avec_mots(texte_complet, VOIX, str(voix_mp3), debit=fiche.get("debit", "+10%"), lang=False)
duree_voix = duree(voix_mp3)

# bornes de chaque morceau (par le compte des lettres, comme scripts/voix.py)
cibles, acc = [], 0
for m in morceaux:
    acc += len(_norm(m)); cibles.append(acc)
bornes, avant, k = [[None, None] for _ in morceaux], 0, 0
for w in mots:
    while k < len(cibles) - 1 and avant >= cibles[k]:
        k += 1
    if bornes[k][0] is None:
        bornes[k][0] = w["debut"]
    bornes[k][1] = w["fin"]
    w["plan"] = k
    avant += len(_norm(w["texte"]))
for i, b in enumerate(bornes):  # repli : morceau sans mot reconnu
    if b[0] is None:
        b[0] = bornes[i - 1][1] if i else 0.0
        b[1] = b[0] + 0.5
TOTAL = duree_voix + 0.6
# découpe temporelle : le plan i va du début de sa voix (0 pour le 1er) au début du suivant
debuts = [0.0] + [bornes[i][0] - 0.05 for i in range(1, len(morceaux))]
fins = debuts[1:] + [TOTAL]


# ---------- 2. Rushes ----------
EXCLUS = ("green screen", "greenscreen", "chroma", "cartoon", "animated", "animation", "3d", "ai generated",
          "illustration", "drawing", "render", "clipart", "background loop")
MOTS_VIDES = {"close", "up", "of", "the", "a", "an", "in", "on", "with", "and", "shot", "view", "4k", "hd"}


def pixabay(requete, deja):
    """Rush le plus PERTINENT (règle n°1 : ce qu'on voit = ce qu'on dit) : on garde l'ordre de pertinence de Pixabay
    et on exige que les mots-clés du sujet figurent dans les tags du rush. Vertical = simple départage."""
    cle = os.environ.get("PIXABAY_API_KEY")
    if not cle:
        raise RuntimeError("PIXABAY_API_KEY manquante")
    import requests
    mots_q = [m for m in re.findall(r"[a-z]+", requete.lower()) if m not in MOTS_VIDES]
    r = requests.get("https://pixabay.com/api/videos/", params={"key": cle, "q": requete, "per_page": 40,
                                                                "safesearch": "true"}, timeout=30)
    r.raise_for_status()
    meilleurs = []
    for rang, h in enumerate(r.json().get("hits", [])):
        tags = h.get("tags", "").lower()
        if h["id"] in deja or any(x in tags for x in EXCLUS):
            continue
        score = sum(1 for m in mots_q if m in tags or m.rstrip("s") in tags)
        vertical = h["videos"]["medium"]["height"] > h["videos"]["medium"]["width"]
        meilleurs.append((-score, rang - (2 if vertical else 0), h))
    meilleurs.sort(key=lambda x: (x[0], x[1]))
    if not meilleurs or -meilleurs[0][0] < len(mots_q):  # tous les mots-clés doivent être dans les tags
        return None
    h = meilleurs[0][2]
    v = h["videos"].get("large") if h["videos"].get("large", {}).get("url") else h["videos"]["medium"]
    print(f"  rush « {requete} » → {h['id']} ({h.get('tags')})", flush=True)
    return h["id"], v["url"], f"Pixabay {h['id']} — {h.get('user', '')} — {h.get('pageURL', '')}"


segments, credits, deja = [], [], set()
for i, p in enumerate(fiche["plans"] + ([{"recherche": fiche.get("recherche_fin", fiche["plans"][0]["recherche"])}] if fiche.get("fin") else [])):
    d = fins[i] - debuts[i]
    n = max(1, math.ceil(d / MAX_PLAN))
    req = p["recherche"] if isinstance(p["recherche"], list) else [p["recherche"]]
    for j in range(n):
        q = req[j % len(req)]
        f = tmp / f"rush-{i}-{j}.mp4"
        if TEST:
            teinte = (i * 3 + j) * 37 % 360
            sh("ffmpeg", "-y", "-f", "lavfi", "-i", f"testsrc2=size=1280x720:rate=30:duration=6", "-vf",
               f"hue=h={teinte}", "-pix_fmt", "yuv420p", f)
        else:
            trouve = None
            for essai in [q] + [x for x in req if x != q]:
                trouve = pixabay(essai, deja)
                if trouve:
                    break
            if not trouve and segments:  # rien de pertinent : on prolonge le plan précédent plutôt que d'en montrer un hors sujet
                segments[-1]["duree"] += d / n
                continue
            if not trouve:
                raise RuntimeError(f"Aucun rush pertinent pour {req}")
            pid, url, cred = trouve
            deja.add(pid); credits.append(cred)
            import requests
            with requests.get(url, stream=True, timeout=120) as r:
                r.raise_for_status()
                with open(f, "wb") as o:
                    for b in r.iter_content(1 << 20):
                        o.write(b)
        segments.append({"fichier": f, "debut": debuts[i] + j * d / n, "duree": d / n, "plan": i})

# ---------- 3. Image : chaque segment recadré plein écran, léger zoom, coupé net ----------
parts = []
for s_i, s in enumerate(segments):
    out = tmp / f"seg-{s_i}.mp4"
    dr = s["duree"]
    src_d = duree(s["fichier"])
    ss = max(0.0, min(src_d - dr - 0.1, src_d * 0.25))
    vitesse = "1" if src_d - ss >= dr else f"{(src_d - ss) / dr:.3f}"
    sens = 1 if s_i % 2 == 0 else -1
    z0, z1 = (1.0, 1.08) if sens > 0 else (1.08, 1.0)
    vf = (f"setpts=PTS/{vitesse},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
          f"scale=w='{W}*({z0}+({z1}-{z0})*t/{dr:.3f})':h=-2:eval=frame,crop={W}:{H},"
          f"eq=contrast=1.06:saturation=1.12,fps={FPS},format=yuv420p")
    sh("ffmpeg", "-y", "-ss", f"{ss:.2f}", "-i", s["fichier"], "-t", f"{dr:.3f}", "-an", "-vf", vf,
       "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", out)
    parts.append(out)
liste = tmp / "liste.txt"
liste.write_text("".join(f"file '{p}'\n" for p in parts))
image = tmp / "image.mp4"
sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", liste, "-c", "copy", image)


# ---------- 4. Texte à l'écran (ASS) ----------
def ts(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def esc(t):
    return t.replace("\\", "").replace("{", "(").replace("}", ")")


ass = [
    "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 0", "",
    "[V4+ Styles]",
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline,"
    " StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
    f"Style: Sous,{POLICE},100,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,7,3,5,90,90,0,1",
    f"Style: Bandeau,{POLICE},82,&H00000000,&H00000000,&H0000D7FF,&H0000D7FF,-1,0,0,0,100,100,0,0,3,22,0,8,90,90,240,1",
    f"Style: Chiffre,{POLICE},210,&H0000D7FF,&H0000D7FF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,10,6,5,60,60,0,1",
    f"Style: Fin,{POLICE},90,&H00FFFFFF,&H00FFFFFF,&H000000FF,&H000000FF,-1,0,0,0,100,100,0,0,3,22,0,5,80,80,0,1",
    "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
]
# bandeau du haut : visible dès la 1re image, tout le Short
ass.append(f"Dialogue: 2,{ts(0)},{ts(TOTAL)},Bandeau,,0,0,0,,{esc(fiche['accroche'])}")
# chiffres chocs : apparaissent quand la voix dit le nombre (premier mot-nombre du plan, ou "chiffre_mot")
NOMBRES = re.compile(r"^(z[ée]ro|une?|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|"
                     r"vingt|trente|quarante|cinquante|soixante|cent|cents|mille|moiti[ée]|quart|tiers|\d)", re.I)


def moment_chiffre(i, p):
    cle = _norm(p["chiffre_mot"]) if p.get("chiffre_mot") else None
    for w in mots:
        if w.get("plan") == i and ((cle and _norm(w["texte"]).startswith(cle)) or (not cle and NOMBRES.match(w["texte"]))):
            return w["debut"]
    return bornes[i][0] + 0.35


for i, p in enumerate(fiche["plans"]):
    p["_chiffre_t"] = moment_chiffre(i, p) if p.get("chiffre") else None
    if p.get("chiffre"):
        a = p["_chiffre_t"]
        ass.append(f"Dialogue: 3,{ts(a)},{ts(fins[i])},Chiffre,,0,0,0,,"
                   f"{{\\pos({W // 2},780)\\fscx150\\fscy150\\t(0,140,\\fscx100\\fscy100)}}{esc(p['chiffre'])}")
# fin : appel à l'abonnement
if fiche.get("fin"):
    ass.append(f"Dialogue: 3,{ts(bornes[-1][0])},{ts(TOTAL)},Fin,,0,0,0,,"
               f"{{\\pos({W // 2},780)\\fscx80\\fscy80\\t(0,160,\\fscx100\\fscy100)}}ABONNE-TOI 🔔".replace(" 🔔", ""))
# sous-titres : 3 mots max, le mot dit en jaune, petit rebond
coupures, n_l = set(), 0
for tok in texte_complet.split():
    n_l += len(_norm(tok))
    if re.search(r"[.!?,:;…]$", tok):
        coupures.add(n_l)
groupes, cur, n_l = [], [], 0
for w in mots:
    cur.append(w)
    n_l += len(_norm(w["texte"]))
    if len(cur) == 3 or n_l in coupures:
        groupes.append(cur); cur = []
if cur:
    groupes.append(cur)
for g_i, g in enumerate(groupes):
    fin_g = groupes[g_i + 1][0]["debut"] if g_i + 1 < len(groupes) else g[-1]["fin"] + 0.4
    for k_i, w in enumerate(g):
        a = w["debut"]
        b = g[k_i + 1]["debut"] if k_i + 1 < len(g) else fin_g
        txt = " ".join(("{\\c&H0000D7FF&}" + esc(x["texte"]).upper() + "{\\c&H00FFFFFF&}") if x is w
                       else esc(x["texte"]).upper() for x in g)
        pop = "\\fscx112\\fscy112\\t(0,90,\\fscx100\\fscy100)" if k_i == 0 else ""
        ass.append(f"Dialogue: 1,{ts(a)},{ts(b)},Sous,,0,0,0,,{{\\pos({W // 2},1180){pop}}}{txt}")
fichier_ass = tmp / "texte.ass"
fichier_ass.write_text("\n".join(ass) + "\n", encoding="utf-8")

# ---------- 5. Son : voix + whoosh aux coupes + pop aux chiffres + musique ----------
sfx = RACINE / "public" / "sfx"
musique = RACINE / "public" / "sfx" / "musique-enquete.wav"
entrees = ["-i", str(image), "-i", str(voix_mp3)]
filtres, mix, n_in = [], ["[1:a]volume=1.0,adelay=0|0[v]"], 2
labels = ["[v]"]
for s in segments[1:]:
    if (sfx / "whoosh.wav").exists():
        entrees += ["-i", str(sfx / "whoosh.wav")]
        mix.append(f"[{n_in}:a]volume=0.22,adelay={int(max(0, s['debut'] - 0.12) * 1000)}:all=1[w{n_in}]")
        labels.append(f"[w{n_in}]"); n_in += 1
for i, p in enumerate(fiche["plans"]):
    if p.get("chiffre") and (sfx / "impact.wav").exists():
        entrees += ["-i", str(sfx / "impact.wav")]
        mix.append(f"[{n_in}:a]volume=0.35,adelay={int(p['_chiffre_t'] * 1000)}:all=1[c{n_in}]")
        labels.append(f"[c{n_in}]"); n_in += 1
if musique.exists():
    entrees += ["-stream_loop", "-1", "-i", str(musique)]
    mix.append(f"[{n_in}:a]volume=0.10,atrim=0:{TOTAL:.2f}[m]")
    labels.append("[m]"); n_in += 1
mix.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:{TOTAL:.2f},"
           "loudnorm=I=-14:TP=-1.5:LRA=9[a]")
polices = str(DOSSIER_POLICES).replace(":", "\\:")
vf = f"[0:v]subtitles='{fichier_ass}':fontsdir='{polices}'[vo]"
sh("ffmpeg", "-y", *entrees, "-filter_complex", vf + ";" + ";".join(mix), "-map", "[vo]", "-map", "[a]",
   "-t", f"{TOTAL:.2f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
   "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", SORTIE)

(sortie_dir / f"{fiche['id']}-credits.txt").write_text("\n".join(credits) + "\n", encoding="utf-8")
# planche : 6 images pour le contrôle
planche = sortie_dir / f"{fiche['id']}-planche.jpg"
pas = TOTAL / 6
sh("ffmpeg", "-y", "-i", SORTIE, "-vf", f"fps=1/{pas:.3f},scale=270:480,tile=6x1", "-frames:v", "1", planche)
print(f"✔ {SORTIE} ({TOTAL:.1f} s, {len(segments)} plans)")
shutil.rmtree(tmp, ignore_errors=True)
