# -*- coding: utf-8 -*-
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
rows, TOTAL, W = d["rows"], d["total"], d["words"]
plans = [r for r in rows if "id" in r]
def mmss(x):
    x = int(round(x)); return f"{x//60}:{x%60:02d}"
def find(tag):
    for r in plans:
        if r.get("tag", "") == tag: return r

rev = find("RÉPONSE PRINCIPALE")
nb_cd = sum(1 for r in plans if r.get("cd"))
nb_cartes = sum(1 for r in plans if r["fmt"] == "titre")
out = []
A = out.append
A(f"Mots : {W}")
A("")
A("# Offre électricité moins chère 2026 : 5 pièges à éviter")
A("")
A(f"> Durée estimée : voix seule ≈ {mmss(W/2.5)} ({W} mots à 150 mots/min) ; vidéo ≈ {mmss(TOTAL)} avec {nb_cd} comptes à rebours de 3 s, "
  f"{nb_cartes} cartes de 2,8 s, respirations et silences. | Ton : copain qui a lu les rapports à ta place, factuel, jamais militant.")
A("> Écrit le 17/11/2026 (run automatique) à partir de `01_strategist_brief.md`, `01b_recherche.md` (VERT et formulations sûres des ORANGE uniquement, aucun ROUGE),")
A("> `00_lecons_analytics.md` et des règles 1, 6, 7 bis, 7 ter, 9, 11, 16-5, 20 de `monteur-chaine`.")
A("> Voix : Edge Vivienne lue d'un seul souffle (transitions `coupe` dans un même chapitre). Accroche p001-p017 par Omar si `episodes/electricite/voix/accroche.m4a` existe.")
A("> Nombres, sigles et dates écrits comme ils se prononcent. Aucun fournisseur nommé à la voix. Médias d'Omar : `episodes/electricite/medias/omar-*.mp4`, prioritaires, données personnelles floutées.")
A("")
A("## À lire avant le montage (contrôles bloquants)")
A("")
A("1. **0:00-0:30 : images réelles plein écran uniquement** (plans d'Omar, rushes, captures de documents). Aucun schéma, aucune carte titre, aucune annonce de plan, aucun panneau sombre. Devinette n°1 = 3 gros chiffres posés sur la facture.")
A("2. **Aucune réponse avant sa révélation** : ni « ≈ 40 € », ni « ≈ 30 € », ni « ×4 », ni « nul », ni « 2 mois », ni « +42 % », ni « 36 c », ni « 1,9 million », ni « 73 c », ni « 8 sur 29 », ni la lettre « A » comme conclusion. "
  "La case verte n°1 du classement reste « ? » jusqu'à " + rev["id"] + ". Le « 42 % » du titre de l'article JeChange est masqué jusqu'à la réponse de la devinette n°4.")
