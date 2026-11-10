"""Source du montage Black Friday (10/11/2026). Génère episodes/black-friday/montage.json et les lots de repérage.
Usage : python3 videos/black-friday/_workspace/montage_src.py [--lots]
Les médias choisis à l'œil sur les planches de repérage sont dans CHOIX (scène -> media_ref, ou liste pour une mosaïque)."""
import json, os, sys

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SRC_UFC = "UFC-Que Choisir, 26/11/2025"
SRC_UE = "Commission européenne, 26/03/2026"

CHOIX = {}  # rempli après repérage
CHOIX_FICHIER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "choix_rushes.json")
if os.path.exists(CHOIX_FICHIER):
    CHOIX = json.load(open(CHOIX_FICHIER))


def R(id, texte, recherche=None, fichier=None, **kw):
    s = {"id": id, "format": "rush", "texte": texte}
    if fichier: s["fichier"] = "medias/" + fichier
    if recherche: s["recherche"] = recherche
    s.update(kw)
    return s


def S(id, texte, schema, **kw):
    s = {"id": id, "format": "schema", "texte": texte, "schema": schema}
    s.update(kw)
    return s


def T(id, numero, titre, recherche, **kw):
    s = {"id": id, "format": "titre", "type": "titre", "numero": numero, "titre": titre, "texte": "", "recherche": recherche, "duree_min": 2.6}
    s.update(kw)
    return s


def E(id, texte, schema, recherche=None, fichier=None, etiquette=None, cote="gauche", **kw):
    s = {"id": id, "format": "ecran_partage", "texte": texte, "schema": schema, "cote": cote}
    if fichier: s["fichier"] = "medias/" + fichier
    if recherche: s["recherche"] = recherche
    if etiquette: s["etiquette_schema"] = etiquette
    s.update(kw)
    return s


def M(id, texte, recherches, legendes=None, fichiers=None, **kw):
    s = {"id": id, "format": "mosaique", "texte": texte}
    if fichiers:
        s["medias"] = [{"fichier": "medias/" + f, **({"legende": legendes[i]} if legendes else {})} for i, f in enumerate(fichiers)]
    else:
        s["recherche"] = recherches
        s["_legendes"] = legendes
    s.update(kw)
    return s


def devine(id, texte, question, choix, **kw):
    return S(id, texte, {"type": "devine", "question": question, "choix": choix, "secondes": 3},
             sons=[{"nom": "tick", "a": 0.2, "volume": 0.3}], **kw)


def src(t):
    return {"type": "source", "texte": t}


TICK = lambda a=0.1: {"nom": "tick", "a": a, "volume": 0.35}
IMPACT = lambda a: {"nom": "impact", "a": a, "volume": 0.5}

