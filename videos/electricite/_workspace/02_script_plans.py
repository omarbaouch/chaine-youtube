# -*- coding: utf-8 -*-
# Usage : python3 02_script_plans.py /tmp/plans.json && python3 02_script_rendu.py /tmp/plans.json 02_scriptwriter_script.md
"""Génère videos/electricite/_workspace/02_scriptwriter_script.md à partir de la liste des plans.
Minutage : 150 mots/min (2,5 mots/s) + 0,15 s de respiration ; carte titre 2,8 s ; compte à rebours 3 s ; silence 0,5 s."""
import re, sys

PX = lambda *q: "Pixabay : " + " · ".join(f"« {x} »" for x in q)

# (format, narration, image, punch, options)
# options : cd=compte à rebours 3 s ; sil=0,5 s de silence avant ; ch=(numero, titre, sous_titre) pour une carte ;
#           tag=étiquette rétention (D1, RH, REV...) ; src=source à l'écran
P = []
def p(fmt, txt, img, punch="", **o):
    P.append(dict(fmt=fmt, txt=txt, img=img, punch=punch, **o))
def sec(titre, note=""):
    P.append(dict(section=titre, note=note))

# ---------------------------------------------------------------- ACCROCHE
sec("00 — Accroche (images réelles plein écran uniquement, aucun schéma, aucune carte, aucune annonce de plan)",
    "Chapitre YouTube 0:00 « Facture d'électricité : où vont tes 100 € ? ». Voix d'Omar si `episodes/electricite/voix/accroche.m4a` existe (p001 à p017, ≈ 58 s ; à défaut p001 à p009, ≈ 31 s), sinon Vivienne.")
p("rush", "Sur cent euros de ta facture d'électricité,",
  "IMAGE DE LA MINIATURE dès la frame 0 : `medias/omar-facture.mp4` (facture d'Omar posée devant son Linky, nom/adresse/n° client/PDL floutés), zoom avant lent sur le montant total (flouté). Sinon "
  + PX("french electricity bill paper close up", "hand holding electricity bill", "paper invoice table close up") + ".",
  tag="1re phrase = promesse de la vidéo Black Friday, sur l'image de la miniature")
p("rush", "combien paient vraiment le courant ?",
  "`medias/omar-linky.mp4` : écran du Linky (boîtier jaune-vert) qui défile, numéro de compteur flouté. Sinon "
  + PX("linky smart meter", "green electricity meter display", "smart meter france close up") + ". Vérifier : compteur français, pas américain.",
  punch="COURANT ?")
p("rush", "Et cet hiver, quelle offre te protège vraiment ?",
  "`medias/omar-radiateur.mp4` (main qui monte le thermostat). Sinon " + PX("electric radiator home winter", "hand adjusting radiator thermostat", "white electric heater living room") + ".",
  punch="TE PROTÈGE", tag="GRANDE QUESTION (avant 8 s)")
p("rush", "Devine d'abord : sur ces cent euros, combien pour ton fournisseur :",
  "`medias/omar-facture.mp4`, autre prise : doigt qui suit les lignes de la facture. Sinon " + PX("finger pointing at bill lines", "reading invoice close up", "person checking utility bill") + ".")
p("rush", "vingt euros, quarante euros, ou soixante euros ?",
  "Même facture en gros plan ; trois GROS chiffres posés sur le papier, un par un, au rythme de la voix : « 20 € » · « 40 € » · « 60 € » (120 px, contour noir). AUCUNE case allumée (règle 20). Compte à rebours 3 s après la question. Pas de panneau sombre.",
  cd=True, tag="D1 (réponse p027)")
p("rush", "Sur les marchés, l'électricité vient de s'envoler.",
  PX("high voltage power lines sunset", "electricity pylons winter france", "power line towers aerial") + ". Pylônes européens (pas de poteaux en bois américains).")
p("rush", "Et certains contrats vont suivre, dès janvier.",
  "`medias/omar-courrier.mp4` (enveloppe dans une boîte aux lettres française). Sinon " + PX("letter in mailbox close up", "hand taking envelope from mailbox", "opening letter envelope") + ".")
p("rush", "Selon la C R E, certains foyers pouvaient économiser",
  "Capture `cap07a_cre_coherence_titre.png` plein écran (couverture du rapport « Cohérence des offres », 03/06/2026), travelling lent ; logo CRE et date lisibles.",
  src="CRE, rapport Cohérence des offres, 03/06/2026")
p("rush", "au moins cinq cent quatre-vingt-onze euros par an, hors taxes.",
  "`medias/omar-facture.mp4` : main qui tient la facture ; gros « 591 € » orange posé sur le papier (même pastille que la miniature), mention 24 px « par an, HT, 1 % des contrats les plus chers · CRE ». C'est l'enjeu promis par la miniature, pas une réponse de devinette.",
  punch="591 €", tag="promesse miniature")
p("mosaique", "Toi aussi, tu paies peut-être trop. Et parfois, c'est pire.",
  "Mosaïque de 3 plans d'Omar : `medias/omar-interrupteur.mp4` (main qui éteint la lumière), `omar-bouilloire.mp4`, `omar-chargeur.mp4`. Sinon " + PX("hand switching off light switch", "electric kettle boiling kitchen", "phone charger plugged socket") + ".",
  tag="RH")
p("rush", "Printemps deux mille vingt-quatre, dans les Yvelines.",
  PX("suburban houses france", "french pavilion house street", "residential street spring") + " ; surtitre « Yvelines · printemps 2024 ».")
p("mosaique", "Un couple ouvre sa facture d'électricité.",
  "Mosaïque de 2 : `medias/omar-enveloppe.mp4` (les mains d'Omar ouvrent une enveloppe ; pas de visage, l'article n'en montre pas) puis la lettre dépliée. Sinon " + PX("hands opening envelope close up", "opening letter at home", "reading letter kitchen table") + ".",
  tag="VRAIE PERSONNE")
p("ecran_partage", "Quatre mille euros, pour un seul mois d'électricité.",
  "À gauche : capture `cap11a_jdn_titre.png` (titre « \"4 000 euros en un mois\" : son compteur Linky devient fou… » + date 15/05/2026, Journal du Net). À droite : gros « 4 000 € » orange qui tombe avec impact.",
  punch="4 000 €", src="Journal du Net, 15/05/2026")
p("rush", "Pourquoi leur compteur s'est arrêté ? Personne n'a la réponse.",
  "`medias/omar-linky.mp4`, plan serré sur l'écran éteint ou figé. Sinon " + PX("electric meter close up dark", "smart meter blinking light", "electricity meter box wall") + ".")
p("ecran_partage", "« On ne sait pas », admet le juriste de leur association.",
  "À gauche : capture `cap11b_jdn_on_ne_sait_pas.png` (phrase « \"On ne sait pas\", admet Matthieu Bertrand Neuser » surlignée). À droite (Vitre) : citation « On ne sait pas. » + « Matthieu Bertrand Neuser, juriste de l'Adéic (Journal du Net, 15/05/2026) ».",
  src="Journal du Net, 15/05/2026")
p("rush", "Tu sauras à la fin combien ils ont vraiment payé.",
  "Retour sur les mains d'Omar et la facture dépliée, montant flouté. Sinon " + PX("worried hands holding bill", "paper bill on table lamp", "person reading bill at night") + ".",
  tag="BOUCLE couple (fermée p146)")
