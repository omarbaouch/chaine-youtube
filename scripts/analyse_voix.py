#!/usr/bin/env python3
"""Mesures d'une voix off : volume, dynamique, bandes de fréquences, sifflantes, souffle, bande passante.
Usage : python3 scripts/analyse_voix.py fichier1 [fichier2 ...] [--png spectre.png]
"""
import subprocess
import sys

import numpy as np

BANDES = [  # (nom, bas, haut) — repères classiques du traitement de voix
    ("infra / grondement", 20, 80),
    ("corps / chaleur", 80, 250),
    ("boue (son « carton »)", 250, 500),
    ("médium (nasal)", 500, 2000),
    ("présence / clarté", 2000, 5000),
    ("sifflantes (s, ch)", 5000, 9000),
    ("air", 9000, 16000),
]


def charger(path, sr=48000):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32), sr


def ebur128(path):
    out = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128=peak=true:framelog=quiet", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    val = {}
    for cle, marq in (("LUFS", "I:"), ("LRA", "LRA:"), ("crete_dBTP", "Peak:")):
        lignes = [l for l in out.splitlines() if l.strip().startswith(marq)]
        val[cle] = float(lignes[-1].split()[1]) if lignes else None
    return val


def ltas(x, sr, n=4096):
    """Spectre moyen à long terme sur les seules trames de parole (on ignore les silences)."""
    hop = n // 2
    win = np.hanning(n)
    trames = [x[i:i + n] * win for i in range(0, len(x) - n, hop)]
    rms = np.array([np.sqrt(np.mean(t ** 2)) for t in trames])
    seuil = np.percentile(rms, 30)
    spec = np.array([np.abs(np.fft.rfft(t)) ** 2 for t, r in zip(trames, rms) if r > seuil])
    return np.fft.rfftfreq(n, 1 / sr), spec.mean(axis=0), spec, rms, seuil


def analyser(path):
    x, sr = charger(path)
    f, p, spec, rms, seuil = ltas(x, sr)
    total = p[(f >= 20) & (f <= 16000)].sum()
    bandes = {nom: 10 * np.log10(p[(f >= lo) & (f < hi)].sum() / total + 1e-12) for nom, lo, hi in BANDES}
    # sifflantes : part des trames où la bande 5-9 kHz dépasse fortement la présence (pic de "s" agressif)
    sib = np.array([s[(f >= 5000) & (f < 9000)].sum() / (s[(f >= 2000) & (f < 5000)].sum() + 1e-12) for s in spec])
    # bande passante utile : fréquence au-delà de laquelle il reste < 0,1 % de l'énergie
    cumul = np.cumsum(p) / p.sum()
    bp = f[np.searchsorted(cumul, 0.999)]
    # souffle : niveau RMS des passages silencieux
    silences = rms[rms < seuil * 0.3]
    souffle = 20 * np.log10(np.median(silences) + 1e-9) if len(silences) else None
    centroide = (f * p).sum() / p.sum()
    return dict(ebur128(path), bandes=bandes, sifflantes_pics=float(np.percentile(sib, 95)), bande_passante=bp,
                souffle_dBFS=souffle, centroide=centroide, spectre=(f, p))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    png = sys.argv[sys.argv.index("--png") + 1] if "--png" in sys.argv else None
    if png:
        args = [a for a in args if a != png]
    res = {a: analyser(a) for a in args}
    for a, r in res.items():
        print(f"\n== {a}")
        print(f"  volume {r['LUFS']} LUFS · dynamique {r['LRA']} LU · crête {r['crete_dBTP']} dBTP · centre spectral {r['centroide']:.0f} Hz")
        print(f"  bande passante utile ≈ {r['bande_passante']:.0f} Hz · souffle dans les pauses {r['souffle_dBFS'] and round(r['souffle_dBFS'], 1)} dBFS"
              f" · pics de sifflantes (5-9k / 2-5k, P95) {r['sifflantes_pics']:.2f}")
        for nom, v in r["bandes"].items():
            print(f"  {nom:<24} {v:6.1f} dB  {'█' * max(0, int((v + 30) / 1.5))}")
    if png:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(11, 5), dpi=110)
        for a, r in res.items():
            f, p = r["spectre"]
            k = 12
            lis = np.convolve(10 * np.log10(p + 1e-20), np.ones(k) / k, mode="same")
            ax.semilogx(f[1:], lis[1:] - lis[(f > 900) & (f < 1100)].mean(), label=a.split("/")[-1])
        for nom, lo, hi in BANDES:
            ax.axvspan(lo, hi, alpha=0.04)
            ax.text(np.sqrt(lo * hi), 12, nom.split(" ")[0], ha="center", fontsize=8)
        ax.set_xlim(40, 16000); ax.set_ylim(-60, 18)
        ax.set_xlabel("Fréquence (Hz)"); ax.set_ylabel("dB (0 = niveau à 1 kHz)")
        ax.set_title("Spectre moyen de la voix"); ax.grid(alpha=0.3, which="both"); ax.legend()
        fig.tight_layout(); fig.savefig(png)
        print(f"\n✔ graphique : {png}")