A("3. **Devinettes (règle 20)** : la voix lit les 3 choix, compte à rebours de 3 s APRÈS la question, aucune case allumée par défaut ; la bonne case s'allume seulement au plan « RÉPONSE ». Regarder l'image de fin de chaque plan devinette.")
A("4. **Jamais deux plans consécutifs du même format** (vérifié par script sur les 159 plans ; seule l'accroche enchaîne des `rush`). Aucune séquence de plus de 6 s sans changement d'image : les plans de plus de 5 s ont une couche qui bouge (surligneur, annotation, élément de schéma qui s'ajoute).")
A("5. **Citations** : toutes celles du Journal du Net sont de **Matthieu Bertrand Neuser, juriste de l'Adéic**, jamais du couple. Bandeau à chaque fois. « J'ai hurlé et même vomi » = une cliente de l'Hérault, Midi Libre via Selectra (07/11/2025). Emmanuelle Wargon via UFC-Que Choisir (18/06/2026).")
A("6. **Noms de fournisseurs** : JDN, JeChange et une page energie-info en citent un : recadrer hors nom (titre + date + phrase seulement). Le tableau des étoiles du médiateur n'est jamais montré, seulement sa légende.")
A("7. **Objets français** : compteur Linky jaune-vert, prises type E, pylônes européens, euros. Aucun compteur, panneau ou billet américain.")
A("8. Sources à l'écran en 24 px minimum sur chaque chiffre (ligne « Source » de chaque plan).")
A("")
A("Légende : chaque plan = numéro · format · début estimé · durée · nombre de mots. « Image » = ce qu'on voit (capture, plan d'Omar, requêtes Pixabay en anglais, ou schéma avec ses valeurs). « Punch » = le seul mot ou chiffre zoomé du plan.")
A("")
A("---")
for r in rows:
    if "section" in r:
        A(""); A(f"## {r['section']}");
        if r.get("note"): A(""); A(f"> {r['note']}")
        continue
    if r["fmt"] == "titre":
        num, titre = r["ch"]
        A(""); A("---"); A("")
        A(f"## {num} — {titre} ({mmss(r['t'])})")
        A("")
        A(f"**{r['id']}** · `titre` · {mmss(r['t'])} · 2,8 s · sans voix")
        A(f"- Image : {r['img']}")
        A(f"- Format : carte titre (`numero` « {num} », `titre` « {titre} »), `duree_min` 2.8, son « impact » discret.")
        continue
    head = f"**{r['id']}** · `{r['fmt']}` · {mmss(r['t'])} · {r['d']:.1f} s · {r['n']} mots".replace('.', ',', 1) if False else f"**{r['id']}** · `{r['fmt']}` · {mmss(r['t'])} · {str(round(r['d'],1)).replace('.', ',')} s · {r['n']} mots"
    if r.get("cd"): head += " · + compte à rebours 3 s"
    if r.get("sil"): head += " · 0,5 s de silence avant (musique coupée)"
    A(""); A(head)
    A(f"> {r['txt']}")
    A(f"- Image : {r['img']}")
    if r.get("punch"): A(f"- Punch : « {r['punch']} »")
    if r.get("src"): A(f"- Source à l'écran : {r['src']}")
    if r.get("tag"): A(f"- Rétention : **{r['tag']}**")

