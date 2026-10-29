#!/usr/bin/env python3
"""Génère des extraits de voix Pocket TTS (Kyutai) pour comparer à l'oreille.
Sortie : out/voix/*.mp3 + out/voix/LISEZMOI.txt (quelle voix = quel fichier, licences).
"""
import os
import subprocess
import time

from huggingface_hub import list_repo_files

texte = open("tests/voix/texte.txt", encoding="utf-8").read().strip()
os.makedirs("out/voix", exist_ok=True)

# Voix françaises utilisables commercialement : estelle (CC0) + voix CML-TTS fr (CC BY 4.0)
fr = sorted(f for f in list_repo_files("kyutai/tts-voices") if f.startswith("cml-tts/fr/") and f.endswith((".wav", ".mp3")))
print(f"{len(fr)} voix CML-TTS fr trouvées")
essais = [
    ("A-estelle-rapide", "french", "estelle"),
    ("B-estelle-haute-qualite", "french_24l", "estelle"),
] + [(f"{chr(67 + i)}-{os.path.splitext(os.path.basename(f))[0]}", "french_24l", f"hf://kyutai/tts-voices/{f}") for i, f in enumerate(fr[:6])]

notes = []
for nom, modele, voix in essais:
    wav = f"out/voix/{nom}.wav"
    t = time.time()
    r = subprocess.run(["pocket-tts", "generate", "--language", modele, "--voice", voix, "--text", texte,
                        "--output-path", wav, "--quiet"], capture_output=True, text=True)
    if r.returncode:
        print(f"✗ {nom} : {r.stderr[-400:]}")
        continue
    d = time.time() - t
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-af", "loudnorm=I=-16:TP=-1.5",
                    "-ar", "44100", "-b:a", "192k", wav[:-4] + ".mp3"], check=True)
    os.remove(wav)
    notes.append(f"{nom}.mp3 : modèle {modele}, voix {voix} — généré en {d:.0f} s")
    print("✔", notes[-1], flush=True)

open("out/voix/LISEZMOI.txt", "w").write(
    "Texte : " + texte + "\n\n" + "\n".join(notes) +
    "\n\nLicences : estelle = CC0 ; voix cml-tts/fr = CC BY 4.0 (créditer Kyutai/CML-TTS). Code Pocket TTS = MIT.\n")
