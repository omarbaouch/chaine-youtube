#!/usr/bin/env python3
"""Repérage musique libre (Kevin MacLeod / Incompetech, CC-BY 4.0) par ambiance.
Écrit out/musique/catalogue.json (tout le catalogue utile) + télécharge 4 candidats par ambiance + extraits analysables."""
import json, os, subprocess, urllib.request, urllib.parse
os.makedirs("out/musique", exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (chaine-youtube musique)"}
def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
pieces = None
for u in ["https://incompetech.com/music/royalty-free/pieces.json", "https://incompetech.com/music/royalty-free/pieces.json?x=1"]:
    try:
        pieces = json.loads(get(u)); print("catalogue :", len(pieces), "morceaux"); break
    except Exception as e:
        print("échec", u, e)
if not pieces:
    raise SystemExit("catalogue introuvable")
json.dump(pieces[:3], open("out/musique/exemple_brut.json", "w"), indent=1)
AMB = {
 "tension": ["Suspenseful", "Dark", "Mysterious", "Tense"],
 "emotion": ["Somber", "Sad", "Melancholy", "Romantic", "Calming", "Peaceful"],
 "revelation": ["Epic", "Dramatic", "Intense", "Heroic", "Triumphant"],
 "leger": ["Bright", "Light", "Uplifting", "Playful", "Grooving", "Mysterious"],
}
def duree(p):
    v = str(p.get("length", "0") or "0")
    try:
        parts = [float(x) for x in v.split(":")]
        t = 0
        for x in parts: t = t * 60 + x
        return t
    except ValueError:
        return 0
def tags(p):
    return " ".join(str(p.get(k, "")) for k in ("feel", "genre", "instruments", "description")).lower()
choix = {}
for amb, mots in AMB.items():
    cand = [p for p in pieces if any(m.lower() in str(p.get("feel", "")).lower() for m in mots)]
    # durée longue (boucle facile), pas trop de percussions agressives pour l'émotion
    def score(p):
        d = duree(p)
        s = min(d, 300) / 60
        t = tags(p)
        if amb == "emotion" and "piano" in t: s += 3
        if amb in ("tension", "revelation") and ("orchestra" in t or "strings" in t or "cinematic" in t): s += 2
        if "vocal" in t or "voice" in t: s -= 5
        return s
    cand.sort(key=score, reverse=True)
    choix[amb] = cand[:6]
    print(f"\n== {amb} : {len(cand)} candidats")
    for p in cand[:6]:
        print("  ", p.get("title"), "|", p.get("feel"), "|", p.get("instruments"), "|", p.get("length"), "|", p.get("filename"))
json.dump({k: [{kk: p.get(kk) for kk in ("title", "filename", "feel", "genre", "instruments", "length", "bpm", "description")} for p in v] for k, v in choix.items()},
          open("out/musique/choix.json", "w"), ensure_ascii=False, indent=1)
for amb, lst in choix.items():
    for i, p in enumerate(lst[:4]):
        fn = p.get("filename") or (p.get("title", "") + ".mp3")
        url = "https://incompetech.com/music/royalty-free/mp3-royaltyfree/" + urllib.parse.quote(fn)
        dest = f"out/musique/{amb}-{i+1}.mp3"
        try:
            open(dest, "wb").write(get(url)); print("✔", dest, fn)
        except Exception as e:
            print("✗", url, e)
