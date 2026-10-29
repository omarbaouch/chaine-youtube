#!/usr/bin/env python3
"""Génère la voix off de chaque scène dans public/ep/<slug>/voix/

Priorité pour chaque scène :
  1. Ta propre voix : episodes/<slug>/voix/<id>.(wav|mp3|m4a|ogg) → nettoyée et normalisée.
  2. Voix IA française Pocket TTS (Kyutai, code MIT) : modèle "french_24l", voix "estelle" (CC0) par défaut.
  3. VOIX_MOTEUR=silence : silence de la bonne durée (tests sans modèle).

Chaque voix IA passe par une chaîne de traitement "radio" réglée par mesure (scripts/analyse_voix.py) :
coupe-bas, creux dans le "carton" (220/380 Hz), présence (2,7/4,3 kHz), sifflantes maîtrisées,
débruitage, porte de bruit, compression douce, limiteur, normalisation en deux passes à -16 LUFS / -1,5 dBTP
(voir scripts/traitement_audio.py).
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
etapes = int(reglages.get("etapes", 5))  # étapes de calcul Pocket TTS : plus = moins de défauts, plus lent
locuteur = reglages.get("locuteur", "estelle")
temperature = float(reglages.get("temperature", 0.3))  # plus haut = plus expressif, moins stable
pause_phrase = float(reglages.get("pause_phrase", 0.22))
sortie = os.path.join("public", "ep", slug, "voix")
cache = os.path.join(".cache", "voix")
os.makedirs(sortie, exist_ok=True)
os.makedirs(cache, exist_ok=True)
SR = 48000

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from traitement_audio import EGALISATION_IA, EGALISATION_MICRO, ffmpeg, traiter  # noqa: E402


def duree(path):
    with wave.open(path) as w:
        return w.getnframes() / w.getframerate()


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
        _modele = TTSModel.load_model(language=modele_nom, temp=temperature, sampler_decode_steps=etapes)
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
        cle = hashlib.sha1(json.dumps([moteur, modele_nom, locuteur, temperature, etapes, p]).encode()).hexdigest()[:16]
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
