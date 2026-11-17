# Fact-check : « Offre électricité moins chère 2026 : 5 pièges à éviter » (slug `electricite`)

Vérifié le **17/11/2026** (run automatique, fact-checker). Fichiers relus : `01b_recherche.md`, `02_script_plans.py` (source des plans),
`02_scriptwriter_script.md` (régénéré), `episodes/electricite/sources.md`. Recoupement en ligne des points sensibles (sources ci-dessous).

## Verdict global
- **Prêt pour la production : ORANGE → VERT après corrections** (toutes appliquées dans `02_script_plans.py`, Markdown régénéré, contrôles du script : « aucune erreur »).
- **Résumé** : les chiffres tiennent. Deux erreurs de logique ou de fait (devinette n°1 qui ne répondait pas à sa propre question ; « pourquoi une somme pareille ? personne ne sait », alors que la cause est connue) et douze formulations à resserrer (dates, « hors taxes », périmètre Selectra, Wargon au passé, Tempo « presque quatre fois »).
- **Exactitude** : 62 affirmations contrôlées → 48 VERT, 12 ORANGE corrigés, 2 ROUGE corrigés. Après correction : 62 sur 62 utilisables (100 %), dont 6 qui reposent sur une source secondaire datée (à surveiller).
- Nouveau minutage : 1 854 mots, 159 plans, ≈ 13 min 46 s ; révélation principale p153 à 13:11 (95,8 %), 35 s de fin.

## Tableau : plan → affirmation → verdict → source → correction

