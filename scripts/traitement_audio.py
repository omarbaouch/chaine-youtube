"""Chaîne de traitement "radio" des voix off, réglée par mesure (scripts/analyse_voix.py).

v2 (après écoute d'Omar : "bruits parasites") :
- afftdn suit le bruit de fond et retire les sifflements constants du modèle (≈ 1,2 / 2,4 kHz),
- porte de bruit : les pauses redeviennent silencieuses (la compression ne remonte plus le souffle),
- clarté remontée plus doucement (+2,5 / +1,5 dB au lieu de +4 / +2,5),
- double passe-bas à 11,5 kHz (-24 dB/oct) : rien d'utile au-dessus pour une voix générée en 24 kHz.
"""
import json
import os
import subprocess

SR = 48000

EGALISATION_IA = ",".join([
    "highpass=f=85:poles=2",
    "afftdn=nr=12:nf=-55:tn=1",
    "equalizer=f=220:t=q:w=1.4:g=-2",
    "equalizer=f=380:t=q:w=1.2:g=-3.5",
    "equalizer=f=2700:t=q:w=0.8:g=2.5",
    "equalizer=f=4300:t=q:w=1.0:g=1.5",
    "equalizer=f=7000:t=q:w=1.2:g=-1.5",
    "lowpass=f=11500:poles=2",
    "lowpass=f=11500:poles=2",
    "deesser=i=0.6:m=0.6:f=0.5",
])
# Voix neuronale déjà propre (Edge) : seulement un coupe-bas et une légère présence.
EGALISATION_NEURONALE = "highpass=f=70:poles=2,equalizer=f=3000:t=q:w=1.0:g=1"
EGALISATION_MICRO = "highpass=f=80:poles=2,afftdn=nr=10:nf=-45:tn=1,equalizer=f=300:t=q:w=1.2:g=-2,deesser=i=0.4:m=0.5:f=0.5"
DYNAMIQUE = ",".join([
    "agate=threshold=0.012:ratio=6:attack=4:release=140:range=0.06:knee=3",
    "acompressor=threshold=-24dB:ratio=2:attack=12:release=180:knee=6:makeup=1",
    "alimiter=limit=0.84:attack=3:release=60:level=disabled",
])


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


def traiter(src, dest, egalisation=EGALISATION_IA, lufs=-16):
    """EQ + débruitage + dynamique, puis normalisation EBU R128 en deux passes (linéaire)."""
    tmp = dest + ".pre.wav"
    ffmpeg("-i", src, "-af", f"{egalisation},{DYNAMIQUE}", "-ar", str(SR), "-ac", "1", tmp)
    mesure = subprocess.run(["ffmpeg", "-nostats", "-i", tmp, "-af", f"loudnorm=I={lufs}:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                            capture_output=True, text=True).stderr
    m = json.loads(mesure[mesure.rindex("{"):mesure.rindex("}") + 1])
    ffmpeg("-i", tmp, "-af",
           f"loudnorm=I={lufs}:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
           f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true",
           "-ar", str(SR), "-ac", "1", dest)
    os.remove(tmp)