p("mosaique", "Mais d'abord, ouvrons ensemble ta facture, ligne par ligne.",
  "Mosaïque de 3 gros plans de la facture d'Omar (lignes « abonnement », « consommation », « taxes ») ; données personnelles floutées.")

# ---------------------------------------------------------------- CH 1
p("titre", "", "Carte titre : numéro « 01 », titre « Facture d'électricité : où vont tes 100 € ? », sur rush flouté de la facture (`medias/omar-facture.mp4`). Petit impact.",
  ch=("01", "Facture d'électricité : où vont tes 100 € ?"))
p("rush", "Sur ta facture, il y a trois grandes familles de lignes.",
  "`medias/omar-facture.mp4` : doigt qui pointe les trois blocs ; annotation `Annotation` « 1 · 2 · 3 » sur chaque bloc.")
p("ecran_partage", "D'abord le réseau : les lignes, les poteaux, et le compteur, jusqu'à chez toi.",
  "À gauche : " + PX("power lines countryside france", "electric pole street", "lineman working on power line") + ". À droite : schéma `decomposition` « Tes 100 € » qui se construit : 1re part « Réseau » (valeur encore masquée).")
p("rush", "Ça, tu le paies pareil, quel que soit ton fournisseur.",
  PX("electrician technician meter installation", "worker installing electric meter", "electric cabinet technician") + ". Étiquette « PAREIL POUR TOUS ».")
p("schema", "Sur cent euros, le réseau en prend un peu moins de trente.",
  "Schéma `decomposition` (fond : rush flouté des pylônes) : « Réseau ≈ 28 € » s'allume. Parts « Taxes » et « Fourniture » encore « ? ». Source 24 px : « calcul Le Vrai Prix, tarif bleu Base 6 kVA, 4 500 kWh/an, d'après la CRE ».",
  punch="≈ 28 €", src="calcul Le Vrai Prix d'après la CRE (délibérations 2026-147 et 2026-105)")
p("mosaique", "Ensuite, les taxes : l'accise, une petite contribution, et la T V A.",
  "Mosaïque de 3 gros plans de la facture d'Omar : ligne « Accise sur l'électricité », ligne « CTA », ligne « TVA » (chacune entourée en orange quand elle est nommée).")
p("rush", "Devine : sur cent euros, dix, vingt, ou trente euros de taxes ?",
  "Facture d'Omar en plein écran ; trois GROS chiffres posés sur le papier : « 10 € » · « 20 € » · « 30 € ». Aucune case allumée. Compte à rebours 3 s.",
  cd=True, tag="D1 bis (réponse p024)")
p("schema", "Une trentaine. Presque un tiers de ta facture, ce sont des taxes.",
  "Schéma `decomposition` : « Taxes ≈ 31 € » s'ajoute à la barre (accise ≈ 13 €, T V A ≈ 17 €, CTA ≈ 1 € en petit). « Fourniture » reste « ? ».",
  punch="≈ 31 €", src="calcul Le Vrai Prix d'après la CRE")
p("rush", "Il reste la fourniture : ce que te vend vraiment ton fournisseur.",
  "`medias/omar-facture.mp4` : doigt sur la ligne « consommation » ; ou `medias/omar-bouilloire.mp4` (bouilloire qui chauffe). Sinon " + PX("electric kettle boiling kitchen", "kettle steam close up", "switching on kettle") + ".")
p("ecran_partage", "C'est la seule part qui change d'un contrat à l'autre.",
  "À gauche : capture `cap06_energieinfo_seule_composante.png`, surligneur jaune sur « Il s'agit de la seule composante soumise à la concurrence. » À droite : la barre, part « Fourniture = ? » qui pulse.",
  src="energie-info.fr (médiateur national de l'énergie), consulté le 17/11/2026")
p("schema", "Réponse à la première devinette : à peu près quarante euros.",
  "PIC n°1. Musique coupée 0,5 s avant, impact. Schéma `decomposition` complet : Fourniture ≈ 41 € (héros orange), Réseau ≈ 28 €, Taxes ≈ 31 €. La case « 40 € » de la devinette revient et s'allume (`bonne`: 1). Source : « ≈ 41 / 28 / 31 € — calcul Le Vrai Prix, tarif bleu Base 6 kVA, 4 500 kWh/an, d'après la CRE ».",
  punch="≈ 40 €", sil=True, tag="RÉPONSE D1", src="calcul Le Vrai Prix d'après la CRE")
p("ecran_partage", "Dans ces quarante euros, environ sept paient la commercialisation et des certificats d'économies d'énergie.",
  "À gauche : " + PX("call center headset office", "customer service desk phone", "office telephone desk") + ". À droite : la part « Fourniture » se coupe en deux : « ≈ 7 € commercialisation + certificats d'économies d'énergie » / « ? ».",
  src="estimation Le Vrai Prix d'après la CRE (délibération 2026-06)")
p("rush", "Et le courant lui-même, celui qui sort des centrales ?",
  PX("nuclear power plant cooling towers", "nuclear plant river france", "power station steam towers") + ". Centrale à tours de refroidissement, ciel européen.")
p("schema", "Une trentaine d'euros seulement, sur tes cent euros.",
  "Schéma `chiffre` : « ? » jusqu'à 1,2 s puis « ≈ 30 € » (revele_a: 1.2), légende « le courant lui-même », comparaison « moins d'un tiers de ta facture », mention « estimation d'après la CRE ». Fond : rush flouté de la centrale.",
  punch="≈ 30 €", src="estimation Le Vrai Prix d'après la CRE (± 3 €)")
p("rush", "Et c'est justement cette part-là qui s'envole sur les marchés. De combien ?",
  PX("stock market screen numbers", "trading floor monitors", "financial chart screen rising") + ". Écrans de cotation, chiffres en mouvement.",
  tag="RH + BOUCLE D2")

# ---------------------------------------------------------------- CH 2
p("titre", "", "Carte titre « 02 » : « Prix de l'électricité 2027 : pourquoi ça monte ? », sur rush flouté des pylônes.",
  ch=("02", "Prix de l'électricité 2027 : pourquoi ça monte ?"))
p("rush", "Jusqu'en deux mille vingt-cinq, les fournisseurs avaient une part du nucléaire à prix régulé.",
  PX("nuclear power plant aerial", "nuclear reactor building", "cooling tower steam sky") + " (autre plan que la centrale du chapitre 01).")
p("mosaique", "Depuis janvier, c'est fini : ils achètent tout sur les marchés, ou le produisent eux-mêmes.",
  "Mosaïque : " + PX("trading floor screens", "electricity grid control room", "wind turbines field") + ". Surtitre « Depuis le 1er janvier 2026 ».",
  src="CRE, délibération 2026-06")
p("ecran_partage", "Deuxième devinette : début novembre, sur le marché, le prix avait été multiplié par combien ?",
  "À gauche : rush d'écrans de cotation. À droite (Vitre) : « Prix de gros · novembre 2025 → novembre 2026 : × ? ».")
p("rush", "Par deux, par quatre, ou par dix, en un an ?",
  "Plein écran sur un écran de cotation réel ; trois GROS chiffres posés dessus : « ×2 » · « ×4 » · « ×10 ». Aucune case allumée. Compte à rebours 3 s.",
  cd=True, tag="D2 (réponse p038)")
