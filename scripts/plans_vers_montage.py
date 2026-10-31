#!/usr/bin/env python3
"""Transforme videos/<slug>/plans.json (découpage du scénariste) en episodes/<slug>/montage.json (entrée du pipeline).
Usage : python3 scripts/plans_vers_montage.py <slug> [fichier_reglages.json]
Le fichier de réglages (facultatif) fusionne des corrections du monteur par id de plan : {"p042": {"media_ref": "..."}}.
"""
import json
import sys

slug = sys.argv[1]
plans = json.load(open(f"videos/{slug}/plans.json", encoding="utf-8"))
reglages = json.load(open(sys.argv[2], encoding="utf-8")) if len(sys.argv) > 2 else {}

GARDER = {"id", "format", "texte", "media_ref", "medias", "fichier", "schema", "etiquette_schema", "cote", "couches", "surtitre",
          "punch", "transition", "sons", "numero", "titre", "sous_titre", "duree_min", "zoom", "vitesse", "debut_media",
          "respiration", "avant_voix", "type", "voix", "ambiance"}
scenes = [dict(x) for x in reglages.get("_avant", [])]
for p in plans:
    s = {k: v for k, v in p.items() if k in GARDER}
    for k, v in reglages.get(p["id"], {}).items():
        if v is None:
            s.pop(k, None)
        else:
            s[k] = v
    if s.get("format") == "titre":
        s["type"] = "titre"
        s["duree_min"] = min(s.get("duree_min", 2.2), 2.2)
    if s.get("medias"):
        s["medias"] = [{k: v for k, v in m.items() if k in ("media_ref", "legende", "fichier")} for m in s["medias"]]
    scenes.append(s)

base = reglages.get("_episode", {})
montage = {
    "titre": base.get("titre", slug),
    "format": {"largeur": 1920, "hauteur": 1080, "fps": 30},
    "transition_defaut": "coupe",
    "duree_transition": 8,
    "voix": {"modele": "french_24l", "locuteur": "estelle", "etapes": 5, "temperature": 0.3, "pause_phrase": 0.2},
    "musique": {"fichier": "../../public/sfx/musique-enquete.wav", "volume": 0.14},
    "etalonnage": {"contraste": 1.06, "saturation": 1.08, "luminosite": 1},
    "grain": True,
    "sous_titres": {"actifs": True, "mots_par_ligne": 4},
    "scenes": scenes,
}
for k in ("voix", "musique", "musiques", "etalonnage", "transition_defaut", "duree_transition", "rushes_a_refaire", "respiration"):
    if k in base:
        montage[k] = base[k]
json.dump(montage, open(f"episodes/{slug}/montage.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"✔ episodes/{slug}/montage.json : {len(scenes)} scènes")
