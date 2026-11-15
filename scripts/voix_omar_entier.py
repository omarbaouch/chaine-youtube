#!/usr/bin/env python3
"""Voix d'Omar enregistrée d'une traite (une prise par Short) → voix propre, qualité studio, sans aucune coupe au milieu.

    python3 scripts/voix_omar_entier.py videos/_shorts/<lot>/voix/entier.json

entier.json : {"modele": "large-v3", "prises": {"../l10o-livre.json": "livre.m4a", ...}}  (chemins relatifs au dossier voix/)
Une fiche dont la prise n'est pas encore là est ignorée.

1. Nettoyage par IA : DeepFilterNet 3 (réduction de bruit et d'écho faite pour la voix, licence MIT/Apache).
2. Bords seulement : on retire le blanc avant le premier mot et après la fin réelle du son du dernier mot (jamais de mot coupé).
3. Traitement « studio » : coupe-bas, moins de boue (200 Hz), plus de présence (3,5 kHz), dé-esseur, compression douce,
   -16 LUFS / crête -1,5 dBTP (normalisation en deux passes).
4. Minutage mot à mot (faster-whisper) recalé sur les mots de la fiche → sous-titres et chiffres chocs justes.
Sorties dans voix/ : <id>.mp3, <id>.mots.json, <id>-brut-nettoye.wav (contrôle), rapport-entier.md.
"""
import difflib, json, re, subprocess, sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from voix_texte import canon  # noqa: E402


def sh(*cmd):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"{cmd[0]} a échoué :\n{r.stderr[-2000:]}")
    return r.stdout + r.stderr


def duree(f):
    return float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f).split()[0])


cfg_chemin = Path(sys.argv[1]).resolve()
dossier = cfg_chemin.parent
cfg = json.loads(cfg_chemin.read_text(encoding="utf-8"))
tmp = Path(tempfile.mkdtemp(prefix="voix-entier-"))
prises = [((dossier / f).resolve(), dossier / a) for f, a in cfg["prises"].items() if (dossier / a).exists()]
if not prises:
    raise SystemExit("Aucune prise trouvée.")

from df.enhance import enhance, init_df, load_audio, save_audio  # noqa: E402
from faster_whisper import WhisperModel  # noqa: E402

df_modele, df_etat, _ = init_df()
whisper = WhisperModel(cfg.get("modele", "large-v3"), device="cpu", compute_type="int8")
rapport = ["# Voix d'Omar en une prise", "", "| Short | Prise | Durée finale | Mots retrouvés | Ce qu'Omar a dit |", "|---|---|---|---|---|"]


def transcrire(wav):
    segs, _ = whisper.transcribe(str(wav), language="fr", word_timestamps=True, beam_size=5,
                                 vad_filter=True, vad_parameters={"min_silence_duration_ms": 250, "speech_pad_ms": 120})
    return [{"texte": w.word.strip(), "debut": float(w.start), "fin": float(w.end)} for s in segs for w in (s.words or [])]