scenes = [
    # ── 00 Accroche ─────────────────────────────────────────────────────────────
    R("s001", "Moins cinquante-trois pour cent sur ce casque,", fichier="casque_q.png", zoom="avant", ambiance="tension",
      couches=[src(SRC_UFC + " (relevé de l'annonce)")]),
    R("s002", "c'est une vraie promo ?", fichier="casque_53.png", zoom="avant", punch={"a": 0.5, "texte": "VRAIE PROMO ?"},
      sons=[IMPACT(0.5)]),
    R("s003", "Combien tu économises vraiment, toi,", ["black over ear headphones close up", "wireless headphones black studio", "headphones product dark background"]),
    R("s004", "si tu l'achètes à ce prix-là ?", ["woman putting on headphones", "man wearing black headphones", "headphones on head close up"]),
    R("s005", "Ce prix barré, trois cent quatre-vingt-dix-neuf euros quatre-vingt-quinze,", fichier="casque_barre.png", zoom="arriere"),
    R("s006", "est parfaitement légal.", fichier="casque_legal.png", zoom="avant", sons=[IMPACT(0.3)]),
    R("s007", "Première devinette : à ce prix barré, il s'est vendu combien de temps ?",
      ["calendar pages turning", "wall calendar month close up", "calendar flipping pages"]),
    R("s008", "Jamais,", fichier="casque_d1.png", zoom="aucun", sons=[TICK()]),
    R("s009", "pendant un seul jour,", fichier="casque_d2.png", zoom="aucun", sons=[TICK()]),
    R("s010", "ou pendant un mois entier ?", fichier="casque_d3.png", zoom="avant", sons=[TICK()], duree_min=2.4),
    R("s011", "Garde ta réponse en tête, et imagine que ce casque, tu le veux.",
      ["hand holding headphones", "unboxing headphones", "headphones in hands close up"]),
    R("s012", "Il est dans ton panier, et ton doigt est sur le bouton payer.",
      ["online shopping smartphone close up", "finger tapping smartphone shopping app", "shopping cart on phone screen"]),
    R("s013", "Avant de payer, on vérifie ce prix barré, en commençant par la loi.",
      ["credit card online payment laptop", "paying online with credit card", "hand holding credit card laptop"]),
    # ── 01 La loi ──────────────────────────────────────────────────────────────
    T("s014", "01", "Prix barré : c'est légal ?", ["price tags store shelf", "supermarket price labels close up"], ambiance="enquete"),
    E("s015", "Depuis le vingt-huit mai deux mille vingt-deux, une règle encadre les prix barrés en France.",
      {"type": "liste", "titre": "La règle des prix barrés", "elements": [{"texte": "En vigueur depuis le", "valeur": "28 mai 2022", "heros": True},
       {"texte": "Texte", "valeur": "Code de la conso, L112-1-1"}], "source": "Code de la consommation, art. L112-1-1"},
      ["supermarket aisle shopping", "shoppers in supermarket aisle", "grocery store shelves"], etiquette="La loi"),
    S("s016", "Le prix barré doit être le prix le plus bas pratiqué ces trente derniers jours.",
      {"type": "chiffre", "valeur": 30, "suffixe": " jours", "legende": "Prix barré = le prix le plus bas des 30 derniers jours",
       "comparaison": "Pour tous les clients, chez ce vendeur", "source": "Code de la consommation, art. L112-1-1"},
      etiquette_schema="La règle des 30 jours"),
    R("s017", "Pas un prix d'il y a deux ans : le plus bas du dernier mois.",
      ["price tag gun labeling", "shop assistant putting price tags", "employee labeling products store"],
      couches=[{"type": "mots", "texte": "LE PLUS BAS DU MOIS", "heros": "DU MOIS", "position": "haut", "a": 0.3}]),
    E("s018", "Et si le vendeur enchaîne plusieurs remises, la référence reste le prix d'avant la première.",
      {"type": "processus", "titre": "Promos en cascade", "etapes": ["Prix d'avant", "1re remise", "2e remise"], "actif": 0,
       "source": "Code de la consommation, art. L112-1-1"},
      ["discount price tag sticker", "red sale price tag", "price reduction label"], etiquette="Remises successives", cote="droite"),
    R("s019", "Alors, ce casque, il a vraiment été vendu trois cent quatre-vingt-dix-neuf euros quatre-vingt-quinze ?",
      fichier="casque_prix.png", zoom="avant"),
    R("s020", "Réponse à la première devinette : un mois entier, tout le mois avant la promo.", fichier="casque_mois.png",
      zoom="avant", punch={"a": 2.0, "texte": "1 MOIS"}, sons=[IMPACT(2.0)], couches=[src(SRC_UFC)]),
    R("s021", "C'est l'U F C Que Choisir qui l'a relevé, pour le Black Friday deux mille vingt-cinq.", fichier="ufc_titre.png", zoom="arriere"),
    R("s022", "À chaque Black Friday, son observatoire part à la pêche aux fausses promos sur internet.", fichier="ufc_peche.png",
      zoom="avant", couches=[src(SRC_UFC)]),
    R("s023", "Donc le prix barré est vrai, la loi est respectée, et la promo est réelle ?",
      ["man looking at smartphone surprised", "surprised man reading phone", "woman looking at phone confused"]),
    S("s024", "Pas si vite, parce que la loi regarde trente jours en arrière, et pas un de plus.",
      {"type": "processus", "titre": "Ce que la loi regarde", "etapes": ["Juillet", "Septembre", "Les 30 derniers jours"], "actif": 2,
       "source": "Code de la consommation, art. L112-1-1"}, etiquette_schema="La fenêtre de 30 jours"),
    R("s025", "Et ce petit détail, un aspirateur va te montrer comment on s'en sert.",
      ["cordless stick vacuum cleaner", "vacuum cleaner cleaning floor", "stick vacuum close up"]),
    # ── 02 Aspirateur ──────────────────────────────────────────────────────────
    T("s026", "02", "Une fausse promo peut-elle être légale ?", ["online shopping laptop dark", "laptop screen shopping night"]),
    R("s027", "Même Black Friday, chez Boulanger : un aspirateur balai Dyson V huit Advanced.", fichier="aspi_q.png", zoom="avant",
      couches=[src(SRC_UFC)]),
    R("s028", "Affiché deux cent quarante-neuf euros au lieu de trois cent quatre-vingt-dix-neuf, soit moins trente-huit pour cent.",
      fichier="aspi_38.png", zoom="avant"),
    devine("s029", "À ton avis, la vraie réduction : moins trente, moins vingt, ou moins onze pour cent ?", "La vraie réduction ?",
           ["−30 %", "−20 %", "−11 %"]),
    R("s030", "Pour répondre, il faut remonter à l'été deux mille vingt-cinq.",
      ["summer city street sunny", "sunny summer day street", "summer sun sky"]),
    R("s031", "En juillet, cet aspirateur se vendait deux cent soixante-dix-neuf euros.", fichier="faille1.png", zoom="aucun"),
    R("s032", "Puis, en octobre, son prix grimpe nettement, juste avant la saison des promos.", fichier="faille2.png", zoom="aucun",
      sons=[IMPACT(0.6)]),
    R("s033", "En novembre, c'est ce prix gonflé qui sert de prix barré.", fichier="faille3.png", zoom="aucun"),
    R("s034", "Le jour J, on le baisse, et on affiche un gros pourcentage, calculé depuis ce prix gonflé.", fichier="faille4.png",
      zoom="aucun"),
    R("s035", "Mais regarde la ligne en pointillés : c'est le prix de juillet.", fichier="faille5.png", zoom="avant"),
    R("s036", "Par rapport à ce prix-là, la vraie réduction, c'est moins onze pour cent.", fichier="aspi_revele.png", zoom="avant",
      punch={"a": 2.3, "texte": "−11 %"}, sons=[IMPACT(2.3)], couches=[src(SRC_UFC)]),
    R("s037", "Et attends, parce que ce n'est même pas le plus fort.",
      ["comparing prices laptop", "browsing online store laptop", "laptop online shopping close up"]),
    R("s038", "Au même moment, au moins dix autres sites le vendaient déjà deux cent quarante-neuf euros.", fichier="aspi_10sites.png",
      zoom="avant", couches=[src(SRC_UFC)]),
    M("s039", "Sans prix barré, sans promo, juste à son prix normal.",
      ["online store product page", "smartphone browsing shop", "tablet online shopping"], legendes=["Site 1", "Site 2", "Site 3"],
      couches=[{"type": "mots", "texte": "249 € SANS REMISE", "heros": "SANS REMISE", "position": "haut", "a": 0.4}]),
    R("s040", "Et ton casque, toujours dans ton panier ? Garde ce mécanisme en tête, on va y revenir.",
      ["headphones on desk laptop", "headphones next to laptop", "headphones on table"]),
    R("s041", "Parce qu'il existe une astuce encore plus simple, qui n'a même pas besoin de monter le prix.",
      ["stainless steel refrigerator kitchen", "modern fridge kitchen", "refrigerator door open"]),
    # ── 03 Prix conseillé ──────────────────────────────────────────────────────
    T("s042", "03", "« Prix conseillé » : vraie réduction ?", ["appliance store", "home appliances shop"]),
    R("s043", "Chez Rakuten, un réfrigérateur Haier affiché mille cinq cent quarante-neuf euros.", fichier="frigo_q.png", zoom="avant",
      couches=[src(SRC_UFC)]),
    R("s044", "Le prix barré : mille sept cent quatre-vingt-dix-neuf euros, soit moins treize pour cent.", fichier="frigo_13.png", zoom="avant"),
    R("s045", "Sauf que ce prix barré, c'est un prix conseillé, celui suggéré par le fabricant.", fichier="frigo_conseille.png",
      zoom="avant", couches=[src(SRC_UFC)]),
    S("s046", "Et selon l'U F C Que Choisir, ce prix-là échappe à la règle des trente jours.",
      {"type": "liste", "titre": "La règle des 30 jours", "elements": [{"texte": "Prix barré", "valeur": "oui"},
       {"texte": "Prix conseillé", "valeur": "non", "heros": True}], "source": SRC_UFC}, etiquette_schema="Qui échappe à la règle"),
    R("s047", "Officiellement, ce prix est juste là pour t'informer, mais tout est fait pour ressembler à une promo.",
      fichier="frigo_30j.png", zoom="avant", couches=[src(SRC_UFC)]),
    devine("s048", "Alors, la vraie réduction sur ce frigo : moins treize, moins cinq, ou zéro pour cent ?", "La vraie réduction ?",
           ["−13 %", "−5 %", "0 %"]),
    R("s049", "Indice : l'U F C a regardé le prix de ce même frigo sur d'autres sites.",
      ["price comparison website phone", "scrolling smartphone shopping", "woman shopping online phone"]),
    R("s050", "Depuis des mois, ailleurs, il se vendait déjà autour de mille cinq cents euros.", fichier="frigo_1500.png", zoom="avant"),
    R("s051", "Réduction réelle selon l'U F C : zéro pour cent, il était même un peu moins cher ailleurs.", fichier="frigo_revele.png",
      zoom="avant", punch={"a": 1.6, "texte": "0 %"}, sons=[IMPACT(1.6)], couches=[src(SRC_UFC)]),
    R("s052", "Et chez Cdiscount, l'U F C parle carrément du roi du prix de comparaison.", fichier="cdiscount_titre.png", zoom="arriere"),
    R("s053", "Le principe : afficher de beaux rabais, sans vraiment baisser les prix.", fichier="cdiscount_rabais.png", zoom="avant",
      couches=[src(SRC_UFC)]),
    S("s054", "Comparer avec le prix d'un autre vendeur, c'est la même brèche : pas de règle des trente jours.",
      {"type": "liste", "titre": "Hors règle des 30 jours", "elements": [{"texte": "Prix conseillé", "valeur": "hors règle"},
       {"texte": "Prix de comparaison", "valeur": "hors règle", "heros": True}], "source": "Code de la consommation, art. L112-1-1 ; " + SRC_UFC},
      etiquette_schema="La brèche"),
    M("s055", "Trois sites, trois façons d'afficher une remise plus grosse que la vraie.", None,
      legendes=["Le casque", "L'aspirateur", "Le frigo"], fichiers=["mos_casque.png", "mos_aspi.png", "mos_frigo.png"]),
    R("s056", "Mais combien de sites, en Europe, vont plus loin que la faille ?",
      ["european union flags", "europe flag waving", "eu flag building"]),
    # ── 04 Le contrôle européen ────────────────────────────────────────────────
    T("s057", "04", "Combien de promos sont fausses ?", ["online shopping laptop night", "shopping website laptop"]),
    R("s058", "En mars deux mille vingt-six, la Commission européenne a publié un grand contrôle des promos en ligne.", fichier="ue_titre.png",
      zoom="avant"),
    R("s059", "Les autorités de vingt-trois pays, plus l'Islande et la Norvège, ont épluché trois cent quatorze sites marchands.",
      ["inspector checking laptop", "people working computers office", "team analyzing data screens"],
      couches=[{"type": "mots", "texte": "314 SITES", "heros": "314", "position": "haut", "a": 2.5}]),
    R("s060", "C'était pendant le Black Friday et le Cyber Monday de deux mille vingt-cinq.",
      ["woman shopping online laptop night", "online shopping at night", "person ordering online laptop"]),
    devine("s061", "Devine combien affichaient des réductions incorrectes : un sur dix, trois sur dix, ou cinq sur dix ?",
           "Réductions incorrectes ?", ["1 sur 10", "3 sur 10", "5 sur 10"]),
    R("s062", "Une réduction correcte, je te rappelle, part du prix le plus bas des trente derniers jours.",
      ["hand holding price tag", "price tag close up hand", "price label shop"],
      couches=[{"type": "mots", "texte": "30 JOURS", "heros": "30", "position": "haut", "a": 1.0}]),
    R("s063", "Résultat : trois sites sur dix ne respectaient pas cette règle.", fichier="ue_30.png", zoom="avant",
      punch={"a": 0.9, "texte": "3 SUR 10"}, sons=[IMPACT(0.9)], couches=[src(SRC_UE)]),
    S("s064", "Et attention, là, on ne parle plus d'une faille légale : ce sont des réductions incorrectes.",
      {"type": "chiffre", "valeur": 30, "suffixe": " %", "legende": "des 314 sites : réductions incorrectes", "comparaison": "Presque un site sur trois",
       "source": SRC_UE}, etiquette_schema="Contrôle européen"),
    R("s065", "Il y a pire : parmi les sites qui comparaient leurs prix avec un prix de référence, six sur dix n'expliquaient pas clairement d'où sortait ce prix.",
      ["online shop product page laptop close up", "e-commerce website screen", "shopping website scrolling"],
      couches=[{"type": "mots", "texte": "6 SUR 10", "heros": "6", "position": "haut", "a": 4.0}]),
    R("s066", "Côté France, la répression des fraudes a fait ses contrôles au Black Friday deux mille vingt-deux.",
      ["shop window sale", "store window shopping street", "shopping street france"]),
    E("s067", "Sur quatre cent onze magasins et sites contrôlés, près d'un sur trois était en infraction.",
      {"type": "liste", "titre": "Black Friday 2022 en France", "elements": [{"texte": "Contrôlés", "valeur": "411"},
       {"texte": "En infraction", "valeur": "près d'1 sur 3", "heros": True}], "source": "DGCCRF, dossier de presse du 20/11/2023"},
      ["shopping mall people", "shoppers walking mall", "busy shopping center"], etiquette="Contrôles en France"),
    R("s068", "Et le prix barré n'est même pas le seul piège de ces journées-là.",
      ["countdown timer screen", "digital countdown clock", "timer counting down"]),
    # ── 05 Urgence ─────────────────────────────────────────────────────────────
    T("s069", "05", "Compte à rebours, stock limité : c'est vrai ?", ["clock ticking close up", "stopwatch close up"]),
    devine("s070", "Sur ces trois cent quatorze sites, combien jouaient sur l'urgence, compte à rebours ou stock presque épuisé ? Un sur vingt, un sur cinq, ou un sur deux ?",
           "Combien jouent sur l'urgence ?", ["1 sur 20", "1 sur 5", "1 sur 2"]),
    R("s071", "Pendant que tu réfléchis : Black Friday, le jour des foules, c'est d'abord un mot de la police de Philadelphie.",
      ["Philadelphia City Hall", "Philadelphia downtown street", "Philadelphia police"], surtitre="Philadelphie"),
    R("s072", "En mille neuf cent soixante et un, elle appelle déjà ainsi ce vendredi de bouchons et de foule.",
      ["Philadelphia 1960s street", "traffic jam city crowd", "crowded street shoppers"], surtitre="Philadelphie : trace écrite de 1961"),
    R("s073", "Aujourd'hui, la foule est dans ton téléphone, et la pression aussi.",
      ["person shopping smartphone sofa", "woman on phone couch night", "scrolling phone on sofa"]),
    R("s074", "Réponse : près d'un site contrôlé sur cinq jouait sur l'urgence, compte à rebours ou stock presque épuisé.", fichier="ue_18.png",
      zoom="avant", punch={"a": 0.8, "texte": "1 SUR 5"}, sons=[IMPACT(0.8)], couches=[src(SRC_UE)]),
    R("s075", "Et dans plus de la moitié de ces cas, l'urgence affichée était trompeuse.",
      ["hourglass sand time", "sand timer close up", "hourglass running out"],
      couches=[{"type": "mots", "texte": "TROMPEUR", "heros": "TROMPEUR", "position": "haut", "a": 1.5}]),
    R("s076", "Un site sur dix ajoutait des frais tard, juste avant le paiement.", fichier="ue_10.png", zoom="avant", couches=[src(SRC_UE)]),
    R("s077", "Et plus d'un sur trois essayait de glisser des options dans ton panier.",
      ["online shopping cart laptop", "adding to cart website", "shopping basket online"],
      couches=[{"type": "mots", "texte": "+ OPTIONS", "heros": "OPTIONS", "position": "haut", "a": 1.2}]),
    R("s078", "Dernier changement, tout neuf cette année : le paiement en trois ou quatre fois.",
      ["contactless payment smartphone", "paying with phone terminal", "mobile payment hand"], surtitre="20 novembre 2026"),
    E("s079", "À partir du vingt novembre, les règles du crédit à la consommation s'appliquent aussi à lui.",
      {"type": "liste", "titre": "Paiement en 3 ou 4 fois", "elements": [{"texte": "À partir du", "valeur": "20/11/2026", "heros": True},
       {"texte": "Nouvelles règles", "valeur": "celles du crédit"}], "source": "Service-Public.fr, 27/10/2026"},
      ["credit card bills calculator", "paying bills credit card", "calculator and credit card"], etiquette="Ce qui change"),
    R("s080", "Sa pub devra rappeler qu'un crédit coûte de l'argent et doit être remboursé.",
      ["credit cards close up", "stack of credit cards", "wallet credit cards"],
      couches=[{"type": "carton", "texte": "Attention ! Un crédit coûte de l'argent et doit être remboursé !", "sous_texte": "Mention obligatoire · Service-Public.fr, 27/10/2026", "a": 0.3}]),
    R("s081", "Alors, comment ne pas se faire avoir ? Trois réflexes, et on les teste sur ton casque.",
      ["finger pressing buy button phone", "hand hesitating phone purchase", "thumb over smartphone screen"]),
    # ── 06 Réflexes ────────────────────────────────────────────────────────────
    T("s082", "06", "Comment savoir si une promo est vraie ?", ["magnifying glass", "magnifying glass close up"]),
    R("s083", "Premier réflexe : un prix barré te montre au mieux le mois dernier, jamais les mois d'avant.",
      ["price tag close up", "price tag in store", "label price close"],
      couches=[{"type": "etiquette", "numero": "01", "texte": "L'historique, pas le prix barré", "a": 0.2}]),
    R("s084", "Va voir l'historique du prix sur plusieurs mois, des sites gratuits le tracent pour toi.",
      ["line chart on laptop screen", "graph on computer screen", "chart data screen"]),
    R("s085", "Deuxième réflexe : prix conseillé ou prix de comparaison, ce n'est pas une promo.", fichier="reflexe2.png", zoom="avant",
      couches=[{"type": "etiquette", "numero": "02", "texte": "Prix conseillé ≠ promo", "a": 0.2}]),
    M("s086", "Troisième réflexe : compare avec au moins deux autres sites avant de cliquer.",
      ["laptop online shop", "tablet shopping website", "phone shopping website"], legendes=["Site 1", "Site 2", "Site 3"],
      couches=[{"type": "etiquette", "numero": "03", "texte": "Compare 3 sites", "a": 0.2}]),
    R("s087", "Si une réduction te semble fausse, signale-la sur SignalConso, le site officiel de la répression des fraudes.",
      fichier="signalconso.png", zoom="avant", couches=[src("signal.conso.gouv.fr")]),
    R("s088", "On revient à ton casque, toujours dans le panier, et on applique les réflexes.", fichier="casque_retour.png", zoom="avant"),
    devine("s089", "Dernière devinette, la plus importante, avant de cliquer sur payer. Ta vraie économie : plus de quarante pour cent, entre vingt et quarante, ou moins de vingt ?",
           "Ta vraie économie ?", ["+ de 40 %", "20 à 40 %", "− de 20 %"], ambiance="tension"),
    R("s090", "Réflexe deux : son prix barré n'est pas un prix conseillé, c'est le vrai prix du mois.", fichier="casque_pasconseille.png",
      zoom="avant"),
    R("s091", "Réflexe trois : sur d'autres sites, l'U F C l'a longtemps vu à deux cent soixante-dix-neuf euros.", fichier="casque_279.png",
      zoom="avant", couches=[src(SRC_UFC)]),
    S("s092", "Déjà, ailleurs, on est loin des trois cent quatre-vingt-dix-neuf euros du prix barré.",
      {"type": "comparaison", "titre": "Le casque", "unite": " €", "decimales": 0, "heros": "b",
       "a": {"label": "Prix barré", "valeur": 400}, "b": {"label": "Ailleurs, longtemps", "valeur": 279}, "source": SRC_UFC + " (399,95 € arrondi)"},
      etiquette_schema="Réflexe 3"),
    R("s093", "Reste le réflexe un, le plus important : l'historique du prix sur plusieurs mois.",
      ["magnifying glass on document", "searching with magnifying glass", "detective magnifying glass"],
      sons=[{"nom": "riser", "a": 1.0, "volume": 0.35}]),
    # ── 07 Révélation ──────────────────────────────────────────────────────────
    R("s094", "On remonte l'historique : en septembre, son prix grimpe ; le mois avant la promo, il est à trois cent quatre-vingt-dix-neuf euros quatre-vingt-quinze.",
      fichier="chrono1.png", zoom="aucun", ambiance="revelation"),
    R("s095", "Mais avant cette hausse, en juillet, il se vendait deux cent cinquante-neuf euros.", fichier="chrono2.png", zoom="aucun"),
    R("s096", "Et le jour du Black Friday, il tombe à cent quatre-vingt-neuf euros.", fichier="chrono3.png", zoom="aucun"),
    R("s097", "Par rapport au prix de juillet, ta vraie économie, c'est moins vingt-sept pour cent.", fichier="casque_revele.png", zoom="avant",
      avant_voix=0.6, punch={"a": 2.9, "texte": "−27 %"}, sons=[IMPACT(2.9)], couches=[{"type": "flash", "a": 2.9}, src(SRC_UFC)]),
    S("s098", "Soixante-dix euros économisés, pas les deux cent onze promis.",
      {"type": "comparaison", "titre": "Ce que tu économises", "unite": " €", "decimales": 0, "heros": "b",
       "a": {"label": "Promis par l'étiquette", "valeur": 211}, "b": {"label": "En vrai, depuis juillet", "valeur": 70}, "source": SRC_UFC + " (calcul : 259 − 189)"},
      etiquette_schema="La vraie économie"),
    R("s099", "Légal du début à la fin, et c'est justement ça, la faille.", fichier="casque_trompeuse.png", zoom="avant", couches=[src(SRC_UFC)]),
    # ── 08 Fin ─────────────────────────────────────────────────────────────────
    R("s100", "Mardi prochain : sur cent euros de ta facture d'électricité, combien paient vraiment le courant ?",
      ["electricity meter close up", "electric radiator home", "power lines sunset"], ambiance="leger"),
    R("s101", "Abonne-toi : chaque semaine, le vrai prix d'un truc que tu paies.",
      ["light switch turning on", "light bulb turning on", "lamp switching on"], duree_min=3.2),
]