| Plan | Affirmation (voix) | Verdict | Source vérifiée | Correction appliquée |
|---|---|---|---|---|
| p004-p005 + p028 | Devinette « sur ces cent euros, pour le courant : 20, 40 ou 60 € ? », réponse « à peu près quarante euros » | **ROUGE** (logique) | Calcul de la recherche : 40 € = la **fourniture** ; le courant lui-même ≈ 30 € (p031). La réponse donnée ne répondait pas à la question posée, et 30 est à égale distance de 20 et de 40. | p004 → « Devine d'abord : sur ces cent euros, combien pour ton fournisseur : ». La promesse « combien paient vraiment le courant ? » (p002) est tenue à p031 (« une trentaine »). |
| p014 | « Pourquoi une somme pareille ? Personne n'a la réponse. » | **ROUGE** (fait) | JDN 15/05/2026 : la somme vient de la facturation **sur estimation** (dit à p063) ; ce qui reste inconnu, c'est « Pourquoi le compteur a-t-il cessé de fonctionner ? La question reste sans réponse. » | → « Pourquoi leur compteur s'est arrêté ? Personne n'a la réponse. » (image déjà cohérente : Linky éteint) |
| p015 | « "On ne sait pas", admet même leur juriste. » | ORANGE (attribution) | JDN : « "On ne sait pas", admet Matthieu Bertrand Neuser », juriste de l'Adéic. Ce n'est pas l'avocat du couple. | → « "On ne sait pas", admet le juriste de leur association. » Bandeau inchangé (nom + Adéic). |
| p001-p003 | Promesse et grande question | VERT | — | — |
| p006 | « l'électricité vient de s'envoler » sur les marchés | VERT | Selectra 11/11/2026 : 39,8 €/MWh en avril, 166,1 en octobre, 266,3 du 1er au 10/11 ; TotalEnergies 20/10/2026. | — |
| p007 | « certains contrats vont suivre, dès janvier » | VERT | JeChange, mis à jour le 11/11/2026 : fin du prix fixe au 31/12/2026, nouvelle grille au 01/01/2027. | — |
| p008-p009 | « certains foyers pourraient économiser au moins 591 € par an » | ORANGE (temps + HT) | CRE, rapport Cohérence des offres, 03/06/2026 : « atteignent au moins 591 €/an HT pour les offres à prix fixe d'électricité », prix « au 1er décembre 2025 ». | → « pouvaient économiser » + « par an, hors taxes. » (les prix ont bougé depuis : présent trompeur) |
| p011-p013 | Yvelines, printemps 2024, 4 000 € pour un mois | VERT | JDN : « Tout commence au printemps 2024 » ; « Pour le seul mois de mai, [le fournisseur] réclame 4 000 euros. » | — |
| p016 | Boucle « combien ils ont vraiment payé » | VERT | Fermée p143. | — |
| p019-p020 | Réseau identique quel que soit le fournisseur | VERT | TURPE, tarif national (CRE 2026-105). | — |
| p022 | Réseau « un peu moins de trente » sur 100 € | VERT (calcul) | Calcul Le Vrai Prix : 27,9 € (Base 6 kVA, 4 500 kWh) ; CRE fin 2025 : ≈ 28 %. | — |
| p023-p025 | Taxes : « une trentaine », « presque un tiers » | VERT | Calcul : 30,7 € ; CRE fin 2025 : ≈ 33 %. Ne dépend pas de l'hypothèse réseau. | — |
| p027 | « la seule part qui change d'un contrat à l'autre » | VERT | energie-info.fr : « Il s'agit de la seule composante soumise à la concurrence. » | — |
| p028 | Réponse D1 « à peu près quarante euros » | VERT (après p004) | Calcul : 41,3 € (sensibilité 39-43 €). | voir p004 |
| p029 | « environ sept » pour commercialisation + CEE | ORANGE (étiquette) | CRE 2026-06 : 18,11 €/MWh dont 9,80 de CEE ; × 4,5 MWh ≈ 7 € : c'est un calcul, pas un chiffre publié. | Source écran → « estimation Le Vrai Prix d'après la CRE (délibération 2026-06) ». |
| p031 | Le courant lui-même ≈ 30 € | ORANGE accepté | Estimation ± 3 € ; déjà étiquetée « estimation » à l'écran, « une trentaine » à la voix. | — (ne jamais mettre « 30 € » sur la miniature) |
| p032-p033 | ARENH jusqu'en 2025, fin en janvier | VERT | CRE 2026-06 : fin de l'ARENH le 31/12/2025. | — |
| p034-p037 + p041 | Prix de marché × 4 en un an | ORANGE accepté | Selectra 11/11/2026 : « environ 266 €/MWh », « près de quatre fois celui de novembre 2025 (65,8 €/MWh) ». Moyenne sur 10 jours contre un mois entier ; pas de source primaire EPEX. Source écran déjà « relevé Selectra des prix spot ». | — |
| p038-p039 | VNU : « Dernière estimation de la C R E : il ne te rendrait rien » | ORANGE (date) | Selectra 01/11/2026 : estimation CRE **au 1er octobre**, 65,50 €/MWh, seuil 78 €/MWh, « 0 € pour l'instant ». La CRE la met à jour chaque mois ; sa page n'a pas pu être ouverte (bloquée) : une estimation de novembre peut exister, et la flambée de novembre pousse les revenus d'EDF vers le haut. | → « Selon la C R E, début octobre, il ne te rendrait rien en deux mille vingt-sept. » |
| p040 | Livrable 2027 « plus que doublé depuis janvier » | VERT | Selectra 10/11 : 128 €/MWh le 30/10 ; TotalEnergies : 109,81 le 19/10. | — |
| p042-p044 | Tarif bleu amortit, lissage 24 mois, rien avant le 1er février | VERT | CRE 2026-06 (« lissée sur 24 mois ») ; CRE 2026-147 (prochain mouvement février 2027). Le mot « gelé » est bien absent. | — |
| p048 | Contrat signé au téléphone ou à la porte | VERT | — | — |
| p049 | « plus d'un tiers des foyers ont déjà signé comme ça » | ORANGE (canal) | Synthèse du baromètre 2026 : « 36 % de l'ensemble des foyers » ont souscrit un contrat « après un démarchage commercial », sans préciser téléphone ou porte. | → « … plus d'un tiers des foyers ont signé après un démarchage. » |
| p050-p051 | Loi au 11/08/2026, plus d'appel sans accord | VERT | Loi n° 2025-594 du 30/06/2025, art. 13 (JO) ; CMS : « à compter du 11 août 2026 ». | — |
| p052 + p055 | Contrat signé après un appel interdit = nul | VERT | Art. L. 223-1 (nullité maintenue, CMS). « Comme s'il n'avait jamais existé » = effet de la nullité. | — |
| p053 | Le vrai médiateur ne démarche jamais | VERT | energie-info.fr : le médiateur « n'effectue aucun démarchage ». | — |
| p054 | Amende jusqu'à 375 000 € pour une entreprise | VERT | Art. L. 242-16 (75 000 € / 375 000 €), CMS. | — |
| p056 | Exception : ton fournisseur actuel, pour le contrat en cours | VERT | L. 223-1 : sollicitation « dans le cadre de l'exécution d'un contrat en cours », en rapport avec ce contrat. | — |
| p057 | Le démarchage à domicile reste permis | VERT | La loi de 2025 vise le téléphone (et, pour la rénovation énergétique, SMS et e-mails). | — |
| p062-p065 | Mars-mai 2024 sans relevé, estimation, résiliation, commissaire de justice | VERT | JDN : « entre mars et mai, leur compteur Linky cesse de transmettre ses relevés » ; « un commissaire de justice sera mandaté par le fournisseur ». | — |
| p066 | Citation « compteur Linky qui dysfonctionne, ça arrive, mais ça reste exceptionnel. » | VERT (mot pour mot) | JDN, Matthieu Bertrand Neuser, juriste de l'Adéic. | — |
| p067 + p072 | Médiateur saisi 2 mois après la réclamation écrite, gratuitement | VERT | energie-info.fr : « 2 mois après ma réclamation écrite » ; « directement et gratuitement ». | — |
| p068 | « L'an dernier, dans l'Hérault, une sexagénaire » | VERT | Selectra 07/11/2025 (d'après Midi Libre). | — |
| p069 | « on lui prélève deux cent onze mille euros » | ORANGE | Selectra : « un prélèvement automatique, déjà effectué », puis « rejeté par la banque » ; le fournisseur dit qu'il « sera annulé ». Elle n'a pas perdu cette somme. | → « Une erreur de saisie, et on lance un prélèvement de deux cent onze mille euros. » + mention écran « prélèvement rejeté par la banque, puis annulé ». |
| p070 | « J'ai hurlé et même vomi » (Midi Libre) | VERT (source secondaire) | Selectra : citation de la cliente « confiée » à Midi Libre. Article d'origine non lu (date inconnue). Bandeau « Midi Libre via Selectra » déjà prévu. | — |
| p073 | Un an avant d'appeler l'Adéic | VERT | JDN : « un an plus tard, en mai 2025, […] le mari contacte l'Adéic ». | — |
| p074-p075 | Adresse dédiée ; « Ça change tout : ils nous répondent et font attention. » | VERT (mot pour mot) | JDN, juriste de l'Adéic (jamais le couple). | — |
| p080-p081 | Fournisseur, JeChange, fin au 31 décembre | VERT | JeChange publié le 06/11/2026, mis à jour le 11/11/2026 après erratum : fin le 31/12/2026. | — |
| p082 | kWh HT 0,1140 → 0,1747 € | VERT | JeChange (option Base, + 53 %). | — |
| p083 | Abonnement « près de cinquante pour cent » | VERT | JeChange : 14,38 → 21,12 €/mois (+ 47 %), option HP/HC. | — |
| p084-p085 + p093 | « pour un client », + 42 % | VERT | JeChange : « environ 42 % », variable selon la conso. | — |
| p086-p088 | La remise ne touche que le kWh HT ; ≈ − 14 % sur la facture | VERT (calcul) | Remise = 20 % du kWh HT du tarif bleu de février 2025 (0,1425 €, JeChange) → 2,85 c HT, 3,42 c TTC × 4 500 kWh = 154 € sur une facture tarif bleu de 1 091 € = **− 14,1 %** (− 13,5 % si l'on prend le kWh HT d'août 2026). « Environ moins quatorze » est juste. Pas d'attribution à UFC (ROUGE de la recherche bien retiré). | Source écran précisée : « calcul Le Vrai Prix : remise sur le seul kWh HT, tarif bleu Base 6 kVA, 4 500 kWh/an ». |
| p089 | « le silence vaut acceptation » | VERT | JeChange. | — |
| p094 | Préavis d'un mois minimum | VERT | energie-info.fr ; art. L. 224-10 du code de la consommation. | — |
| p096 | Partir à tout moment, sans frais | VERT | energie-info.fr. | — |
| p099 | Offre dynamique : prix qui change tous les jours et toutes les heures | VERT | energie-info.fr (offres dynamiques). | — |
| p100-p101 + p098 | 36 c marché + taxes, sans réseau ni abonnement ; tarif bleu 20 c | VERT | Selectra 11/11 : (0,2663 + 0,03062) × 1,2 = 0,3563 €, réseau, abonnement et marge exclus ; tarif bleu 0,2001 € (CRE 2026-147, recalculé). | — |
| p102-p104 | Niveaux A à D ; D « aléatoire ou imprévisible » | VERT | CRE, fiche « Niveau de certitude » ; Lignes directrices, annexe 3 (niveau 4). | — |
| p105 | Demander la lettre si elle manque | VERT | CRE 2026-110 (lettre omise dans certains courriers). | — |
| p110 | En juin, la CRE a passé les offres au crible | VERT | Rapport du 03/06/2026. | — |
| p111-p112 + p116 | 1,9 million de foyers en prix fixe à + 5 % | ORANGE (temps) | CRE : « 1,9 millions de consommateurs sont en offre à prix fixe dont le prix est supérieur au TRVE de plus de 5 % », prix au 01/12/2025. | p111 « paient » → « payaient » ; p116 → « …un million neuf cent mille foyers, fin deux mille vingt-cinq. » |
| p113-p114 | 1 % des contrats les plus chers : au moins 591 € HT | VERT | Rapport CRE (mot pour mot). | Découpage revu (p113 faisait 17 mots) : « au moins » passe dans p114. |
| p115 | « presque toutes ces offres chères » sont vertes | VERT | CRE : « 91 % des contrats en offre à prix supérieur à TRVE +5 % sont des offres vertes ». | — |
| p117 | « Sa présidente, Emmanuelle Wargon, va contacter… » | ORANGE (temps et citation) | Wargon est bien présidente de la CRE en novembre 2026 (communiqué CRE du 15/01/2026 ; AFP du 15/09/2026, « la présidente de la CRE, Emmanuelle Wargon »). La phrase date de juin (UFC, 18/06/2026) ; citation complète : « … très onéreuses pour leur demander des explications ». | → « En juin, sa présidente Emmanuelle Wargon annonçait vouloir contacter les fournisseurs de ces offres très onéreuses. » Citation complétée dans la Vitre. |
| p122 | Huit heures creuses par jour, surtout la nuit | VERT | CRE 2026-147, annexe B : « 16 heures pleines et 8 heures creuses ». | — |
| p123 | « l'été, une partie passe en début d'après-midi » | ORANGE | Selectra 20/07/2026 d'après la CRE : jusqu'à 3 h creuses déplaçables dans la plage **11 h-17 h** l'été, déploiement progressif par Enedis. | → « Et l'été, une partie peut passer en milieu de journée. » |
| p124 | 15 % ignorent leurs horaires | VERT | Synthèse du baromètre 2026 : « 15 % des foyers concernés ne connaissent pas les horaires exacts ». | — |
| p126 | 300 bleus, 22 rouges | VERT | Selectra (saison 2026-2027 : 300 / 43 / 22). Moneyvox (22/10/2026) écrit 22 puis 21 : coquille de leur côté, on suit la grille. | — |
| p127-p129 | Jour rouge HP : 73 c, « presque quatre fois le tarif de base » | ORANGE | 0,7295 € TTC (CRE annexe B 57,73 c HT, recalculé ; confirmé par Moneyvox 22/10/2026). 0,7295 / 0,2001 = **3,65**. | p129 → « Plus de trois fois et demie le tarif de base. » |
| p128 | Novembre-mars, jamais le week-end, connu la veille | VERT | Selectra ; Moneyvox 22/10/2026 : jours rouges du 1er novembre au 31 mars, prévenus la veille à 11 h ; RTE envisage un tirage à J-2 (non daté) et la CRE propose d'exclure les 24 et 31 décembre. | — (à surveiller) |
| p131 | 19 millions de foyers au tarif bleu | VERT | Observatoire CRE T2 2026 via Kelwatt : 19,20 millions de sites (54,8 %). | — |
| p132 | Tarif fixé sur proposition de la CRE | VERT | — | — |
| p134 | + 2,5 % au 1er août, ≈ 26 €/an | VERT | AFP 16/07/2026 : 1 046 → 1 072 € TTC. | — |
| p135 | Fin juin, la moitié des offres moins chères | VERT | Kelwatt (observatoire CRE) : 52 %, 40 offres. | — |
| p136 | Selectra : 15 offres en hausse en un mois | VERT | Selectra 10/11/2026 (12/10 → 09/11). | — |
| p137-p138 + p147 | « début novembre, combien d'offres à prix fixe battaient le tarif bleu ? » → 8 sur 29 | ORANGE (périmètre) | Selectra 10/11/2026 : « 8 sur 29 » à prix fixe, Base 6 kVA, 4 500 kWh ; uniquement les offres **de son propre comparateur**, ouvertes le 09/11. Le comparateur officiel n'a pas pu être relevé (page bloquée). | p137 → « Sixième devinette : sur le comparateur Selectra, début novembre, combien d'offres fixes battaient le tarif bleu ? » + mention écran « comparateur Selectra, relevé du 9 novembre 2026 ». p147 déjà sourcé. |
| p140-p145 | Dénouement : février 2026, ≈ 700 kWh, geste de 300 €, 3 000 €, 30 × ≈ 100 €, nouveau compteur et fournisseur | VERT | JDN (mot pour mot). | — |
| p148-p149 | Comparateur officiel « public, gratuit, neutre et indépendant », affiche A-D | VERT | energie-info.fr (nouveautés du comparateur). | — |
| p150-p151 | Quinze minutes, PDL à 14 chiffres, aucun frais, pas de coupure | VERT | UFC 24/09/2026 (sauf « pas de coupure » : fait général, non attribué à UFC). | — |
| p153-p156 | Réponse : prix fixe A, moins cher que le tarif bleu, 4 étoiles ; sinon tarif bleu | VERT | Critères tirés de la CRE (A), du comparateur officiel et du médiateur (étoiles de 1 à 4 : 4 = au plus 25 saisines pour 100 000 contrats). Aucun fournisseur nommé. | — |
| p158 | « Mardi premier décembre » | VERT | Le 01/12/2026 est bien un mardi. | — |

## Points demandés par le producteur

1. **Fonction d'Emmanuelle Wargon en novembre 2026** : VERT, présidente de la CRE (communiqué CRE du 15/01/2026, AFP du 15/09/2026). Seule la phrase au futur a été mise au passé (p117).
2. **« 8 offres sur 29 »** : relevé Selectra affiché comme tel à la voix et à l'écran (p137, p147), avec le périmètre « comparateur Selectra ». Si quelqu'un relève le comparateur officiel à la capture, remplacer voix et écran et l'écrire dans `sources.md`.
3. **Citations du juriste de l'Adéic** : les trois (« On ne sait pas », « Ça change tout : ils nous répondent et font attention. », « compteur Linky qui dysfonctionne, ça arrive, mais ça reste exceptionnel. ») sont **mot pour mot** dans le JDN et attribuées à Matthieu Bertrand Neuser, jamais au couple.
4. **« Environ − 14 % »** : juste (− 14,1 % sur la base de février 2025, − 13,5 % sur celle d'août 2026).
5. **591 € HT** : VERT, « au moins », hors taxes, 1 % des contrats les plus chers, prix au 01/12/2025. « Hors taxes » est maintenant dit dès l'accroche.
6. **1,9 million** : VERT, daté « fin deux mille vingt-cinq » à la voix.
7. **Tarif bleu 0,2001 €/kWh** : VERT (recalcul CRE 2026-147 ; Selectra, Kelwatt).
8. **Tempo** : 22 jours rouges et 0,7295 € VERT ; « presque quatre fois » corrigé en « plus de trois fois et demie ».
9. **Heures creuses** : 8 h VERT ; l'été, « milieu de journée » (11 h-17 h) et « peut », car Enedis déploie la réforme peu à peu.
10. **Loi n° 2025-594, art. 13, au 11/08/2026** : VERT (JO via associatheque, CMS, Selectra). Légifrance n'a pas été ouvert, comme pour la recherche : la capture `cap09` est une reproduction du JO, ce qui est acceptable.
11. **36 % démarchage** : VERT après correction du canal (p049).
12. **Étoiles du médiateur** : VERT, quatre au maximum (et pas cinq).
13. **VNU** : estimation datée « début octobre » (p039).
14. **Aucune réponse chiffrée avant sa révélation** : VERT. Contrôle des 10 devinettes : chaque réponse arrive après son compte à rebours (p028, p025, p041, p055, p072, p093, p100, p116, p129, p147). La lettre « A » n'apparaît comme conclusion qu'à p153 (95,8 %). Le « + 42 % » du titre JeChange est masqué jusqu'à p093. Le 591 € de l'accroche est l'enjeu de la miniature, pas une réponse.
15. **Aucun avis maison sur un fournisseur nommé** : VERT. Aucun fournisseur n'est nommé à la voix. Le seul fournisseur identifiable vient de la presse (JeChange : son nom est dans le titre et l'URL ; JDN : nommé dans le texte). Recadrages déjà prévus (cap10, cap11, cap12) : à respecter strictement au montage. La conclusion (p156) est un conseil général, tiré des critères publics, sans marque.
16. **Nombres écrits comme ils se prononcent** : VERT. Aucun chiffre, sigle collé ou symbole (%, €) dans la narration (contrôle par script) ; « C R E », « T V A », « point F R » épelés.

## RED : à corriger impérativement (corrigé)
1. **p004 / p028** : la devinette n°1 demandait le prix « du courant » et répondait par celui de la fourniture. Corrigé (« combien pour ton fournisseur »).
2. **p014** : « Pourquoi une somme pareille ? Personne n'a la réponse » était faux (la cause est l'estimation, dite plus tard). Corrigé (« Pourquoi leur compteur s'est arrêté ? »).

## YELLOW : corrections recommandées (toutes appliquées)
p008-p009 (passé + hors taxes), p015 (juriste de l'association), p029 (étiquette « estimation »), p039 (VNU daté), p049 (36 % : « après un démarchage »), p069 (prélèvement lancé puis rejeté), p088 (source du calcul), p111/p116 (1,9 million daté), p117 (Wargon au passé + citation entière), p123 (heures creuses l'été), p129 (Tempo 3,65 fois), p137 (périmètre Selectra). Et une correction technique : p113 (17 mots) redécoupé avec p114.

## GREEN : notes
1. **Dépendance à Selectra** : quatre chiffres viennent d'un comparateur commercial (× 4, 36 c, 15 hausses, 8 sur 29). Ce ne sont pas des critères du classement, qui repose sur la CRE, le médiateur et UFC, comme demandé. Toujours afficher « relevé Selectra » ou « calcul Selectra ».
2. **« Foyers » ou « consommateurs »** : la CRE dit « consommateurs » ou « sites ». « Foyers » est un raccourci acceptable pour des sites résidentiels.
3. **Midi Libre** : la citation est lue via Selectra ; l'article d'origine n'a pas été retrouvé. Le bandeau dit « via Selectra ».
4. **Prononciation** : vérifier « Adéic » (a-dé-ik) et « Selectra » à l'écoute de la voix.
5. **Vie privée** : couple et cliente anonymes, sans visage. Données d'Omar (nom, adresse, n° client, PDL, n° de compteur) à flouter sur tous les plans `omar-*`. C'est un point de contrôle au montage.
6. **Droits** : captures de presse et de documents publics, recadrées sur une phrase et pendant 3 à 6 s : courte citation avec source, acceptable. Pas d'extrait vidéo tiers.

## Matrice de cohérence
| Contrôle | Statut | Notes |
|---|---|---|
| Exactitude des faits | PASS | Après les 2 ROUGE et les 12 ORANGE corrigés |
| Fiabilité des sources | WARN | CRE, médiateur, JO, AFP solides ; Selectra (commercial) pour 4 chiffres, Midi Libre et l'estimation VNU lus via Selectra |
| Équilibre | PASS | Le Linky est présenté comme « exceptionnel » quand il dysfonctionne ; le tarif bleu n'est pas idéalisé (+ 2,5 %, hausse possible en février) |
| Recherche ↔ narration | PASS | Toutes les formulations sûres de `01b_recherche.md` sont reprises ; aucun ROUGE de la recherche n'est utilisé |
| Juridique et éthique | PASS | Aucun fournisseur nommé ni dénigré à la voix ; recadrages à tenir au montage |

## Reste à surveiller avant la mise en ligne
- **VNU** : la page CRE (estimation mensuelle) était bloquée. Si une estimation de novembre donne plus de 0 €, réécrire p039.
- **Comparateur officiel** : relever le nombre d'offres sous le tarif bleu au moment de la capture `cap01`. Si on l'utilise, remplacer p137, p138 et p147 et l'écrire dans `sources.md`.
- **Tempo** : RTE pourrait annoncer certains jours rouges deux jours avant, et la CRE propose d'exclure les 24 et 31 décembre. « Tu le sais la veille » reste juste aujourd'hui.
- **Captures** : nom du fournisseur hors cadre (JeChange, JDN, page energie-info « à domicile ») ; grille JeChange datée du 01/02/2027 jamais montrée ; tableau des étoiles jamais montré.

## Liste finale des livrables
- [x] Recherche (`01b_recherche.md`)
- [x] Brief / traitement (`01_strategist_brief.md`)
- [ ] Guide d'entretien : sans objet (pas d'interview ; témoignage = presse citée)
- [x] Script parlé (`02_script_plans.py` → `02_scriptwriter_script.md`, régénéré le 17/11/2026, contrôles : aucune erreur)

