"""Source du montage Électricité (17/11/2026). Génère episodes/electricite/montage.json et les lots de repérage.
Usage : python3 videos/electricite/_workspace/montage_src.py [--lots]
Modèle : videos/black-friday/_workspace/montage_src.py. La narration n'est PAS recopiée ici : elle est lue dans
02_script_plans.py (script fact-checké), plan par plan, pour rester mot pour mot identique (ids p001…p159).
Aucun plan filmé par Omar (pas de episodes/electricite/medias/omar-*) : requêtes Pixabay de secours partout.
Les médias choisis à l'œil sur les planches de repérage vont dans choix_rushes.json
(scène -> media_ref, ou liste de media_ref pour une mosaïque : une par requête, dans l'ordre, captures exclues)."""
import json, os, subprocess, sys, tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(ICI)))

# ── Narration : lue dans le script fact-checké ──────────────────────────────────
with tempfile.TemporaryDirectory() as tmp:
    sortie = os.path.join(tmp, "plans.json")
    subprocess.run([sys.executable, os.path.join(ICI, "02_script_plans.py"), sortie], check=True, capture_output=True)
    PLANS = [r for r in json.load(open(sortie))["rows"] if "id" in r]
TXT = {r["id"]: r["txt"] for r in PLANS}
FMT_SCRIPT = {r["id"]: r["fmt"] for r in PLANS}
SRC_SCRIPT = {r["id"]: r.get("src") for r in PLANS}

CHOIX = {}  # rempli après repérage
CHOIX_FICHIER = os.path.join(ICI, "choix_rushes.json")
_L = os.path.join(ICI, "commons_local.json")
LOCAL = json.load(open(_L)) if os.path.exists(_L) else {}
if os.path.exists(CHOIX_FICHIER):
    CHOIX = json.load(open(CHOIX_FICHIER))

# Sources (texte affiché, 24 px)
JDN = "Journal du Net, 15/05/2026"
CRE_COH = "CRE, rapport Cohérence des offres, 03/06/2026"
CRE_147 = "CRE, délibération 2026-147, annexe B"
NIV = "CRE, fiche « Niveau de certitude »"
EI = "energie-info.fr (médiateur national de l'énergie), consulté le 17/11/2026"
JC = "JeChange, mis à jour le 11/11/2026"
CALC = "calcul Le Vrai Prix, tarif bleu Base 6 kVA, 4 500 kWh/an, d'après la CRE (délibérations 2026-147 et 2026-105)"
CPS = 15.0  # caractères lus par seconde (Edge Vivienne, +2 %) : sert à caler punch / révélations, à revoir sur la planche


def src(t):
    return {"type": "source", "texte": t}


def a_mot(id, mot, avant=0.0):
    """Seconde (dans la scène) où la voix dit `mot` : estimation au prorata des caractères."""
    t = TXT[id]
    i = t.lower().find(mot.lower())
    if i < 0:
        raise ValueError(f"{id} : « {mot} » absent de la narration")
    return round(avant + i / CPS, 1)


def P(id, mot, texte, avant=0.0):
    return {"a": a_mot(id, mot, avant), "texte": texte}


def base(id, fmt, recherche=None, fichier=None, **kw):
    s = {"id": id, "format": fmt, "texte": TXT[id]}
    if fichier: s["fichier"] = "medias/" + fichier
    if recherche: s["recherche"] = recherche
    s.update(kw)
    return s


def R(id, recherche=None, fichier=None, **kw):
    return base(id, "rush", recherche, fichier, **kw)


def S(id, schema, recherche=None, fichier=None, **kw):
    """Schéma plein écran. recherche/fichier = fond flouté (lien avec le réel, règle n°3), facultatif."""
    return base(id, "schema", recherche, fichier, schema=schema, **kw)


def T(id, numero, titre, recherche, sous_titre=None, **kw):
    s = {"id": id, "format": "titre", "type": "titre", "numero": numero, "titre": titre, "texte": "", "recherche": recherche,
         "duree_min": 2.6, "transition": "fondu"}
    if sous_titre: s["sous_titre"] = sous_titre
    s.update(kw)
    return s


def E(id, schema, recherche=None, fichier=None, etiquette=None, cote="gauche", **kw):
    s = base(id, "ecran_partage", recherche, fichier, schema=schema, cote=cote, **kw)
    if etiquette: s["etiquette_schema"] = etiquette
    return s


def M(id, items, legendes=None, **kw):
    """Mosaïque : items = requêtes Pixabay (une case chacune) et/ou captures « capXX….png » (case fixe)."""
    s = {"id": id, "format": "mosaique", "texte": TXT[id], "_items": items, "_legendes": legendes}
    fixes = [x for x in items if x.endswith(".png")]
    requetes = [x for x in items if not x.endswith(".png")]
    if requetes:
        s["recherche"] = requetes
    if fixes:  # brouillon : seules les captures s'affichent tant que les rushes ne sont pas choisis
        s["medias"] = [{"fichier": "medias/" + x, **({"legende": legendes[i]} if legendes else {})}
                       for i, x in enumerate(items) if x.endswith(".png")]
    s.update(kw)
    return s


def DV(id, question, choix, **kw):
    """Devinette (règle 20) : pas de `bonne`, rien ne s'allume, la réponse vient plus tard. Compte à rebours de 3 s
    lancé par construire.mjs quand la voix a fini de poser la question."""
    return S(id, {"type": "devine", "question": question, "choix": choix, "secondes": 3},
             sons=[{"nom": "tick", "a": 0.2, "volume": 0.3}], **kw)


def DV_RUSH(id, recherche, choix_texte, **kw):
    """Devinette posée SUR l'objet réel (pas de panneau sombre) : 3 gros chiffres en couche `mots`, aucune case allumée,
    3 s de silence après la question (respiration) rythmées par 3 tics."""
    fin = round(len(TXT[id]) / CPS, 1)
    return R(id, recherche, couches=[{"type": "mots", "texte": choix_texte, "position": "centre", "a": 0.2}],
             respiration=3.4, sons=[{"nom": "tick", "a": round(fin + 0.2 + k, 1), "volume": 0.5} for k in range(3)], **kw)


def citation(texte, qui, source):
    return {"type": "liste", "titre": "Ce qu'il dit" if "juriste" in qui else "Ce qu'elle dit",
            "elements": [{"texte": texte, "heros": True}, {"texte": qui}], "source": source}


IMPACT = lambda a: {"nom": "impact", "a": a, "volume": 0.5}
RISER = lambda a: {"nom": "riser", "a": a, "volume": 0.35}
SIL = 0.5  # « sil » du script : 0,5 s de silence avant la voix (avant_voix)
NEU = "Matthieu Bertrand Neuser, juriste de l'Adéic"

