#!/usr/bin/env python3
"""Découpe un enregistrement d'Omar (plusieurs Shorts lus d'un coup, avec reprises) en une voix propre par Short.

    python3 scripts/voix_omar.py videos/_shorts/<lot>/voix/decoupe.json

decoupe.json : {"enregistrement": "omar-15nov.m4a", "fiches": ["../l10v-livre.json", ...]}  (chemins relatifs au dossier voix/,
fiches dans l'ordre où Omar les a lues).

1. Transcription mot à mot (faster-whisper, français).
2. Chaque phrase attendue (plans + fin de chaque fiche) est cherchée dans la transcription ; quand Omar a repris une phrase,
   on garde la meilleure prise (à égalité : la dernière). L'ordre des phrases est respecté (programmation dynamique).
3. Chaque Short = ses phrases recollées avec des respirations courtes (pas de pauses à rallonge), son nettoyé, -16 LUFS.
4. Minutage mot à mot écrit avec les mots DE LA FICHE (sous-titres, chiffres chocs et découpe des plans restent justes).

Sorties dans voix/ : <id>.mp3, <id>.mots.json, rapport.md (prises gardées, scores, transcription complète).
"""
import json, re, subprocess, sys, tempfile, unicodedata, difflib
from pathlib import Path

from num2words import num2words
from rapidfuzz import fuzz

PAUSE_PHRASE = 0.14     # entre deux phrases d'un même plan
PAUSE_PLAN = 0.22       # entre deux plans
MARGE_AVANT, MARGE_APRES = 0.07, 0.10
SEUIL = 62              # score minimal (0-100) pour accepter une prise


def sh(*cmd):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"{cmd[0]} a échoué :\n{r.stderr[-2000:]}")
    return r.stdout


def _sans_accents(t):
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")


def _nombre(m):
    s = m.group(0)
    if re.fullmatch(r"\d+[.,]\d+", s):
        a, b = re.split(r"[.,]", s)
        return f" {num2words(int(a), lang='fr')} {num2words(int(b), lang='fr')} "
    return f" {num2words(int(s), lang='fr')} "


def canon(texte):
    """Texte → jetons comparables (chiffres en lettres, sigles épelés, sans accents ni ponctuation)."""
    t = texte.replace("’", "'").replace(" ", " ")
    t = re.sub(r"\b1er\b", "premier", t)
    t = re.sub(r"(?<=\d) (?=\d{3}\b)", "", t)                 # 2 000 → 2000
    t = re.sub(r"\b([A-Z]{2,4})\b", lambda m: " ".join(m.group(1)), t)  # TVA → T V A
    t = t.replace("€", " euros ").replace("%", " pour cent ")
    t = re.sub(r"\d+(?:[.,]\d+)?", _nombre, t)
    t = _sans_accents(t.lower()).replace("-", " ").replace("'", " ")
    return ["euro" if x == "euros" else x for x in re.findall(r"[a-z]+", t)]


def phrases(texte):
    return [p.strip() for p in re.split(r"(?<=[.?!…])\s+", texte.strip()) if p.strip()]


# ---------- entrée ----------
cfg_chemin = Path(sys.argv[1]).resolve()
dossier = cfg_chemin.parent
cfg = json.loads(cfg_chemin.read_text(encoding="utf-8"))
enreg = dossier / cfg["enregistrement"]
fiches = [(dossier / f).resolve() for f in cfg["fiches"]]
tmp = Path(tempfile.mkdtemp(prefix="voix-omar-"))

wav16 = tmp / "a16.wav"
wav48 = tmp / "a48.wav"
sh("ffmpeg", "-y", "-i", enreg, "-ac", "1", "-ar", "16000", wav16)
sh("ffmpeg", "-y", "-i", enreg, "-ac", "1", "-ar", "48000", wav48)

# phrases attendues, dans l'ordre de lecture
attendu = []  # (fiche_i, morceau_i, texte)
for fi, f in enumerate(fiches):
    d = json.loads(f.read_text(encoding="utf-8"))
    morceaux = [p["texte"] for p in d["plans"]] + ([d["fin"]] if d.get("fin") else [])
    for mi, m in enumerate(morceaux):
        for p in phrases(m):
            attendu.append((fi, mi, p))

# ---------- 1. transcription ----------
from faster_whisper import WhisperModel
modele = WhisperModel(cfg.get("modele", "medium"), device="cpu", compute_type="int8")
# découpage par silences (VAD) : sans lui, Whisper « avale » les reprises et étire un mot sur 10 s
segs, _ = modele.transcribe(str(wav16), language="fr", word_timestamps=True, beam_size=5,
                            vad_filter=True, vad_parameters={"min_silence_duration_ms": 250, "speech_pad_ms": 120},
                            condition_on_previous_text=False)
