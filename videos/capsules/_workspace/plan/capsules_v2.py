# Capsules v2 — « Le voyage à l'envers d'une capsule » (documentaire, émotion, vraies vidéos)
# Génère episodes/capsules/montage.json. Retour d'Omar 07/11 0 h 32 : ennui (photos fixes, trop d'écrans de texte, voix monotone, histoire).
import json, sys
sys.path.insert(0, '/tmp/claude-0/-home-claude/3e299887-a5a8-5943-804a-16a7d66faba1/scratchpad')
import refs
C = refs.C
def R(x):
    p, c = x.split(); return C[p][c]['ref']

CTX = 'wc:File:The bean that could save coffee from climate change.webm'   # Context (Thomson Reuters Foundation), CC BY-SA 4.0
TVB = 'wc:File:Antiga plantação de café em São Paulo atrai visitantes.webm'  # TV Brasil, CC BY 3.0
MAC = 'wc:File:Macro Espresso Process.webm'                                  # CC BY 2.0
PAN = 'wc:File:Pantheon, Rome 123028.webm'
ROM = 'wc:File:Flight over Rome 184729.webm'
CTX_CROP = [0.06, 0.08, 0.8]   # enlève le logo « Context » et les sous-titres anglais incrustés
TVB_CROP = [0.03, 0.05, 0.7]   # enlève le logo, l'horloge et l'interprète en langue des signes

def W(ref, t, d=6, crop=None):
    m = {"media_ref": ref, "extrait": t, "extrait_duree": d}
    if crop: m["recadre"] = crop
    return m

T, E, RV, L = 'tension', 'emotion', 'revelation', 'leger'
def mots(t, h, a=0.3, pos='haut'): return {"type": "mots", "texte": t, "heros": h, "position": pos, "a": a}
def src(t, a=0.8): return {"type": "source", "texte": t, "a": a}
def etape(n, t, a=0.2): return {"type": "etiquette", "numero": n, "texte": t, "a": a}
def carton(t, st, a=0.8): return {"type": "carton", "texte": t, "sous_texte": st, "a": a}
CLIC = [{"nom": "metal", "a": 0.05, "volume": 0.55}]

def rush(i, texte, media, amb, look=None, **kw):
    d = {"id": i, "format": "rush", "texte": texte, "ambiance": amb}
    d.update(media if isinstance(media, dict) else {"media_ref": media})
    if look: d["look"] = look
    d.update(kw); return d

def mosa(i, texte, medias, amb, **kw):
    d = {"id": i, "format": "mosaique", "texte": texte, "ambiance": amb,
         "medias": [m if isinstance(m, dict) else {"media_ref": m} for m in medias]}
    d.update(kw); return d

