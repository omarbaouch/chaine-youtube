#!/usr/bin/env python3
"""Exécute une liste d'appels d'outils OpenMontage (dossier studio/) — lancé sur GitHub Actions.

La session Claude prépare les décisions (brief, script, plan de scènes…) et écrit un fichier d'appels :
  videos/<slug>/appels/<etape>.json = {"appels": [{"outil": "direct_clip_search", "entrees": {...}, "nom": "m1"}]}
Ce script les exécute dans studio/, écrit les résultats dans videos/<slug>/resultats/<etape>.json
et laisse les médias produits dans studio/projects/<slug>/ (publiés en Release par le workflow).
Usage : python scripts/studio_executer.py videos/<slug>/appels/<etape>.json
"""
import json
import os
import sys
import traceback
from pathlib import Path

DEPOT = Path(__file__).resolve().parents[1]
fichier = (DEPOT / sys.argv[1]).resolve()
slug, etape = fichier.parts[-3], fichier.stem
os.chdir(DEPOT / "studio")
sys.path.insert(0, str(DEPOT / "studio"))
from tools.tool_registry import registry  # noqa: E402

registry.discover()
demande = json.loads(fichier.read_text(encoding="utf-8"))
resultats = []
for appel in demande.get("appels", []):
    outil = registry.get(appel["outil"])
    if outil is None:
        resultats.append({"nom": appel.get("nom"), "outil": appel["outil"], "succes": False, "erreur": "outil inconnu"})
        continue
    entrees = dict(appel.get("entrees", {}))
    entrees.setdefault("project_dir", str(DEPOT / "studio" / "projects" / slug))
    print(f"▶ {appel.get('nom', '')} · {appel['outil']}", flush=True)
    try:
        r = outil.execute(entrees)
        resultats.append({"nom": appel.get("nom"), "outil": appel["outil"], "succes": r.success, "erreur": r.error,
                          "donnees": r.data, "fichiers": r.artifacts, "cout_usd": r.cost_usd})
        print(("  ✔ " if r.success else "  ✗ ") + (r.error or f"{len(r.artifacts)} fichier(s)"), flush=True)
    except Exception as exc:  # noqa: BLE001
        resultats.append({"nom": appel.get("nom"), "outil": appel["outil"], "succes": False, "erreur": repr(exc),
                          "trace": traceback.format_exc()[-2000:]})
        print(f"  ✗ {exc!r}", flush=True)

sortie = DEPOT / "videos" / slug / "resultats" / f"{etape}.json"
sortie.parent.mkdir(parents=True, exist_ok=True)
sortie.write_text(json.dumps(resultats, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
print(f"✔ résultats → {sortie.relative_to(DEPOT)}")
if demande.get("inventaire"):
    inv = DEPOT / "videos" / slug / "resultats" / "inventaire-outils.json"
    inv.write_text(json.dumps(registry.provider_menu_summary(), ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(f"✔ inventaire des outils → {inv.relative_to(DEPOT)}")