p("mosaique", "Et le mécanisme censé prendre le relais s'appelle le versement nucléaire universel.",
  "Mosaïque : centrale, ligne haute tension, Linky d'Omar. Surtitre « Versement nucléaire universel ».")
p("schema", "Selon la C R E, début octobre, il ne te rendrait rien en deux mille vingt-sept.",
  "Schéma `chiffre` : « 0 € », légende « reversement prévu en 2027 », source « estimation CRE du 1er octobre 2026, rapportée par Selectra et Hello Watt ». Fond : rush flouté de la centrale.",
  punch="0 €", src="estimation CRE, 01/10/2026 (via Selectra, 01/11/2026)")
p("rush", "Et le courant livrable l'an prochain a plus que doublé depuis janvier.",
  PX("financial graph rising screen", "stock chart going up monitor", "price chart close up") + ".", src="Selectra, 10/11/2026 ; TotalEnergies, 20/10/2026")
p("schema", "Réponse : début novembre, l'électricité s'échangeait environ quatre fois plus cher qu'un an plus tôt.",
  "Schéma `comparaison` : « novembre 2025 ≈ 66 €/MWh » contre « 1er-10 novembre 2026 ≈ 266 €/MWh » (héros), gros « ×4 » avec impact. La case « ×4 » s'allume. Source 24 px : « relevé Selectra des prix spot, 11/11/2026 ».",
  punch="×4", sil=True, tag="RÉPONSE D2", src="relevé Selectra des prix spot, 11/11/2026")
p("rush", "Ta facture, elle, n'a pas pris fois quatre. Le tarif bleu amortit le choc.",
  "`medias/omar-facture.mp4`, nouvelle prise (facture de face). Sinon " + PX("bill on table with calculator", "calculator and invoice", "person calculating bills") + ".")
p("ecran_partage", "Son prix est calculé sur des achats étalés sur vingt-quatre mois.",
  "À gauche : " + PX("calendar pages turning", "wall calendar months", "desk calendar close up") + ". À droite : schéma `processus` « 24 mois d'achats » (24 petites cases qui se remplissent).",
  src="CRE, délibération 2026-06")
p("rush", "Il ne bouge pas avant le premier février. Après, personne ne sait de combien il montera.",
  PX("calendar february page", "calendar date circled red", "marking calendar pen") + ". Surtitre « 1er février 2027 ».", tag="RH")
p("mosaique", "Les autres offres n'ont pas toutes cette protection. Certaines changent déjà de prix, en silence.",
  "Mosaïque : courrier ouvert, téléphone avec un e-mail, boîte aux lettres. Sinon " + PX("reading letter at home", "email on smartphone close up", "mailbox letters") + ".")
p("schema", "Voilà les cinq pièges à éviter cet hiver, et les trois choix qui te protègent.",
  "Schéma `liste` = le tableau du classement (seule annonce de plan, après 30 s) : colonne rouge « À ÉVITER 5 → 1 », colonne verte « À PRENDRE 3 → 1 » ; toutes les cases fermées, la case verte n°1 affiche « ? ». Fond : rush flouté de la facture.",
  tag="annonce du classement (une seule fois)")

# ---------------------------------------------------------------- CH 3  À ÉVITER 5
p("titre", "", "Carte « À ÉVITER · 5 » (rouge) : « Démarchage électricité : est-ce légal ? », sur rush flouté d'un téléphone.",
  ch=("À éviter n°5", "Démarchage électricité : est-ce légal ?"))
p("rush", "Piège numéro cinq : le contrat signé au téléphone, ou sur le pas de ta porte.",
  PX("smartphone ringing unknown number table", "phone ringing on kitchen table", "incoming call smartphone close up") + ". Écran sans nom de marque.")
p("schema", "D'après le baromètre du médiateur, plus d'un tiers des foyers ont signé après un démarchage.",
  "Schéma `chiffre` : « 36 % » (« ? » jusqu'à 1 s), légende « des foyers ont signé un contrat d'énergie après un démarchage ». Fond : capture `cap15_barometre_2026.png` floutée.",
  punch="36 %", src="baromètre énergie-info 2026, médiateur national de l'énergie, 03/11/2026")
p("ecran_partage", "Mais depuis le onze août deux mille vingt-six, la loi a changé.",
  "À gauche : capture `cap09_loi_2025_594.png` (reproduction du JO), surligneur sur « Il est interdit de démarcher par téléphone, directement ou par l'intermédiaire d'un tiers… ». À droite : « Loi n° 2025-594 · en vigueur le 11 août 2026 ».",
  src="loi n° 2025-594 du 30/06/2025, art. 13")
p("mosaique", "Un vendeur n'a plus le droit de t'appeler sans ton accord préalable.",
  "Mosaïque : " + PX("hand rejecting phone call", "declining call smartphone", "phone call screen close up") + " + `medias/omar-telephone.mp4` si présent.")
p("rush", "Troisième devinette : un contrat signé après un appel interdit, il est valable, annulable, ou nul ?",
  "Téléphone posé sur un contrat papier ; trois GROS mots posés sur l'objet : « VALABLE » · « ANNULABLE » · « NUL ». Aucune case allumée. Compte à rebours 3 s.",
  cd=True, tag="D3 (réponse p058)")
p("ecran_partage", "Et méfie-toi des faux médiateurs : le vrai ne démarche jamais, et ne vend aucun contrat.",
  "À gauche : capture `cap10_energieinfo_faux_mediateur.png` recadrée sur le TITRE seulement (le texte nomme un fournisseur). À droite : étiquette « FAUX MÉDIATEUR ».",
  src="energie-info.fr, consulté le 17/11/2026")
p("schema", "Et l'entreprise qui appelle sans accord risque jusqu'à trois cent soixante-quinze mille euros d'amende.",
  "Schéma `chiffre` : « 375 000 € », légende « amende maximale pour une entreprise », source « code de la consommation, art. L. 242-16 ».",
  punch="375 000 €", src="code de la consommation, art. L. 242-16")
p("rush", "Réponse à la devinette : le contrat est nul, comme s'il n'avait jamais existé.",
  PX("tearing paper contract", "ripping document close up", "torn paper sheet hands") + ". Gros « NUL » orange ; la case « NUL » de la devinette s'allume.",
  punch="NUL", sil=True, tag="RÉPONSE D3", src="code de la consommation, art. L. 223-1")
p("ecran_partage", "Deux limites quand même : ton fournisseur actuel peut t'appeler pour ton contrat en cours.",
  "À gauche : téléphone qui sonne. À droite : schéma `liste` « Ce que dit la loi » : ✔ « appel sans accord : interdit » · ✖ « ton fournisseur actuel, pour ton contrat » (s'allume) · ✖ « à ta porte ».")
p("rush", "Et cette loi parle du téléphone. À ta porte, le démarchage reste permis.",
  "`medias/omar-porte.mp4`, autre prise (sonnette). Sinon " + PX("salesman at front door", "man ringing doorbell", "door knock close up") + ". Ligne « à ta porte » de la liste qui pulse en surimpression.")
p("mosaique", "Le réflexe : ne signe jamais sur le moment. Raccroche, ferme, et compare au calme.",
  "Mosaïque : main qui raccroche, porte qui se ferme, téléphone avec un comparateur. Étiquette « RÉFLEXE n°5 ».", tag="UTILITÉ")