S = [
# ── PROLOGUE ─────────────────────────────────────────────────────────
rush("v001", "Ton café en capsule, tu le paies combien au kilo ?", R("P01 I3"), T, "bijou",
     couches=[mots("? € LE KILO", "?", 0.1)], sons=CLIC),
{"id": "v002", "format": "schema", "texte": "Vingt euros ? Soixante ? Cent vingt ? Garde ta réponse.", "ambiance": T,
 "media_ref": R("Q08 I4"), "etiquette_schema": "À toi de deviner", "duree_min": 3.6,
 "schema": {"type": "liste", "titre": "Ton café en capsule : combien au kilo ?",
            "elements": [{"texte": "A", "valeur": "20 € ?"}, {"texte": "B", "valeur": "60 € ?"}, {"texte": "C", "valeur": "120 € ?"}],
            "source": "Réponse plus loin"}, "sons": [{"nom": "tick", "a": 1.4, "volume": 0.3}, {"nom": "tick", "a": 2.0, "volume": 0.3}]},
rush("v003", "Pour la trouver, on va faire le chemin de ta capsule… à l'envers.", R("V01 V7"), T, "bijou"),
rush("v004", "De ta cuisine…", R("V13 V2"), T),
rush("v005", "…jusqu'à la main qui a cueilli ton café, à des milliers de kilomètres.", W(CTX, 492, 5, CTX_CROP), E, "champ"),
rush("v006", "Sur la route, un homme qui a inventé ta capsule… et qu'on a poussé dehors.", W(MAC, 22, 6), E, "bijou"),
rush("v007", "Et une question : sur tes quarante-cinq centimes, qui garde quoi ?", R("P27 V1"), T,
     punch={"a": 2.6, "texte": "QUI GARDE QUOI ?"}),
{"id": "v008", "format": "titre", "type": "titre", "texte": "", "numero": "", "titre": "La capsule", "sous_titre": "Le Vrai Prix · Épisode 4",
 "media_ref": R("V06 V6"), "duree_min": 3.0, "ambiance": E, "look": "bijou",
 "sons": [{"nom": "riser", "a": 0, "volume": 0.35}, {"nom": "impact", "a": 0.3, "volume": 0.7}]},

# ── ÉTAPE 1 : TA CUISINE ────────────────────────────────────────────
rush("v009", "Première étape : ta cuisine. Une capsule, quarante-cinq centimes.", R("Q03 C1"), T, "bijou",
     couches=[etape("01", "TA CUISINE")], sons=CLIC),
rush("v010", "Dedans, cinq grammes de café. Il en faut deux cents pour faire un kilo.", R("Q08 I3"), T,
     punch={"a": 3.2, "texte": "200 CAPSULES"}, couches=[src("Nespresso (FAQ) : 5 g par capsule", 0.6)]),
{"id": "v011", "format": "schema", "texte": "Alors, ta réponse ?", "ambiance": RV, "media_ref": R("Q02 I4"), "etiquette_schema": "Ta réponse ?",
 "duree_min": 4.2, "schema": {"type": "devine", "question": "Ton café en capsule, au kilo ?", "choix": ["20 €", "60 €", "120 €"], "bonne": 1, "secondes": 2},
 "sons": [{"nom": "tick", "a": 1.0, "volume": 0.3}, {"nom": "tick", "a": 1.6, "volume": 0.3}, {"nom": "impact", "a": 2.4, "volume": 0.7}]},
rush("v012", "Près de soixante euros le kilo, en moyenne. Trois fois le prix du même café en grains.", R("V09 V8"), RV,
     couches=[{"type": "compteur", "vers": 60, "decimales": 0, "suffixe": " €/kg", "legende": "les capsules, en moyenne",
               "source": "UFC-Que Choisir, 08/12/2025", "a": 0.3, "position": "centre"}]),
mosa("v013", "Bah, c'est le prix du génie ! Une invention pareille, ça se paie !", [R("V01 V11"), R("Q02 C5")], T, voix="sceptique"),
rush("v014", "Une invention de génie, oui. Mais son inventeur a eu un drôle de destin.", R("P05 C1"), E, "bijou"),

# ── L'INVENTEUR ─────────────────────────────────────────────────────
rush("v015", "Rome, mille neuf cent soixante-quinze. Éric Favre, ingénieur chez Nestlé, y passe du temps avec sa femme, Anna-Maria.",
     W(ROM, 10, 7), E, surtitre="Rome, 1975"),
mosa("v016", "Ils ont leurs habitudes dans un café, près du Panthéon : le Sant'Eustachio.",
     [W(PAN, 8, 4), {"media_ref": R("Q09 C1"), "legende": "Le Sant'Eustachio"}], E),
rush("v017", "Favre veut prouver à sa femme qu'il peut faire l'espresso parfait.", R("V01 V3"), E, "bijou"),
mosa("v018", "Il interroge le personnel. Et le barista, Eugenio, finit par lui montrer son geste.", [R("P05 I6"), R("P05 C2")], E),
rush("v019", "Il actionne le levier par petits coups. De l'air entre dans l'eau… et le goût change tout.", W(MAC, 34, 7), E, "bijou"),
rush("v020", "Favre a son idée : enfermer ce secret dans une capsule.", R("Q02 C5"), E, "bijou", sons=CLIC),
rush("v021", "Il le résumera ainsi : « Je n'ai pas inventé une capsule, j'ai inventé une formule. »", R("V06 V12"), E, "bijou",
     couches=[carton("« J'AI INVENTÉ UNE FORMULE »", "Éric Favre · OMPI Magazine, 2010", 1.4)]),
rush("v022", "Mille neuf cent quatre-vingt-six : Nespresso sort, d'abord pour les bureaux. C'est un échec.", R("P05 C7"), T,
     surtitre="1986", punch={"a": 4.0, "texte": "ÉCHEC"}),
rush("v023", "Mille neuf cent quatre-vingt-onze : Nespresso peine encore. Éric Favre est poussé vers la sortie.", R("P10 C1"), E,
     surtitre="1991", couches=[src("House of Switzerland (DFAE)")]),
rush("v024", "Il quitte l'entreprise avant que sa capsule ne devienne un succès mondial.", R("V13 V5"), E,
     couches=[carton("POUSSÉ DEHORS", "", 0.6)]),
rush("v025", "Garde son nom en tête. La fin de son histoire répond à notre question.", R("V06 V11"), T, "bijou"),

# ── ÉTAPE 2 : LE PORT ───────────────────────────────────────────────
rush("v026", "On remonte le chemin. Avant ton magasin, ton café a traversé l'océan.", R("V12 V11"), T,
     couches=[etape("02", "LE PORT")]),
mosa("v027", "Il voyage en sacs de jute. Il arrive cru : c'est du café vert.", [W(CTX, 156, 5, CTX_CROP), W(CTX, 480, 5, CTX_CROP)], T),

# ── ÉTAPE 3 : LA BOURSE ─────────────────────────────────────────────
rush("v028", "Son prix se joue à la bourse de New York. En deux mille vingt-cinq, il a doublé.", R("V10 V2"), T,
     couches=[etape("03", "LA BOURSE")], punch={"a": 4.2, "texte": "× 2"}),
mosa("v029", "Tu vois ! Voilà pourquoi ta capsule est si chère !", [R("V11 V1"), R("V09 V1")], T, voix="sceptique"),
rush("v030", "Sauf que depuis, il a perdu trente et un pour cent en un an.", R("V10 V4"), T,
     punch={"a": 2.2, "texte": "− 31 %"}, couches=[src("Trading Economics, 06/11/2026", 0.5)]),
{"id": "v031", "format": "schema", "texte": "Alors devine : le café vert de ta capsule, au prix de la bourse… il vaut combien ?",
 "ambiance": T, "media_ref": R("P20 I7"), "etiquette_schema": "À toi de deviner", "duree_min": 4.0,
 "schema": {"type": "liste", "titre": "Le café de ta capsule vaut…", "elements": [{"texte": "A", "valeur": "3 c ?"}, {"texte": "B", "valeur": "10 c ?"},
            {"texte": "C", "valeur": "20 c ?"}], "source": "Réponse au champ"}},

# ── ÉTAPE 4 : LE CHAMP ──────────────────────────────────────────────
rush("v032", "Dernière étape. Le début de tout.", R("V04 V2"), E, "champ", couches=[etape("04", "LE CHAMP")],
     sons=[{"nom": "riser", "a": 0.2, "volume": 0.3}]),
rush("v033", "Ton café, c'est la graine d'une cerise. Elle mûrit sur un arbuste, sous les tropiques.", W(CTX, 396, 6, CTX_CROP), E, "champ"),
rush("v034", "On la cueille souvent à la main.", W(TVB, 48, 5, TVB_CROP), E, "champ"),
mosa("v035", "Puis on la sèche au soleil, on la trie, on la décortique.", [W(CTX, 48, 4, CTX_CROP), R("V03 V1")], E, look="champ"),
rush("v036", "Au Brésil, premier producteur du monde, Henrique Sloper cultive du café.", W(CTX, 70, 6, CTX_CROP), E, "champ",
     couches=[src("Images : Context (Thomson Reuters Foundation), CC BY-SA 4.0", 0.6)]),
{"id": "v037", "format": "schema", "texte": "Ta réponse ? Le café de ta capsule vaut…", "ambiance": RV, "media_ref": R("P13 C5"),
 "etiquette_schema": "Ta réponse ?", "duree_min": 4.2,
 "schema": {"type": "devine", "question": "Le café vert de ta capsule ?", "choix": ["3 c", "10 c", "20 c"], "bonne": 0, "secondes": 2},
 "sons": [{"nom": "tick", "a": 1.0, "volume": 0.3}, {"nom": "tick", "a": 1.6, "volume": 0.3}]},
rush("v038", "Trois centimes. Cinq grammes de café vert, au prix de la bourse.", W(TVB, 63, 5, TVB_CROP), RV, "champ",
     couches=[{"type": "compteur", "vers": 3, "decimales": 0, "suffixe": " c", "legende": "le café vert de ta capsule",
               "source": "ICE arabica 2,80 $/lb (06/11/2026), 1 € = 1,117 $", "a": 0.4, "position": "centre"}],
     sons=[{"nom": "impact", "a": 0.4, "volume": 0.7}]),
rush("v039", "Et ces trois centimes, le caféiculteur ne les touche même pas en entier.", W(TVB, 57, 5, TVB_CROP), E, "champ"),
rush("v040", "Sur vingt ans, la part du prix restée dans les pays producteurs est passée de vingt-quatre à seize pour cent.",
     W(CTX, 120, 8, CTX_CROP), E, "champ", punch={"a": 5.0, "texte": "24 % → 16 %"}, couches=[src("BASIC / Max Havelaar, 2018")]),
rush("v041", "Au Pérou et en Éthiopie, en deux mille dix-sept, les caféiculteurs gagnaient vingt pour cent de moins qu'en deux mille cinq.",
     R("P24 C6"), E, "champ", couches=[src("BASIC 2018, repris par la RTBF")], punch={"a": 5.2, "texte": "− 20 %"}),

# ── LA VÉRITÉ ───────────────────────────────────────────────────────
{"id": "v042", "format": "titre", "type": "titre", "texte": "", "numero": "", "titre": "La vérité", "sous_titre": "Qui garde la différence ?",
 "media_ref": R("P29 V4"), "duree_min": 2.6, "ambiance": RV, "look": "bijou",
 "sons": [{"nom": "riser", "a": 0, "volume": 0.35}, {"nom": "impact", "a": 0.25, "volume": 0.7}]},
rush("v043", "Quarante-cinq centimes payés. Trois pour le café. Où partent les quarante-deux autres ?", R("Q01 C5"), RV, "bijou",
     punch={"a": 4.4, "texte": "42 c ?"}),
rush("v044", "Deux centimes pour l'État : la TVA du café, à cinq virgule cinq pour cent.", R("P27 C7"), RV,
     couches=[src("Code général des impôts, art. 278-0 bis")]),
{"id": "v045", "format": "schema", "texte": "Et le reste ? Torréfacteurs et magasins gardent… trente, soixante, ou quatre-vingt-cinq pour cent ?",
 "ambiance": RV, "media_ref": R("P32 C2"), "etiquette_schema": "La dernière devinette", "duree_min": 4.6,
 "schema": {"type": "devine", "question": "Torréfacteurs + magasins : quelle part ?", "choix": ["30 %", "60 %", "85 %"], "bonne": 2, "secondes": 2},
 "sons": [{"nom": "tick", "a": 1.0, "volume": 0.3}, {"nom": "tick", "a": 1.6, "volume": 0.3}, {"nom": "impact", "a": 2.4, "volume": 0.7}]},
rush("v046", "Entre quatre-vingt-cinq et quatre-vingt-dix pour cent du prix. Torréfaction, aluminium, pub, boutiques… et marges.",
     R("Q08 C2"), RV, "bijou",
     couches=[{"type": "compteur", "vers": 85, "decimales": 0, "suffixe": " à 90 %", "legende": "pour torréfacteurs et distributeurs",
               "source": "BASIC / Max Havelaar / Commerce Équitable France, 2018", "a": 0.3, "position": "centre"}]),
{"id": "v047", "format": "ecran_partage", "texte": "Ta capsule, c'est quinze fois le prix du café qu'elle contient.", "ambiance": RV,
 "media_ref": R("Q02 C3"), "cote": "gauche", "etiquette_schema": "Ta capsule à 45 c",
 "schema": {"type": "decomposition", "titre": "Ta capsule à 45 c", "total": 45, "unite": " c", "decimales": 0,
            "parts": [{"label": "Café vert", "valeur": 3, "heros": True}, {"label": "État (TVA)", "valeur": 2},
                      {"label": "Marque, magasin, emballage…", "valeur": 40}], "source": "Calculs ; BASIC 2018 ; CGI"}},
mosa("v048", "Donc on se fait avoir ?", [R("P26 C8"), R("V13 V4")], T, voix="sceptique"),
mosa("v049", "Non. Tu paies une marque et du confort. Et pour payer moins : compatibles, ou capsule réutilisable à dix centimes la tasse.",
     [R("Q02 C7"), R("P20 V2")], L, couches=[src("graindexpert 04/11/2026 ; calcul 5 g à 20 €/kg")]),

# ── LA FIN D'ÉRIC FAVRE ────────────────────────────────────────────
rush("v050", "Et Éric Favre ? Il fonde sa propre entreprise, Monodor… et fabrique des capsules pour d'autres marques.", R("P25 C8"), E,
     couches=[src("OMPI Magazine, 2010")]),
rush("v051", "Contre Nestlé, des années de procès. Jusqu'à un accord, en deux mille trois.", R("P23 I8"), E, surtitre="2003"),
rush("v052", "Des années plus tard, il écrira : « De toutes mes erreurs, celle que je regrette le plus, c'est d'avoir mis si longtemps à faire les autres. »",
     W(MAC, 46, 10), E, "bijou",
     couches=[carton("« SI LONGTEMPS À FAIRE LES AUTRES »", "Éric Favre, 2014 · House of Switzerland (traduit)", 3.2)]),
rush("v053", "Abonne-toi : la semaine prochaine, le vrai prix de ton chauffage.", R("V13 V12"), L),
rush("v054", "Et demain matin, au moment du clic… tu sauras où partent tes quarante-cinq centimes.", R("Q03 C1"), E, "bijou",
     sons=[{"nom": "metal", "a": 2.6, "volume": 0.6}]),
]