scenes = [
    # ── 00 Accroche (0-30 s : images réelles plein écran, aucun schéma, aucune carte) ─────────────────────────
    R("p001", ["french electricity bill paper close up", "hand holding electricity bill", "paper invoice table close up"],
      zoom="avant", ambiance="tension"),
    R("p002", ["linky smart meter", "green electricity meter display", "smart meter france close up"],
      punch=P("p002", "courant", "COURANT ?")),
    R("p003", ["electric radiator home winter", "hand adjusting radiator thermostat", "white electric heater living room"],
      punch=P("p003", "protège", "TE PROTÈGE")),
    R("p004", ["finger pointing at bill lines", "reading invoice close up", "person checking utility bill"]),
    DV_RUSH("p005", ["electricity bill close up desk", "utility bill paper macro", "bill amount paper close up"], "20 € · 40 € · 60 € ?"),
    R("p006", ["high voltage power lines sunset", "electricity pylons winter france", "power line towers aerial"]),
    R("p007", ["letter in mailbox close up", "hand taking envelope from mailbox", "opening letter envelope"]),
    R("p008", fichier="cap07a_cre_coherence_titre.png", zoom="avant", couches=[src(CRE_COH)]),
    R("p009", ["hand holding paper bill close up", "woman holding invoice paper", "man reading paper bill"],
      punch=P("p009", "cinq cent", "591 €"), couches=[src("CRE, 03/06/2026 · par an, hors taxes, 1 % des contrats les plus chers")]),
    M("p010", ["hand switching off light switch", "electric kettle boiling kitchen", "phone charger plugged socket"]),
    R("p011", ["suburban houses france", "french pavilion house street", "residential street spring"], surtitre="Yvelines · printemps 2024"),
    M("p012", ["hands opening envelope close up", "unfolded letter reading hands"]),
    E("p013", {"type": "chiffre", "valeur": 4000, "suffixe": " €", "legende": "pour un seul mois", "revele_a": 0.3, "source": JDN},
      fichier="cap11a_jdn_titre.png", etiquette="La facture du couple"),
    R("p014", ["electric meter close up dark", "smart meter blinking light", "electricity meter box wall"]),
    E("p015", citation("« On ne sait pas. »", NEU, JDN), fichier="cap11b_jdn_on_ne_sait_pas.png", etiquette="Citation"),
    R("p016", ["worried hands holding bill", "paper bill on table lamp", "person reading bill at night"]),
    M("p017", ["invoice lines close up pen", "utility bill details macro", "bill table numbers close up"]),
    # ── 01 La facture ───────────────────────────────────────────────────────────────────────────────────────
    T("p018", "01", "Facture d'électricité : où vont tes 100 € ?", ["electricity bill blurred background", "invoice papers desk"],
      ambiance="leger"),
    R("p019", ["pen pointing invoice sections", "hand pointing document lines", "reviewing bill with pen"], transition="fondu",
      couches=[{"type": "mots", "texte": "1 · 2 · 3", "position": "haut", "a": 1.0}]),
    E("p020", {"type": "liste", "titre": "Tes 100 €", "elements": [{"texte": "Réseau", "valeur": "? €", "heros": True}]},
      ["power lines countryside france", "electric pole street", "lineman working on power line"], etiquette="Tes 100 €"),
    R("p021", ["electrician technician meter installation", "worker installing electric meter", "electric cabinet technician"],
      couches=[{"type": "mots", "texte": "PAREIL POUR TOUS", "heros": "TOUS", "position": "haut", "a": 0.4}]),
    S("p022", {"type": "decomposition", "titre": "Tes 100 €", "total": 100, "unite": " €", "decimales": 0,
               "parts": [{"label": "Réseau ≈", "valeur": 28, "heros": True}], "source": CALC},
      ["high voltage pylons fog", "transmission towers field"], etiquette_schema="Où vont tes 100 €"),
    M("p023", ["invoice tax line close up", "calculator and receipts", "paper bill numbers macro"],
      legendes=["Accise", "Contribution (CTA)", "TVA"]),
    # devinette sur l'objet (format du script ; un schéma ici collerait deux schémas p024-p025)
    DV_RUSH("p024", ["electricity invoice on kitchen table", "bill paper top view", "printed bill close up light"], "10 € · 20 € · 30 € ?"),
    S("p025", {"type": "decomposition", "titre": "Tes 100 €", "total": 100, "unite": " €", "decimales": 0,
               "parts": [{"label": "Réseau ≈", "valeur": 28}, {"label": "Taxes ≈", "valeur": 31, "heros": True}], "source": CALC},
      etiquette_schema="Où vont tes 100 €"),
    R("p026", ["kettle steam close up", "switching on kettle", "woman pouring from electric kettle"]),
    E("p027", {"type": "liste", "titre": "Tes 100 €", "elements": [{"texte": "Réseau", "valeur": "≈ 28 €"}, {"texte": "Taxes", "valeur": "≈ 31 €"},
               {"texte": "Fourniture", "valeur": "?", "heros": True}], "source": EI},
      fichier="cap06_energieinfo_seule_composante.png", etiquette="La seule part en concurrence"),
    S("p028", {"type": "decomposition", "titre": "Tes 100 €", "total": 100, "unite": " €", "decimales": 0,
               "parts": [{"label": "Fourniture ≈", "valeur": 41, "heros": True}, {"label": "Réseau ≈", "valeur": 28},
                         {"label": "Taxes ≈", "valeur": 31}], "source": CALC},
      etiquette_schema="Réponse n°1", avant_voix=SIL),
    E("p029", {"type": "decomposition", "titre": "Fourniture ≈ 41 €", "total": 41, "unite": " €", "decimales": 0,
               "parts": [{"label": "Commercialisation + certificats", "valeur": 7, "heros": True}],
               "source": "estimation Le Vrai Prix d'après la CRE (délibération 2026-06)"},
      ["call center headset office", "customer service desk phone", "office telephone desk"], etiquette="Dans tes 40 €"),
    R("p030", ["nuclear power plant cooling towers", "nuclear plant river france", "power station steam towers"]),
    S("p031", {"type": "chiffre", "valeur": 30, "prefixe": "≈ ", "suffixe": " €", "revele_a": 1.2, "legende": "le courant lui-même",
               "comparaison": "Moins d'un tiers de ta facture", "source": "estimation Le Vrai Prix d'après la CRE (± 3 €)"},
      ["cooling tower steam close up", "nuclear plant at dusk"], etiquette_schema="Le courant"),
    R("p032", ["stock market screen numbers", "trading floor monitors", "financial chart screen rising"]),
    # ── 02 Les marchés ──────────────────────────────────────────────────────────────────────────────────────
    T("p033", "02", "Prix de l'électricité 2027 : pourquoi ça monte ?", ["pylons silhouette dusk", "power grid towers evening"],
      ambiance="tension"),
    R("p034", ["nuclear power plant aerial", "nuclear reactor building", "cooling tower steam sky"], transition="fondu"),
    M("p035", ["trading floor screens", "electricity grid control room", "wind turbines field"], surtitre="Depuis le 1er janvier 2026",
      couches=[src("CRE, délibération 2026-06")]),
    E("p036", {"type": "liste", "titre": "Prix de gros", "elements": [{"texte": "Novembre 2025 → novembre 2026", "valeur": "× ?", "heros": True}]},
      ["stock ticker screen close up", "market prices monitor", "trading screen numbers"], etiquette="Devinette n°2"),
    DV("p037", "Le prix de gros, en un an ?", ["×2", "×4", "×10"]),
    M("p038", ["nuclear plant landscape", "high voltage line close up", "electricity meter linky"], surtitre="Versement nucléaire universel"),
    S("p039", {"type": "chiffre", "valeur": 0, "suffixe": " €", "revele_a": a_mot("p039", "rien"), "legende": "reversement prévu en 2027",
               "source": "estimation CRE, 01/10/2026 (via Selectra, 01/11/2026)"},
      ["nuclear power station winter", "reactor dome aerial"], etiquette_schema="Versement nucléaire"),
    R("p040", ["financial graph rising screen", "stock chart going up monitor", "price chart close up"],
      couches=[src("Selectra, 10/11/2026 ; TotalEnergies, 20/10/2026")]),
    S("p041", {"type": "comparaison", "titre": "Prix de gros de l'électricité", "unite": " €/MWh", "decimales": 0, "heros": "b",
               "a": {"label": "Novembre 2025", "valeur": 66}, "b": {"label": "1er-10 novembre 2026", "valeur": 266},
               "source": "relevé Selectra des prix spot, 11/11/2026"},
      etiquette_schema="Réponse n°2 : × 4", avant_voix=SIL),
    R("p042", ["bill on table with calculator", "calculator and invoice", "person calculating bills"]),
    E("p043", {"type": "processus", "titre": "Achats étalés sur 24 mois", "etapes": ["Mois 1", "Mois 12", "Mois 24"], "actif": 2,
               "source": "CRE, délibération 2026-06"},
      ["calendar pages turning", "wall calendar months", "desk calendar close up"], etiquette="Le tarif bleu"),
    R("p044", ["calendar february page", "calendar date circled red", "marking calendar pen"], surtitre="1er février 2027"),
    M("p045", ["reading letter at home", "email on smartphone close up", "mailbox letters"]),
    S("p046", {"type": "liste", "titre": "Le classement", "elements": [{"texte": "À éviter", "valeur": "5 pièges"},
               {"texte": "À prendre", "valeur": "3 choix"}, {"texte": "Le n°1 à prendre", "valeur": "?", "heros": True}]},
      ["electricity bill on table blurred", "bills stacked on desk"], etiquette_schema="Le classement"),
    # ── 03 À éviter n°5 : démarchage ────────────────────────────────────────────────────────────────────────
    T("p047", "03", "Démarchage électricité : est-ce légal ?", ["smartphone on table dark", "phone screen glow night"],
      sous_titre="À éviter · n°5", ambiance="leger"),
    R("p048", ["smartphone ringing unknown number table", "phone ringing on kitchen table", "incoming call smartphone close up"],
      transition="fondu"),
    S("p049", {"type": "chiffre", "valeur": 36, "suffixe": " %", "revele_a": 1.0,
               "legende": "des foyers ont signé après un démarchage",
               "source": "baromètre énergie-info 2026, médiateur national de l'énergie, 03/11/2026"},
      fichier="cap15_barometre_2026.png", etiquette_schema="Baromètre du médiateur"),
    E("p050", {"type": "liste", "titre": "La loi a changé", "elements": [{"texte": "Loi", "valeur": "n° 2025-594"},
               {"texte": "En vigueur le", "valeur": "11 août 2026", "heros": True}], "source": "loi n° 2025-594 du 30/06/2025, art. 13"},
      fichier="cap09_loi_2025_594.png", etiquette="Démarchage par téléphone"),
    M("p051", ["hand rejecting phone call", "declining call smartphone", "phone call screen close up"]),
    DV("p052", "Contrat signé après un appel interdit ?", ["VALABLE", "ANNULABLE", "NUL"]),
    E("p053", {"type": "liste", "titre": "Le vrai médiateur", "elements": [{"texte": "Il démarche", "valeur": "jamais", "heros": True},
               {"texte": "Il vend un contrat", "valeur": "jamais"}], "source": EI},
      fichier="cap10_energieinfo_faux_mediateur.png", etiquette="Faux médiateur"),
    S("p054", {"type": "chiffre", "valeur": 375000, "suffixe": " €", "revele_a": a_mot("p054", "trois cent"),
               "legende": "amende maximale pour une entreprise", "source": "code de la consommation, art. L. 242-16"},
      etiquette_schema="Ce que risque l'entreprise"),
    R("p055", ["tearing paper contract", "ripping document close up", "torn paper sheet hands"], avant_voix=SIL,
      punch=P("p055", "nul", "NUL", SIL), couches=[src("code de la consommation, art. L. 223-1")]),
    E("p056", {"type": "liste", "titre": "Ce que dit la loi", "elements": [{"texte": "Appel sans ton accord", "valeur": "interdit"},
               {"texte": "Ton fournisseur, pour ton contrat", "valeur": "permis", "heros": True}, {"texte": "À ta porte", "valeur": "permis"}],
               "source": "loi n° 2025-594 du 30/06/2025, art. 13"},
      ["phone ringing on desk office", "mobile phone vibrating table"], etiquette="Deux limites"),
    R("p057", ["salesman at front door", "man ringing doorbell", "door knock close up"],
      couches=[{"type": "mots", "texte": "À TA PORTE : PERMIS", "heros": "PERMIS", "position": "haut", "a": a_mot("p057", "à ta porte")}]),
    M("p058", ["hand hanging up phone", "closing front door", "comparing offers on laptop"],
      couches=[{"type": "etiquette", "numero": "05", "texte": "Ne signe jamais sur le moment", "a": 0.2}]),
    R("p059", ["hand taking letter from mailbox", "envelope in letterbox", "mail delivery letterbox"]),
    # ── 04 À éviter n°4 : facture estimée ───────────────────────────────────────────────────────────────────
    T("p060", "04", "Facture d'électricité trop élevée : que faire ?", ["electric meter wall blurred", "meter display dark"],
      sous_titre="À éviter · n°4", ambiance="emotion"),
    R("p061", ["smart meter display digits", "electricity meter reading close up", "meter counter numbers"], transition="fondu",
      couches=[{"type": "mots", "texte": "INDEX RÉEL ?", "heros": "INDEX", "position": "haut", "a": 1.0}]),
    E("p062", {"type": "processus", "titre": "Mars → mai 2024", "etapes": ["Plus de relevés", "Estimation", "Résiliation"], "actif": 0,
               "source": JDN},
      fichier="cap11a_jdn_titre_releves.png", etiquette="L'histoire du couple"),
    R("p063", ["calculator and bill close up", "invoice total amount paper", "shocked hands holding paper bill"],
      couches=[{"type": "mots", "texte": "ESTIMATION : 4 000 €", "heros": "ESTIMATION", "position": "haut", "a": a_mot("p063", "quatre mille")},
               src(JDN)]),
    M("p064", ["pushing paper bill away table", "access denied phone screen", "recorded delivery letter hand"],
      couches=[{"type": "mots", "texte": "RÉSILIATION", "heros": "RÉSILIATION", "position": "haut", "a": a_mot("p064", "résilié")}]),
    R("p065", ["official letter envelope stamp", "registered mail letter", "door with letter on floor"]),
    E("p066", citation("« Compteur Linky qui dysfonctionne, ça arrive, mais ça reste exceptionnel. »", NEU, JDN),
      fichier="cap11c_jdn_exceptionnel.png", etiquette="Citation"),
    DV("p067", "Réclamation sans réponse : le médiateur après…", ["2 SEMAINES", "2 MOIS", "6 MOIS"]),
    M("p068", ["etang de thau sete", "mediterranean village france", "south france lagoon village"], surtitre="Hérault · 2025"),
    R("p069", ["bank statement close up", "bank card payment terminal", "hands holding bank statement"],
      punch=P("p069", "deux cent onze", "211 993 €"),
      couches=[src("Midi Libre, repris par Selectra (07/11/2025, mis à jour le 14/01/2026) · prélèvement rejeté par la banque, puis annulé")]),
    E("p070", {"type": "liste", "titre": "Ce qu'elle dit", "elements": [{"texte": "« J'ai hurlé et même vomi. »", "heros": True},
               {"texte": "1 556 kWh enregistrés comme", "valeur": "1 001 556 kWh"}],
               "source": "une cliente de l'Hérault, Midi Libre via Selectra, 07/11/2025"},
      ["hands covering face paper bill", "woman hands paper bill close up", "crumpled paper bill hand"], etiquette="Citation"),
    S("p071", {"type": "processus", "titre": "Si ça t'arrive", "etapes": ["Réclamation écrite", "?", "Médiateur"], "actif": 0},
      ["pen writing letter desk", "handwritten letter close up"], etiquette_schema="La marche à suivre"),
    R("p072", ["laptop online form typing", "person filling form laptop", "hands typing keyboard home"], avant_voix=SIL,
      punch=P("p072", "deux mois", "2 MOIS", SIL),
      couches=[{"type": "mots", "texte": "MÉDIATEUR : GRATUIT", "heros": "GRATUIT", "position": "haut", "a": a_mot("p072", "gratuitement", SIL)},
               src("energie-info.fr, « J'ai une réclamation… », consulté le 17/11/2026")]),
    M("p073", ["cap11e_jdn_mai2025.png", "stack of letters desk", "phone call home desk"], surtitre="Mai 2025", couches=[src(JDN)]),
    R("p074", ["email inbox laptop screen", "sending email laptop", "office desk letters"]),
    E("p075", citation("« Ça change tout : ils nous répondent et font attention. »", NEU, JDN),
      fichier="cap11d_jdn_ca_change_tout.png", etiquette="Citation"),
    R("p076", ["reading electricity meter flashlight", "checking meter numbers", "meter reading notebook"],
      couches=[{"type": "etiquette", "numero": "04", "texte": "Compare l'index du compteur et de la facture", "a": 0.2}]),
    M("p077", ["pile of unopened envelopes", "unread email notification phone", "waste paper bin letters"]),
    # ── 05 À éviter n°3 : la remise qui bascule ─────────────────────────────────────────────────────────────
    T("p078", "05", "Offre électricité −20 % : où est le piège ?", ["letter on desk blurred", "envelope close up dark"],
      sous_titre="À éviter · n°3", ambiance="tension"),
    R("p079", ["reading letter close up", "unfolding letter hands", "letter on table"], transition="fondu",
      punch=P("p079", "moins vingt", "−20 %"), couches=[src(JC)]),
    E("p080", {"type": "liste", "titre": "Le courrier", "elements": [{"texte": "Courrier aux clients", "valeur": "rapporté par la presse"},
               {"texte": "Hausse de la facture", "valeur": "? %", "heros": True}], "source": JC},
      fichier="cap12_jechange.png", etiquette="Courrier rapporté par la presse"),
    R("p081", ["calendar december 31", "new year calendar page", "calendar last day of year"], surtitre="31/12/2026", couches=[src(JC)]),
    S("p082", {"type": "comparaison", "titre": "Le kWh hors taxes : +53 %", "unite": " € HT", "decimales": 4, "heros": "b",
               "a": {"label": "Avec la remise", "valeur": 0.1140}, "b": {"label": "Après le 31 décembre", "valeur": 0.1747}, "source": JC},
      fichier="cap12_jechange.png", etiquette_schema="Le prix du kWh"),
    M("p083", ["french electrical outlet", "wall socket type e", "electricity meter cabinet"],
      couches=[{"type": "mots", "texte": "ABONNEMENT ≈ +50 %", "heros": "ABONNEMENT", "position": "haut", "a": 0.4}, src(JC)]),
    E("p084", {"type": "liste", "titre": "Pour un client", "elements": [{"texte": "Facture annuelle", "valeur": "+ ? %", "heros": True}]},
      ["letter reading hands table", "paper letter unfolded close up"], etiquette="Devinette n°4"),
    # devinette sur l'objet (format du script ; un schéma ici collerait deux schémas p085-p086)
    DV_RUSH("p085", ["letter on wooden table close up", "folded letter close up", "letter paper top view"], "+12 % · +25 % · +42 % ?"),
    # liste plutôt que `decomposition` : aucune répartition chiffrée vérifiée de la « facture type » de cette offre
    S("p086", {"type": "liste", "titre": "La remise de −20 %", "elements": [{"texte": "Prix du kWh hors taxes", "valeur": "−20 %", "heros": True},
               {"texte": "Abonnement", "valeur": "pas de remise"}, {"texte": "Taxes", "valeur": "pas de remise"}], "source": JC},
      etiquette_schema="Ce que touche la remise"),
    R("p087", ["paper bill pen crossing lines", "crossing out text with marker", "marker on document close up"],
      couches=[{"type": "mots", "texte": "PAS L'ABONNEMENT · PAS LES TAXES", "heros": "PAS", "position": "haut", "a": a_mot("p087", "pas l'abonnement")}]),
    S("p088", {"type": "comparaison", "titre": "La vraie remise", "unite": " %", "decimales": 0, "heros": "b",
               "a": {"label": "Affiché : −20 % sur une ligne", "valeur": 20}, "b": {"label": "Sur la facture : ≈ −14 %", "valeur": 14},
               "source": "calcul Le Vrai Prix : remise sur le seul kWh HT, tarif bleu Base 6 kVA, 4 500 kWh/an"},
      etiquette_schema="Remise réelle"),
    R("p089", ["highlighter on letter", "reading fine print document", "letter highlighted text"],
      couches=[{"type": "mots", "texte": "SILENCE = ACCEPTATION", "heros": "SILENCE", "position": "haut", "a": a_mot("p089", "le silence")}]),
    E("p090", {"type": "chiffre", "valeur": 42, "prefixe": "+", "suffixe": " %", "revele_a": a_mot("p090", "plus quarante", SIL),
               "legende": "facture annuelle", "comparaison": "Pour le client dont le courrier circule", "source": JC},
      fichier="cap12_jechange_revele.png", etiquette="Réponse n°4", avant_voix=SIL),
    R("p091", ["smartphone email inbox close up", "checking emails phone", "spam folder email phone"], couches=[src(EI)]),
    M("p092", ["cap13_energieinfo_messages.png", "bill end date line close up", "junk mail folder smartphone"],
      couches=[{"type": "etiquette", "numero": "03", "texte": "Date de fin du prix + spams", "a": 0.2}, src(EI)]),
    R("p093", fichier="cap13_energieinfo_messages_surligne.png", zoom="avant", couches=[src(EI)]),
    E("p094", {"type": "liste", "titre": "Pire qu'un prix qui s'arrête", "elements": [{"texte": "Prix fixe", "valeur": "s'arrête un jour"},
               {"texte": "Prix qui bouge", "valeur": "sans arrêt", "heros": True}]},
      ["stock chart zigzag screen", "volatile market graph monitor"], etiquette="Il y a pire"),
    # ── 06 À éviter n°2 : offres indexées / dynamiques ──────────────────────────────────────────────────────
    T("p095", "06", "Prix fixe ou indexé : que choisir ?", ["stock screen blurred", "trading monitor dark"],
      sous_titre="À éviter · n°2", ambiance="leger"),
    R("p096", ["electrical panel home breakers", "fuse box house", "circuit breaker panel close up"], transition="fondu"),
    E("p097", {"type": "liste", "titre": "Offre dynamique", "elements": [{"texte": "Le prix change", "valeur": "tous les jours"},
               {"texte": "et même", "valeur": "toutes les heures", "heros": True}], "source": EI},
      fichier="cap14_energieinfo_dynamiques.png", etiquette="Offre dynamique"),
    DV("p098", "Le kWh, marché + taxes seuls ?", ["25 c", "36 c", "50 c"]),
    M("p099", ["city apartment windows lit at night winter", "kitchen cooking evening stove", "living room lights evening winter"],
      couches=[src("energie-info.fr, offres dynamiques")]),
    S("p100", {"type": "comparaison", "titre": "Le kWh début novembre", "unite": " €/kWh", "decimales": 2, "heros": "b",
               "a": {"label": "Tarif bleu, réseau compris", "valeur": 0.20},
               "b": {"label": "Marché + taxes, sans réseau ni abonnement", "valeur": 0.36}, "source": "calcul Selectra, 11/11/2026"},
      etiquette_schema="Réponse : 36 c", avant_voix=SIL),
    R("p101", ["plug in wall socket europe", "electric kettle on counter", "boiling water kettle light"], couches=[src(CRE_147)]),
    E("p102", {"type": "liste", "titre": "Niveau de certitude", "elements": [{"texte": "Une note", "valeur": "A · B · C · D"}], "source": NIV},
      fichier="cap03_cre_niveau_certitude.png", etiquette="Niveau de certitude"),
    S("p103", {"type": "liste", "titre": "Niveau de certitude", "elements": [
        {"texte": "A", "valeur": "prix entièrement fixe garanti"},
        {"texte": "B", "valeur": "stable, ajusté si la réglementation change"},
        {"texte": "C", "valeur": "suit une formule définie à l'avance"},
        {"texte": "D", "valeur": "soumis à des facteurs externes", "heros": True}], "source": NIV},
      etiquette_schema="Les 4 lettres"),
    R("p104", ["contract document pen", "signing contract close up", "paper contract desk"],
      punch=P("p104", "imprévisible", "IMPRÉVISIBLE"), couches=[src("CRE, Lignes directrices, annexe 3 (niveau 4, l'équivalent de D)")]),
    M("p105", ["flipping through contract pages", "magnifying glass on document", "renewal letter envelope"],
      couches=[{"type": "etiquette", "numero": "02", "texte": "Cherche la lettre sur ton contrat", "a": 0.2}, src("CRE, délibération 2026-110")]),
    R("p106", fichier="cap03_cre_niveau_certitude_b.png", zoom="arriere", couches=[src(NIV)]),
    M("p107", ["opening drawer papers", "old documents in drawer", "file folder documents home"]),
    # ── 07 À éviter n°1 : le vieux contrat ──────────────────────────────────────────────────────────────────
    T("p108", "07", "Est-ce que je paie mon électricité trop cher ?", ["drawer papers blurred", "old files dark"],
      sous_titre="À éviter · n°1", ambiance="tension"),
    R("p109", ["old contract paper folder", "dusty documents box", "binder papers shelf"], transition="fondu"),
    E("p110", {"type": "liste", "titre": "Le crible de la CRE", "elements": [{"texte": "Prix analysés au", "valeur": "1er déc. 2025", "heros": True}],
               "source": CRE_COH},
      fichier="cap07a_cre_coherence_titre_sommaire.png", etiquette="Rapport de la CRE"),
    M("p111", ["apartment building windows night", "french houses street evening", "residential building lights"]),
    DV("p112", "Combien de foyers ?", ["100 000", "1,9 MILLION", "5 MILLIONS"]),
    E("p113", {"type": "liste", "titre": "1 % des contrats les plus chers", "elements": [{"texte": "Économie par an", "valeur": "? €", "heros": True}],
               "source": CRE_COH},
      fichier="cap07b_cre_coherence_591.png", etiquette="Calcul de la CRE"),
    S("p114", {"type": "chiffre", "valeur": 591, "suffixe": " €/an HT", "revele_a": 0.6,
               "legende": "économie possible, 1 % des contrats les plus chers", "source": "CRE, 03/06/2026"},
      ["bill and coins on table", "euro coins on invoice"], etiquette_schema="Au moins"),
    R("p115", ["wind turbines green field", "solar panels roof", "green energy wind farm"],
      couches=[{"type": "mots", "texte": "OFFRE VERTE", "heros": "VERTE", "position": "haut", "a": a_mot("p115", "vertes")},
               src("CRE, 03/06/2026 (91 % des contrats au-delà de +5 %)")]),
    S("p116", {"type": "chiffre", "valeur": 1.9, "decimales": 1, "suffixe": " million", "revele_a": a_mot("p116", "un million", SIL),
               "legende": "foyers en prix fixe à + de 5 % au-dessus du tarif bleu", "source": CRE_COH + " (prix au 1er décembre 2025)"},
      etiquette_schema="Réponse n°5", avant_voix=SIL),
    E("p117", {"type": "liste", "titre": "Ce qu'elle dit", "elements": [{"texte": "« Nous allons prendre contact avec les quelques fournisseurs qui "
               "maintiennent ces offres à prix fixe très onéreuses pour leur demander des explications »", "heros": True},
               {"texte": "Emmanuelle Wargon, présidente de la CRE"}], "source": "UFC-Que Choisir, 18/06/2026"},
      fichier="cap08_ufc_wargon.png", etiquette="Citation"),
    M("p118", ["price per kilowatt hour bill close up", "bill subscription line close up", "cap04_cre_annexeB.png"],
      couches=[{"type": "etiquette", "numero": "01", "texte": "Compare au tarif bleu", "a": 0.2}, src(CRE_147)]),
    R("p119", ["hand turning on light switch", "lamp turning on evening", "light bulb switching on"]),
    # ── 08 À prendre n°3 : heures creuses / Tempo ───────────────────────────────────────────────────────────
    T("p120", "08", "Heures creuses ou Tempo : ça vaut le coup ?", ["washing machine blurred", "laundry room dark"],
      sous_titre="À prendre · n°3", ambiance="leger"),
    R("p121", ["washing machine start button night", "loading washing machine", "washing machine running"], transition="fondu"),
    E("p122", {"type": "liste", "titre": "Ta journée", "elements": [{"texte": "Heures pleines", "valeur": "16 h"},
               {"texte": "Heures creuses, surtout la nuit", "valeur": "8 h", "heros": True}], "source": CRE_147},
      ["water heater tank home", "boiler cylinder house", "hot water tank basement"], etiquette="Heures creuses"),
    R("p123", ["summer afternoon sun house", "solar panels roof sunny day", "sunny garden afternoon"],
      couches=[src("Enedis via Selectra, 20/07/2026")]),
    S("p124", {"type": "chiffre", "valeur": 15, "suffixe": " %", "revele_a": a_mot("p124", "quinze"),
               "legende": "des foyers en heures creuses ignorent leurs horaires", "source": "baromètre énergie-info 2026, 03/11/2026"},
      fichier="cap15_barometre_2026.png", etiquette_schema="Baromètre du médiateur"),
    R("p125", ["washing machine timer setting", "programming washing machine delay", "hot water heater switch"],
      couches=[{"type": "etiquette", "numero": "HC", "texte": "Vérifie tes horaires", "a": 0.2}]),
    M("p126", ["calendar colored days", "radiator in winter home", "winter sky clouds"], surtitre="300 bleus · 43 blancs · 22 rouges",
      couches=[src("CRE, délibération 2026-147")]),
    DV("p127", "Jour rouge, heures pleines : le kWh ?", ["30 c", "50 c", "73 c"]),
    E("p128", {"type": "liste", "titre": "Les jours rouges", "elements": [{"texte": "Quand", "valeur": "novembre → mars", "heros": True},
               {"texte": "Le week-end", "valeur": "jamais"}, {"texte": "Tu le sais", "valeur": "la veille"}], "source": "Selectra (règles Tempo)"},
      ["winter morning frost window", "snowy street france", "cold winter day house"], etiquette="Tempo"),
    S("p129", {"type": "comparaison", "titre": "Le kWh Tempo", "unite": " €/kWh", "decimales": 2, "heros": "b",
               "a": {"label": "Tarif bleu Base", "valeur": 0.20}, "b": {"label": "Jour rouge, heures pleines", "valeur": 0.73},
               "source": "CRE, délibération 2026-147, annexe B (57,73 c HT)"},
      etiquette_schema="Réponse : 73 c", avant_voix=SIL),
    R("p130", ["hand turning radiator thermostat", "electric heater knob", "radiator valve close up"]),
    M("p131", ["aerial view french town houses", "village rooftops france", "city rooftops aerial"], couches=[src("CRE, observatoire T2 2026")]),
    # ── 09 À prendre n°2 : le tarif bleu ────────────────────────────────────────────────────────────────────
    T("p132", "09", "Tarif bleu 2027 : faut-il le garder ?", ["bill papers blurred desk", "invoice stack dark"],
      sous_titre="À prendre · n°2", ambiance="tension"),
    R("p133", fichier="cap04_cre_annexeB_base.png", zoom="avant", transition="fondu",
      couches=[{"type": "mots", "texte": "= 20 c TTC", "position": "haut", "a": 1.5}, src(CRE_147)]),
    E("p134", {"type": "chiffre", "valeur": 26, "prefixe": "+", "suffixe": " €/an", "revele_a": a_mot("p134", "vingt-six"),
               "legende": "tarif bleu au 1er août 2026", "comparaison": "Facture moyenne : de 1 046 à 1 072 € TTC par an",
               "source": "AFP / Connaissance des énergies, 16/07/2026"},
      fichier="cap05_afp_facture_moyenne.png", etiquette="+2,5 %"),
    S("p135", {"type": "chiffre", "valeur": 52, "suffixe": " %", "revele_a": a_mot("p135", "la moitié"),
               "legende": "des offres moins chères que le tarif bleu, fin juin 2026", "source": "CRE, observatoire T2 2026 (via Kelwatt, 05/10/2026)"},
      ["electricity offers comparison paper", "energy bills comparison table"], etiquette_schema="Observatoire de la CRE"),
    R("p136", ["smartphone price comparison", "person comparing prices phone", "phone screen scrolling list"], couches=[src("Selectra, 10/11/2026")]),
    E("p137", {"type": "liste", "titre": "Comparateur Selectra", "elements": [{"texte": "Offres à prix fixe moins chères que le tarif bleu",
               "valeur": "? sur 29", "heros": True}], "source": "comparateur Selectra, relevé du 9 novembre 2026"},
      ["hand holding smartphone scrolling", "phone in hand close up"], etiquette="Devinette n°6"),
    DV("p138", "Offres fixes moins chères que le tarif bleu ?", ["3/29", "8/29", "20/29"]),
    # ── 10 À prendre n°1 ────────────────────────────────────────────────────────────────────────────────────
    T("p139", "10", "Changer de fournisseur d'électricité : la bonne offre", ["glowing light bulb dark", "lamp light blurred"],
      sous_titre="À prendre · n°1 : ?", ambiance="emotion"),
    R("p140", ["closing envelope hands", "sealing letter envelope", "envelope on table"], surtitre="Février 2026", transition="fondu"),
    E("p141", {"type": "processus", "titre": "Février 2026", "etapes": ["Relevé annulé", "≈ 700 kWh corrigés", "Geste de 300 €"], "actif": 1,
               "source": JDN},
      fichier="cap11f_jdn_denouement.png", etiquette="Le dénouement"),
    R("p142", ["hands holding paper document", "reading letter relief", "paper letter close up"], couches=[src(JDN)]),
    S("p143", {"type": "comparaison", "titre": "La facture du couple", "unite": " €", "decimales": 0, "heros": "b",
               "a": {"label": "Réclamé", "valeur": 4000}, "b": {"label": "Au final", "valeur": 3000}, "source": JDN},
      etiquette_schema="Le dénouement"),
    R("p144", ["calendar months marking", "monthly calendar pages", "paying bills at desk"], couches=[src(JDN)]),
    M("p145", ["new electricity meter installed", "signed contract close up", "hand holding pen"]),
    R("p146", fichier="cap01_comparateur_resultat_accueil.png", zoom="avant", couches=[src("comparateur.energie-info.fr")]),
    S("p147", {"type": "chiffre", "valeur": 8, "suffixe": " sur 29", "revele_a": a_mot("p147", "huit"),
               "legende": "offres à prix fixe moins chères que le tarif bleu",
               "source": "relevé Selectra, 9 novembre 2026, Base 6 kVA, 4 500 kWh/an"},
      etiquette_schema="Réponse n°6"),
    R("p148", fichier="cap01_comparateur_resultat_saisie.png", zoom="avant", couches=[src("comparateur.energie-info.fr")]),
    E("p149", {"type": "liste", "titre": "Il affiche la lettre", "elements": [{"texte": "A"}, {"texte": "B"}, {"texte": "C"}, {"texte": "D"}],
               "source": EI},
      fichier="cap02_energieinfo_nouveautes.png", etiquette="Comparateur officiel"),
    R("p150", ["bill customer number close up", "invoice details pen", "electricity bill reference number"],
      couches=[{"type": "mots", "texte": "15 MIN", "heros": "MIN", "position": "haut", "a": a_mot("p150", "quinzaine")},
               src("UFC-Que Choisir, 24/09/2026")]),
    M("p151", ["light bulb glowing", "electric meter wall", "power line close up"],
      couches=[{"type": "mots", "texte": "0 € DE FRAIS · 0 COUPURE", "heros": "COUPURE", "position": "haut", "a": 0.3},
               src("UFC-Que Choisir, 24/09/2026")]),
    R("p152", ["electricity bill and meter", "bill next to electric meter", "electric bill on table close up"],
      sons=[RISER(1.0)], ambiance="revelation"),
    S("p153", {"type": "liste", "titre": "À prendre · n°1", "elements": [{"texte": "Une offre à prix fixe", "valeur": "classée A", "heros": True},
               {"texte": "Kilowattheure", "valeur": "bloqué"}, {"texte": "Abonnement", "valeur": "bloqué"}], "source": NIV},
      etiquette_schema="Le numéro un", avant_voix=SIL, punch=P("p153", "classée a", "A", SIL),
      couches=[{"type": "flash", "a": a_mot("p153", "classée a", SIL)}]),
    E("p154", {"type": "liste", "titre": "Le n°1", "elements": [{"texte": "Prix fixe classé A", "valeur": "✔"},
               {"texte": "Moins cher que le tarif bleu", "valeur": "comparateur officiel", "heros": True}], "source": "comparateur.energie-info.fr"},
      fichier="cap01_comparateur_resultat.png", etiquette="Critère 2"),
    R("p155", fichier="cap16_energieinfo_etoiles.png", zoom="avant", couches=[src("energie-info.fr, Qualité de service clients")]),
    S("p156", {"type": "liste", "titre": "Le classement", "elements": [{"texte": "N°1", "valeur": "prix fixe A + moins cher + 4 étoiles"},
               {"texte": "Aucune ?", "valeur": "tarif bleu", "heros": True}, {"texte": "Les 5 pièges", "valeur": "à éviter"}]},
      etiquette_schema="Le classement final", punch=P("p156", "tarif bleu", "TARIF BLEU")),
    # ── 11 Fin ──────────────────────────────────────────────────────────────────────────────────────────────
    M("p157", ["bill end date close up", "typing comment on phone", "alphabet letter blocks"], ambiance="leger",
      couches=[{"type": "mots", "texte": "TON PRIX FIXE FINIT QUAND ?", "heros": "QUAND", "position": "haut", "a": 0.3}]),
    R("p158", ["christmas toys under tree", "wrapped gifts christmas tree", "toy shop christmas"]),
    E("p159", {"type": "liste", "titre": "Le Vrai Prix", "elements": [{"texte": "Abonne-toi", "heros": True},
               {"texte": "Prochaine enquête", "valeur": "les jouets de Noël"}]},
      ["hand pressing button smartphone", "notification bell phone"], etiquette="La suite", duree_min=10),
]

