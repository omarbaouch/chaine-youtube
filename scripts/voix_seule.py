#!/usr/bin/env python3
"""Voix Edge Vivienne + minutage mot à mot pour un Short animé : videos/_anim/<slug>/voix.txt → out/anim/<slug>-voix.mp3 + -mots.json"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from voix_edge import dire_avec_mots
src = Path(sys.argv[1]); slug = src.parent.name
out = Path("out/anim"); out.mkdir(parents=True, exist_ok=True)
texte = " ".join(l.strip() for l in src.read_text(encoding="utf-8").splitlines() if l.strip())
mots = dire_avec_mots(texte, "fr-FR-VivienneMultilingualNeural", str(out / f"{slug}-voix.mp3"), debit="+10%", lang=False)
(out / f"{slug}-mots.json").write_text(json.dumps(mots, ensure_ascii=False, indent=1), encoding="utf-8")
print(slug, len(mots), "mots", mots[-1]["fin"] if mots else 0)