ess = json.load(open('/home/claude/chaine-youtube/episodes/essence/montage.json'))
m = {k: v for k, v in ess.items() if k != 'scenes'}
m['titre'] = "Capsule de café : combien tu la paies au kilo ?"
m['voix'] = dict(m['voix'], debit="+4%", debit_continu="+4%")
vus = {}
for s in S:
    s.setdefault('transition', 'coupe')
    if s.get('look') == 'bijou' and s['format'] not in ('rush', 'titre'): s.pop('look')
    for r in ([x['media_ref'] for x in s.get('medias', [])] or [s.get('media_ref')]):
        if r: vus.setdefault((r, json.dumps([x.get('extrait') for x in s.get('medias', [])] or s.get('extrait'))), []).append(s['id'])
m['scenes'] = S
json.dump(m, open('/home/claude/chaine-youtube/episodes/capsules/montage.json', 'w'), ensure_ascii=False, indent=1)
w = sum(len(s['texte'].split()) for s in S)
vid = sum(1 for s in S for r in ([x['media_ref'] for x in s.get('medias', [])] or [s.get('media_ref')]) if r and (r.startswith('pv:') or r.endswith('.webm')))
tot = sum(1 for s in S for r in ([x['media_ref'] for x in s.get('medias', [])] or [s.get('media_ref')]) if r)
print(len(S), 'plans,', w, 'mots ≈', round(w / 2.9 / 60, 1), 'min de voix ; vidéos', vid, '/', tot)
print('doublons', {k[0][:40]: v for k, v in vus.items() if len(v) > 1})