# ------------------------------------------------------------------ récap
A(""); A("---"); A("")
A("## Récapitulatif rétention")
A("")
A("| Élément | Où |")
A("|---|---|")
g = find("GRANDE QUESTION (avant 8 s)")
A(f"| Image de la miniature (facture + Linky) à la frame 0 ; promesse « TU PAIES TROP ? » + « 591 € » dite et montrée avant 0:35 | p001, p009, p010 |")
A(f"| Grande question « Cet hiver, quelle offre te protège vraiment ? » | {g['id']}, {mmss(g['t'])} (finie vers 0:08) ; reposée en p152 juste avant la réponse |")
A(f"| Réponse principale (prix fixe classé A + moins cher que le tarif bleu sur le comparateur officiel + 4 étoiles du médiateur ; sinon tarif bleu) | {rev['id']}, {mmss(rev['t'])} sur ≈ {mmss(TOTAL)}, soit {rev['t']/TOTAL*100:.0f} % (≥ 85 %) ; fin ≈ 13 s après la dernière phrase de la réponse |")
dv = [r for r in plans if r.get("tag", "").startswith("D") and "réponse" in r.get("tag", "")]
A("| Devinettes à 3 choix (" + str(len(dv)) + ") | " + " · ".join(f"{r['tag'].split(' (')[0]} {mmss(r['t'])} → {r['tag'].split('réponse ')[1].rstrip(')')}" for r in dv) + " |")
gaps = [dv[i+1]["t"] - dv[i]["t"] for i in range(len(dv)-1)]
A(f"| Écart maximal entre deux devinettes | {max(gaps):.0f} s |")
rh = [r for r in plans if "RH" in r.get("tag", "")]
A("| Re-hooks (toutes les 60-90 s, avec les devinettes) | " + " · ".join(f"{r['id']} {mmss(r['t'])}" for r in rh) + " |")
cp = [r for r in plans if "couple" in r.get("tag", "").lower() or r.get("tag") == "VRAIE PERSONNE"]
A("| Vraie personne : le couple des Yvelines (JDN, 15/05/2026) | " + " · ".join(f"{r['id']} {mmss(r['t'])} ({r['tag']})" for r in cp) + " |")
A("| Boucles imbriquées | couple ouvert à 0:51, fermé en p143 ; lettre A annoncée en p106 (« l'une d'elles va revenir »), révélée en " + rev["id"] + " ; chaque chapitre se termine sur la question du suivant ; chaque devinette s'ouvre avant que la précédente soit oubliée |")
A("| Retournements (un par partie) | ch.01 : sur 100 €, le courant lui-même ne fait qu'une trentaine · ch.02 : les marchés ×4 mais ta facture non, le tarif bleu amortit · n°5 : le contrat est nul, mais la loi ne vise pas ta porte · n°4 : 4 000 € sur estimation, et le Linky qui déraille reste rare · n°3 : −20 % sur une ligne = ≈ −14 % sur la facture, puis +42 % · n°2 : rien que le marché et les taxes = 36 c contre 20 c · n°1 : 1,9 million de foyers, des offres « vertes » · n°1 à prendre : la meilleure offre est la plus stable, parfois celle que tu as déjà |")
A("| Utilité concrète (un réflexe par piège) | " + " · ".join(f"{r['id']}" for r in plans if r.get("tag") == "UTILITÉ") + " |")
A("| Carte titre | aucune avant 0:30 (1re carte en p018, " + mmss([r for r in plans if r['fmt']=='titre'][0]['t']) + ") ; annonce du classement une seule fois (p046, 3:21) |")
A("| Abonnement | une seule fois, dernière phrase (p159) |")
A("| Émotions | indignation juste (1,9 million de foyers, silence = acceptation, 4 000 € sur estimation), surprise (×4, 36 c, 73 c, 211 993 €), utilité (réflexes, médiateur gratuit, 15 minutes sans frais) |")
A("")
A("Minutage : 150 mots/min (2,5 mots/s) + 0,15 s de respiration par plan, comme demandé. **Attention** : Black Friday (1 315 mots) a donné 6 min 56 au rendu,")
A("soit ≈ 3,2 mots/s avec Edge à +8 %. À ce débit, ce script ferait ≈ 10 min 30 : régler `debit` / `debit_continu` à « +0% » pour viser 12 min, et remesurer les chapitres SUR LE RENDU FINAL (règle 14).")