p("rush", "Mais le piège suivant arrive par la poste. Et notre couple des Yvelines le connaît bien.",
  "`medias/omar-courrier.mp4` (main qui prend une enveloppe). Sinon " + PX("hand taking letter from mailbox", "envelope in letterbox", "mail delivery letterbox") + ".", tag="RH + retour couple")

# ---------------------------------------------------------------- CH 4  À ÉVITER 4
p("titre", "", "Carte « À ÉVITER · 4 » : « Facture d'électricité trop élevée : que faire ? », sur rush flouté du Linky.",
  ch=("À éviter n°4", "Facture d'électricité trop élevée : que faire ?"))
p("rush", "Piège numéro quatre : la facture estimée que tu ne vérifies jamais.",
  "`medias/omar-linky.mp4`, gros plan de l'écran (index). Annotation « INDEX RÉEL ? ».")
p("ecran_partage", "Entre mars et mai deux mille vingt-quatre, leur Linky n'envoie plus aucun relevé.",
  "À gauche : capture `cap11a_jdn_titre.png` (recadrage différent de l'accroche : paragraphe sur les relevés). À droite : schéma `processus` « Mars → Mai 2024 : plus de relevés » (étape 1 allumée).",
  src="Journal du Net, 15/05/2026")
p("rush", "Leur fournisseur facture donc à l'estimation, et réclame quatre mille euros pour le mois de mai.",
  PX("calculator and bill close up", "invoice total amount paper", "shocked hands holding paper bill") + ". Étape 2 « Estimation → 4 000 € » en surimpression.")
p("mosaique", "Ils ne paient pas. Le contrat est résilié, et leur espace client est coupé.",
  "Mosaïque : facture repoussée sur la table, téléphone « accès refusé » (écran générique), lettre recommandée. Étape 3 « Résiliation ».")
p("rush", "Puis arrive un commissaire de justice, l'ancien huissier.",
  PX("official letter envelope stamp", "registered mail letter", "door with letter on floor") + ".")
p("ecran_partage", "Leur juriste le dit pourtant : « compteur Linky qui dysfonctionne, ça arrive, mais ça reste exceptionnel. »",
  "À gauche : `medias/omar-linky.mp4`. À droite (Vitre) : la citation mot pour mot + « Matthieu Bertrand Neuser, juriste de l'Adéic (Journal du Net, 15/05/2026) » ; capture `cap11c_jdn_exceptionnel.png` en vignette.",
  src="Journal du Net, 15/05/2026")
p("rush", "Devinette : réclamation sans réponse, tu saisis le médiateur après deux semaines, deux mois, ou six mois ?",
  "`medias/omar-facture.mp4` (facture tenue à la main) ; trois GROS mots posés sur le papier : « 2 SEMAINES » · « 2 MOIS » · « 6 MOIS ». Aucune case allumée. Compte à rebours 3 s.",
  cd=True, tag="D3 bis (réponse p000)")
p("mosaique", "Garde ta réponse. L'an dernier, dans l'Hérault, une sexagénaire a vécu pire.",
  "Mosaïque : " + PX("etang de thau sete", "mediterranean village france", "south france lagoon village") + ". Surtitre « Hérault · 2025 ».")
p("rush", "Une erreur de saisie, et on lance un prélèvement de deux cent onze mille euros.",
  PX("bank statement close up", "bank card payment terminal", "hands holding bank statement") + " (mains seulement). Gros « 211 993 € » orange ; en petit : « prélèvement rejeté par la banque, puis annulé ».",
  punch="211 993 €", src="Midi Libre, repris par Selectra (07/11/2025, mis à jour le 14/01/2026)")
p("ecran_partage", "Elle a raconté à Midi Libre : « J'ai hurlé et même vomi. »",
  "À gauche : " + PX("hands covering face paper bill", "woman hands paper bill close up", "crumpled paper bill hand") + " (mains seulement, jamais un visage de banque d'images qu'on prendrait pour elle). À droite (Vitre) : la citation + « une cliente de l'Hérault, Midi Libre via Selectra, 07/11/2025 » ; en petit dessous : « 1 556 kWh enregistrés comme 1 001 556 kWh ».",
  src="Midi Libre, via Selectra (07/11/2025)")
p("schema", "Si ça t'arrive : fais d'abord une réclamation écrite à ton fournisseur.",
  "Schéma `processus` (fond : rush flouté « pen writing letter desk ») : « 1. Réclamation écrite → 2. ? → 3. Médiateur » ; étape 1 allumée, la durée de l'étape 2 reste « ? ».")
p("rush", "Réponse : pas de solution deux mois après ta réclamation ? Tu saisis le médiateur, gratuitement.",
  PX("laptop online form typing", "person filling form laptop", "hands typing keyboard home") + ". Étapes 2 et 3 en surimpression, « GRATUIT » en orange.",
  punch="2 MOIS", sil=True, tag="RÉPONSE D3 bis", src="energie-info.fr, « J'ai une réclamation… », consulté le 17/11/2026")
p("mosaique", "Notre couple, lui, a attendu un an avant d'appeler une association, l'Adéic.",
  "Mosaïque : capture JDN (paragraphe « mai 2025 », recadré), pile de courriers, téléphone. Surtitre « Mai 2025 ».",
  tag="COUPLE (milieu)")
p("rush", "Cette association a une adresse directe chez leur fournisseur.",
  PX("email inbox laptop screen", "sending email laptop", "office desk letters") + ".")
p("ecran_partage", "Son juriste le dit : « Ça change tout : ils nous répondent et font attention. »",
  "À gauche : capture `cap11d_jdn_ca_change_tout.png` (phrase surlignée). À droite (Vitre) : la citation + « Matthieu Bertrand Neuser, juriste de l'Adéic (Journal du Net) ». Ne jamais l'attribuer au couple.",
  src="Journal du Net, 15/05/2026")
p("rush", "Le réflexe : compare l'index de ton compteur avec celui écrit sur ta facture.",
  "`medias/omar-linky.mp4` puis la facture d'Omar (ligne « index ») ; annotation qui relie les deux. Étiquette « RÉFLEXE n°4 ».", tag="UTILITÉ")
p("mosaique", "Eux, au moins, ont vu leur facture. D'autres reçoivent juste un courrier qu'ils ne lisent pas.",
  "Mosaïque : pile d'enveloppes non ouvertes, e-mail non lu sur téléphone, poubelle à papier.", tag="RH + BOUCLE couple (dénouement à la fin)")

# ---------------------------------------------------------------- CH 5  À ÉVITER 3
p("titre", "", "Carte « À ÉVITER · 3 » : « Offre électricité −20 % : où est le piège ? », sur rush flouté d'un courrier.",
  ch=("À éviter n°3", "Offre électricité −20 % : où est le piège ?"))
p("rush", "Piège numéro trois : la remise de moins vingt pour cent, qui bascule en silence.",
  "`medias/omar-courrier.mp4`, lettre dépliée. Sinon " + PX("reading letter close up", "unfolding letter hands", "letter on table") + ". Gros « −20 % » posé sur la lettre.", punch="−20 %")
p("ecran_partage", "Un fournisseur vient d'écrire à ses clients, et le site Je Change a publié les chiffres.",
  "À gauche : capture `cap12_jechange.png` recadrée sur le titre + « mis à jour le 11/11/2026 », nom du fournisseur hors cadre si possible, et le « 42 % » du titre MASQUÉ (cache opaque) jusqu'à la réponse de la devinette n°4. Ne pas montrer la grille datée du 01/02/2027. À droite : « Courrier rapporté par la presse ».",
  src="JeChange, mis à jour le 11/11/2026")