montage = {
    "titre": "Black Friday : les fausses promos",
    "format": {"largeur": 1920, "hauteur": 1080, "fps": 30},
    "transition_defaut": "coupe",
    "duree_transition": 8,
    "voix": {"moteur": "edge", "locuteur": "fr-FR-VivienneMultilingualNeural", "debit": "+6%", "debit_continu": "+6%", "pause_phrase": 0.15},
    "musique": {"fichier": "../../public/sfx/musique-enquete.wav", "volume": 0.2},
    "etalonnage": {"contraste": 1.06, "saturation": 1.08, "luminosite": 1},
    "grain": True,
    "sous_titres": {"actifs": True, "mots_par_ligne": 4},
    "scenes": [],
}

lots = []
for s in scenes:
    s = dict(s)
    leg = s.pop("_legendes", None)
    c = CHOIX.get(s["id"])
    if c and s["format"] == "mosaique" and isinstance(c, list):
        s["medias"] = [{"media_ref": r, **({"legende": leg[i]} if leg else {})} for i, r in enumerate(c)]
    elif c:
        s["media_ref"] = c
    if c:
        s.pop("recherche", None)
    montage["scenes"].append(s)

if __name__ == "__main__":
    ep = os.path.join(RACINE, "episodes", "black-friday")
    os.makedirs(ep, exist_ok=True)
    json.dump(montage, open(os.path.join(ep, "montage.json"), "w"), ensure_ascii=False, indent=1)
    sans = [s for s in montage["scenes"] if s.get("recherche") and not s.get("media_ref") and not s.get("medias")]
    print(f"{len(montage['scenes'])} scènes, {len(sans)} à repérer")
    if "--lots" in sys.argv:
        n = 8
        for k in range(0, len(sans), n):
            d = os.path.join(RACINE, "videos", f"bf-rep-{k // n + 1}")
            os.makedirs(d, exist_ok=True)
            json.dump({"titre": "repérage black friday", "scenes": [{"id": s["id"], "texte": s["texte"], "recherche": s["recherche"]} for s in sans[k:k + n]]},
                      open(os.path.join(d, "lot.json"), "w"), ensure_ascii=False, indent=1)
            print("lot", d)
