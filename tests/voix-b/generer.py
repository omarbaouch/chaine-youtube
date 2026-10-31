#!/usr/bin/env python3
"""Vivienne (multilingue) bascule en anglais sur les phrases courtes isolées (« Six centimes. »).
Test : 1) Vivienne, phrase courte isolée ; 2) Vivienne, phrase courte rattachée ; 3) Denise (100 % français) ; 4) Henri (sceptique)."""
import os, sys
sys.path.insert(0, "scripts")
import voix_edge
os.makedirs("out/voix", exist_ok=True)
T1 = "Dans cette baguette à un euro, le blé coûte… six centimes. Six centimes. Le meunier : sept centimes."
T2 = "Dans cette baguette à un euro, le blé coûte… six centimes. Oui, six petits centimes, pas un de plus. Et le meunier ? Sept centimes."
for nom, voix, t in [("1-vivienne-phrase-courte", "fr-FR-VivienneMultilingualNeural", T1),
                     ("2-vivienne-phrase-rattachee", "fr-FR-VivienneMultilingualNeural", T2),
                     ("3-denise-100pc-francais", "fr-FR-DeniseNeural", T1),
                     ("4-henri-sceptique", "fr-FR-HenriNeural", "Attends… quatre-vingt-trois centimes pour le boulanger ? Il se gave, non ?")]:
    voix_edge.dire(t, voix, f"out/voix/{nom}.mp3", "+5%", lang=False); print("✔", nom)
