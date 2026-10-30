# Fact-check : la baguette

**Slug :** `baguette` · **Rôle :** fact-checker · **Date :** 29/10/2026
**Fichiers vérifiés :** `plans.json` (voix `texte`, écran `schema` / `couches` / `surtitre` / `punch` / légendes), `02_scriptwriter_script.md`, `01b_recherche.md` (F01–F49), `episodes/baguette/sources.md`.

## Bilan

- **Prêt pour la production** : OUI, avec les corrections appliquées ci-dessous.
- **Résultat** : 4 ROUGE (tous corrigés) · 16 ORANGE (15 corrigés, 1 à surveiller) · 52 VERT (lignes du tableau, plus 2 faits vérifiés absents du script).
- **Re-vérifié en ligne (source primaire relue le 29/10/2026)** : OFPM 2026 section 7 (graphiques 171 et 172), série INSEE 000442615 (unité 1 kg), Fiducial 2026, Sud Radio / Fiducial 2025, UFC-Que Choisir 2026 et 2025, CNBPF DP 2025, Pleinchamp et Journal de l'économie (Leclerc), Connexion France (Lidl), DRAAF CVL bilan 2025, FranceAgriMer Qualit@lim 2025, fiche GMP 00234, décret 93-1074 art. 2 (FAOLEX), CNRS Le Journal 2023, Innograin 2024, INBP n° 105, Nomad Éducation CAP, AFP / Le Petit Journal 2022, Connexion France (liberté des prix en 1987).
- **Règles conservées** : de 7 à 18 mots par plan (contrôlé par script), pas de chiffre écrit dans la voix, formats inchangés, jamais deux formats identiques à la suite, aucun chiffre inventé. Le JSON est valide et contient 120 plans.

## Points ROUGE (corrigés)

| Plan | Problème | Avant | Après |
|---|---|---|---|
| p114 | **Accusation implicite d'une marque.** Juste après Leclerc, « Le secret ? Des pâtons faits en usine, surgelés… » laissait entendre que la baguette Leclerc à 29 c est faite de pâte surgelée. Aucune source ne le dit (ni Pleinchamp, ni le Journal de l'économie). Que Choisir 2025 parle seulement des « terminaux de cuisson », et Que Choisir 2026 dit que les baguettes de GMS, hors hypermarchés avec boulangerie, « ne sont pas pétries sur place ». | Le secret ? Des pâtons faits en usine, surgelés, puis seulement cuits en magasin. · schéma « Premier prix : Pâtons en usine → Surgelés → Cuits en magasin » | En supermarché, souvent, les pâtons arrivent surgelés et sont seulement cuits sur place. · schéma « Terminal de cuisson : Pâtons livrés → Surgelés → Cuits sur place », source « UFC-Que Choisir, 2025 et 2026 » |
| p059 | **Mécanisme faux.** Selon l'INBP, le manque de buée donne un pain *peu développé* et une croûte terne. Le pain *plat* vient d'un *excès* de buée ou d'une coupe trop profonde. | …sortirait du four plate, la croûte terne. | …sortirait du four peu gonflée, la croûte terne. |
| p067 | Même erreur, dans la voix et à l'écran. | Sans buée, pain plat et croûte terne. · écran « pain plat, croûte terne » | Sans buée, pain peu gonflé et croûte terne. · écran « pain peu développé, croûte terne » |
| p052 | **Fait mal attribué.** La source (Nomad, CAP) décrit une pousse lente de 24 h entre 8 et 12 °C pour une pâte *pétrie, pesée et façonnée la veille*. Ce n'est donc pas le pointage. | Ce repos, c'est le pointage. Au froid, jusqu'à environ vingt-quatre heures. · légende « pousse lente, entre 8 et 12 °C (environ) » | Ce repos, c'est le pointage. En pousse lente, au froid, la pâte façonnée attend environ vingt-quatre heures. · légende « pâte façonnée, en pousse lente entre 8 et 12 °C » |

## Tableau des vérifications

V = VERT, O = ORANGE, R = ROUGE. Dans la colonne « Correction », ✔ veut dire que la correction est appliquée dans `plans.json` et dans le script.