# ------------------------------------------------------------------ captures
A(""); A("## Captures nécessaires (dossier `episodes/electricite/medias/captures/`)")
A("")
A("Recadrer sur la phrase, jamais une page entière ; 3 à 6 s ; date visible quand elle existe ; noms de fournisseurs hors cadre.")
A("")
A("| Fichier | URL | Ce qu'on voit | Élément mis en valeur | Plans |")
A("|---|---|---|---|---|")
caps = [
 ("cap01_comparateur_resultat.png", "https://comparateur.energie-info.fr/", "page d'accueil du comparateur officiel, puis un résultat Base 6 kVA, 4 500 kWh/an", "la lettre A-D d'une offre (nom illisible) ; relever le nombre d'offres à prix fixe sous le tarif bleu pour remplacer « 8 sur 29 » si possible", "p146, p148, p154"),
 ("cap02_energieinfo_nouveautes.png", "https://www.energie-info.fr/le-comparateur-du-mediateur-national-de-lenergie-evolue-decouvrez-ses-nouveautes/", "article du médiateur sur les nouveautés du comparateur", "« un outil public, gratuit, neutre et indépendant »", "p149"),
 ("cap03_cre_niveau_certitude.png", "https://cre.fr/fileadmin/Documents/Autres/Niveau_de_certitude.pdf", "fiche CRE, les 4 pastilles A (vert foncé) → D (jaune)", "les 4 pastilles, sans en privilégier une avant la réponse", "p102, p106, p153 (pastille A)"),
 ("cap04_cre_annexeB.png", "https://www.cre.fr/fileadmin/Documents/Deliberations/2026/260715_2026-147_TRVE_Annexe_B.pdf", "barème du tarif bleu au 01/08/2026", "ligne Base résidentiel 13,61 c€/kWh HT et ligne 6 kVA 143,28 €/an (annotation « = 20 c TTC »)", "p118, p133"),
 ("cap05_afp_facture_moyenne.png", "https://www.connaissancedesenergies.org/afp/electricite-le-gouvernement-suit-lavis-du-regulateur-cre-dune-hausse-de-25-des-tarifs-reglementes-260716", "dépêche AFP du 16/07/2026", "« une facture moyenne passant de 1 046 à 1 072 euros TTC par an »", "p134"),
 ("cap06_energieinfo_seule_composante.png", "https://www.energie-info.fr/fiche_pratique/prix-de-lelectricite-et-du-gaz-que-payons-nous/", "fiche « Prix de l'électricité et du gaz : que payons-nous ? »", "« Il s'agit de la seule composante soumise à la concurrence. »", "p027"),
 ("cap07a_cre_coherence_titre.png", "https://www.cre.fr/fileadmin/Documents/Rapports_et_etudes/2026/Rapport_Coherence_des_offres_2026.pdf", "couverture / sommaire du rapport Cohérence des offres (03/06/2026)", "titre + logo CRE + date", "p008, p111"),
 ("cap07b_cre_coherence_591.png", "même URL", "page du rapport sur les économies potentielles", "« au moins 591 €/an HT pour les offres à prix fixe d'électricité »", "p113"),
 ("cap08_ufc_wargon.png", "https://www.quechoisir.org/actualite-gaz-et-electricite-des-centaines-d-euros-a-economiser-en-faisant-jouer-la-concurrence-n176850/", "article UFC-Que Choisir du 18/06/2026", "titre + date + citation d'Emmanuelle Wargon", "p117"),
 ("cap09_loi_2025_594.png", "Légifrance : rechercher « loi n° 2025-594 du 30 juin 2025 » (adresse non relevée) ; à défaut la reproduction du JO https://www.associatheque.fr/fr/fichiers/actualite/loi-2025-594-NOR-ECOX2432287L.pdf", "article 13 de la loi", "« Il est interdit de démarcher par téléphone, directement ou par l'intermédiaire d'un tiers… » et « entrent en vigueur le 11 août 2026 »", "p049"),
 ("cap10_energieinfo_faux_mediateur.png", "https://www.energie-info.fr/demarchage-a-domicile-certains-commerciaux-se-font-passer-pour-le-mediateur-national-de-lenergie/", "actualité du médiateur sur les faux médiateurs", "le TITRE seulement (le texte nomme un fournisseur)", "p052"),
 ("cap11a_jdn_titre.png", "https://www.journaldunet.com/magazine/1550239-cd1-compteur-linky-4000-euros/", "article du Journal du Net du 15/05/2026", "titre « \"4 000 euros en un mois\" » + date ; puis le paragraphe sur les relevés de mars à mai 2024 ; puis le paragraphe du dénouement (≈ 700 kWh, 300 €, 3 000 €)", "p013, p061, p073, p141"),
 ("cap11b_jdn_on_ne_sait_pas.png", "même URL", "même article", "« \"On ne sait pas\", admet Matthieu Bertrand Neuser »", "p015"),
 ("cap11c_jdn_exceptionnel.png", "même URL", "même article", "« compteur Linky qui dysfonctionne, ça arrive, mais ça reste exceptionnel »", "p065"),
 ("cap11d_jdn_ca_change_tout.png", "même URL", "même article (nom du fournisseur hors cadre)", "« Ça change tout : ils nous répondent et font attention. »", "p075"),
 ("cap12_jechange.png", "https://www.jechange.fr/energie/electricite/news/primeo-energie-fin-offre-fixe-20-hausse-42-fevrier-2027", "article JeChange mis à jour le 11/11/2026", "titre + « mis à jour le 11/11/2026 » (le « 42 % » masqué jusqu'à la réponse) ; puis « +42 % » et « le silence vaut acceptation ». Ne jamais montrer la grille datée du 01/02/2027 ; nom du fournisseur hors cadre si possible", "p078, p090"),
 ("cap13_energieinfo_messages.png", "https://www.energie-info.fr/attention-aux-messages-que-vous-recevez-de-votre-fournisseur-denergie/", "actualité « Attention aux messages que vous recevez de votre fournisseur »", "« vous pouvez changer de fournisseur à tout moment et sans frais »", "p093, p094"),
 ("cap14_energieinfo_dynamiques.png", "https://www.energie-info.fr/offres-a-tarification-dynamique-informations-pratiques-et-alerte-pour-sensibiliser-sur-leur-complexite/", "page du médiateur sur les offres dynamiques", "« le prix de l'énergie fluctue tous les jours et toutes les heures »", "p097"),
 ("cap15_barometre_2026.png", "https://www.banquedesterritoires.fr/sites/default/files/2026-11/Synthese_Barometre_Energie-Info_2026.pdf (ou https://www.energie-mediateur.fr/le-mediateur/publications/barometre/)", "synthèse du baromètre énergie-info 2026", "« 36 % » (contrat signé après démarchage) puis « 15 % » (horaires d'heures creuses inconnus)", "p048, p124"),
 ("cap16_energieinfo_etoiles.png", "https://www.energie-info.fr/qualite-de-service-clients/", "page « Qualité de service clients » du médiateur", "la légende des étoiles (4 étoiles = 25 saisines ou moins pour 100 000 contrats), sans le tableau des noms", "p155"),
]
def usage(base):
    ids = [r["id"] for r in plans if base in r["img"] or (base == "cap11a_jdn_titre" and "capture JDN" in r["img"])]
    return ", ".join(ids) if ids else "—"
