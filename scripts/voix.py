#!/usr/bin/env python3
"""Génère la voix off de chaque scène dans public/ep/<slug>/voix/

Priorité pour chaque scène :
  1. Ta propre voix : episodes/<slug>/voix/<id>.(wav|mp3|m4a|ogg) → nettoyée et normalisée.
  2. Voix IA française Pocket TTS (Kyutai, code MIT) : modèle "french_24l", voix "estelle" (CC0) par défaut.
  3. VOIX_MOTEUR=silence : silence de la bonne durée (tests sans modèle).

Chaque voix IA passe par une chaîne de traitement "radio" réglée par mesure (scripts/analyse_voix.py) :
coupe-bas, creux dans le "carton" (220/380 Hz), présence (2,7/4,3 kHz), sifflantes maîtrisées,
compression douce, limiteur, puis normalisation en deux passes à -16 LUFS / -1,5 dBTP.
Écrit aussi <id>.json avec le minutage de chaque phrase (pour caler les sous-titres).
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import wave

slug = sys.argv[1]
dossier_ep = os.path.join("episodes", slug)
montage = json.load(open(os.path.join(dossier_ep, "montage.json"), encoding="utf-8"))
reglages = montage.get("voix", {})
moteur = os.environ.get("VOIX_MOTEUR", reglages.get("moteur", "pocket"))
modele_nom = reglages.get("modele", "french_24l")
locuteur = reglages.get("locuteur", "estelle")
temperature = float(reglages.get("temperature", 0.3))  # plus haut = plus expressif, moins stable
pause_phrase = float(reglages.get("pause_phrase", 0.22))
sortie = os.path.join("public", "ep", slug, "voix")
cache = os.path.join(".cache", "voix")
os.makedirs(sortie, exist_ok=True)
os.makedirs(cache, exist_ok=True)
SR = 48000

# Égalisation mesurée sur la voix Pocket TTS (voir scripts/analyse_voix.py) — à refaire si on change de voix.
EGALISATION_IA = ",".join([
    "highpass=f=85:poles=2",
    "equalizer=f=220:t=q:w=1.4:g=-2",
    "equalizer=f=380:t=q:w=1.2:g=-4",
    "equalizer=f=2700:t=q:w=0.8:g=4",
    "equalizer=f=4300:t=q:w=1.0:g=2.5",
    "equalizer=f=7000:t=q:w=1.2:g=-1.5",
    "lowpass=f=11500:poles=2",
    "deesser=i=0.6:m=0.6:f=0.5",
])
EGALISATION_MICRO = "highpass=f=80:poles=2,afftdn=nr=10:nf=-45,equalizer=f=300:t=q:w=1.2:g=-2,deesser=i=0.4:m=0.5:f=0.5"
DYNAMIQUE = "acompressor=threshold=-26dB:ratio=2.2:attack=10:release=160:knee=6:makeup=2,alimiter=limit=0.84:attack=3:release=60:level=disabled"


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


def duree(path):
    with wave.open(path) as w:
        return w.getnframes() / w.getframerate()


def traiter(src, dest, egalisation):
    """EQ + dynamique, puis normalisation EBU R128 en deux passes (linéaire : ne déforme pas la voix)."""
    tmp = dest + ".pre.wav"
    ffmpeg("-i", src, "-af", f"{egalisation},{DYNAMIQUE}", "-ar", str(SR), "-ac", "1", tmp)
    mesure = subprocess.run(["ffmpeg", "-nostats", "-i", tmp, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                            capture_output=True, text=True).stderr
    m = json.loads(mesure[mesure.rindex("{"):mesure.rindex("}") + 1])
    ffmpeg("-i", tmp, "-af",
           f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
           f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true",
           "-ar", str(SR), "-ac", "1", dest)
    os.remove(tmp)


def phrases(texte):
    morceaux = re.split(r"(?<=[.!?…])\s+", texte.strip())
    resultat = []
    for m in morceaux:  # coupe les phrases très longues sur les virgules (le modèle reste plus naturel)
        while len(m) > 220 and "," in m[:220]:
            i = m[:220].rfind(",") + 1
            resultat.append(m[:i].strip())
            m = m[i:].strip()
        if m:
            resultat.append(m)
    return resultat


_modele, _etat = None, None


def modele():
    global _modele, _etat
    if _modele is None:
        from pocket_tts import TTSModel

        print(f"Chargement de Pocket TTS ({modele_nom}, voix {locuteur})…", flush=True)
        _modele = TTSModel.load_model(language=modele_nom, temp=temperature)
        _etat = _modele.get_state_for_audio_prompt(locuteur)
    return _modele, _etat


def synthese(texte, dest):
    if moteur == "silence":
        ffmpeg("-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono", "-t", f"{max(0.6, len(texte.split()) / 2.6):.2f}", dest)
        return
    import scipy.io.wavfile

    m, etat = modele()
    audio = m.generate_audio(etat, texte)
    scipy.io.wavfile.write(dest, m.sample_rate, audio.numpy())


for s in montage["scenes"]:
    sid, texte = s["id"], (s.get("texte") or "").strip()
    perso = next((os.path.join(dossier_ep, "voix", f"{sid}.{ext}") for ext in ("wav", "mp3", "m4a", "ogg")
                  if os.path.exists(os.path.join(dossier_ep, "voix", f"{sid}.{ext}"))), None)
    dest = os.path.join(sortie, f"{sid}.wav")
    if perso:
        traiter(perso, dest, EGALISATION_MICRO)
        json.dump({"segments": [{"texte": texte, "debut": 0, "fin": duree(dest)}]}, open(dest[:-4] + ".json", "w"), ensure_ascii=False)
        print(f"✔ {sid} : ta voix ({os.path.basename(perso)})")
        continue
    if not texte:
        continue
    segments, fichiers, t = [], [], 0.0
    for p in phrases(texte):
        cle = hashlib.sha1(json.dumps([moteur, modele_nom, locuteur, temperature, p]).encode()).hexdigest()[:16]
        brut = os.path.join(cache, f"{cle}.wav")
        if not os.path.exists(brut):
            synthese(p, brut + ".tmp.wav")
            ffmpeg("-i", brut + ".tmp.wav", "-ar", str(SR), "-ac", "1", brut)
            os.remove(brut + ".tmp.wav")
        d = duree(brut)
        segments.append({"texte": p, "debut": t, "fin": t + d})
        fichiers.append(brut)
        t += d + pause_phrase
    # Assemble les phrases avec de courtes pauses naturelles, puis traite l'ensemble.
    liste = os.path.join(cache, f"{slug}-{sid}.txt")
    silence = os.path.join(cache, f"silence-{pause_phrase}.wav")
    if not os.path.exists(silence):
        ffmpeg("-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono", "-t", str(pause_phrase), silence)
    with open(liste, "w") as f:
        for i, fi in enumerate(fichiers):
            if i:
                f.write(f"file '{os.path.abspath(silence)}'\n")
            f.write(f"file '{os.path.abspath(fi)}'\n")
    brut_scene = os.path.join(cache, f"{slug}-{sid}-brut.wav")
    ffmpeg("-f", "concat", "-safe", "0", "-i", liste, "-c", "copy", brut_scene)
    if moteur == "silence":
        shutil.copy(brut_scene, dest)
    else:
        traiter(brut_scene, dest, EGALISATION_IA)
    json.dump({"segments": segments}, open(dest[:-4] + ".json", "w"), ensure_ascii=False)
    print(f"✔ {sid} : voix {moteur} ({t:.1f} s, {len(segments)} phrase(s))", flush=True)
