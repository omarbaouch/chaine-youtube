"""Test voix D (02/11/2026) : retour d'Omar sur la version 2 : « trop de pauses entre chaque phrase, il faut de l'intonation ».

Cause : chaque phrase était lue seule, la voix repartait à plat et les pauses s'additionnaient.
  A-souffle-continu   tout le texte en un seul appel : l'intonation suit le sens d'une phrase à l'autre
  B-groupes-souffle   phrases regroupées par 2 ou 3 (un « souffle »), débit qui varie d'un groupe à l'autre,
                      pause courte (0,08 à 0,18 s) entre les groupes
  C-groupes-vif       comme B, un peu plus rapide et plus haut : ton de conteur enthousiaste
Les trois ont le traitement « studio » de la version 2.
"""
import asyncio
import os
import random
import re
import subprocess

OUT, TMP = "out/voix", "out/tmp"
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)
random.seed(3)
VOIX = "fr-FR-VivienneMultilingualNeural"
TEXTE = open(os.path.join(os.path.dirname(__file__), "texte.txt"), encoding="utf-8").read().strip()

STUDIO = ("highpass=f=70,equalizer=f=180:t=q:w=1:g=2,equalizer=f=3200:t=q:w=1.2:g=1.5,deesser=i=0.4,"
          "acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,aecho=0.8:0.6:18|32:0.05|0.03,"
          "loudnorm=I=-16:TP=-1.5:LRA=9")


def sh(*cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def phrases(t):
    return [p.strip() for p in re.split(r"(?<=[.!?])\s+", t) if p.strip()]


def groupes(ps):
    """Regroupe les phrases par souffle : 2 ou 3 phrases, ou une phrase longue seule."""
    gs, cur = [], []
    for p in ps:
        cur.append(p)
        mots = sum(len(x.split()) for x in cur)
        if len(cur) >= 3 or mots >= 16:
            gs.append(" ".join(cur)); cur = []
    if cur:
        gs.append(" ".join(cur))
    return gs


async def edge(texte, dest, rate, pitch):
    import edge_tts
    for essai in range(5):
        try:
            await edge_tts.Communicate(texte, VOIX, rate=rate, pitch=pitch).save(dest)
            return
        except Exception as e:
            print("edge-tts :", e, flush=True)
            await asyncio.sleep(3 + 3 * essai)
    raise RuntimeError("edge-tts indisponible")


def finaliser(src, nom):
    sh("ffmpeg", "-y", "-i", src, "-af", STUDIO, "-ar", "44100", "-b:a", "192k", os.path.join(OUT, nom + ".mp3"))


async def par_groupes(nom, rates, pitches, pause):
    morceaux = []
    for i, g in enumerate(groupes(phrases(TEXTE))):
        mp3 = os.path.join(TMP, f"{nom}{i}.mp3"); wav = mp3[:-4] + ".wav"
        await edge(g, mp3, random.choice(rates), random.choice(pitches))
        # coupe le silence de fin que Edge ajoute, pour maîtriser la pause nous-mêmes
        sh("ffmpeg", "-y", "-i", mp3, "-af", "areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse",
           "-ar", "24000", "-ac", "1", wav)
        morceaux.append(wav)
        s = os.path.join(TMP, f"{nom}s{i}.wav")
        sh("ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", f"{random.uniform(*pause):.2f}", s)
        morceaux.append(s)
    liste = os.path.join(TMP, nom + ".txt")
    open(liste, "w").write("".join(f"file '{os.path.abspath(m)}'\n" for m in morceaux))
    brut = os.path.join(TMP, nom + ".wav")
    sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", liste, brut)
    finaliser(brut, nom)


async def main():
    mp3 = os.path.join(TMP, "A.mp3")
    await edge(TEXTE, mp3, "+6%", "+0Hz")
    finaliser(mp3, "A-souffle-continu")
    await par_groupes("B-groupes-souffle", ["+4%", "+6%", "+9%"], ["+0Hz", "+2Hz", "-1Hz"], (0.08, 0.18))
    await par_groupes("C-groupes-vif", ["+9%", "+11%", "+13%"], ["+3Hz", "+5Hz"], (0.06, 0.14))


asyncio.run(main())
open(os.path.join(OUT, "LISEZMOI.txt"), "w", encoding="utf-8").write(__doc__)
print(sorted(os.listdir(OUT)))
