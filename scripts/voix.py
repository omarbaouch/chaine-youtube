#!/usr/bin/env python3
"""Génère la voix off de chaque scène dans public/ep/<slug>/voix/

Priorité pour chaque scène :
  1. Ta propre voix : episodes/<slug>/voix/<id>.(wav|mp3|m4a|ogg)  → utilisée telle quelle (nettoyée)
  2. Voix IA naturelle Chatterbox Multilingual (MIT, français), clonée depuis
     assets/voix/reference.wav (10-20 s de ta voix) si ce fichier existe.
  3. VOIX_MOTEUR=silence : silence de la bonne durée (tests sans modèle).

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
moteur = os.environ.get("VOIX_MOTEUR", reglages.get("moteur", "chatterbox"))
reference = reglages.get("reference") or ("assets/voix/reference.wav" if os.path.exists("assets/voix/reference.wav") else None)
expressivite = float(reglages.get("expressivite", 0.5))  # "exaggeration" : 0.3 posé → 0.8 très animé
rythme = float(reglages.get("cfg", 0.5))  # plus bas = débit plus naturel/rapide
pause_phrase = float(reglages.get("pause_phrase", 0.22))
sortie = os.path.join("public", "ep", slug, "voix")
cache = os.path.join(".cache", "voix")
os.makedirs(sortie, exist_ok=True)
os.makedirs(cache, exist_ok=True)
SR = 48000


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


def duree(path):
    with wave.open(path) as w:
        return w.getnframes() / w.getframerate()


def nettoyer(src, dest):
    # Coupe les basses parasites, compresse doucement, normalise à -16 LUFS (standard YouTube).
    ffmpeg("-i", src, "-af", "highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80,loudnorm=I=-16:TP=-1.5:LRA=7",
           "-ar", str(SR), "-ac", "1", dest)


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


_modele = None


def modele():
    global _modele
    if _modele is None:
        import torch
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS

        torch.manual_seed(42)
        appareil = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Chargement de Chatterbox Multilingual sur {appareil}…", flush=True)
        _modele = ChatterboxMultilingualTTS.from_pretrained(device=appareil)
    return _modele


def synthese(texte, dest):
    if moteur == "silence":
        ffmpeg("-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono", "-t", f"{max(0.6, len(texte.split()) / 2.6):.2f}", dest)
        return
    import torchaudio as ta

    m = modele()
    kwargs = dict(language_id="fr", exaggeration=expressivite, cfg_weight=rythme)
    if reference:
        kwargs["audio_prompt_path"] = reference
    wav = m.generate(texte, **kwargs)
    ta.save(dest, wav, m.sr)


for s in montage["scenes"]:
    sid, texte = s["id"], (s.get("texte") or "").strip()
    perso = next((os.path.join(dossier_ep, "voix", f"{sid}.{ext}") for ext in ("wav", "mp3", "m4a", "ogg")
                  if os.path.exists(os.path.join(dossier_ep, "voix", f"{sid}.{ext}"))), None)
    dest = os.path.join(sortie, f"{sid}.wav")
    if perso:
        nettoyer(perso, dest)
        json.dump({"segments": [{"texte": texte, "debut": 0, "fin": duree(dest)}]}, open(dest[:-4] + ".json", "w"))
        print(f"✔ {sid} : ta voix ({os.path.basename(perso)})")
        continue
    if not texte:
        continue
    segments, fichiers, t = [], [], 0.0
    for i, p in enumerate(phrases(texte)):
        cle = hashlib.sha1(json.dumps([moteur, reference, expressivite, rythme, p]).encode()).hexdigest()[:16]
        brut = os.path.join(cache, f"{cle}.wav")
        if not os.path.exists(brut):
            synthese(p, brut + ".tmp.wav")
            ffmpeg("-i", brut + ".tmp.wav", "-ar", str(SR), "-ac", "1", brut)
            os.remove(brut + ".tmp.wav")
        d = duree(brut)
        segments.append({"texte": p, "debut": t, "fin": t + d})
        fichiers.append(brut)
        t += d + pause_phrase
    # Assemble les phrases avec de courtes pauses naturelles, puis nettoie l'ensemble.
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
        nettoyer(brut_scene, dest)
    json.dump({"segments": segments}, open(dest[:-4] + ".json", "w"), ensure_ascii=False)
    print(f"✔ {sid} : voix {moteur} ({t:.1f} s, {len(segments)} phrase(s))", flush=True)