montage = {
    "titre": "Offre électricité moins chère 2026 : 5 pièges à éviter",
    "format": {"largeur": 1920, "hauteur": 1080, "fps": 30},
    "transition_defaut": "coupe",
    "duree_transition": 8,
    "voix": {"moteur": "edge", "locuteur": "fr-FR-VivienneMultilingualNeural", "debit": "+2%", "debit_continu": "+2%", "pause_phrase": 0.15},
    "musique": {"fichier": "../../public/sfx/musique-enquete.wav", "volume": 0.2},
    # musique par ambiance (scripts/musique_libre.py, Kevin MacLeod CC-BY) : sans ces fichiers, la musique générée ci-dessus sert
    "musiques": {"tension": "public/musique/tension.mp3", "emotion": "public/musique/emotion.mp3",
                 "revelation": "public/musique/revelation.mp3", "leger": "public/musique/leger.mp3"},
    "etalonnage": {"contraste": 1.06, "saturation": 1.08, "luminosite": 1},
    "grain": True,
    "sous_titres": {"actifs": True, "mots_par_ligne": 4},
    "respiration": 0.15,
    "scenes": [],
}

for s in scenes:
    s = dict(s)
    items = s.pop("_items", None)
    leg = s.pop("_legendes", None)
    c = CHOIX.get(s["id"])
    if c and s["format"] == "mosaique" and isinstance(c, list):
        refs = iter(c)
        s["medias"] = [{**({"fichier": "medias/" + x} if x.endswith(".png") else {"media_ref": next(refs)}),
                        **({"legende": leg[i]} if leg else {})} for i, x in enumerate(items)]
    elif c:
        s["media_ref"] = c
    if c:
        s.pop("recherche", None)
    # Commons : originaux téléchargés par le workflow Captures (le 429 des miniatures bloquait le rendu)
    if s.get("media_ref") in LOCAL:
        s["fichier"] = LOCAL[s.pop("media_ref")]
    for m in s.get("medias", []):
        if m.get("media_ref") in LOCAL:
            m["fichier"] = LOCAL[m.pop("media_ref")]
    montage["scenes"].append(s)