p("rush", "Leur offre à moins vingt pour cent s'arrête le trente et un décembre.",
  PX("calendar december 31", "new year calendar page", "calendar last day of year") + ". Surtitre « 31/12/2026 ».")
p("schema", "Le kilowattheure hors taxes passe de onze centimes quarante, à dix-sept centimes quarante-sept.",
  "Schéma `comparaison` : « 0,1140 € HT » contre « 0,1747 € HT » (héros), puis « +53 % ». Fond : capture JeChange floutée.",
  punch="+53 %", src="JeChange, 11/11/2026")
p("mosaique", "Et l'abonnement, lui, prend près de cinquante pour cent.",
  "Mosaïque : ligne « abonnement » de la facture d'Omar, prise électrique française (type E), compteur. Étiquette « ABONNEMENT ≈ +50 % ».")
p("ecran_partage", "Quatrième devinette : pour un client, au total, sa facture prend combien ?",
  "À gauche : la lettre (rush). À droite (Vitre) : « Facture annuelle : + ? % ».")
p("rush", "Plus douze, plus vingt-cinq, ou plus quarante-deux pour cent ?",
  "La lettre en plein écran ; trois GROS chiffres posés dessus : « +12 % » · « +25 % » · « +42 % ». Aucune case allumée. Compte à rebours 3 s.",
  cd=True, tag="D4 (réponse p093)")
p("schema", "Et cette remise n'a jamais valu moins vingt pour cent sur ta facture.",
  "Schéma `decomposition` : barre de la facture type ; seule la case « kWh hors taxes » est éclairée sous l'étiquette « −20 % ». Abonnement, accise, T V A grisés.")
p("rush", "Elle ne touchait que le kilowattheure hors taxes. Pas l'abonnement, pas les taxes.",
  "Facture d'Omar : les lignes « abonnement » et « taxes » barrées d'un trait orange, l'une après l'autre.")
p("schema", "Sur une facture type, ça fait environ moins quatorze pour cent, pas moins vingt.",
  "Schéma `comparaison` : « −20 % sur une ligne » contre « ≈ −14 % sur la facture » (héros). Source : « calcul Le Vrai Prix : remise sur le seul kWh HT, tarif bleu Base 6 kVA, 4 500 kWh/an ».",
  punch="≈ −14 %", src="calcul Le Vrai Prix")
p("rush", "Et le plus fort : sans réponse de ta part, le silence vaut acceptation.",
  "La lettre, gros plan ; surlignage animé d'une ligne ; mot « SILENCE » en orange.")
p("ecran_partage", "Si tu ne fais rien, le nouveau prix s'applique. Réponse : plus quarante-deux pour cent.",
  "À gauche : capture `cap12_jechange.png`, le cache saute sur « +42 % » et sur « le silence vaut acceptation » (surligneur). À droite : gros « +42 % » avec impact ; la case « +42 % » de la devinette s'allume. Mention « pour le client dont le courrier circule ».",
  punch="+42 %", sil=True, tag="RÉPONSE D4", src="JeChange, 11/11/2026")
p("rush", "C'est légal : le fournisseur doit juste te prévenir au moins un mois avant.",
  PX("smartphone email inbox close up", "checking emails phone", "spam folder email phone") + ".", src="energie-info.fr, consulté le 17/11/2026")
p("mosaique", "Le réflexe : cherche la date de fin de ton prix, et fouille tes spams.",
  "Mosaïque : capture `cap13_energieinfo_messages.png`, facture d'Omar (ligne « date de fin »), téléphone dossier « Spam ». Étiquette « RÉFLEXE n°3 ».", tag="UTILITÉ")
p("rush", "Tu peux partir à tout moment, sans frais. Mais ça, c'est un prix fixe qui s'arrête.",
  "Capture `cap13_energieinfo_messages.png` plein écran, surligneur sur « vous pouvez changer de fournisseur à tout moment et sans frais ».",
  src="energie-info.fr, consulté le 17/11/2026")
p("ecran_partage", "Il y a pire : un prix qui ne s'arrête jamais de bouger.",
  "À gauche : rush d'écran de cotation qui zigzague. À droite : courbe qui monte et descend sans arrêt.", tag="RH")

# ---------------------------------------------------------------- CH 6  À ÉVITER 2
p("titre", "", "Carte « À ÉVITER · 2 » : « Prix fixe ou indexé : que choisir ? », sur rush flouté d'un écran de cotation.",
  ch=("À éviter n°2", "Prix fixe ou indexé : que choisir ?"))
p("rush", "Piège numéro deux : l'offre indexée sur le marché, ou dynamique, en plein hiver.",
  "`medias/omar-tableau.mp4` (tableau électrique d'Omar). Sinon " + PX("electrical panel home breakers", "fuse box house", "circuit breaker panel close up") + ".")
p("ecran_partage", "Avec une offre dynamique, le prix change tous les jours, et même toutes les heures.",
  "À gauche : capture `cap14_energieinfo_dynamiques.png`, surligneur sur « le prix de l'énergie fluctue tous les jours et toutes les heures ». À droite : horloge 24 h dont chaque heure change de couleur.",
  src="energie-info.fr, consulté le 17/11/2026")
p("rush", "Devinette : début novembre, marché et taxes seuls, le kilowattheure coûtait vingt-cinq, trente-six, ou cinquante centimes ?",
  "`medias/omar-chargeur.mp4` (chargeur sur une prise française) ; trois GROS chiffres posés à côté de la prise : « 25 c » · « 36 c » · « 50 c ». Aucune case allumée. Compte à rebours 3 s.",
  cd=True, tag="D4 bis (réponse p000)")
p("mosaique", "Indice : le plus cher, c'est en hiver, le soir, quand tout le monde consomme.",
  "Mosaïque : " + PX("city apartment windows lit at night winter", "kitchen cooking evening stove", "living room lights evening winter") + ".",
  src="energie-info.fr, offres dynamiques")
p("schema", "Réponse : trente-six centimes, sans même compter le réseau ni l'abonnement.",
  "Schéma `comparaison` : « Marché + taxes, sans réseau ni abonnement : 0,36 € » (héros) contre « Tarif bleu, réseau compris : 0,20 € ». Source : « calcul Selectra, 1er au 10 novembre 2026 ».",
  punch="36 c", sil=True, tag="RÉPONSE D4 bis", src="calcul Selectra, 11/11/2026")
p("rush", "Le tarif bleu, lui, réseau compris : vingt centimes.",
  "`medias/omar-bouilloire.mp4` (bouilloire qui chauffe). Sinon " + PX("electric kettle boiling kitchen", "plug in wall socket europe", "kettle steam close up") + ".")
p("ecran_partage", "La C R E et les fournisseurs ont créé une note, de A à D.",
  "À gauche : capture `cap03_cre_niveau_certitude.png` (les 4 pastilles A vert foncé → D jaune). À droite : étiquette « Niveau de certitude ».",
  src="CRE, fiche « Niveau de certitude »")
p("schema", "A, le prix est entièrement fixe et garanti. D, il dépend de facteurs extérieurs.",
  "Schéma `liste` aux couleurs CRE : A (vert foncé) « prix entièrement fixe garanti » · B · C · D (jaune, héros) « soumis à des facteurs externes ». Rien n'indique quelle lettre prendre.",
  src="CRE, fiche « Niveau de certitude »")
