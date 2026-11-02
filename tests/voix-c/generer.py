"""Test voix C (02/11/2026) : rendre la voix plus naturelle.

Même texte (l'accroche de la vidéo chocolat) en 5 versions, à écouter côte à côte :
  1-edge-actuelle          Edge Vivienne, réglage actuel (débit +8 %), phrase par phrase, pauses fixes
  2-edge-naturelle         Edge Vivienne, débit et hauteur qui varient selon la phrase, pauses variées,
                           respirations, traitement « studio » (chaleur, compression douce, petite pièce)
  3-chatterbox-neutre      Chatterbox Multilingual (Resemble AI, licence MIT), français, réglages par défaut,
                           voix de référence = Vivienne (pour garder l'accent français)
  4-chatterbox-expressive  Chatterbox, plus d'émotion (exaggeration 0.7, cfg 0.3)
  5-chatterbox-naturelle   version 4 + même traitement studio que la 2
"""
import asyncio
import os
import random
import re
import subprocess
import sys

OUT = "out/voix"
os.makedirs(OUT, exist_ok=True)
TMP = "out/tmp"
os.makedirs(TMP, exist_ok=True)
random.seed(7)

TEXTE = open(os.path.join(os.path.dirname(__file__), "texte.txt"), encoding="utf-8").read().strip()
VOIX = "fr-FR-VivienneMultilingualNeural"


def phrases(t):
    return [p.strip() for p in re.split(r"(?<=[.!?…])\s+", t) if p.strip()]


