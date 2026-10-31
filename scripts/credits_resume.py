#!/usr/bin/env python3
"""Résumé des crédits pour la description YouTube (seulement les médias du montage actuel) + liste complète pour commentaires.
Usage : python3 scripts/credits_resume.py <slug> <credits.txt> <sortie_prefixe>"""
import json, re, sys, collections
slug, src, out = sys.argv[1:4]
m = json.load(open(f"episodes/{slug}/montage.json", encoding="utf-8"))
ids = set()
for s in m["scenes"]:
    if s.get("media_ref") or s.get("fichier") or s.get("recherche"): ids.add(s["id"])
    for k, _ in enumerate(s.get("medias", []) or []): ids.add(f"{s['id']}-{k+1}")
musique, lignes = [], {}
for l in open(src, encoding="utf-8"):
    l = l.strip()
    if not l: continue
    if l.startswith("Musique"): musique.append(l.split(" : ", 1)[1]); continue
    i, reste = l.split(" : ", 1)
    if i in ids: lignes[i] = reste  # la dernière occurrence gagne (cache)
par_lic, pixa = collections.defaultdict(set), set()
for r in lignes.values():
    g = re.search(r"\((.*)\)\s*$", r).group(1)
    if g.startswith("Pixabay"): pixa.add(g.split(",", 1)[1].strip() if "," in g else g)
    elif g.startswith("Wikimedia Commons"):
        parts = [x.strip() for x in g.split(",")]
        lic, auteur = parts[-1] or "licence ?", ", ".join(parts[1:-1]) or "auteur inconnu"
        par_lic[lic].add(auteur)
txt = ["Musique :"] + [f"- {x}" for x in dict.fromkeys(musique)] + ["", "Images et vidéos — Wikimedia Commons :"]
txt += [f"- {lic} : " + ", ".join(sorted(a)) for lic, a in sorted(par_lic.items())]
txt += ["Pixabay (licence Pixabay) : " + ", ".join(sorted(pixa))]
open(out + "-resume.txt", "w").write("\n".join(txt) + "\n")
urls = sorted({re.match(r"(\S+)", r).group(1) + " " + re.search(r"\((.*)\)\s*$", r).group(1) for r in lignes.values()})
open(out + "-liens.txt", "w").write("Crédits complets (liens) :\n" + "\n".join(urls) + "\n")
print(len(lignes), "médias ;", len(par_lic), "licences Commons ;", len(pixa), "auteurs Pixabay ;", sum(len(x) for x in txt), "caractères")