p("rush", "Pour la C R E, ce dernier niveau peut évoluer de façon aléatoire ou imprévisible.",
  "Contrat papier d'Omar (ou " + PX("contract document pen", "signing contract close up", "paper contract desk") + ") ; pastille « D » jaune posée sur la page (Annotation).",
  punch="IMPRÉVISIBLE", src="CRE, Lignes directrices, annexe 3 (niveau 4, l'équivalent de D)")
p("mosaique", "Le réflexe : cherche la lettre sur ton contrat. Si elle manque, demande-la.",
  "Mosaïque : main d'Omar qui feuillette son contrat (données floutées), loupe animée qui cherche la pastille, courrier de renouvellement. Étiquette « RÉFLEXE n°2 ».",
  tag="UTILITÉ", src="CRE, délibération 2026-110")
p("rush", "Garde ces quatre lettres en tête : l'une d'elles va revenir, tout à la fin.",
  "Capture `cap03_cre_niveau_certitude.png` plein écran, autre recadrage ; les 4 pastilles pulsent une à une, aucune mise en valeur.", tag="BOUCLE (lettre A au n°1)")
p("mosaique", "Et le pire piège ? C'est celui que tu as peut-être déjà, au fond d'un tiroir.",
  "Mosaïque : " + PX("opening drawer papers", "old documents in drawer", "file folder documents home") + ".", tag="RH")

# ---------------------------------------------------------------- CH 7  À ÉVITER 1
p("titre", "", "Carte « À ÉVITER · 1 » : « Est-ce que je paie mon électricité trop cher ? », sur rush flouté du tiroir.",
  ch=("À éviter n°1", "Est-ce que je paie mon électricité trop cher ?"))
p("rush", "Piège numéro un : le vieux contrat que tu n'as jamais comparé.",
  PX("old contract paper folder", "dusty documents box", "binder papers shelf") + ".")
p("ecran_partage", "En juin, la C R E a passé au crible les prix des offres de marché.",
  "À gauche : capture `cap07a_cre_coherence_titre.png` (autre recadrage : sommaire / date 03/06/2026). À droite : « Prix analysés au 1er décembre 2025 ».",
  src="CRE, rapport Cohérence des offres, 03/06/2026")
p("mosaique", "Cinquième devinette : combien de foyers payaient un prix fixe plus de cinq pour cent",
  "Mosaïque : " + PX("apartment building windows night", "french houses street evening", "residential building lights") + ".")
p("rush", "au-dessus du tarif bleu ? Cent mille, près de deux millions, ou cinq millions ?",
  "Immeuble aux fenêtres éclairées, plein écran ; trois GROS chiffres posés dessus : « 100 000 » · « 1,9 MILLION » · « 5 MILLIONS ». Aucune case allumée. Compte à rebours 3 s.",
  cd=True, tag="D5 (réponse p121)")
p("ecran_partage", "Pour le un pour cent des contrats les plus chers, la C R E calcule",
  "À gauche : capture `cap07b_cre_coherence_591.png`, surligneur sur « au moins 591 €/an HT pour les offres à prix fixe d'électricité ». À droite : « ? € » qui attend.",
  src="CRE, rapport Cohérence des offres, 03/06/2026")
p("schema", "au moins cinq cent quatre-vingt-onze euros d'économie par an, hors taxes.",
  "Schéma `chiffre` : « 591 €/an HT », légende « économie possible pour le 1 % des contrats les plus chers », pas de comparaison chiffrée (aucune n'est vérifiée), on rappelle seulement la pastille de la miniature. Fond : rush flouté de la facture.",
  punch="591 €", tag="promesse miniature tenue", src="CRE, 03/06/2026")
p("rush", "Et presque toutes ces offres chères ont un point commun : elles sont vertes.",
  PX("wind turbines green field", "solar panels roof", "green energy wind farm") + ". Étiquette « OFFRE VERTE » posée en biais.",
  src="CRE, 03/06/2026 (91 % des contrats au-delà de +5 %)")
p("schema", "Réponse : selon la C R E, un million neuf cent mille foyers, fin deux mille vingt-cinq.",
  "Schéma `chiffre` : « 1,9 million », légende « foyers en prix fixe à plus de 5 % au-dessus du tarif bleu », source « CRE, prix au 1er décembre 2025 ». La case « 1,9 MILLION » s'allume.",
  punch="1,9 MILLION", sil=True, tag="RÉPONSE D5", src="CRE, rapport Cohérence des offres, 03/06/2026")
p("ecran_partage", "En juin, sa présidente Emmanuelle Wargon annonçait vouloir contacter les fournisseurs de ces offres très onéreuses.",
  "À gauche : capture `cap08_ufc_wargon.png` (titre + date 18/06/2026). À droite (Vitre) : la citation entière « Nous allons prendre contact avec les quelques fournisseurs qui maintiennent ces offres à prix fixe très onéreuses pour leur demander des explications » + « Emmanuelle Wargon, présidente de la CRE, via UFC-Que Choisir, 18/06/2026 ».",
  src="UFC-Que Choisir, 18/06/2026")
p("mosaique", "Le réflexe : compare ton prix du kilowattheure et ton abonnement à ceux du tarif bleu.",
  "Mosaïque : ligne « prix du kWh » de la facture d'Omar, ligne « abonnement », capture `cap04_cre_annexeB.png` (ligne Base 6 kVA). Étiquette « RÉFLEXE n°1 ».", tag="UTILITÉ")
p("rush", "Voilà pour les pièges. Maintenant, ce qu'il faut prendre, en commençant par le numéro trois.",
  "`medias/omar-interrupteur.mp4` (main qui rallume la lumière). Sinon " + PX("hand turning on light switch", "lamp turning on evening", "light bulb switching on") + ".", tag="RH")

# ---------------------------------------------------------------- CH 8  À PRENDRE 3
p("titre", "", "Carte verte « À PRENDRE · 3 » : « Heures creuses ou Tempo : ça vaut le coup ? », sur rush flouté d'une machine à laver.",
  ch=("À prendre n°3", "Heures creuses ou Tempo : ça vaut le coup ?"))
p("rush", "Numéro trois : les heures creuses, ou Tempo. Seulement si tu peux décaler ta consommation.",
  PX("washing machine start button night", "loading washing machine", "washing machine running") + ".")
p("ecran_partage", "Tu as huit heures creuses par jour, la plupart la nuit.",
  "À gauche : " + PX("water heater tank home", "boiler cylinder house", "hot water tank basement") + ". À droite : horloge 24 h, 8 cases « creuses » surtout la nuit.",
  src="CRE, délibération 2026-147, annexe B")
p("rush", "Et l'été, une partie peut passer en milieu de journée.",
  PX("summer afternoon sun house", "solar panels roof sunny day", "sunny garden afternoon") + ".", src="Enedis via Selectra, 20/07/2026")
p("schema", "Selon le médiateur, quinze pour cent des foyers en heures creuses ignorent leurs horaires.",
  "Schéma `chiffre` : « 15 % », légende « des foyers en heures creuses ne connaissent pas leurs horaires ». Fond : capture `cap15_barometre_2026.png` floutée.",
  punch="15 %", src="baromètre énergie-info 2026, 03/11/2026")