def controles(sc):
    err, avert = [], []
    ids = [s["id"] for s in sc]
    if len(ids) != len(set(ids)): err.append("ids en double : " + ", ".join(sorted({i for i in ids if ids.count(i) > 1})))
    if ids != [r["id"] for r in PLANS]: err.append("les ids ne suivent pas les plans du script")
    for s in sc:
        if s["texte"] != TXT[s["id"]]: err.append(f"{s['id']} : narration différente du script")
        if s["format"] != FMT_SCRIPT[s["id"]]:
            avert.append(f"{s['id']} : format {s['format']} (script : {FMT_SCRIPT[s['id']]})")
        aMedia = s.get("fichier") or s.get("recherche") or s.get("media_ref") or s.get("medias")
        if s["format"] in ("rush", "ecran_partage", "mosaique", "titre") and not aMedia:
            err.append(f"{s['id']} ({s['format']}) sans média")
        if s["format"] == "schema" and not s.get("schema"): err.append(f"{s['id']} : schéma manquant")
        if s["format"] == "ecran_partage" and not s.get("schema"): err.append(f"{s['id']} : écran partagé sans schéma")
        if (s.get("schema") or {}).get("type") == "devine" and "bonne" in s["schema"]: err.append(f"{s['id']} : devinette avec `bonne`")
        if SRC_SCRIPT[s["id"]] and not (any(c["type"] == "source" for c in s.get("couches", [])) or (s.get("schema") or {}).get("source")):
            err.append(f"{s['id']} : source du script absente de l'écran")
        if s.get("punch") and (s.get("schema") or {}).get("type") in ("chiffre", "comparaison", "decomposition"):
            avert.append(f"{s['id']} : punch + schéma à impact (double emphase)")
    for a, b in zip(sc, sc[1:]):
        if a["format"] == b["format"] and int(b["id"][1:]) > 17:
            avert.append(f"{a['id']}→{b['id']} : même format {b['format']} (règle n°6)")
    vues = {}
    for s in sc:
        for q in (s.get("recherche") or []):
            if q in vues: err.append(f"requête « {q} » en double : {vues[q]} et {s['id']}")
            vues.setdefault(q, s["id"])
    return err, avert