| Plan | Affirmation (voix / écran) | Verdict | Source vérifiée | Correction appliquée |
|---|---|---|---|---|
| p001 | Baguette à un euro : le blé coûte six centimes ; écran « 6 CENTIMES », périmètre OFPM | V | OFPM 2026, graph. 171 : blé 0,24 €/kg × 0,25 = 0,060 € | — |
| p002 | 0,06 € = une pièce de 5 c + une pièce de 1 c | V | Calcul | — |
| p003 | « quatre-vingt-quatorze autres centimes » ; légende écran « 1,01 € » | O | 1,00 − 0,06 = 0,94, mais 1,01 − 0,06 = 0,95 : l'écran contredisait la voix | ✔ légende → « ≈ 1 € » |
| p004 | Six milliards de baguettes vendues par an en France | V | CNBPF DP 2025 : « 6 milliards de baguettes vendues par an » | — |
| p005 | Cent quatre-vingt-dix par seconde | V | CNBPF DP 2025 : « 190 baguettes achetées chaque seconde ». Calcul : 6 × 10⁹ / 31 536 000 s = 190,3 | — |
| p010 | Des mois entre le semis et la moisson | V | Cycle du blé d'hiver (connaissance générale) | — |
| p011 | Récolte 2025 : trente-trois millions de tonnes ; écran « 33,3 Mt » | V | FranceAgriMer Qualit@lim 2025 : « 33,3 millions de tonnes » (estimation SSP du 01/09/2025) | — |
| p012-p015 | La moissonneuse coupe, bat, sépare la paille ; le grain va au réservoir, puis en remorque, puis au silo | V | Fonctionnement standard | — |
| p016-p017 | Environ 270 g de blé par baguette, plus lourd que la baguette | V (calcul B) | GMP 00234 (1 000 g de farine, pâton de 350 g) + CAP (350 g cru → 250 g cuit) + taux filière 78,6 %. La fourchette 263–292 g reste toujours > 250 g | — (« environ » bien présent) |
| p018 | Baguette cuite : 250 g | V | Éduscol CAP ; Que Choisir 2025 (250 g en GMS, 240 g en moyenne en boulangerie) | — |
| p020 | Blé 2025 : environ 200 €/t ; écran « 201 €/t, rendu Rouen » | V | DRAAF CVL bilan 2025 : « 201 €/t », −6 % sur un an | — |
| p021 | Vingt centimes le kilo de blé | V | 201 €/t = 0,201 €/kg | — |
| p022 | Baguette à quatre euros le kilo, vingt fois plus cher ; écran 0,20 / 4,05, « × 20 » | V | INSEE 4,05 €/kg (série « Pain baguette (1 kg) ») ; 4,05 / 0,201 = 20,1 | — |
| p026 | Meules de pierre mues par l'eau ou le vent | V | Histoire de la meunerie | — |
| p027 | « cylindres d'acier » | O | Les cylindres de broyage sont en général en fonte trempée, pas en acier | ✔ « cylindres de métal » |
| p029-p030 | Plansichters = tamis géants qui secouent ; le son d'un côté, la farine de l'autre | V | Principe du tamisage | — |
| p031 | Sur 100 kg de blé, environ 78 kg de farine | V | Intercéréales 2021 : 2,2 Mt de farine pour 2,8 Mt de blé = 78,6 % ; dans la fourchette OQLF de 72 à 80 % | — |
| p032 | Environ 210 g de farine | V (calcul B) | 350 × 1 000 / 1 663 = 210 g (210 g aussi en comptant les 5 g de correcteur de la fiche) | — |
| p033 | Tradition : souvent farine T65 | V | Label Rouge LA 05/14 : T65 → « pain de tradition française » | — |
| p034 | « Le T, c'est le taux de cendres » ; écran T55 0,50–0,60 %, T65 0,62–0,75 % | O | T = *type*, défini par le taux de cendres. Les valeurs à l'écran sont justes | ✔ « Le T, c'est le type, fixé par le taux de cendres… » |
| p036 | Meunier : sept centimes, un peu plus que le blé | V | OFPM : 0,27 × 0,25 = 0,0675 € ; part du HT : meunerie 7,2 % > blé 6,2 % | — |
| p037 | Marge brute ≠ bénéfice | V | Définition OFPM | — |
| p041-p042 | Décret de 1993 : farine, eau, sel, levure ou levain, aucun additif, jamais surgelé | V | Décret 93-1074 du 13/09/1993, art. 2 (relu). Il tolère aussi la fève (2 %), le soja (0,5 %) et le malt (0,3 %), qui ne sont pas des additifs. Le texte dit « pain de tradition française », pas « baguette » | — |
| p043 | Recette : 1 kg de farine, 630 g d'eau ; écran sel 18 g, levure 15 g | O | Fiche GMP 00234 relue : chiffres exacts, mais la fiche ajoute 5 g de « Sécur'Détente » (correcteur), absents de la liste | ✔ source « …réf. 00234 (extrait) » |
| p044 | Quinze grammes de levure fraîche | V | GMP : 15 g ± 2 (méthode directe) | — |
| p046 | Le gluten n'existe pas dans la farine, il naît au pétrissage | V | CNRS : « Le gluten n'existe pas en tant que tel dans les farines » ; il se forme avec l'eau et le pétrissage | — |
| p047 | Deux familles de protéines | V | Wieser 2007 : gliadines et gluténines | — |
| p048 | Filet élastique qui se répare tout seul | V | CNRS : « propriétés d'autocicatrisation » ; les liaisons cassent et se reforment | — |
| p049-p050 | Levure = champignon microscopique ; sucres → CO₂ + alcool | V | Universalis ; Planet-Vie | — |
| p051 | Le gluten piège le gaz | V | Mécanisme classique (CNRS + fermentation) | — |
| p052 | Pointage au froid jusqu'à 24 h | **R** | Nomad (CAP) : 24 h entre 8 et 12 °C pour une pâte *déjà façonnée* (pousse lente) | ✔ voir ROUGE |
| p054 | 350 g par pâton | V | GMP : division à 350 g ; CAP : 350 g → 250 g | — |
| p057 | Pétrir → pointage → diviser → façonner → apprêt | V | Fiche CAP | — |
| p059 | Sans buée : baguette « plate », croûte terne | **R** | INBP n° 105 : le manque de buée donne un pain *peu développé*. Le pain plat vient d'un excès de buée | ✔ voir ROUGE |
| p061-p063 | Coup de lame : coupes longues, peu profondes, lame de biais ; les entailles deviennent les grignes | V | INBP : « coupes longues, parallèles…, peu profondes et tenir la lame de biais » | — |
| p060, p064 | Four à environ 240 °C (± 20) | V | Fiche GMP : « 240 °C (± 20 °C) » | — |
| p065 | Buée = vapeur d'eau | V | — | — |
| p066 | La buée garde la croûte souple pour que la baguette gonfle | O | Innograin : l'extérieur reste plus souple au début, ce qui peut améliorer *un peu* l'expansion (« not as evident ») ; l'INBP le confirme (sans buée, pain peu développé) | ✔ « Elle garde la croûte souple plus longtemps : la baguette gonfle mieux. » |
| p067 | Sans buée : « pain plat » (voix et écran) ; trop de buée : pas de grigne, croûte molle | **R** / V | INBP : excès de buée → absence de grigne et croûte molle (juste) ; manque de buée → pain peu développé (pas « plat ») | ✔ voir ROUGE |
| p068 | Vers 50 °C la levure meurt ; « ses bulles restent figées » | O | Nomad : la levure meurt à environ 50 °C. Mais la mie ne fige que vers 70 °C (amidon, Innograin) : le lien de cause était trompeur | ✔ « …la levure meurt. Mais ses bulles, elles, resteront dans la mie. » |
| p069 | 70 °C : l'amidon gélifie ; 100 °C en surface tant que l'eau s'évapore ; 130 °C : la croûte dore | V | Innograin : gélatinisation vers 70 °C ; la zone extérieure plafonne pendant l'évaporation ; Maillard visible vers 130 °C | — |
| p070-p072 | Au-delà de 130 °C la croûte dore ; Maillard = sucres + acides aminés + chaleur → couleur et parfum | V | Innograin ; Futura Sciences | — |
| p073-p074 | Le pâton perd environ 100 g d'eau, reste 250 g | V | CAP : 350 → 250 g | — |
| p076 | Énergie : près de 4,5 % du CA « d'une boulangerie » ; écran 4,48 %, données 2024 | O | Sud Radio / Fiducial 2025 : « Coût de l'énergie : 4,48 % du chiffre d'affaires » (résultats 2024, 400 points de vente). C'est une moyenne, pas une boulangerie type | ✔ « …du chiffre d'affaires des boulangeries, en moyenne. » |
| p079-p080 | L'OFPM décortique la baguette courante, boulangeries et supermarchés confondus | V | OFPM : baguette courante, « tous circuits de vente confondus » (artisans, industrie, GMS) | — |
| p081 | Prix moyen 2025 : un euro et un centime ; écran « 4,05 € le kilo » | V | OFPM / INSEE 4,05 €/kg (série par kg) × 0,25 = 1,0125 €. Cohérent avec 2021 : 3,58 × 0,25 = 0,90 €, chiffre INSEE cité par la filière | — |
| p083 | Blé 6 c, meunier 7 c | V | OFPM 2025 | — |
| p084 | TVA à 5,5 % : cinq centimes | V / O | 0,21 × 0,25 = 0,0525 € ; 4,05 / 1,055 = 3,839 € HT. Sigle « TVA » à épeler pour la voix IA | ✔ « T V A » |
| p085 | Après le moulin : 83 centimes ; écran « artisans, usines, magasins » | V | OFPM : marge brute de l'aval 3,33 × 0,25 = 0,8325 € ; tous les acteurs « depuis la transformation de la farine jusqu'à la vente » | — |
| p087 | Décomposition 0,06 + 0,07 + 0,83 + 0,05 = 1,01 € ; blé « à peine six pour cent du prix HT » | V | OFPM, graph. 172 : 6,2 % ; somme exacte | — |
| p088 | Après le moulin : près de 87 % | V | OFPM, graph. 172 : 86,7 % | — |
| p089-p090 | Ce n'est pas le bénéfice du boulanger ; la marge brute paie salaires, énergie, loyer, levure ; écran « Pas un bénéfice » | O | La voix est juste. L'écran l'était moins : la marge brute *contient* le bénéfice, elle n'en est pas le contraire | ✔ écran → « Le bénéfice, s'il en reste » |
| p091 | Elle concerne aussi les usines et les supermarchés | V | OFPM (périmètre) | — |
| p092-p093 | 2022 : le blé atteint 11,4 % du prix HT | V | OFPM, graph. 172 : 11,4 % | — |
| p094 | Le blé a reculé d'environ 4 c par baguette ; écran 0,10 → 0,06 € | V | 0,41 × 0,25 = 10,25 c → 6,0 c, soit −4,25 c | — |
| p095 | La baguette a pris environ 8 c ; surtitre « 0,94 € → 1,01 € » | O | 3,74 → 4,05 €/kg, soit +7,75 c par baguette (juste). Mais le surtitre arrondi faisait lire +7 c sous un punch « + 8 » | ✔ surtitre → « OFPM : 3,74 €/kg (2022) → 4,05 €/kg (2025), soit + 7,75 c pour 250 g » |
| p096 | L'observatoire pointe les coûts de l'aval : énergie, salaires | V | OFPM : « coûts de production étant toujours élevés (énergie, salaires) » | — (voir note d'équilibre plus bas) |
| p099 | 56 heures d'ouverture par semaine en moyenne | V | Fiducial 2026 : « ouverture hebdomadaire moyenne de 56 heures » | — |
| p100 | Baguette en boulangerie : 1,12 € en 2026 | V | Fiducial 2026 : « Prix de la baguette : 1,12 € (en 2025 : 1,10 €) » ; échantillon de 400 clients Fiducial (surtitre présent) | — |
| p101 | Ratios sur 1,06 € HT : salaires ≈ 0,43, matières ≈ 0,33, loyer ≈ 0,06, énergie ≈ 0,05 | O | Fiducial 2026 : personnel 41 % (IS), matières 31 %, loyers 6 %. L'énergie n'est pas isolée en 2026 (elle est dans les 13 % d'« autres charges externes ») : elle vient de Fiducial 2025. Calculs : 1,12 / 1,055 = 1,06 ; ×0,41 = 0,435 ; ×0,31 = 0,33 ; ×0,06 = 0,064 ; ×0,0448 = 0,048 | ✔ source « …; énergie : Fiducial 2025 (données 2024) » |
| p102-p104 | Salaires environ 43 c, le plus gros poste ; matières 33 c ; loyer 6 c ; énergie 5 c | V | idem (43,5 c avec 1,0616 € : « environ » couvre l'écart) | — |
| p105 | Bénéfice net : environ 3 c par baguette | O | Fiducial 2026 : résultat net 3 % (IS). C'est une illustration (ratio moyen de toute l'activité), pas une mesure, alors que la voix l'affirmait avant la mise en garde de p106 | ✔ « Et le bénéfice net ? Sur ce calcul, environ trois centimes par baguette. » |
| p106 | Les ratios couvrent toute l'activité | V | Fiducial (ratios globaux du point de vente) | — |
| p107 | À son compte, le patron affiche 11 %, sa paie est dedans | V | Fiducial 2026 : 11 % à l'IR ; à l'IR, la rémunération du dirigeant est dans le résultat | — |
| p108 | « Ce que tu paies surtout, ce sont des heures humaines. Souvent de nuit. » | O | Le personnel est le premier poste (41 %), pas la majorité. « Souvent de nuit » relève du savoir commun, sans F.. | ✔ « surtout » → « d'abord » |
| p110 | Environ 35 000 boulangeries, contre 55 000 en 1970 | V | CNBPF DP 2025 : 35 000 ; AFP 30/11/2022 : environ 55 000 en 1970 (une pour 790 habitants), environ 400 fermetures par an | — |
| p111-p112 | 11 janvier 2022 : Leclerc bloque sa baguette à 29 c maximum, pendant au moins 4 mois | V | Pleinchamp 12/01/2022 : annonce sur RMC le 11/01, 0,29 € pour 250 g, « au moins quatre mois » | — |
| p113 | Un concurrent s'aligne neuf jours après ; la filière dénonce une opération « démagogique » | V | Connexion France : Lidl à 0,29 € le 20/01/2022 (20 − 11 = 9 jours) ; communiqué AGPB, Intercéréales et ANMF : « démagogique » | — |
| p114 | Pâtons d'usine surgelés et cuits en magasin, présentés comme « le secret » de la baguette Leclerc | **R** | Rien de tel n'est sourcé pour Leclerc ; Que Choisir 2025 et 2026 ne parlent que des terminaux de cuisson et des GMS en général | ✔ voir ROUGE |
| p115 | « C'est aussi un prix d'appel » (affirmé comme un fait sur Leclerc) | O | Le mot « produit d'appel » vient de la filière (ANMF, Pleinchamp) ; Leclerc parle de « produit phare » | ✔ « Pour la filière, c'est un produit d'appel, pour faire venir les clients. » (faits F35, F36) |
| p116 | « L'enseigne dit ne pas vendre à perte » ; premier prix aujourd'hui : 28 c ; écran 0,28 € (« Premier prix ») contre 1,12 € (« Boulangerie ») | O | Journal de l'économie : Leclerc affirme garder une marge ; Que Choisir 2026 : 0,28 € chez Lidl, Aldi et Leclerc, *relevé de mars 2026*. L'écran comparait un minimum à une moyenne sans le dire | ✔ « Leclerc affirme y garder une marge. En mars deux mille vingt-six, le premier prix : vingt-huit centimes. » ; écran « Le moins cher en supermarché » contre « Moyenne en boulangerie », source « UFC-Que Choisir (mars 2026) ; Fiducial 2026 » |
| p117-p118, p120 | « Une baguette à 28 c… qui la paie vraiment ? Le boulanger ? L'agriculteur ? Ou toi, sur le reste du caddie ? » | O (à surveiller) | Question ouverte, pas une affirmation. Elle suggère pourtant une vente sous le coût ou une compensation, que rien ne source (Leclerc affirme garder une marge) | Non modifié (boucle ouverte voulue). Ne rien ajouter qui y réponde par l'affirmative sans source |
| — | Liberté des prix (ordonnance du 01/12/1986, pain libre au 01/01/1987) | V (absent du script) | Réponse ministérielle AN 2011 ; Connexion France : contrôle arrêté le 1er janvier 1987 | — |
| — | UNESCO, 30/11/2022 | V (absent du script) | AFP / Le Petit Journal 30/11/2022 ; ONU Info | — |

**Comptage :** 4 ROUGE (p052, p059, p067, p114). 16 ORANGE (p003, p027, p034, p043, p066, p068, p076, p084, p090, p095, p101, p105, p108, p115, p116 corrigés ; p117-p118 à surveiller). 52 lignes VERT pour le script, plus 2 faits vérifiés qui n'y figurent pas (1987, UNESCO).

## Arithmétique (recontrôlée)

- 0,24 + 0,27 + 3,33 + 0,21 = 4,05 €/kg ✓ → × 0,25 : 6,0 + 6,75 + 83,25 + 5,25 = 101,25 c → 6 + 7 + 83 + 5 = 101 c ✓
- 4,05 / 1,055 = 3,839 € HT ; TVA 0,211 €/kg ✓ ; parts HT : 0,24 / 3,84 = 6,25 % (OFPM : 6,2 %), 3,33 / 3,84 = 86,7 % ✓
- 2022 → 2025 : blé −4,25 c ; prix +7,75 c ✓
- 6 × 10⁹ / (365 × 86 400) = 190,3 par seconde ✓
- 201 €/t = 0,201 €/kg ; 4,05 / 0,201 = 20,1 ✓
- 350 × 1 000 / 1 663 = 210,5 g de farine ; 210 / 0,786 = 267 g de blé ✓ ; 350 − 250 = 100 g d'eau ✓
- 1,12 / 1,055 = 1,062 € HT ; 41 % = 0,435 ; 31 % = 0,329 ; 6 % = 0,064 ; 4,48 % = 0,048 ; 3 % = 0,032 ✓
- Leclerc → Lidl : du 11 au 20 janvier 2022 = 9 jours ✓

## Nombres dans la voix (voix IA)

Aucun chiffre n'est écrit dans un champ `texte`, tout est en toutes lettres et a été contrôlé par script. Le seul sigle, « TVA », est maintenant épelé « T V A ». « T soixante-cinq » se prononce correctement. À écouter au premier rendu : « T V A » et « Le T, c'est le type » (la lettre isolée doit se dire « té »).

## Équilibre et risques juridiques

- **Leclerc** : nommé seulement pour des faits datés et sourcés (annonce du 11/01/2022, 29 c, au moins 4 mois, et sa propre affirmation sur la marge). La pâte surgelée n'est plus rattachée à l'enseigne. Lidl n'est pas nommé (« un concurrent ») et Aldi ne l'est pas non plus.
- **Boulangers** : le « 3 c de bénéfice » est maintenant dit comme un calcul, et la mise en garde suit (p106). Les 83 c sont toujours présentés comme une marge brute de toute la chaîne, jamais comme un gain du boulanger.
- **Note d'équilibre (VERT, facultatif)** : l'OFPM ajoute que les marges brutes de la meunerie et de l'aval restent au-dessus de leur niveau d'avant l'inflation. Le script ne cite que l'explication par les coûts. Ce n'est pas faux, mais c'est incomplet. On peut l'ajouter dans une future version si un plan se libère.

## À surveiller

1. p117-p118 et la carte p120 : question ouverte. Ne pas y répondre plus tard par « vendue à perte » sans source.
2. Les 270 g de blé et les 210 g de farine sont des calculs (confiance B) : garder « environ » partout, y compris dans la miniature et le titre.
3. Prix du blé : 201 €/t est la moyenne 2025 au rendu Rouen. La série OFPM utilise le départ Eure-et-Loir (environ 180 €/t). Ne pas les mélanger dans la description.
4. Fiducial = échantillon de 400 clients, pas un recensement : le surtitre de p100 le dit, il faut le garder.
5. Corrections faites dans `01b_recherche.md` ? Non : seuls `plans.json` et le script ont été modifiés. Note pour le documentaliste : F36 (Que Choisir 2025) parle des terminaux de cuisson en général, pas de la baguette Leclerc ; F43 et F46 sont précisés plus haut.