## Sources consultées pour ce fact-check (17/11/2026)
- CRE, communiqué « Nomination Jérôme Dupont », 15/01/2026 (Emmanuelle Wargon, présidente) : https://www.cre.fr/fileadmin/Documents/Communiques_de_presse/2026/260115_CP_Nomination_Jerome_Dupont.pdf
- AFP / Connaissance des énergies, 15/09/2026 (« la présidente de la CRE, Emmanuelle Wargon ») : https://www.connaissancedesenergies.org/afp/gaz-la-facture-moyenne-2026-superieure-de-120-euros-a-2025-calcule-le-regulateur-de-lenergie-260915
- CRE, rapport Cohérence des offres, 03/06/2026 : https://www.cre.fr/fileadmin/Documents/Rapports_et_etudes/2026/Rapport_Coherence_des_offres_2026.pdf
- UFC-Que Choisir, 18/06/2026 (citation Wargon complète) : https://www.quechoisir.org/actualite-gaz-et-electricite-des-centaines-d-euros-a-economiser-en-faisant-jouer-la-concurrence-n176850/
- Journal du Net, 15/05/2026 : https://www.journaldunet.com/magazine/1550239-cd1-compteur-linky-4000-euros/
- Synthèse du baromètre énergie-info 2026 : https://www.banquedesterritoires.fr/sites/default/files/2026-11/Synthese_Barometre_Energie-Info_2026.pdf
- Selectra, remise nucléaire 2027, 01/11/2026 : https://selectra.info/energie/actualites/marche/remise-nucleaire-2027-estimation-cre-novembre
- Selectra, 15 offres sous le tarif bleu, 10/11/2026 : https://selectra.info/energie/actualites/marche/offres-electricite-15-hausses-sous-tarif-bleu
- Selectra, tarif dynamique + 78 %, 11/11/2026 : https://selectra.info/energie/actualites/marche/tarif-dynamique-novembre-kwh-78-pourcent-base
- Selectra, erreur de 211 993 € dans l'Hérault : https://selectra.info/energie/actualites/marche/facture-electricite-village-entier-erreur-200-000-euros
- Moneyvox, jours rouges Tempo, 22/10/2026 : https://www.moneyvox.fr/energie/actualites/110948/electricite-ce-qui-va-changer-pour-les-jours-rouges-de-option-tempo-edf-et-des-eld
- JeChange, mis à jour le 11/11/2026 : https://www.jechange.fr/energie/electricite/news/primeo-energie-fin-offre-fixe-20-hausse-42-fevrier-2027
- Kelwatt, observatoire CRE T2 2026, 05/10/2026 : https://www.kelwatt.fr/actu/cre-observatoire-marche-deuxieme-trimestre-2026
- CMS, démarchage téléphonique : https://cms.law/en/fra/news-information/interdiction-prochaine-du-demarchage-telephonique-sans-consentement-prealable-du-consommateur
- Page bloquée (non lue) : https://www.cre.fr/electricite/marche-de-detail-de-lelectricite/vnu-estimation-des-revenus-nucleaires-dedf.html