for fiche_f, prise in prises:
    d = json.loads(fiche_f.read_text(encoding="utf-8"))
    ident = d["id"]
    # 1. nettoyage IA (48 kHz mono, ce qu'attend DeepFilterNet)
    brut = tmp / f"{ident}-48k.wav"
    sh("ffmpeg", "-y", "-i", prise, "-ac", "1", "-ar", str(df_etat.sr()), "-c:a", "pcm_f32le", brut)
    audio, _ = load_audio(str(brut), sr=df_etat.sr())
    propre = enhance(df_modele, df_etat, audio, atten_lim_db=float(cfg.get("attenuation_max_db", 18)))
    nettoye = dossier / f"{ident}-brut-nettoye.wav"
    save_audio(str(nettoye), propre, df_etat.sr())

    # 2. bords : premier mot → fin réelle du son du dernier mot
    mots_t = transcrire(nettoye)
    if not mots_t:
        raise SystemExit(f"{ident} : rien entendu dans {prise.name}")
    total = duree(nettoye)
    t0 = max(0.0, mots_t[0]["debut"] - 0.15)
    fin_dernier = mots_t[-1]["fin"]
    sil = sh("ffmpeg", "-hide_banner", "-nostats", "-i", nettoye, "-af", "silencedetect=noise=-48dB:d=0.2", "-f", "null", "-")
    debuts_sil = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", sil)]
    apres = [x for x in debuts_sil if x >= fin_dernier - 0.1]
    t1 = min(total, (apres[0] if apres else total) + 0.15)

    # 3. traitement studio + normalisation en deux passes
    chaine = ("highpass=f=75,equalizer=f=200:t=q:w=1:g=-1.5,equalizer=f=3500:t=q:w=1.2:g=2,deesser=i=0.35,"
              "acompressor=threshold=-22dB:ratio=2.5:attack=8:release=120:makeup=2")
    coupe = tmp / f"{ident}-coupe.wav"
    sh("ffmpeg", "-y", "-ss", f"{t0:.3f}", "-to", f"{t1:.3f}", "-i", nettoye,
       "-af", f"{chaine},afade=t=in:d=0.03,afade=t=out:st={max(t1 - t0 - 0.12, 0):.3f}:d=0.12", coupe)
    mesure = sh("ffmpeg", "-hide_banner", "-i", coupe, "-af", "loudnorm=I=-16:TP=-1.5:LRA=7:print_format=json", "-f", "null", "-")
    m = json.loads(mesure[mesure.rindex("{"):mesure.rindex("}") + 1])
    norm = (f"loudnorm=I=-16:TP=-1.5:LRA=7:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
            f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    sortie = dossier / f"{ident}.mp3"
    sh("ffmpeg", "-y", "-i", coupe, "-af", norm, "-ar", "48000", "-c:a", "libmp3lame", "-b:a", "256k", sortie)

    # 4. minutage : mots de la fiche calés sur les mots entendus (temps décalés de t0)
    ref_mots = []
    for p in [pl["texte"] for pl in d["plans"]] + ([d["fin"]] if d.get("fin") else []):
        for w in p.split():
            if ref_mots and not re.search(r"\w", w):
                ref_mots[-1] += " " + w
            else:
                ref_mots.append(w)
    jetons = []
    for w in mots_t:
        c = canon(w["texte"])
        for k, j in enumerate(c):
            pas = (w["fin"] - w["debut"]) / max(len(c), 1)
            jetons.append((j, w["debut"] + k * pas - t0, w["debut"] + (k + 1) * pas - t0))
    flat = [(j, wi) for wi, m_ in enumerate(ref_mots) for j in canon(m_)]
    sm = difflib.SequenceMatcher(a=[x[0] for x in flat], b=[x[0] for x in jetons], autojunk=False)
    temps = {}
    for blk in sm.get_matching_blocks():
        for q in range(blk.size):
            wi = flat[blk.a + q][1]
            a_, b_ = jetons[blk.b + q][1], jetons[blk.b + q][2]
            lo, hi = temps.get(wi, (a_, b_))
            temps[wi] = (min(lo, a_), max(hi, b_))
    trouves = len(temps)
    connus = sorted(temps)
    fin_audio = t1 - t0
    for wi in range(len(ref_mots)):
        if wi in temps:
            continue
        g = max([x for x in connus if x < wi], default=None)
        dr = min([x for x in connus if x > wi], default=None)
        a_ = temps[g][1] if g is not None else 0.05
        b_ = temps[dr][0] if dr is not None else fin_audio - 0.1
        temps[wi] = (a_, max(b_, a_ + 0.1))
    mots = [{"texte": w, "debut": round(max(temps[i][0], 0), 3), "fin": round(max(temps[i][1], temps[i][0] + 0.05), 3)}
            for i, w in enumerate(ref_mots)]
    (dossier / f"{ident}.mots.json").write_text(json.dumps(mots, ensure_ascii=False, indent=1), encoding="utf-8")
    dit = " ".join(w["texte"] for w in mots_t)
    rapport.append(f"| {ident} | {prise.name} ({t0:.2f}–{t1:.2f} s) | {duree(sortie):.1f} s | {trouves}/{len(ref_mots)} | {dit} |")
    print(f"✔ {ident} : {duree(sortie):.1f} s, {trouves}/{len(ref_mots)} mots retrouvés", flush=True)

(dossier / "rapport-entier.md").write_text("\n".join(rapport) + "\n", encoding="utf-8")
print("\n".join(rapport))
