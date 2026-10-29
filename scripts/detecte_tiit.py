#!/usr/bin/env python3
"""Détecte les "tiiit" : bips brefs et purs (bande étroite, 1,5-12 kHz, 25-400 ms) qui dépassent nettement
leur voisinage spectral. Usage : python3 scripts/detecte_tiit.py fichier [fichier...]"""
import subprocess
import sys

import numpy as np


def charger(p, sr=48000):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(r, np.float32), sr


def detecter(p, seuil_db=18, n=2048, hop=256):
    x, sr = charger(p)
    win = np.hanning(n)
    S = np.array([np.abs(np.fft.rfft(x[i:i + n] * win)) for i in range(0, len(x) - n, hop)])
    f = np.fft.rfftfreq(n, 1 / sr)
    db = 20 * np.log10(S + 1e-9)
    lo, hi = np.searchsorted(f, 1500), np.searchsorted(f, 12000)
    # saillance : bin vs médiane de ses voisins (±12 bins ≈ ±280 Hz)
    from scipy.ndimage import median_filter
    voisinage = median_filter(db, size=(1, 25))
    saillance = db - voisinage
    niveau_trame = db.max(axis=1, keepdims=True)
    actif = (saillance > seuil_db) & (db > niveau_trame - 30)
    actif[:, :lo] = False
    actif[:, hi:] = False
    evenements = []
    vus = np.zeros_like(actif)
    for t0, k0 in zip(*np.nonzero(actif)):
        if vus[t0, k0]:
            continue
        t, k, long = t0, k0, 0
        while t < actif.shape[0]:
            fen = actif[t, max(0, k - 2):k + 3]
            if not fen.any():
                break
            k = max(0, k - 2) + int(np.argmax(fen))
            vus[t, max(0, k - 2):k + 3] = True
            t += 1
            long += 1
        d = long * hop / sr
        if 0.025 <= d <= 0.4:
            evenements.append((t0 * hop / sr, f[k0], d, float(saillance[t0, k0])))
    return evenements


for p in sys.argv[1:]:
    ev = detecter(p)
    print(f"\n== {p} : {len(ev)} 'tiiit' détecté(s)")
    for t, fr, d, s in sorted(ev)[:25]:
        print(f"  à {t:5.2f} s · {fr:6.0f} Hz · {d * 1000:4.0f} ms · +{s:.0f} dB au-dessus du voisinage")
