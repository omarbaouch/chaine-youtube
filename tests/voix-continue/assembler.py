"""Assemble les voix des plans comme le fait construire.mjs (avant_voix + voix + respiration), pour écouter le rendu final."""
import json, os, subprocess, sys
slug, nom = sys.argv[1], sys.argv[2]
m = json.load(open(f"episodes/{slug}/montage.json"))
fps, dt = 30, m.get("duree_transition", 12)
morceaux, tmp = [], f"out/tmp-{slug}"
os.makedirs(tmp, exist_ok=True); os.makedirs("out/voix", exist_ok=True)
def sil(sec, i):
    p = f"{tmp}/s{i}.wav"
    subprocess.run(["ffmpeg","-y","-v","error","-f","lavfi","-i","anullsrc=r=48000:cl=mono","-t",f"{max(sec,0.001):.3f}",p], check=True)
    return p
sc = m["scenes"]
for i, s in enumerate(sc):
    wav = f"public/ep/{slug}/voix/{s['id']}.wav"
    js = json.load(open(wav[:-4] + ".json"))
    continu = js.get("continu") is True
    fav = i > 0 and (s.get("transition") or m.get("transition_defaut", "fondu")) != "coupe"
    nxt = sc[i + 1] if i + 1 < len(sc) else None
    fap = nxt is not None and (nxt.get("transition") or m.get("transition_defaut", "fondu")) != "coupe"
    avant = (dt / 2 / fps if fav else 0) if continu else (0.15 if i == 0 else 0.3)
    resp = (dt / 2 / fps if fap else 0.02) if continu else m.get("respiration", 0.35)
    # pendant un fondu les plans se chevauchent de dt images : on retire ce chevauchement
    if fav: avant -= dt / fps
    morceaux += [sil(avant, f"a{i}"), wav, sil(resp, f"r{i}")] if avant > 0 else [wav, sil(resp, f"r{i}")]
open(f"{tmp}/l.txt","w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in morceaux))
subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",f"{tmp}/l.txt","-ar","44100","-b:a","192k",f"out/voix/{nom}.mp3"], check=True)
print(nom, "ok")