p("rush", "Le réflexe : vérifie tes horaires, puis lance machine et ballon dedans.",
  "Facture d'Omar, ligne « heures creuses » entourée, puis `medias/omar-tableau.mp4` (contacteur heures creuses). Étiquette « RÉFLEXE ».", tag="UTILITÉ")
p("mosaique", "Tempo, c'est plus radical : trois cents jours bleus pas chers, et vingt-deux jours rouges.",
  "Mosaïque : calendrier avec jours colorés, radiateur, ciel d'hiver. Surtitre « 300 bleus · 43 blancs · 22 rouges ».",
  src="CRE, délibération 2026-147")
p("rush", "Devinette : un jour rouge, en heures pleines, le kilowattheure coûte trente, cinquante, ou soixante-treize centimes ?",
  "`medias/omar-radiateur.mp4`, autre prise (radiateur allumé le soir) ; trois GROS chiffres posés dessus : « 30 c » · « 50 c » · « 73 c ». Aucune case allumée. Compte à rebours 3 s.",
  cd=True, tag="D5 bis (réponse p000)")
p("ecran_partage", "Ils tombent de novembre à mars, jamais le week-end, et tu le sais la veille.",
  "À gauche : " + PX("winter morning frost window", "snowy street france", "cold winter day house") + ". À droite : calendrier de novembre à mars, quelques jours rouges en semaine.",
  src="Selectra (règles Tempo)")
p("schema", "Réponse : soixante-treize centimes. Plus de trois fois et demie le tarif de base.",
  "Schéma `comparaison` : « Jour rouge, heures pleines : 0,73 € » (héros rouge) contre « Tarif bleu Base : 0,20 € » ; la case « 73 c » s'allume.",
  punch="73 c", sil=True, tag="RÉPONSE D5 bis", src="CRE, délibération 2026-147, annexe B (57,73 c HT)")
p("rush", "Si tu chauffes à l'électricité et que tu ne peux pas décaler, méfie-toi.",
  "`medias/omar-radiateur.mp4` (main qui baisse le thermostat). Sinon " + PX("hand turning radiator thermostat", "electric heater knob", "radiator valve close up") + ".")
p("mosaique", "Il y a plus simple : un tarif que dix-neuf millions de foyers ont déjà.",
  "Mosaïque : " + PX("aerial view french town houses", "village rooftops france", "city rooftops aerial") + ".", tag="RH", src="CRE, observatoire T2 2026")

# ---------------------------------------------------------------- CH 9  À PRENDRE 2
p("titre", "", "Carte verte « À PRENDRE · 2 » : « Tarif bleu 2027 : faut-il le garder ? », sur rush flouté de la facture.",
  ch=("À prendre n°2", "Tarif bleu 2027 : faut-il le garder ?"))
p("rush", "Numéro deux : le tarif bleu, le tarif réglementé, fixé sur proposition de la C R E.",
  "Capture `cap04_cre_annexeB.png` plein écran, travelling sur la ligne « Base résidentiel 13,61 c€/kWh HT » ; annotation « = 20 c TTC ».",
  src="CRE, délibération 2026-147, annexe B")
p("ecran_partage", "Au premier août, il a pris deux virgule cinq pour cent, environ vingt-six euros par an.",
  "À gauche : capture `cap05_afp_facture_moyenne.png`, surligneur sur « une facture moyenne passant de 1 046 à 1 072 euros TTC par an ». À droite : « +26 €/an ».",
  src="AFP / Connaissance des énergies, 16/07/2026")
p("schema", "Fin juin, selon la C R E, la moitié des offres étaient moins chères que lui.",
  "Schéma `chiffre` : « 52 % », légende « des offres moins chères que le tarif bleu, fin juin 2026 ». Fond : rush flouté.",
  punch="52 %", src="CRE, observatoire T2 2026 (via Kelwatt, 05/10/2026)")
p("rush", "Mais depuis la flambée, d'après Selectra, quinze offres ont augmenté en un mois.",
  PX("smartphone price comparison", "person comparing prices phone", "phone screen scrolling list") + ".", src="Selectra, 10/11/2026")
p("ecran_partage", "Sixième devinette : sur le comparateur Selectra, début novembre, combien d'offres fixes battaient le tarif bleu ?",
  "À gauche : rush du téléphone. À droite (Vitre) : « Offres à prix fixe moins chères que le tarif bleu : ? sur 29 » + « comparateur Selectra, relevé du 9 novembre 2026 ».")
p("rush", "Trois sur vingt-neuf, huit sur vingt-neuf, ou vingt sur vingt-neuf ?",
  "Téléphone en plein écran ; trois GROS chiffres posés dessus : « 3/29 » · « 8/29 » · « 20/29 ». Aucune case allumée. Compte à rebours 3 s.",
  cd=True, tag="D6 (réponse p150)")

# ---------------------------------------------------------------- CH 10  À PRENDRE 1
p("titre", "", "Carte verte « À PRENDRE · 1 » : « Changer de fournisseur d'électricité : la bonne offre », la case reste « ? ».",
  ch=("À prendre n°1", "Changer de fournisseur d'électricité : la bonne offre"))
p("rush", "D'abord, notre couple des Yvelines. Leur histoire se termine en février deux mille vingt-six.",
  "`medias/omar-enveloppe.mp4`, autre prise (enveloppe qu'on referme). Surtitre « Février 2026 ».", tag="DÉNOUEMENT couple")
p("ecran_partage", "Leur relevé contesté est annulé, et environ sept cents kilowattheures sont corrigés.",
  "À gauche : capture JDN (paragraphe du dénouement). À droite : schéma `processus` « Relevé annulé → ≈ 700 kWh corrigés → geste de 300 € ».",
  src="Journal du Net, 15/05/2026")
p("rush", "Leur fournisseur ajoute un geste exceptionnel de trois cents euros.",
  PX("hands holding paper document", "reading letter relief", "paper letter close up") + ".")
p("schema", "Au final, la facture ne fait plus quatre mille euros, mais trois mille.",
  "Schéma `comparaison` : « 4 000 € » barré contre « 3 000 € » (héros). PIC émotionnel : musique qui se relâche.",
  punch="3 000 €", tag="FIN BOUCLE couple", src="Journal du Net, 15/05/2026")
p("rush", "À payer en trente mensualités d'environ cent euros.",
  PX("calendar months marking", "monthly calendar pages", "paying bills at desk") + ".")
p("mosaique", "Et ils ont fait deux choses : changer de compteur, et changer de fournisseur.",
  "Mosaïque : Linky neuf (`medias/omar-linky.mp4`, autre plan), contrat signé, main qui serre un stylo.")
p("rush", "Mais pour aller où ? C'est exactement notre numéro un.",
  "Capture `cap01_comparateur_resultat.png`, page d'accueil du comparateur officiel (travelling lent).", tag="RH")
p("schema", "Avant ça, la devinette : huit offres à prix fixe sur vingt-neuf, d'après un relevé de Selectra.",
  "Schéma `chiffre` : « 8 sur 29 », source « relevé Selectra, 9 novembre 2026, Base 6 kVA, 4 500 kWh/an ». La case « 8/29 » s'allume. (Si le comparateur officiel a été relevé à la capture : remplacer par son chiffre, voix ET écran, et le noter dans `sources.md`.)",
  punch="8 SUR 29", tag="RÉPONSE D6", src="relevé Selectra, 09/11/2026")