mots_t = []
for s in segs:
    for w in s.words or []:
        mots_t.append({"texte": w.word.strip(), "debut": float(w.start), "fin": float(w.end)})
if not mots_t:
    raise SystemExit("Transcription vide.")
(dossier / "transcription.json").write_text(json.dumps(mots_t, ensure_ascii=False, indent=0), encoding="utf-8")
print("TRANSCRIPTION :", " ".join(f"[{w['debut']:.1f}]{w['texte']}" for w in mots_t), flush=True)
# jetons de la transcription, chacun rattaché à son mot (minutage partagé à parts égales)
jetons = []  # (jeton, i_mot, debut, fin)
for i, w in enumerate(mots_t):
    c = canon(w["texte"])
    for k, j in enumerate(c):
        d = (w["fin"] - w["debut"]) / max(len(c), 1)
        jetons.append((j, i, w["debut"] + k * d, w["debut"] + (k + 1) * d))
TJ = [j[0] for j in jetons]

# ---------- 2. prises candidates par phrase ----------
candidats = []
for (fi, mi, p) in attendu:
    ref = canon(p)
    n = len(ref)
    trouves = []
    for a in range(len(TJ)):
        for L in range(max(1, int(n * 0.7)), int(n * 1.4) + 2):
            b = a + L
            if b > len(TJ):
                break
            r_, w_ = " ".join(ref), " ".join(TJ[a:b])
            sc = 0.5 * fuzz.ratio(r_, w_) + 0.5 * fuzz.token_sort_ratio(r_, w_)  # « 7,50 € » = « sept euros cinquante »
            # un « mot » de plus de 1,3 s cache presque toujours une reprise avalée par la transcription
            if any(jetons[q][3] - jetons[q][2] > 1.3 for q in range(a, b)):
                sc -= 30
            if sc >= SEUIL:
                trouves.append((sc, a, b))
    # on garde la meilleure fenêtre parmi celles qui se chevauchent
    trouves.sort(reverse=True)
    gardes = []
    for sc, a, b in trouves:
        if all(b <= a2 or a >= b2 for _, a2, b2 in gardes):
            gardes.append((sc, a, b))
    candidats.append(sorted(gardes, key=lambda x: x[1]))
    if not gardes:
        print(f"⚠ phrase introuvable : « {p} »", flush=True)

# ---------- 3. choix des prises (ordre respecté, meilleure prise, la dernière à égalité) ----------
# Chaque phrase peut aussi être « absente » (forte pénalité) : une phrase ratée ne bloque pas tout le reste.
ABSENT = -60.0
etats = []  # par phrase : liste de (score_cumulé, précédent, fin_jeton) ; l'option absente garde la fin précédente
for k, cands in enumerate(candidats):
    ligne = []
    prec_lignes = etats[k - 1] if k else [(0.0, None, 0, None)]
    for c_i, (sc, a, b) in enumerate(cands):
        poss = [(v[0], j) for j, v in enumerate(prec_lignes) if v[2] <= a]
        if poss:
            best = max(poss)
            ligne.append((best[0] + sc + 0.02 * jetons[a][2], best[1], b, c_i))
    # absent : on reprend chaque état précédent tel quel
    for j, v in enumerate(prec_lignes):
        ligne.append((v[0] + ABSENT, j, v[2], None))
    etats.append(ligne)
choix = [None] * len(candidats)
j = max(range(len(etats[-1])), key=lambda i: etats[-1][i][0])
for k in range(len(candidats) - 1, -1, -1):
    choix[k] = etats[k][j][3]
    j = etats[k][j][1]
manquantes = [attendu[k][2] for k in range(len(attendu)) if choix[k] is None]
for m in manquantes:
    print(f"⚠ phrase non retrouvée, à réenregistrer : « {m} »", flush=True)

# ---------- 4. montage de chaque Short ----------
rapport = ["# Découpe de la voix d'Omar", "", f"Enregistrement : `{cfg['enregistrement']}`", "",
           "| Short | Phrase attendue | Score | Prise (s) | Ce qu'Omar a dit |", "|---|---|---|---|---|"]
FILTRE = ("highpass=f=80,afftdn=nf=-30,"
          "acompressor=threshold=-20dB:ratio=2.5:attack=6:release=90:makeup=2,"
          "loudnorm=I=-16:TP=-1.5:LRA=7")