if __name__ == "__main__":
    erreurs, avertissements = controles(montage["scenes"])
    for a in avertissements: print("⚠", a)
    if erreurs:
        print("\n".join("✖ " + e for e in erreurs)); sys.exit(1)
    ep = os.path.join(RACINE, "episodes", "electricite")
    os.makedirs(ep, exist_ok=True)
    json.dump(montage, open(os.path.join(ep, "montage.json"), "w"), ensure_ascii=False, indent=1)
    sans = [s for s in montage["scenes"] if s.get("recherche")]
    par_format = {}
    for s in montage["scenes"]: par_format[s["format"]] = par_format.get(s["format"], 0) + 1
    print(f"{len(montage['scenes'])} scènes {par_format}, {len(sans)} à repérer")
    if "--lots" in sys.argv:
        n = 8
        for k in range(0, len(sans), n):
            nom = f"electricite-rep-{k // n + 1}"
            d = os.path.join(RACINE, "videos", nom)  # videos/*/montage.json : motif qui lance le workflow Repérage au push
            os.makedirs(d, exist_ok=True)
            json.dump({"titre": nom, "scenes": [{"id": s["id"], "texte": s["texte"] or s.get("titre", ""), "recherche": s["recherche"]}
                                                for s in sans[k:k + n]]},
                      open(os.path.join(d, "montage.json"), "w"), ensure_ascii=False, indent=1)
            print("lot", os.path.relpath(d, RACINE))