p("rush", "Pour les trouver, il y a le comparateur officiel du médiateur : énergie-info point F R.",
  "Capture `cap01_comparateur_resultat.png`, saisie « Base 6 kVA, 4 500 kWh » (sans nom de fournisseur lisible).",
  src="comparateur.energie-info.fr")
p("ecran_partage", "Un outil public, gratuit, neutre et indépendant. Et il affiche la fameuse lettre.",
  "À gauche : capture `cap02_energieinfo_nouveautes.png`, surligneur sur « un outil public, gratuit, neutre et indépendant ». À droite : les 4 pastilles A-D, aucune mise en valeur.",
  src="energie-info.fr, consulté le 17/11/2026")
p("rush", "Changer prend une quinzaine de minutes, avec ton numéro de point de livraison à quatorze chiffres.",
  "Facture d'Omar : la ligne « PDL » entourée, le numéro FLOUTÉ ; chrono « 15 min » en surimpression.",
  src="UFC-Que Choisir, 24/09/2026")
p("mosaique", "Aucun frais, et le courant ne s'arrête pas : c'est le même réseau.",
  "Mosaïque : ampoule allumée, Linky, ligne électrique. Étiquette « 0 € · 0 COUPURE ».")
p("rush", "Alors, cet hiver, quelle offre te protège vraiment ?",
  "Retour sur l'IMAGE DE LA MINIATURE (facture + Linky d'Omar). Riser, puis musique coupée net 0,5 s.", tag="la grande question revient")
p("schema", "Le numéro un : une offre à prix fixe classée A, kilowattheure et abonnement bloqués.",
  "PLUS BEAU MOMENT VISUEL. Tableau du classement (`liste`, celui de l'annonce du classement) : la case verte n°1 « ? » éclate, la pastille A vert foncé de la CRE (découpée dans `cap03_cre_niveau_certitude.png`) surgit avec impact et zoom punch.",
  punch="A", sil=True, tag="RÉPONSE PRINCIPALE", src="CRE, fiche « Niveau de certitude »")
p("ecran_partage", "Moins chère que le tarif bleu sur le comparateur officiel,",
  "À gauche : capture `cap01_comparateur_resultat.png`, résultat avec la lettre A d'une offre (nom illisible). À droite : critère 2 qui s'ajoute sous le A : « < tarif bleu (comparateur officiel) ».",
  src="comparateur.energie-info.fr")
p("rush", "chez un fournisseur qui a les quatre étoiles du médiateur : le moins de litiges.",
  "Capture `cap16_energieinfo_etoiles.png`, légende des étoiles « ≤ 25 saisines pour 100 000 contrats » (sans le tableau des noms) ; 4 étoiles qui s'allument.",
  src="energie-info.fr, Qualité de service clients")
p("schema", "Aucune ? Tu restes au tarif bleu. Cet hiver, la stabilité vaut plus que la remise.",
  "Tableau final : n°1 = « Prix fixe A + moins cher + 4 étoiles », sous-ligne « Aucune ? → tarif bleu » (héros). Récap des 5 pièges grisés à gauche.",
  punch="TARIF BLEU")

# ---------------------------------------------------------------- FIN
sec("11 — Fin (≤ 20 s après la réponse)", "Chapitre YouTube « Ton contrat finit quand ? ».")
p("mosaique", "Et toi, ton prix fixe, il se termine quand ? Dis-le en commentaire.",
  "Mosaïque : facture (ligne « date de fin »), téléphone, pastilles A-D. Grosse question à l'écran.", tag="QUESTION OUVERTE")
p("rush", "Mardi premier décembre : les jouets de Noël, et ce qu'ils coûtent vraiment à fabriquer.",
  PX("christmas toys under tree", "wrapped gifts christmas tree", "toy shop christmas") + ".", tag="VIDÉO SUIVANTE")
p("ecran_partage", "Abonne-toi pour ne pas la rater.",
  "Écran de fin : vidéo « la plus adaptée au spectateur » (Black Friday) + playlist « Le Vrai Prix — les enquêtes » + bouton d'abonnement. 20 s d'écran de fin dans Studio.",
  tag="ABONNEMENT (seule fois)")

# ====================================================================== calcul
def words(t):
    return [w for w in t.split() if re.search(r"\w", w)]

t = 0.0
num = 0
rows = []
for it in P:
    if "section" in it:
        rows.append(it); continue
    num += 1
    it["id"] = f"p{num:03d}"
    n = len(words(it["txt"]))
    it["n"] = n
    if it["fmt"] == "titre":
        d = 2.8
    else:
        d = n / 2.5 + 0.15
    if it.get("sil"): t += 0.5
    it["t"] = t
    it["d"] = d
    t += d
    if it.get("cd"): t += 3.0
    rows.append(it)
TOTAL = t

plans = [r for r in rows if "id" in r]
# remplace les références « pNNN » écrites à la main par les vrais numéros
def find(tagstart):
    for r in plans:
        if r.get("tag", "").startswith(tagstart): return r["id"]
refs = {}
for r in plans:
    m0 = re.match(r"RÉPONSE (D\d( bis)?)$", r.get("tag", ""))
    if m0: refs[m0.group(1)] = r["id"]
# D1 bis = plan juste après la devinette taxes
for i, r in enumerate(plans):
    if r.get("tag", "").startswith("D1 bis"): refs["D1 bis"] = plans[i + 1]["id"]
    if r.get("tag", "").startswith("RÉPONSE D1 bis"): pass
for r in plans:
    tg = r.get("tag", "")
    m = re.match(r"(D\d( bis)?) \(réponse p\d+\)", tg)
    if m: r["tag"] = f"{m.group(1)} (réponse {refs[m.group(1)]})"
    if tg.startswith("BOUCLE couple (fermée"):
        r["tag"] = "BOUCLE couple (fermée " + find("FIN BOUCLE") + ")"

def mmss(x):
    x = int(round(x)); return f"{x//60}:{x%60:02d}"

# contrôles
errs = []
prev = None
for r in plans:
    if r["fmt"] != "titre" and r["n"] < 4: errs.append(f"{r['id']} moins de 4 mots")
    if r["n"] > 16: errs.append(f"{r['id']} {r['n']} mots (> 16) : {r['txt']}")
    if r["t"] < 60 and r["fmt"] != "titre" and r["d"] > 4.4: errs.append(f"{r['id']} {r['d']:.1f} s dans la 1re minute")
    if prev and prev["fmt"] == r["fmt"] and r["t"] >= 30: errs.append(f"{prev['id']}→{r['id']} même format {r['fmt']} à {mmss(r['t'])}")
    if r["t"] < 30 and r["fmt"] in ("schema", "titre"): errs.append(f"{r['id']} {r['fmt']} avant 30 s")
    prev = r
narr_words = sum(r["n"] for r in plans)
print("mots", narr_words, "plans", len(plans), "durée", mmss(TOTAL), "voix seule", mmss(narr_words / 2.5))
rev = find("RÉPONSE PRINCIPALE")
rv = [r for r in plans if r["id"] == rev][0]
print("révélation", rev, mmss(rv["t"]), f"{rv['t']/TOTAL*100:.1f} %", "fin après révélation", f"{TOTAL-rv['t']:.1f} s")
for r in plans:
    if r.get("tag"): print(r["id"], mmss(r["t"]), r["tag"])
print("\n".join(errs) if errs else "aucune erreur")

import json
json.dump({"rows": rows, "total": TOTAL, "words": narr_words}, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