def sh(*cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def silence(path, secondes):
    sh("ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=24000:cl=mono", "-t", f"{secondes:.2f}", path)


def respiration(path):
    # souffle très discret : bruit rose filtré, 0,25 s, enveloppe douce
    sh("ffmpeg", "-y", "-f", "lavfi", "-i", "anoisesrc=c=pink:r=24000:a=0.02", "-t", "0.25",
       "-af", "highpass=f=300,lowpass=f=2500,afade=t=in:d=0.1,afade=t=out:st=0.12:d=0.13,volume=0.35", path)


def concat(morceaux, dest):
    liste = os.path.join(TMP, os.path.basename(dest) + ".txt")
    with open(liste, "w") as f:
        for m in morceaux:
            f.write(f"file '{os.path.abspath(m)}'\n")
    sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", liste, "-ar", "24000", "-ac", "1", dest)


STUDIO = ("highpass=f=70,"
          "equalizer=f=180:t=q:w=1:g=2,"        # chaleur
          "equalizer=f=3200:t=q:w=1.2:g=1.5,"   # présence
          "deesser=i=0.4,"
          "acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,"
          "aecho=0.8:0.6:18|32:0.05|0.03,"      # petite pièce, à peine audible
          "loudnorm=I=-16:TP=-1.5:LRA=9")


def finaliser(src, nom, studio):
    af = STUDIO if studio else "loudnorm=I=-16:TP=-1.5:LRA=9"
    sh("ffmpeg", "-y", "-i", src, "-af", af, "-ar", "44100", "-b:a", "192k", os.path.join(OUT, nom + ".mp3"))


def reglage_naturel(p, i):
    """Débit / hauteur selon le rôle de la phrase (comme un humain qui raconte)."""
    mots = len(p.split())
    if p.endswith("?"):
        return "+2%", "+4Hz"           # question : un peu plus haut, pas pressé
    if mots <= 4:
        return "-6%", "-2Hz"           # phrase choc courte : on ralentit, on pose
    if p.endswith("…"):
        return "-2%", "-3Hz"           # suspense : on retient
    return f"+{random.choice([3, 5, 7, 9])}%", f"{random.choice([-1, 0, 1, 2]):+d}Hz"


def pause_naturelle(p):
    if p.endswith("?"):
        return random.uniform(0.45, 0.6)
    if p.endswith("…"):
        return random.uniform(0.5, 0.7)
    if len(p.split()) <= 4:
        return random.uniform(0.35, 0.5)
    return random.uniform(0.18, 0.32)


async def edge(texte, dest, rate, pitch):
    import edge_tts
    for essai in range(5):
        try:
            await edge_tts.Communicate(texte, VOIX, rate=rate, pitch=pitch).save(dest)
            return
        except Exception as e:  # le serveur coupe parfois
            print("edge-tts :", e, flush=True)
            await asyncio.sleep(3 + 3 * essai)
    raise RuntimeError("edge-tts indisponible")


async def versions_edge():
    ps = phrases(TEXTE)
    # 1 : actuel
    morceaux = []
    for i, p in enumerate(ps):
        mp3 = os.path.join(TMP, f"a{i}.mp3"); wav = mp3[:-4] + ".wav"
        await edge(p, mp3, "+8%", "+0Hz")
        sh("ffmpeg", "-y", "-i", mp3, "-ar", "24000", "-ac", "1", wav)
        morceaux.append(wav)
        s = os.path.join(TMP, f"as{i}.wav"); silence(s, 0.22); morceaux.append(s)
    concat(morceaux, os.path.join(TMP, "edge_actuelle.wav"))
    finaliser(os.path.join(TMP, "edge_actuelle.wav"), "1-edge-actuelle", False)

    # 2 : naturel
    morceaux = []
    souffle = os.path.join(TMP, "souffle.wav"); respiration(souffle)
    for i, p in enumerate(ps):
        rate, pitch = reglage_naturel(p, i)
        mp3 = os.path.join(TMP, f"n{i}.mp3"); wav = mp3[:-4] + ".wav"
        await edge(p, mp3, rate, pitch)
        sh("ffmpeg", "-y", "-i", mp3, "-ar", "24000", "-ac", "1", wav)
        if i and len(p.split()) > 9:      # respiration avant une phrase longue
            morceaux.append(souffle)
        morceaux.append(wav)
        s = os.path.join(TMP, f"ns{i}.wav"); silence(s, pause_naturelle(p)); morceaux.append(s)
    concat(morceaux, os.path.join(TMP, "edge_naturelle.wav"))
    finaliser(os.path.join(TMP, "edge_naturelle.wav"), "2-edge-naturelle", True)
    # référence française pour Chatterbox : les 12 premières secondes de la voix actuelle
    sh("ffmpeg", "-y", "-i", os.path.join(TMP, "edge_actuelle.wav"), "-t", "12", os.path.join(TMP, "reference.wav"))


def versions_chatterbox():
    import torch
    import torchaudio as ta
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    torch.set_num_threads(os.cpu_count() or 4)
    model = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
    ref = os.path.join(TMP, "reference.wav")
    ps = phrases(TEXTE)
    for nom, exag, cfg, studio in [("3-chatterbox-neutre", 0.5, 0.5, False),
                                   ("4-chatterbox-expressive", 0.7, 0.3, False)]:
        morceaux = []
        for i, p in enumerate(ps):
            wav = model.generate(p, language_id="fr", audio_prompt_path=ref, exaggeration=exag, cfg_weight=cfg)
            chemin = os.path.join(TMP, f"{nom}-{i}.wav")
            ta.save(chemin, wav, model.sr)
            r = chemin[:-4] + "-24k.wav"
            sh("ffmpeg", "-y", "-i", chemin, "-ar", "24000", "-ac", "1", r)
            morceaux.append(r)
            s = os.path.join(TMP, f"{nom}-s{i}.wav"); silence(s, pause_naturelle(p)); morceaux.append(s)
            print(nom, i + 1, "/", len(ps), flush=True)
        brut = os.path.join(TMP, nom + ".wav")
        concat(morceaux, brut)
        finaliser(brut, nom, studio)
        if nom.startswith("4"):
            finaliser(brut, "5-chatterbox-naturelle", True)


asyncio.run(versions_edge())
try:
    versions_chatterbox()
except Exception as e:
    print("Chatterbox a échoué :", repr(e), flush=True)
    with open(os.path.join(OUT, "ERREUR-chatterbox.txt"), "w") as f:
        f.write(repr(e))

with open(os.path.join(OUT, "LISEZMOI.txt"), "w", encoding="utf-8") as f:
    f.write(__doc__)
print(sorted(os.listdir(OUT)))