for fi, f in enumerate(fiches):
    d = json.loads(f.read_text(encoding="utf-8"))
    ks = [k for k, (fi2, _, _) in enumerate(attendu) if fi2 == fi]
    morceaux_cliques, t_sortie, mots_sortie, liste = [], 0.0, [], []
    for n_k, k in enumerate(ks):
        _, mi, p = attendu[k]
        if choix[k] is None:
            rapport.append(f"| {d['id']} | {p} | — | absente | (non retrouvée) |")
            continue
        sc, a, b = candidats[k][choix[k]]
        i_deb, i_fin = jetons[a][1], jetons[b - 1][1]
        debut = mots_t[i_deb]["debut"]; fin = mots_t[i_fin]["fin"]
        avant = mots_t[i_deb - 1]["fin"] if i_deb > 0 else 0.0
        apres = mots_t[i_fin + 1]["debut"] if i_fin + 1 < len(mots_t) else fin + 1
        c0 = max(debut - MARGE_AVANT, (avant + debut) / 2, 0.0)
        c1 = min(fin + MARGE_APRES, (fin + apres) / 2)
        clip = tmp / f"c{fi}_{n_k}.wav"
        sh("ffmpeg", "-y", "-ss", f"{c0:.3f}", "-to", f"{c1:.3f}", "-i", wav48,
           "-af", f"afade=t=in:d=0.012,afade=t=out:st={max(c1 - c0 - 0.02, 0):.3f}:d=0.02", clip)
        # minutage : mots de la fiche calés sur les jetons transcrits (alignement des jetons)
        ref_mots = []
        for m in p.split():  # ponctuation isolée (« combien ? ») collée au mot d'avant
            if ref_mots and not re.search(r"\w", m):
                ref_mots[-1] += " " + m
            else:
                ref_mots.append(m)
        ref_jet = [(canon(m), m) for m in ref_mots]
        flat = [(j, wi) for wi, (c, _) in enumerate(ref_jet) for j in c]
        seg = jetons[a:b]
        sm = difflib.SequenceMatcher(a=[x[0] for x in flat], b=[x[0] for x in seg], autojunk=False)
        temps = {}
        for blk in sm.get_matching_blocks():
            for q in range(blk.size):
                wi = flat[blk.a + q][1]
                t0, t1 = seg[blk.b + q][2], seg[blk.b + q][3]
                lo, hi = temps.get(wi, (t0, t1))
                temps[wi] = (min(lo, t0), max(hi, t1))
        # mots non retrouvés : interpolés entre voisins
        connus = sorted(temps)
        for wi in range(len(ref_mots)):
            if wi in temps:
                continue
            g = max([x for x in connus if x < wi], default=None)
            dr = min([x for x in connus if x > wi], default=None)
            t0 = temps[g][1] if g is not None else debut
            t1 = temps[dr][0] if dr is not None else fin
            if t1 <= t0:
                t1 = t0 + 0.12
            temps[wi] = (t0, t1)
        for wi, m in enumerate(ref_mots):
            t0, t1 = temps[wi]
            mots_sortie.append({"texte": m, "debut": round(t_sortie + max(t0 - c0, 0), 3),
                                "fin": round(t_sortie + max(t1 - c0, 0.05), 3)})
        morceaux_cliques.append(clip)
        t_sortie += c1 - c0
        # pause après la phrase
        suivant = attendu[ks[n_k + 1]][1] if n_k + 1 < len(ks) else None
        if suivant is not None:
            pause = PAUSE_PHRASE if suivant == mi else PAUSE_PLAN
            sil = tmp / f"s{fi}_{n_k}.wav"
            sh("ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", f"{pause:.3f}", sil)
            morceaux_cliques.append(sil)
            t_sortie += pause
        dit = " ".join(mots_t[i]["texte"] for i in range(i_deb, i_fin + 1))
        rapport.append(f"| {d['id']} | {p} | {sc:.0f} | {c0:.2f}–{c1:.2f} | {dit} |")
    liste_f = tmp / f"liste{fi}.txt"
    liste_f.write_text("".join(f"file '{c}'\n" for c in morceaux_cliques))
    brut = tmp / f"brut{fi}.wav"
    sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", liste_f, "-c", "copy", brut)
    sortie = dossier / f"{d['id']}.mp3"
    sh("ffmpeg", "-y", "-i", brut, "-af", FILTRE, "-ar", "48000", "-c:a", "libmp3lame", "-q:a", "2", sortie)
    (dossier / f"{d['id']}.mots.json").write_text(json.dumps(mots_sortie, ensure_ascii=False, indent=1), encoding="utf-8")
    duree = float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", sortie))
    print(f"✔ {d['id']} : {duree:.1f} s", flush=True)
    rapport.append(f"| **{d['id']}** | **durée finale** | | **{duree:.1f} s** | |")

rapport += ["", "## Transcription complète", "",
            " ".join(f"[{w['debut']:.1f}] {w['texte']}" if i % 12 == 0 else w["texte"] for i, w in enumerate(mots_t))]
(dossier / "rapport.md").write_text("\n".join(rapport) + "\n", encoding="utf-8")
print("\n".join(rapport))
