#!/usr/bin/env python3
"""Extraits de voix Pocket TTS pour comparer à l'oreille (WAV, sans perte).
Variantes : étapes de calcul 1 vs 5, brut vs traité (chaîne scripts/traitement_audio.py).
"""
import os
import sys
import time

import scipy.io.wavfile

sys.path.insert(0, "scripts")
from traitement_audio import traiter  # noqa: E402
from pocket_tts import TTSModel  # noqa: E402

texte = open("tests/voix/texte.txt", encoding="utf-8").read().strip()
os.makedirs("out/voix", exist_ok=True)
notes = []
for etapes in (1, 5):
    t = time.time()
    m = TTSModel.load_model(language="french_24l", sampler_decode_steps=etapes)
    etat = m.get_state_for_audio_prompt("estelle")
    audio = m.generate_audio(etat, texte)
    brut = f"out/voix/{etapes}-etapes-brut.wav"
    scipy.io.wavfile.write(brut, m.sample_rate, audio.numpy())
    traiter(brut, f"out/voix/{etapes}-etapes-traite.wav")
    notes.append(f"{etapes} étape(s) : généré en {time.time() - t:.0f} s")
    print("✔", notes[-1], flush=True)
open("out/voix/LISEZMOI.txt", "w").write("Texte : " + texte + "\n\n" + "\n".join(notes) + "\n")