# ── Images à fabriquer (1920×1080, dans episodes/electricite/medias/) ─────────────────────────────────────────
# Règle commune : aucun nom de fournisseur lisible (recadrer titre + date + phrase), aucune donnée personnelle,
# en-tête du site/document + date visibles, surlignage jaune sur la phrase citée.
#  cap01_comparateur_resultat_accueil.png  (p146) page d'accueil du comparateur officiel comparateur.energie-info.fr.
#  cap01_comparateur_resultat_saisie.png   (p148) le formulaire rempli « Base 6 kVA, 4 500 kWh/an », sans nom de fournisseur.
#  cap01_comparateur_resultat.png          (p154) un résultat avec la pastille A d'une offre, nom de l'offre/fournisseur masqué.
#  cap02_energieinfo_nouveautes.png        (p149) surligneur sur « un outil public, gratuit, neutre et indépendant ».
#  cap03_cre_niveau_certitude.png          (p102) fiche CRE : les 4 pastilles A (vert foncé) → D (jaune), aucune mise en valeur.
#  cap03_cre_niveau_certitude_b.png        (p106) même fiche, autre recadrage (plus serré sur les 4 pastilles), aucune mise en valeur.
#  cap04_cre_annexeB.png                   (p118, case de mosaïque) annexe B de la délibération 2026-147 : ligne Base 6 kVA.
#  cap04_cre_annexeB_base.png              (p133) annexe B, cadrage sur la ligne « Base résidentiel 13,61 c€/kWh HT ».
#  cap05_afp_facture_moyenne.png           (p134) surligneur sur « une facture moyenne passant de 1 046 à 1 072 euros TTC par an ».
#  cap06_energieinfo_seule_composante.png  (p027) surligneur sur « Il s'agit de la seule composante soumise à la concurrence. »
#  cap07a_cre_coherence_titre.png          (p008) couverture du rapport « Cohérence des offres » (03/06/2026), logo CRE + date.
#  cap07a_cre_coherence_titre_sommaire.png (p110) même rapport, autre recadrage : sommaire / date 03/06/2026.
#  cap07b_cre_coherence_591.png            (p113) surligneur sur « au moins 591 €/an HT pour les offres à prix fixe d'électricité ».
#  cap08_ufc_wargon.png                    (p117) article UFC-Que Choisir : titre + date 18/06/2026 (+ la citation de Wargon si visible).
#  cap09_loi_2025_594.png                  (p050) reproduction du JO, surligneur sur « Il est interdit de démarcher par téléphone… ».
#  cap10_energieinfo_faux_mediateur.png    (p053) recadrée sur le TITRE seulement (le texte nomme un fournisseur).
#  cap11a_jdn_titre.png                    (p013) titre JDN « "4 000 euros en un mois" : son compteur Linky devient fou… » + date 15/05/2026.
#  cap11a_jdn_titre_releves.png            (p062) même article, paragraphe « entre mars et mai… cesse de transmettre ses relevés ».
#  cap11b_jdn_on_ne_sait_pas.png           (p015) phrase « "On ne sait pas", admet Matthieu Bertrand Neuser » surlignée.
#  cap11c_jdn_exceptionnel.png             (p066) phrase « compteur Linky qui dysfonctionne, ça arrive, mais ça reste exceptionnel » surlignée.
#  cap11d_jdn_ca_change_tout.png           (p075) phrase « Ça change tout : ils nous répondent et font attention » surlignée.
#  cap11e_jdn_mai2025.png                  (p073, case de mosaïque) paragraphe « mai 2025 » (le couple contacte l'Adéic), nom du fournisseur masqué.
#  cap11f_jdn_denouement.png               (p141) paragraphe du dénouement (février 2026 : relevé annulé, ≈ 700 kWh, geste de 300 €).
#  cap12_jechange.png                      (p080, fond flou p082) titre + « mis à jour le 11/11/2026 », nom du fournisseur hors cadre,
#                                          le « 42 % » du titre MASQUÉ par un cache opaque ; pas la grille datée du 01/02/2027.
#  cap12_jechange_revele.png               (p090) même cadrage, cache retiré : « +42 % » visible + surligneur sur « le silence vaut acceptation ».
#  cap13_energieinfo_messages.png          (p092, case de mosaïque) page energie-info sur les messages / changements de prix, sans surlignage.
#  cap13_energieinfo_messages_surligne.png (p093) même page, surligneur sur « vous pouvez changer de fournisseur à tout moment et sans frais ».
#  cap14_energieinfo_dynamiques.png        (p097) surligneur sur « le prix de l'énergie fluctue tous les jours et toutes les heures ».
#  cap15_barometre_2026.png                (fond flou p049 et p124) baromètre énergie-info 2026 (03/11/2026), page des chiffres.
#  cap16_energieinfo_etoiles.png           (p155) légende des étoiles « ≤ 25 saisines pour 100 000 contrats », SANS le tableau des noms.
