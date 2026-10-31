#!/usr/bin/env python3
"""Échantillons de voix françaises gratuites, même texte pour toutes : Omar choisit à l'oreille.
Chaque moteur est essayé séparément : si l'un échoue, les autres sortent quand même."""
import asyncio, os, subprocess, traceback, urllib.request, wave

TEXTE = ("Dans cette baguette à un euro, le blé coûte… six centimes. "
         "Alors, où passent les quatre-vingt-quatorze autres centimes ? "
         "Pour le savoir, il faut suivre la baguette. Du champ, jusqu'à ta main.")
OUT = "out/voix"
os.makedirs(OUT, exist_ok=True)
fait = []

def finir(brut, nom, desc):
    dest = f"{OUT}/{nom}.mp3"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", brut, "-af", "highpass=f=70,loudnorm=I=-16:TP=-1.5:LRA=11",
                    "-ar", "44100", "-b:a", "192k", dest], check=True)
    fait.append(f"{nom}.mp3 : {desc}")
    print("✔", nom)

def essai(fn):
    try: fn()
    except Exception: traceback.print_exc()

# 1) Pocket TTS (voix actuelle, référence)
def pocket():
    import scipy.io.wavfile
    from pocket_tts import TTSModel
    m = TTSModel.load_model(language="french_24l", temp=0.3, sampler_decode_steps=5)
    a = m.generate_audio(m.get_state_for_audio_prompt("estelle"), TEXTE)
    scipy.io.wavfile.write("/tmp/pocket.wav", m.sample_rate, a.numpy())
    finir("/tmp/pocket.wav", "1-actuelle-pocket-estelle", "voix actuelle (référence), femme")
essai(pocket)

# 2) Piper (Rhasspy, modèles libres)
PIPER = {"2-piper-tom": ("fr/fr_FR/tom/medium/fr_FR-tom-medium", "homme, Piper"),
         "3-piper-siwis": ("fr/fr_FR/siwis/medium/fr_FR-siwis-medium", "femme, Piper"),
         "4-piper-upmc-pierre": ("fr/fr_FR/upmc/medium/fr_FR-upmc-medium", "homme, Piper (UPMC)")}
for nom, (chemin, desc) in PIPER.items():
    def p(nom=nom, chemin=chemin, desc=desc):
        base = "https://huggingface.co/rhasspy/piper-voices/resolve/main/" + chemin
        for ext in (".onnx", ".onnx.json"):
            urllib.request.urlretrieve(base + ext, f"/tmp/{nom}{ext}")
        args = ["piper", "-m", f"/tmp/{nom}.onnx", "-f", f"/tmp/{nom}.wav", "--length_scale", "1.0", "--sentence_silence", "0.25"]
        if "upmc" in nom: args += ["--speaker", "1"]
        subprocess.run(args, input=TEXTE.encode(), check=True)
        finir(f"/tmp/{nom}.wav", nom, desc)
    essai(p)

# 3) Kokoro (Apache 2.0)
def kokoro():
    from kokoro import KPipeline
    import numpy as np, soundfile as sf
    pipe = KPipeline(lang_code="f")
    morceaux = [a for _, _, a in pipe(TEXTE, voice="ff_siwis", speed=1.0)]
    sf.write("/tmp/kokoro.wav", np.concatenate(morceaux), 24000)
    finir("/tmp/kokoro.wav", "5-kokoro-siwis", "femme, Kokoro")
essai(kokoro)

# 4) Voix neuronales Microsoft Edge (gratuites, mais conditions d'utilisation floues pour une chaîne monétisée)
EDGE = {"6-edge-henri": ("fr-FR-HenriNeural", "homme, Microsoft Edge"),
        "7-edge-remy": ("fr-FR-RemyMultilingualNeural", "homme, Microsoft Edge"),
        "8-edge-denise": ("fr-FR-DeniseNeural", "femme, Microsoft Edge"),
        "9-edge-vivienne": ("fr-FR-VivienneMultilingualNeural", "femme, Microsoft Edge")}
for nom, (voix, desc) in EDGE.items():
    def e(nom=nom, voix=voix, desc=desc):
        import edge_tts
        asyncio.run(edge_tts.Communicate(TEXTE, voix, rate="+5%").save(f"/tmp/{nom}.mp3"))
        finir(f"/tmp/{nom}.mp3", nom, desc)
    essai(e)

open(f"{OUT}/LISEZMOI.txt", "w").write("Même phrase, voix différentes. Dis-moi le numéro que tu préfères.\n\n" + "\n".join(fait) + "\n")
print("\n".join(fait))