for c in caps:
    base = c[0].split(".")[0]
    A("| `" + c[0] + "` | " + c[1] + " | " + c[2] + " | " + c[3] + " | " + usage(base) + " |")

# ------------------------------------------------------------------ chapitres
A(""); A("## Chapitres (description YouTube : titres = recherches tapées ; temps estimés, à remesurer sur le rendu)")
A("")
A("| Temps estimé | Numéro de carte | Titre du chapitre |")
A("|---|---|---|")
A("| 0:00 | (pas de carte, accroche) | Facture d'électricité : où vont tes 100 € ? |")
cards = [r for r in plans if r["fmt"] == "titre"]
for i, r in enumerate(cards):
    if i == 0:
        A(f"| ({mmss(r['t'])}, carte) | {r['ch'][0]} | (même chapitre que 0:00 : la carte ouvre la décomposition) |")
    else:
        A(f"| {mmss(r['t'])} | {r['ch'][0]} | {r['ch'][1]} |")
fin = find("QUESTION OUVERTE")
A(f"| {mmss(fin['t'])} | — | Ton contrat finit quand ? (fin, ≈ 13 s : chapitre facultatif, YouTube demande 10 s minimum) |")

# ------------------------------------------------------------------ autres rôles
A(""); A("## Écarts avec le brief (décidés en mode automatique, consignés)")
A("")
A("- **Devinette n°5 changée** : le brief demandait « 59 € / 191 € / 591 € », mais 591 € est dit dès l'accroche (promesse de la miniature). Nouvelle devinette : « combien de foyers ont un prix fixe plus de 5 % au-dessus du tarif bleu ? 100 000 / près de 2 millions / 5 millions » → 1,9 million (CRE, `01b` §8, formulation sûre).")
A("- **« Cette partie-là vient de quadrupler » (ROUGE) supprimé** : remplacé par « cette part-là s'envole sur les marchés » + réponse « ×4 sur le marché » + « ta facture, elle, n'a pas pris fois quatre ».")
A("- **« Un million de foyers paient plus de 10 % trop cher », « jusqu'à 591 € », « 150 € » (ORANGE)** : remplacés par « 1,9 million de foyers à plus de 5 % », « au moins 591 € par an, hors taxes, pour le 1 % le plus cher » (« certains foyers » dans l'accroche), 157 € non utilisé (coupé pour la durée).")
A("- **« UFC : remise sur le kWh HT ≠ remise sur la facture » (ROUGE d'attribution)** : dit comme un calcul Le Vrai Prix (≈ −14 % sur une facture type).")
A("- **« 5 étoiles » (ROUGE)** : « les quatre étoiles du médiateur ».")
A("- **« Gelé » évité** : « il ne bouge pas avant le premier février ; après, personne ne sait de combien il montera ».")
A("- **« Zéro coupure »** : dit « le courant ne s'arrête pas, c'est le même réseau », sans l'attribuer à UFC.")
A("- **« Record depuis 2007 », 86 %, label VertVolt, jours rouges déjà tombés, baisse de taxe 2027** : non utilisés (non vérifiés ou mot ORANGE).")
A("- **Citations du JDN** : toutes attribuées au juriste de l'Adéic (aucune au couple), comme exigé par `01b` §5.")
A("- **Comment changer (brief 11:00)** : placé AVANT la révélation (p150-p151) pour que la fin reste ≤ 20 s après la réponse.")
A("- **4 devinettes ajoutées** (taxes, délai du médiateur, 36 c, jour rouge) pour tenir « une toutes les 2 min » ; toutes VERT ou formulation sûre.")
A("- **Vidéo suivante** : « Mardi premier décembre : les jouets de Noël » (calendrier `etude-marche.md`, consigne du lancement).")
A("")
A("## Pour les autres rôles")
A("")
A("- **SEO** (vérifier la densité) : mots-clés dits à l'oral (comptés dans la narration) : « facture » ×14, « fournisseur » ×14, « C R E » ×9, « tarif bleu » ×8, « médiateur » ×7, « kilowattheure » ×7, « marché(s) » ×7, « prix fixe » ×6, « heures creuses » ×3, « changer » ×3, « dynamique » ×2, « Tempo » ×2, « démarchage » ×2, « comparateur officiel » ×2, « indexée » ×1. La requête exacte « offre électricité moins chère » n'est pas dite mot pour mot (phrase peu naturelle à l'oral) : la mettre en 1re ligne de description et dans le titre.")
A("- **Miniature** : l'accroche dit mot pour mot la promesse de la variante A (« tu paies peut-être trop », p010) et montre le « 591 € » (p009) sur la facture devant le Linky, image de la frame 0. Ne jamais mettre « A », « 30 € » ni « 40 € » sur la miniature.")
A("- **Production / relecteur** : contrôle 7 bis à faire sur la planche : frame 0 non noire, pas de carte avant 30 s, au moins 2 questions ouvertes à 30 s (grande question, devinette 1, et le couple à 0:38), aucune réponse avant révélation, aucun plan > 6 s sans changement.")
A("- **Voix d'Omar** (règle 17.6) : proposer d'enregistrer p001-p017 (≈ 55 s) ou au moins p001-p009 (≈ 30 s) au téléphone dans `episodes/electricite/voix/accroche.m4a`.")
A("- **Shorts** (sans jamais dévoiler le n°1) : D1 (« sur cent euros, combien pour le courant ? »), D3 (« un appel, un contrat : valable ? »), D4 (« moins vingt… puis combien ? »), le couple (« quatre mille euros en un mois »), les lettres A-D (« ton offre a une lettre, tu la connais ? »), D5 bis (« un jour rouge, combien le kilowattheure ? »), heures creuses (« tu connais tes horaires ? »).")
A("")
A("## Nombre de mots / durée estimée")
A(f"- Mots de narration : {W} (fourchette demandée 1 650-1 950)")
A(f"- Voix seule à 150 mots/min : ≈ {mmss(W/2.5)}")
A(f"- Vidéo complète estimée : ≈ {mmss(TOTAL)} ({len(plans)} plans dont {nb_cartes} cartes titre sans voix, {nb_cd} comptes à rebours)")
A(f"- Formats : " + ", ".join(f"{k} {v}" for k, v in sorted({f: sum(1 for r in plans if r['fmt']==f) for f in set(r['fmt'] for r in plans)}.items(), key=lambda x: -x[1])))
open(sys.argv[2], "w", encoding="utf-8").write("\n".join(out) + "\n")
print("ok", len(out), "lignes")
