#!/usr/bin/env python3
"""Test prononciation « centimes » avec Vivienne : avant / après forçage du français."""
import asyncio, os, subprocess, sys
sys.path.insert(0, "scripts")
import edge_tts
TEXTE = "Dans cette baguette à un euro, le blé coûte… six centimes. Six centimes. Le meunier : sept centimes."
V = "fr-FR-VivienneMultilingualNeural"
os.makedirs("out/voix", exist_ok=True)
asyncio.run(edge_tts.Communicate(TEXTE, V, rate="+8%").save("out/voix/A-avant.mp3")); print("✔ A")
import voix_edge
voix_edge.dire(TEXTE, V, "out/voix/B-francais-force.mp3", lang=False); print("✔ B")
for f in sorted(os.listdir("out/voix")):
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"out/voix/{f}"], capture_output=True, text=True).stdout.strip()
    print(f, d, os.path.getsize(f"out/voix/{f}"))
