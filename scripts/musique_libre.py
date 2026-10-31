#!/usr/bin/env python3
"""Musique libre automatique par ambiance : Kevin MacLeod (incompetech.com), licence CC-BY 4.0.
Usage : python3 scripts/musique_libre.py <slug>
Lit montage.musiques_titres (facultatif) sinon la liste par défaut ; télécharge public/musique/<ambiance>.mp3 ;
ajoute les crédits obligatoires dans public/ep/<slug>/credits.txt. Aucun compte, aucune clé, gratuit."""
import json, os, sys, urllib.parse, urllib.request
slug = sys.argv[1]
montage = json.load(open(f"episodes/{slug}/montage.json", encoding="utf-8"))
UA = {"User-Agent": "Mozilla/5.0 (chaine-youtube musique)"}
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90).read()
# Choix éditorial (ordre de préférence) : morceaux cinématiques connus, sans voix
DEFAUT = {
  "tension":    ["Lightless Dawn", "Long Note Four", "Dark Times", "Ossuary 6 - Air", "Unseen Horrors", "The Escalation"],
  "emotion":    ["Heartbreaking", "Sad Trio", "Lasting Hope", "Long Road Ahead B", "Bittersweet", "Dreamer"],
  "revelation": ["Five Armies", "Volatile Reaction", "Ascending the Vale", "Heroic Age", "Crusade - Heavy Industry", "Noble Race"],
  "leger":      ["Investigations", "Hidden Agenda", "Sneaky Snitch", "Night on the Docks - Piano", "Thinking Music", "Fluffing a Duck"],
}
voulues = montage.get("musiques_titres", DEFAUT)
pieces = json.loads(get("https://incompetech.com/music/royalty-free/pieces.json"))
par_titre = {p.get("title", "").lower(): p for p in pieces}
os.makedirs("public/musique", exist_ok=True)
credits = []
for amb, titres in voulues.items():
    dest = f"public/musique/{amb}.mp3"
    for t in titres:
        p = par_titre.get(t.lower())
        if not p:
            print(f"  {amb} : « {t} » absent du catalogue"); continue
        fn = p.get("filename") or f"{p['title']}.mp3"
        try:
            open(dest, "wb").write(get("https://incompetech.com/music/royalty-free/mp3-royaltyfree/" + urllib.parse.quote(fn)))
        except Exception as e:
            print(f"  {amb} : échec {fn} ({e})"); continue
        credits.append(f'Musique ({amb}) : "{p["title"]}" Kevin MacLeod (incompetech.com) — Licensed under Creative Commons: By Attribution 4.0 License http://creativecommons.org/licenses/by/4.0/')
        print(f"✔ {amb} : {p['title']} ({p.get('feel')})")
        break
os.makedirs(f"public/ep/{slug}", exist_ok=True)
open(f"public/ep/{slug}/credits-musique.txt", "w").write("\n".join(credits) + "\n")
