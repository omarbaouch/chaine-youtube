# Le cacao s'effondre. Ta tablette, non. Pourquoi ? — script v1

> Slug `chocolat` · scénariste · 03/11/2026 · mode automatique (aucune validation demandée).
> **120 plans · 1 351 mots de narration** (compteur du générateur : un mot élidé comme « l'arbre » compte pour un) ·
> **durée estimée ≈ 9 min 25** (voix ≈ 8 min 40 à 2,6 mots/s, plus 5 comptes à rebours, 3 cartes, 1 plan muet).
> Voix : Edge Vivienne (narratrice, « je » / « tu ») et Rémy (`"voix": "sceptique"`, 5 répliques de 10 à 15 mots).
> Ton : enquête complice, jamais moralisatrice, aucune marque accusée (Lindt n'est nommé que pour l'histoire du conchage, 1879).
> Plans machine : `videos/chocolat/plans.json` (sans `media_ref` : au repérage de les choisir). Chaque plan a un champ
> `faits` (identifiants F.. de `01b_recherche.md`), ignoré par `construire.mjs`.

## Contrôle règle n°7 bis (prioritaire)

| # | Contrôle | Résultat | Où |
|---|---|---|---|
| 1 | Aucune réponse chiffrée avant sa révélation | OK. Les 30 premières secondes ne contiennent aucun chiffre-réponse : seulement le prix de la tablette (prémisse, F10) et les trois choix de la devinette. La part du planteur (13 c aujourd'hui) n'est donnée qu'à **p095-p097 (≈ 7:20)**, après 7 minutes d'attente ; sa part 2018 (11 c) n'apparaît qu'à la découpe de « La vérité » (p080, ≈ 6:10). Chaque part de suspect est révélée dans sa propre partie, après une question ou une devinette. | p005 → p094 |
| 2 | Frame 0 non noire | OK sur le papier : p001 = rush de fèves de cacao qui tombent + mots « LE CACAO S'EFFONDRE » dès 0,2 s. Au repérage : refuser un rush qui commence par un fondu au noir, sinon `debut_media` +1 s (règle n°12). | p001 |
| 3 | Pas de carte titre ni « Partie 01 » avant 30 s | OK. Carte titre p010 à **≈ 0:34**, aucune carte de partie numérotée (les suspects s'ouvrent par une fiche `suspect`, pas par une carte). | p010 |
| 4 | Au moins 2 questions ouvertes à 30 s | OK, trois : « qui a pris la différence ? » (p003, 0:07), devinette « combien pour le planteur ? » (p005, 0:15, sans réponse), « une graine amère… une tablette qui claque » (p007, 0:24) ; puis Laurent annoncé et gardé pour la fin (p008-p009, 0:28-0:34). | p003-p009 |
| 5 | Aucune séquence de plus de 6 s sans changement d'image | OK pour 114 plans sur 120 (moyenne 4,7 s). Les 5 devinettes `devine` durent 7,8 à 9 s, mais le compte à rebours change l'image chaque seconde puis la réponse s'allume ; p113 (citation finale de Laurent, ≈ 6,3 s) : laisser la liste s'animer en deux temps. | p016, p024, p058, p074, p094, p113 |

Autres contrôles faits par script : jamais deux formats identiques consécutifs ; 43 rushes sur 120 (36 %, au-dessus du tiers) ;
rush 43 · schéma 31 · écran partagé 22 · mosaïque 21 · titre 3 ; 7 `punch` (6 %), jamais deux à moins de 5 plans d'écart ;
un seul `heros` par schéma ; chaque schéma chiffré a un champ `source` ; aucun chiffre écrit en chiffres dans un texte lu ;
aucune phrase de moins de 6 mots (les plans découpés au milieu d'une phrase sont lus d'un seul souffle par `voix.py`) ;
transitions `coupe` partout, `fondu` à l'entrée de chaque partie (carte titre, fiche suspect 02 à 05, carte « La vérité », Laurent) ;
aucun whoosh (sons : impact, riser, tick ; le `flash` du « clac » à p055). Rythme : plans de 2,5 à 4,8 s de voix avant 1:00
(p005, la devinette, fait 4,8 s), puis 3 à 6 s.

## L'arc

| Partie | Début estimé | Ce qu'on montre (« comment c'est fait ») | Ce qu'on révèle (« combien ça coûte ») | Émotion |
|---|---|---|---|---|
| Ouverture | 0:00 | fèves, rayon, tablette qui casse, cabosse | la question, la devinette, Laurent annoncé | tension, injustice |
| 01 Le planteur | 0:37 | cabosse sur le tronc, machette, pulpe blanche, fermentation, séchage | 2 cabosses par tablette ; prix garanti record 2 800 F CFA ; verdict « À suivre » | gourmandise, surprise (amer) |
| 02 Négociant et broyeur | 2:12 | sacs, port, cargo, torréfaction, broyage, pressage | 7 c + 6 c sur 1 € ; « Innocents » | curiosité |
| 03 La marque | 3:19 | conchage (Lindt, Berne, 1879), tempérage, cristaux forme V, moulage | 37 c sur 1 €, dont ≈ 9 c de marge ; « Coupable ? » | émerveillement puis soupçon |
| 04 Le supermarché | 4:40 | rayon, caisse, Pâques | +36 % en 4 ans, +4 % en 2026 ; 32 c, dont ≈ 8 c de marge ; « Coupable ? » | agacement |
| 05 L'État | 5:20 | caisse, ticket, tablette au lait | TVA 5,5 % (≈ 5 c) contre 20 % sur la plupart des tablettes au lait ; « Petit joueur » | surprise légère |
| Abonnement | 6:00 | — | — | — |
| La vérité (PIC) | 6:05 | l'euro découpé sur une vraie tablette | 11 c (2018) ; 70 % de la valeur et 90 % des marges ; record > 12 900 $, plus bas 2 846 $ ; 2 800 → 1 200 F CFA ; **13 c, de 11 % à 5 %** ; la défense (achats à terme) ; cacao remonté vers 5 400 $, planteur bloqué à 1 200 | indignation, puis nuance |
| Laurent, puis la fin | 8:08 | village, plantation (images d'illustration) | 54 ans, planteur depuis 1996, pas de toit ; engrais = 18 kg de cacao ; « Je ne veux pas que mes enfants soient planteurs comme moi » ; question ouverte ; prochaine enquête : le lait UHT | émotion, puis question |

## Faits utilisés (tous dans `01b_recherche.md`, aucun autre chiffre)

| Fait | Ce qu'on dit / affiche | Plans |
|---|---|---|
| F01 | étude BASIC, prix moyen d'une tablette noire, ramené à « un euro de chocolat noir » | p036 |
| F02 | parts BASIC 2018 sur 1 € : planteur 11 c, négociant 7 c, broyeur 6 c, ingrédients 2 c, marque 37 c, distribution 37 c (dont TVA) | p037, p042-p043, p050, p059, p061, p067, p080-p081 |
| F03 | marges BASIC : marque ≈ 9 c, supermarché ≈ 8 c ; taxes ivoiriennes ≈ 2 c ; « l'État français prend trois fois plus que l'État ivoirien » (4,9 c contre 1,6 c) | p037, p057, p060, p067-p068, p073, p077, p080 |
| F05 | marques + distributeurs : 70 % de la valeur, 90 % des marges (moyenne) ; pays producteurs < 7,5 % des marges | p082-p083, p116 |
| F06 | collecte, transport, taxes à l'export | p034-p035 |
| F10 | tablette noire 70 % de grande marque ≈ 2,60 € (mai 2026) | p005, p093, p095, p097 |
| F12, F14 | record > 12 900 $/t en décembre 2024 ; « cinq fois sa moyenne d'avant » (2 525 $/t en 2012-2022) | p001, p085-p087 |
| F16, F18 | plus bas 2 846 $/t le 02/03/2026 ; ≈ 5 394 $/t le 02/11/2026 (jamais « 3 000 $ aujourd'hui ») | p001-p002, p087, p100 |
| F19, F33 | prix garanti record 2 800 F CFA/kg le 01/10/2025 = 4,27 €/kg | p026-p030, p089, p096-p097, p107 |
| F21 | 1 200 F CFA/kg annoncé le 04/03/2026, −57 % ; citation du ministre Bruno Nabagné Koné | p030, p088-p092, p095, p097, p102-p103, p112 |
| F22 | 1 200 F CFA reconduit pour 2026-2027 ; « environ 5 millions de personnes » ; Côte d'Ivoire ≈ 40 % (affiché en comparaison seulement) | p091, p101-p102, p111 |
| F24 | Afrique de l'Ouest | p012 |
| F28 | Pâques : +36 % en 4 ans contre 14 % d'inflation ; +4 % en 2026 | p002, p065-p066, p102 |
| F29, F30 | Syndicat du chocolat : cacao « acheté il y a de nombreux mois », parfois au pic ; achats 6 mois à 1 an à l'avance ; distributeurs qui « dénoncent » les hausses (non utilisé à l'antenne, coupé) | p099, p116 |
| F32 | TVA 5,5 % sur le noir, 20 % sur « la plupart des tablettes au lait » (le chocolat de ménage au lait reste à 5,5 %) | p067, p072-p077, p080 |
| F34 | Laurent Koné, 54 ans, planteur depuis 1996, près de Guiglo, torchis, bâche, pas d'électricité ; engrais 22 000 F CFA ; citations exactes (AFP 26/01/2026, reprise Le360 Afrique) | p008-p009, p104-p114 |
| F40-F43 | cabosse 15-20 cm, ≈ 380 g ; 30 à 40 graines ; ouverture « à la machette » (§ 3 : au bâton ou à la machette) | p013-p015, p025 |
| F44-F45 | fermentation ≈ 5 jours, 40-45 °C, sous feuilles de bananier ; séchage 5 à 7 jours, 60 % → 7,5 % d'humidité | p018-p022 |
| F46-F49 | torréfaction (aucune température), broyage en masse, pressage beurre/poudre ; conchage Lindt, Berne, 1879, « de quelques heures à plusieurs jours » ; tempérage ≈ 50 → 27 → 31 °C, six formes de cristaux, forme V | p039-p055 |
| F50-F51 | 70 g de cacao dans une tablette à 70 % ; « à peu près deux cabosses » | p005, p025, p095-p097 |
| § 2.2 (calcul B) | 70 g × 1,83 €/kg ≈ 13 c (depuis mars 2026) ; ≈ 30 c au record ; part ≈ 11 % → ≈ 5 % | p094-p097 |
| § 7 (calcul B) | sac d'engrais 22 000 F CFA = 18 kg de cacao à 1 200 F CFA | p111 |
| § 3 (connaissance générale) | la graine fraîche est amère, la pulpe blanche est sucrée (non chiffré) | p016-p017 |

Non utilisés volontairement (cohérence de Mayer) : travail des enfants (F36), Ghana (F23), production mondiale (F25), commerce
équitable (F27), tablette au lait BASIC (F04). Aucun « rétrécissement », aucun « prix moyen national », aucune température de torréfaction,
aucune durée de conchage chez une marque.

## Décisions consignées (decision_log)

| # | Décision | Raison |
|---|---|---|
| 1 | Devinette du début en `schema` **`liste`** (« 3 c ? / 13 c ? / 50 c ? »), pas en `devine` | Le composant `Devine` (`src/motion/Schemas.tsx`) allume toujours une réponse à la fin du compte à rebours : il révélerait la réponse à 0:20 (règle 7 bis). La vraie `devine` avec la bonne réponse est rejouée à p094 (≈ 7:11). Amélioration possible pour le monteur : une option « sans réponse » dans `Devine`. |
| 2 | Toutes les parts de suspects en « centimes sur un euro de chocolat noir » (BASIC 2018), et UN SEUL calcul 2026 sur la tablette à 2,60 € (la réponse) | Les parts BASIC ne doivent pas être appliquées au prix 2026 (§ 2.3, extrapolation interdite). Un euro rend les pourcentages lisibles (11 % = 11 c) et l'année est affichée (`surtitre` « Étude BASIC · données 2018 », titre de la découpe « 1 € de chocolat noir (2018) »). |
| 3 | Distribution coupée en supermarché 32 c (hors TVA) + État 5 c | TVA 5,5 % d'un prix TTC = 5,2 % ; hypothèse « prix BASIC TTC » signalée par la recherche (§ 2.1), indiquée dans les `source`. Somme de la découpe : 37 + 32 + 5 + 7 + 6 + 2 + 11 = 100. |
| 4 | Le verdict du planteur reste « À suivre » à 2:10 et devient « Victime » à 8:03 | Boucle imbriquée : son prix record (2 800) est posé tôt, sa chute gardée pour « La vérité ». |
| 5 | Réponse à la question centrale formulée honnêtement : la baisse est « arrivée chez le planteur », pas « dans ton rayon » ; la défense des achats à terme est dite, puis la remontée du cacao (≈ 5 400 $) et le prix planteur resté bloqué | Pas de procès d'un seul coupable (brief, décision 6) ; la fin reste une vraie question (« achats à terme, ou marges ? »). |
| 6 | Laurent : voix off + citations exactes écrites (`ecran_partage` / `liste`), images de planteurs anonymes avec « Image d'illustration » | Règle n°13 et § 5 de la recherche : aucun extrait AFP, aucune photo de lui. La citation 1 est lue en deux plans (p109-p110) et affichée en entier. |
| 7 | Pas de carte « Partie 0X » : la carte titre (0:34) puis des fiches `suspect` avec `fondu`, et une carte « La vérité » | Règle 7 bis ; deux cartes de suite seraient deux formats `titre` consécutifs. |
| 8 | Pas de devinette sur le négociant ni sur Pâques (coupées à l'écriture) | Durée : 10 min 55 au premier jet, ramenée à ≈ 9 min 25 ; on garde 5 `devine` (goût, cabosses, marque, TVA lait, planteur). |

## Points d'attention pour la suite

- Rushes à risque (vidéos rares, photos fréquentes) : cabosse ouverte, fermentation sous feuilles, séchage, conche, portrait de Rodolphe Lindt (Commons, domaine public probable). Le repérage passe par Commons d'abord pour ces plans ; garder le plafond d'un tiers de photos (p013-p031 surtout).
- p080 (`decoupe`) : il faut une photo de tablette entière, vue de dessus, sur fond uni, puis régler `zone` / `zone_y` après l'avoir regardée (règle n°12).
- p055 (« clac ») et p003 (casse d'ouverture) : deux rushes différents (un rush ne sert qu'une fois).
- Prononciation à écouter : « Guiglo », « Rodolphe Lindt », « francs C F A », « U H T », « Agence France-Presse », « Bruno Nabagné Koné » (nom seulement à l'écran).
- `sources.md` : déjà rempli par la documentaliste ; ajouter seulement la ligne « calcul engrais = 18 kg » si le relecteur le demande.

---

## Ouverture

**p001** · 0:00.0 · `rush` · tension
> NARRATRICE : Le prix du cacao s'est effondré depuis son record.
- À l'écran : couche mots « LE CACAO S'EFFONDRE »
- Rush visé : cocoa beans pouring close up ; cocoa beans falling slow motion ; pile of roasted cocoa beans ; cocoa beans hands close up
- Faits : F12, F18

**p002** · 0:03.6 · `ecran_partage` · tension
> NARRATRICE : Mais ta tablette, au rayon, elle, n'a pas baissé.
- À l'écran : LISTE « Depuis le record » : Le cacao ↓ en chute | Ta tablette pas de baisse [héros] · source : Cours ICE (Trading Economics, 02/11/2026) ; UFC-Que Choisir, 01/04/2026 · média réel à gauche
- Rush visé : supermarket chocolate shelf ; chocolate bars on store shelf ; hand taking chocolate bar from shelf
- Faits : F18, F28

**p003** · 0:07.2 · `rush` · tension
> NARRATRICE : Alors, une seule question : qui a pris la différence ?
- À l'écran : PUNCH « QUI ? » à 2.4 s · sons : impact@2.4
- Rush visé : dark chocolate bar breaking close up ; breaking chocolate bar slow motion ; snapping chocolate bar pieces ; chocolate bar split in two hands

**p004** · 0:10.8 · `mosaique` · tension
> SCEPTIQUE : Facile, c'est le cacao qui rend le chocolat si cher !
- À l'écran : mosaïque : Le cacao + Le chocolat
- Rush visé : cocoa beans in jute sack close up ; stack of chocolate bars close up

**p005** · 0:14.8 · `schema` · tension
> NARRATRICE : Devine : sur une tablette à deux euros soixante, combien pour le planteur ?
- À l'écran : LISTE « Combien pour le planteur ? » : A 3 c ? | B 13 c ? | C 50 c ? · source : Tablette noire 70 %, grande marque, ≈ 2,60 € (Que Choisir, mai 2026) · réponse plus tard · sons : tick@3.4, tick@4.0
- Rush visé : cocoa pods on tree trunk ; cacao tree pods close up ; cocoa plantation forest
- Faits : F10, F21, F50

**p006** · 0:19.6 · `rush` · tension
> NARRATRICE : On va suivre une fève, de l'arbre jusqu'à ta main.
- À l'écran : plein écran réel
- Rush visé : cocoa pod hanging on tree ; cocoa tree pods sunlight ; cacao fruit on branch close up ; cocoa plantation walking

**p007** · 0:23.6 · `mosaique` · tension
> NARRATRICE : Cinq suspects, une graine amère, et une tablette qui claque.
- À l'écran : mosaïque : Une graine amère + Une tablette qui claque · couche mots « 5 SUSPECTS »
- Rush visé : fresh cocoa beans white pulp close up ; chocolate bar snap close up slow motion

**p008** · 0:27.6 · `ecran_partage` · emotion
> NARRATRICE : Et à la fin, je te lirai les mots
- À l'écran : LISTE « Le témoin » : Laurent [héros] | Planteur de cacao depuis 1996 | Côte d'Ivoire · source : AFP, 26/01/2026 (reprise Le360 Afrique) · média réel à gauche · couche source « Image d'illustration »
- Rush visé : cocoa farmer Ivory Coast ; African farmer cocoa plantation ; cocoa farmer carrying pods ; cocoa farmer hands pods
- Faits : F34

**p009** · 0:31.2 · `rush` · emotion
> NARRATRICE : de Laurent, planteur de cacao depuis trente ans.
- À l'écran : couche source « Image d'illustration »
- Rush visé : cocoa farmer hands holding beans ; farmer hands cocoa beans close up ; cocoa farmer back walking plantation
- Faits : F34

**p010** · 0:34.4 · `titre` · tension · transition fondu
> (sans voix)
- À l'écran : CARTE TITRE « Le cacao s'effondre. Ta tablette, non. » / « Qui a pris la différence ? » · sons : riser@0, impact@0.2
- Rush visé : dark chocolate pieces dark background ; chocolate bar black background slow ; cocoa beans dark background


---

## Suspect 01 — Le planteur

**p011** · 0:37.0 · `schema` · tension · transition fondu
> NARRATRICE : Premier suspect : celui qui fait pousser le cacao.
- À l'écran : FICHE SUSPECT 01 Le planteur
- Rush visé : cocoa farmer harvesting pods ; farmer cutting cocoa pod from tree ; cocoa harvest Ghana farmer

**p012** · 0:40.3 · `rush` · leger
> NARRATRICE : Tout commence sur un arbre d'Afrique de l'Ouest, le cacaoyer.
- À l'écran : plein écran réel
- Rush visé : cacao tree with pods ; cocoa tree trunk pods ; cocoa plantation Ivory Coast ; theobroma cacao tree
- Faits : F24

**p013** · 0:44.2 · `ecran_partage` · leger
> NARRATRICE : Ses fruits, les cabosses, poussent directement sur le tronc.
- À l'écran : CHIFFRE ≈ 380 g — une cabosse de 15 à 20 cm (« ? » jusqu'à 1.6 s) · source : CNUCED, profil produit cacao · média réel à gauche
- Rush visé : cocoa pods growing on trunk ; yellow cocoa pod close up ; red cocoa pod on tree ; cocoa flowers and pods trunk
- Faits : F40

**p014** · 0:47.9 · `rush` · leger
> NARRATRICE : On les cueille, puis on les ouvre à la machette.
- À l'écran : plein écran réel
- Rush visé : opening cocoa pod machete ; cutting cocoa pod open ; cocoa pod split open ; farmer breaking cocoa pod
- Faits : F43

**p015** · 0:51.9 · `mosaique` · leger
> NARRATRICE : Dedans, trente à quarante graines, enrobées d'une pulpe blanche et sucrée.
- À l'écran : mosaïque : 30 à 40 graines + La pulpe blanche
- Rush visé : cocoa pod open seeds white pulp ; fresh cocoa beans pulp close up
- Faits : F41

**p016** · 0:56.2 · `schema` · tension
> NARRATRICE : Alors, à ton avis… une graine fraîche, elle a quel goût ?
- À l'écran : DEVINETTE « Le goût d'une graine fraîche ? » Sucré / Chocolat / Amer (bonne : Amer) · sons : tick@1.5
- Rush visé : fresh cocoa beans close up ; raw cacao seeds pulp ; cocoa beans in pulp hands

**p017** · 1:04.1 · `rush` · revelation
> NARRATRICE : Amère, très amère : à ce stade, aucun goût de chocolat.
- À l'écran : PUNCH « AMÈRE » à 0.4 s · sons : impact@0.4
- Rush visé : raw cocoa beans pile ; fresh cacao beans macro ; wet cocoa beans close up ; cocoa beans pulp spoon
- Faits : §3

**p018** · 1:08.1 · `ecran_partage` · leger
> NARRATRICE : Le goût naît ensuite, en tas, sous des feuilles de bananier.
- À l'écran : PROCESSUS « Chez le planteur » : Cueillir → Écabosser → Fermenter → Sécher (actif : Fermenter) · source : ICCO ; World Cocoa Foundation · média réel à droite
- Rush visé : cocoa beans fermentation banana leaves ; cocoa fermentation heap ; fermenting cocoa beans covered leaves
- Faits : F44

**p019** · 1:12.4 · `rush` · leger
> NARRATRICE : Pendant environ cinq jours, ça fermente,
- À l'écran : surtitre « ≈ 5 jours de fermentation »
- Rush visé : fermenting cocoa beans wooden box ; cocoa beans fermentation boxes ; turning fermenting cocoa beans ; cocoa fermentation heap leaves
- Faits : F44

**p020** · 1:14.9 · `schema` · leger
> NARRATRICE : et la masse chauffe jusqu'à quarante-cinq degrés.
- À l'écran : CHIFFRE 45 °C — dans le tas qui fermente (40 à 45 °C) (« ? » jusqu'à 1.8 s) · source : ICCO ; World Cocoa Foundation
- Rush visé : cocoa fermentation steam ; fermenting cocoa beans close up ; cocoa beans fermentation box top view
- Faits : F44

**p021** · 1:17.7 · `mosaique` · leger
> NARRATRICE : Ensuite, les fèves sèchent au soleil, de cinq à sept jours.
- À l'écran : mosaïque : Au soleil + Retournées au râteau
- Rush visé : cocoa beans drying sun ; farmer raking cocoa beans drying
- Faits : F45

**p022** · 1:22.1 · `schema` · leger
> NARRATRICE : Leur humidité tombe d'environ soixante à sept et demi pour cent.
- À l'écran : CHIFFRE 7.5 % — d'humidité après séchage (« ? » jusqu'à 2.8 s) · source : World Cocoa Foundation ; ICCO
- Rush visé : cocoa beans drying racks ; cocoa beans drying mats aerial ; dried cocoa beans spread
- Faits : F45

**p023** · 1:26.5 · `rush` · leger
> NARRATRICE : Voilà la matière première de ta tablette : des fèves sèches.
- À l'écran : plein écran réel
- Rush visé : dried cocoa beans close up ; dry cocoa beans pouring hands ; cocoa beans sack filling ; cocoa beans heap dried

**p024** · 1:30.5 · `schema` · tension
> NARRATRICE : Alors, à ton avis… combien de cabosses faut-il pour une seule tablette ?
- À l'écran : DEVINETTE « Combien de cabosses pour une tablette ? » ½ / ≈ 2 / 10 (bonne : ≈ 2) · sons : tick@1.5
- Rush visé : cocoa pods pile harvest ; heap of cocoa pods ; harvested cocoa pods basket

**p025** · 1:38.7 · `rush` · revelation
> NARRATRICE : À peu près deux, pour les soixante-dix grammes de cacao d'une tablette noire.
- À l'écran : PUNCH « ≈ 2 CABOSSES » à 0.5 s · sons : impact@0.5
- Rush visé : two cocoa pods hands ; cocoa pod cut in half ; holding cocoa pod close up ; cocoa pod opened showing beans
- Faits : F42, F50, F51

**p026** · 1:43.9 · `mosaique` · tension
> NARRATRICE : Leur prix, en Côte d'Ivoire, c'est l'État qui le fixe.
- À l'écran : mosaïque : Côte d'Ivoire + Abidjan
- Rush visé : Ivory Coast flag waving ; Abidjan city skyline aerial
- Faits : F19

**p027** · 1:47.9 · `rush` · tension
> NARRATRICE : Le premier octobre deux mille vingt-cinq, il annonce un prix record.
- À l'écran : surtitre « 1er octobre 2025 »
- Rush visé : cocoa farmers weighing sacks ; cocoa beans weighing scale ; cocoa buying center sacks ; cocoa beans bags scale
- Faits : F19

**p028** · 1:52.2 · `ecran_partage` · revelation
> NARRATRICE : Deux mille huit cents francs C F A le kilo, environ quatre euros vingt-sept.
- À l'écran : CHIFFRE 2800 F CFA/kg — prix garanti au planteur ivoirien, record (« ? » jusqu'à 0.6 s) · source : Financial Afrik, 02/10/2025 · média réel à gauche · sons : impact@0.6
- Rush visé : cocoa beans in hands close up ; cocoa beans sack open ; dried cocoa beans pouring
- Faits : F19, F33

**p029** · 1:57.8 · `rush` · tension
> SCEPTIQUE : Avec un prix record pareil, le planteur doit s'en mettre plein les poches !
- À l'écran : couche source « Image d'illustration »
- Rush visé : cocoa farmer smiling plantation ; farmer holding cocoa beans ; cocoa farmer portrait plantation ; cocoa farmer counting

**p030** · 2:02.9 · `mosaique` · tension
> NARRATRICE : Attends un peu : ce record va durer à peine cinq mois.
- À l'écran : mosaïque : Octobre 2025 + … et après ?
- Rush visé : cocoa beans sacks warehouse dark ; cocoa trader inspecting beans
- Faits : F19, F21

**p031** · 2:07.3 · `schema` · tension
> NARRATRICE : Premier suspect, le planteur : son verdict, je le garde pour la vérité.
- À l'écran : FICHE SUSPECT 01 Le planteur — verdict « À suivre »
- Rush visé : cocoa farmer silhouette plantation ; cocoa plantation sunset ; cocoa farmer walking away


---

## Suspect 02 — Le négociant et le broyeur

**p032** · 2:12.1 · `rush` · tension · transition fondu
> NARRATRICE : Maintenant, ces fèves doivent traverser l'océan, et ça se paie.
- À l'écran : plein écran réel
- Rush visé : cargo ship at sea ; container ship ocean aerial ; cargo ship sailing ; cargo ship port leaving

**p033** · 2:16.1 · `schema` · tension
> NARRATRICE : Deuxième suspect, un duo : le négociant qui exporte, et le broyeur.
- À l'écran : FICHE SUSPECT 02 Le négociant et le broyeur
- Rush visé : cocoa sacks port warehouse ; jute sacks stacked warehouse ; cocoa export warehouse

**p034** · 2:20.5 · `rush` · leger
> NARRATRICE : Le négociant collecte les sacs, les transporte, et les charge au port.
- À l'écran : plein écran réel
- Rush visé : workers carrying sacks port ; jute sacks loading truck ; sacks loaded on ship crane ; dock workers sacks
- Faits : F06

**p035** · 2:25.2 · `ecran_partage` · leger
> NARRATRICE : Sur chaque kilo exporté, l'État ivoirien prélève aussi ses taxes.
- À l'écran : PROCESSUS « Du planteur au bateau » : Collecte → Transport → Taxes → Port (actif : Taxes) · source : BASIC 2020 (données 2018) · média réel à gauche
- Rush visé : port cranes containers Africa ; Abidjan port containers ; cocoa sacks warehouse port
- Faits : F06

**p036** · 2:29.2 · `rush` · tension
> NARRATRICE : Imagine un euro dépensé en chocolat noir : combien en garde le négociant ?
- À l'écran : surtitre « Étude BASIC · données 2018 »
- Rush visé : euro coin on table close up ; euro coin spinning ; hand placing coin on table ; euro coins close up
- Faits : F01

**p037** · 2:34.0 · `ecran_partage` · revelation
> NARRATRICE : Environ sept centimes, dont presque deux centimes de taxes pour l'État ivoirien.
- À l'écran : CHIFFRE 0.07 € — pour le négociant, sur 1 € de chocolat noir (« ? » jusqu'à 1.2 s) · source : BASIC 2020, données 2018, tablette noire (9,32 €/kg), ramené à 1 € · média réel à droite
- Rush visé : cocoa sacks being weighed ; cocoa sacks truck loading ; sacks port warehouse workers
- Faits : F02, F03

**p038** · 2:38.7 · `rush` · leger
> NARRATRICE : En Europe, le broyeur prend le relais, et là, tout commence à chauffer.
- À l'écran : plein écran réel
- Rush visé : roasting cocoa beans machine ; cocoa roaster factory drum ; cocoa beans roasting industrial ; roaster drum rotating beans

**p039** · 2:43.9 · `mosaique` · leger
> NARRATRICE : D'abord, on torréfie les fèves, un peu comme du café.
- À l'écran : mosaïque : Torréfaction + Fèves grillées
- Rush visé : roasting cocoa beans pan ; roasted cocoa beans close up
- Faits : F46

**p040** · 2:47.9 · `schema` · leger
> NARRATRICE : On les décortique, puis on les broie en pâte liquide : la masse de cacao.
- À l'écran : PROCESSUS « Chez le broyeur » : Torréfier → Concasser → Broyer → Presser (actif : Broyer) · source : World Cocoa Foundation
- Rush visé : cocoa liquor grinding ; cocoa mass liquid flowing ; grinding cocoa nibs paste
- Faits : F46

**p041** · 2:53.4 · `mosaique` · leger
> NARRATRICE : On la presse ensuite : d'un côté le beurre de cacao, de l'autre la poudre.
- À l'écran : mosaïque : Beurre de cacao + Poudre de cacao
- Rush visé : cocoa butter pieces close up ; cocoa powder falling slow motion
- Faits : F46

**p042** · 2:59.0 · `rush` · revelation
> NARRATRICE : Pour tout ce travail, le broyeur garde environ six centimes.
- À l'écran : compteur → 6 c
- Rush visé : cocoa grinding mill factory ; cocoa processing plant machines ; industrial cocoa press ; cocoa factory machinery
- Faits : F02

**p043** · 3:03.0 · `schema` · revelation
> NARRATRICE : Sept et six centimes, c'est trop peu : ce duo n'est pas notre voleur.
- À l'écran : FICHE SUSPECT 02 Le négociant et le broyeur — verdict « Innocents »
- Rush visé : cocoa beans sacks warehouse ; cargo ship port ; cocoa factory
- Faits : F02

**p044** · 3:08.1 · `rush` · tension
> NARRATRICE : À ce stade, ton chocolat n'est qu'une pâte amère qui gratte la langue.
- À l'écran : plein écran réel
- Rush visé : cocoa liquor close up ; liquid cocoa mass stirring ; dark cocoa paste spoon ; cocoa mass melting

**p045** · 3:13.3 · `mosaique` · tension
> NARRATRICE : Ce qui le rend fondant vient de Suisse, d'un homme dont tu connais le nom.
- À l'écran : mosaïque : Suisse + Une fabrique de chocolat
- Rush visé : Bern old town aerial ; vintage chocolate factory
- Faits : F47


---

## Suspect 03 — La marque

**p046** · 3:19.2 · `schema` · tension · transition fondu
> NARRATRICE : Troisième suspect : la marque, celle qui signe l'emballage.
- À l'écran : FICHE SUSPECT 03 La marque
- Rush visé : chocolate bars wrapped on shelf ; chocolate wrapper close up ; chocolate packaging

**p047** · 3:22.4 · `rush` · leger
> NARRATRICE : Notre inventeur, c'est Rodolphe Lindt, à Berne, en mille huit cent soixante-dix-neuf.
- À l'écran : surtitre « Berne, 1879 »
- Rush visé : Bern Switzerland old town ; Bern river Aare aerial ; Bern clock tower street ; Swiss old town street
- Faits : F47

**p048** · 3:27.2 · `ecran_partage` · leger
> NARRATRICE : Sa machine brasse la pâte longtemps, et elle devient fondante.
- À l'écran : LISTE « Le conchage » : Rodolphe Lindt, Berne 1879 | Brasser la pâte des heures à des jours [héros] · source : Chocosuisse ; World Cocoa Foundation · média réel à gauche
- Rush visé : Rodolphe Lindt portrait ; chocolate conche machine ; chocolate mixing stirring
- Faits : F47, F48

**p049** · 3:31.2 · `rush` · leger
> NARRATRICE : Ça s'appelle le conchage, et ça dure de quelques heures à plusieurs jours.
- À l'écran : plein écran réel
- Rush visé : chocolate conching machine ; chocolate conche mixing ; chocolate mixer factory stirring ; liquid chocolate machine rollers
- Faits : F48

**p050** · 3:36.3 · `mosaique` · leger
> NARRATRICE : On y ajoute le sucre : les autres ingrédients ne pèsent qu'environ deux centimes.
- À l'écran : mosaïque : Le sucre + Le mélange
- Rush visé : sugar pouring close up ; chocolate mixing machine sugar
- Faits : F02

**p051** · 3:41.5 · `rush` · leger
> NARRATRICE : Reste l'étape la plus délicate : le tempérage, une affaire de degrés.
- À l'écran : plein écran réel
- Rush visé : chocolate tempering marble slab ; chocolatier tempering chocolate ; tempering chocolate spatula ; chocolate thermometer tempering
- Faits : F49

**p052** · 3:45.8 · `schema` · leger
> NARRATRICE : On chauffe vers cinquante degrés, on refroidit, puis on remonte vers trente et un.
- À l'écran : PROCESSUS « Le tempérage (chocolat noir) » : Chauffer ≈ 50 °C → Refroidir ≈ 27 °C → Remonter ≈ 31 °C (actif : Remonter ≈ 31 °C) · source : theGIST (Université de Glasgow), 2015
- Rush visé : melted chocolate thermometer ; chocolate tempering machine ; melting chocolate bowl
- Faits : F49

**p053** · 3:51.4 · `ecran_partage` · leger
> NARRATRICE : Le beurre de cacao peut cristalliser de six façons,
- À l'écran : CHIFFRE 6 — formes de cristaux possibles (« ? » jusqu'à 1.6 s) · source : theGIST (Université de Glasgow), 2015 · média réel à droite
- Rush visé : cocoa butter close up ; melted chocolate surface close up ; chocolate cooling crystallizing
- Faits : F49

**p054** · 3:55.0 · `schema` · leger
> NARRATRICE : et une seule est la bonne, la forme cinq.
- À l'écran : LISTE « 6 formes de cristaux » : Formes I à IV molles, ternes | Forme V brillante, cassante [héros] | Forme VI voile blanc · source : theGIST (Université de Glasgow), 2015
- Rush visé : shiny dark chocolate surface close up ; glossy chocolate bar macro ; chocolate surface light reflection
- Faits : F49

**p055** · 3:58.6 · `rush` · revelation
> NARRATRICE : C'est elle qui rend ta tablette brillante, et qui lui donne ce clac.
- À l'écran : flash à 3.2 s · sons : impact@3.2
- Rush visé : chocolate bar snapping close up slow motion ; breaking dark chocolate bar macro ; chocolate snap sound close up
- Faits : F49

**p056** · 4:03.8 · `mosaique` · leger
> NARRATRICE : Ensuite, on coule dans des moules, on refroidit, on démoule, et on emballe.
- À l'écran : mosaïque : Moulage + Démoulage + Emballage
- Rush visé : chocolate filling molds factory ; chocolate bars demolding ; chocolate bar packaging machine

**p057** · 4:08.9 · `rush` · tension
> NARRATRICE : Usines, salaires, emballages : tout ce savoir-faire, la marque le facture.
- À l'écran : plein écran réel
- Rush visé : chocolate factory workers ; chocolate production line conveyor ; chocolate factory interior ; chocolate bars conveyor belt
- Faits : F03

**p058** · 4:12.9 · `schema` · tension
> NARRATRICE : Alors, à ton avis… sur un euro de chocolat noir, combien pour la marque ?
- À l'écran : DEVINETTE « Sur 1 €, combien pour la marque ? » 12 c / 25 c / 37 c (bonne : 37 c) · sons : tick@1.5
- Rush visé : chocolate bars stacked ; chocolate bars conveyor ; chocolate factory packaging

**p059** · 4:21.9 · `rush` · revelation
> NARRATRICE : Trente-sept centimes, de loin le plus gros morceau vu jusqu'ici.
- À l'écran : compteur → 37 c
- Rush visé : stack of chocolate bars ; many chocolate bars piled ; chocolate bars falling ; chocolate bars warehouse
- Faits : F02

**p060** · 4:25.9 · `ecran_partage` · leger
> NARRATRICE : Mais sa vraie marge, une fois tout payé, c'est environ neuf centimes.
- À l'écran : DECOMPOSITION « Les 37 c de la marque » : Coûts 25.3, Taxes 2.3, Marge 9.4 [héros] · source : BASIC 2020, données 2018 (marge 0,88 €/kg sur 9,32 €/kg) · média réel à gauche
- Rush visé : chocolate factory production line ; chocolate bars packaging line ; chocolate factory worker
- Faits : F03

**p061** · 4:30.6 · `schema` · tension
> NARRATRICE : La marque prend le plus gros morceau : je la note coupable, pour l'instant.
- À l'écran : FICHE SUSPECT 03 La marque — verdict « Coupable ? »
- Rush visé : chocolate brand bars shelf ; chocolate bars wrapped ; chocolate factory exterior
- Faits : F02

**p062** · 4:35.8 · `rush` · tension
> NARRATRICE : Mais elle n'est pas seule à se servir sur ta tablette.
- À l'écran : plein écran réel
- Rush visé : truck delivery supermarket ; pallet chocolate delivery warehouse ; supermarket warehouse forklift ; delivery truck loading dock


---

## Suspect 04 — Le supermarché

**p063** · 4:40.2 · `schema` · tension · transition fondu
> NARRATRICE : Quatrième suspect : celui qui met ta tablette en rayon, le supermarché.
- À l'écran : FICHE SUSPECT 04 Le supermarché
- Rush visé : supermarket aisle wide shot ; supermarket shelves store ; grocery store aisle walking

**p064** · 4:44.6 · `mosaique` · tension
> SCEPTIQUE : Le cacao a baissé, donc ma tablette va forcément baisser, c'est logique !
- À l'écran : mosaïque : — + —
- Rush visé : woman choosing chocolate supermarket ; chocolate bar price tag shelf

**p065** · 4:49.3 · `rush` · revelation
> NARRATRICE : Pourtant, en quatre ans, les chocolats de Pâques ont grimpé de trente-six pour cent.
- À l'écran : PUNCH « +36 % » à 0.6 s · couche source « UFC-Que Choisir, 01/04/2026 · inflation : +14 % » · sons : impact@0.6
- Rush visé : easter chocolate eggs shop window ; chocolate easter bunnies store shelf ; easter chocolates supermarket ; easter eggs chocolate display
- Faits : F28

**p066** · 4:54.9 · `schema` · tension
> NARRATRICE : Et à Pâques deux mille vingt-six, malgré la chute du cacao, encore quatre pour cent.
- À l'écran : CHIFFRE +4 % — chocolats de Pâques, sur un an (2026) (« ? » jusqu'à 3.6 s) · source : UFC-Que Choisir, 01/04/2026
- Rush visé : easter chocolate eggs basket ; chocolate eggs close up ; easter chocolate shop
- Faits : F28

**p067** · 5:00.8 · `rush` · revelation
> NARRATRICE : Et sur un euro, le supermarché garde environ trente-deux centimes, hors taxes.
- À l'écran : compteur → 32 c
- Rush visé : supermarket checkout chocolate ; cash register supermarket ; paying at supermarket checkout ; customer paying cashier
- Faits : F02, F03, F32

**p068** · 5:05.5 · `ecran_partage` · leger
> NARRATRICE : Dont environ huit centimes de vraie marge, presque autant que la marque.
- À l'écran : DECOMPOSITION « Les 32 c du supermarché » : Coûts 21.0, Autres taxes 2.3, Marge 8.4 [héros] · source : BASIC 2020, données 2018 (marge 0,78 €/kg) ; TVA retirée par calcul · média réel à droite
- Rush visé : supermarket shelves restocking ; supermarket aisle chocolate ; supermarket employee shelves
- Faits : F03

**p069** · 5:10.3 · `schema` · tension
> NARRATRICE : Quatrième suspect, le supermarché : lui aussi, je le note coupable, pour l'instant.
- À l'écran : FICHE SUSPECT 04 Le supermarché — verdict « Coupable ? »
- Rush visé : supermarket aisle empty ; supermarket shelves ; shopping cart supermarket

**p070** · 5:15.1 · `rush` · tension
> NARRATRICE : Reste un dernier suspect, discret, qui se sert à chaque passage en caisse.
- À l'écran : plein écran réel
- Rush visé : receipt printing cash register ; supermarket receipt close up ; cash register receipt printing ; receipt in hand


---

## Suspect 05 — L'État

**p071** · 5:20.2 · `schema` · tension · transition fondu
> NARRATRICE : Cinquième suspect : l'État français, avec sa T V A.
- À l'écran : FICHE SUSPECT 05 L'État français
- Rush visé : Bercy ministry of finance Paris ; french government building paris ; french flag on building

**p072** · 5:23.8 · `rush` · leger
> NARRATRICE : Sur le chocolat noir, la T V A est de cinq virgule cinq pour cent.
- À l'écran : surtitre « TVA 5,5 % »
- Rush visé : dark chocolate bar checkout ; receipt close up tax ; paying chocolate bar cashier ; chocolate bar scanned checkout
- Faits : F32

**p073** · 5:29.8 · `ecran_partage` · revelation
> NARRATRICE : Sur notre euro, ça fait environ cinq centimes pour l'État français.
- À l'écran : CHIFFRE 0.05 € — TVA sur 1 € de chocolat noir (« ? » jusqu'à 2.4 s) · source : Calcul TVA 5,5 % (CGI art. 278-0 bis) ; BASIC 2020 · média réel à gauche
- Rush visé : euro coins counting ; coins on receipt ; euro coin hand
- Faits : F32, F03

**p074** · 5:34.1 · `schema` · tension
> NARRATRICE : Alors, à ton avis… et ta tablette au lait, elle est taxée à combien ?
- À l'écran : DEVINETTE « TVA d'une tablette au lait ? » 5,5 % / 10 % / 20 % (bonne : 20 %) · sons : tick@1.5
- Rush visé : milk chocolate bar close up ; milk chocolate pieces ; milk chocolate bar wrapper

**p075** · 5:43.1 · `rush` · revelation
> NARRATRICE : Vingt pour cent pour la plupart des tablettes au lait, comme une console de jeux.
- À l'écran : PUNCH « 20 % » à 0.5 s · sons : impact@0.5
- Rush visé : milk chocolate bar unwrapping ; milk chocolate pieces close up ; milk chocolate bar breaking ; milk chocolate squares
- Faits : F32

**p076** · 5:49.0 · `ecran_partage` · leger
> NARRATRICE : Le noir, lui, compte comme un produit de base, au même taux que le pain.
- À l'écran : COMPARAISON Chocolat noir 5.5 / La plupart des tablettes au lait 20 % (héros : b) · source : CGI art. 278-0 bis ; question AN n° 99374 (JO 06/12/2016) · média réel à droite
- Rush visé : dark chocolate bar and bread ; dark chocolate squares close up ; baguette bread close up
- Faits : F32

**p077** · 5:55.0 · `schema` · leger
> NARRATRICE : L'État français prend trois fois plus que l'État ivoirien, mais sa part reste petite.
- À l'écran : FICHE SUSPECT 05 L'État français — verdict « Petit joueur »
- Rush visé : Paris government building ; french tricolor flag ; Ivory Coast flag
- Faits : F03, F32

**p078** · 6:00.5 · `mosaique` · leger
> NARRATRICE : Si tu aimes suivre l'argent des objets du quotidien, abonne-toi, ça m'aide vraiment.
- À l'écran : mosaïque : — + — · couche carton « ABONNE-TOI »
- Rush visé : chocolate bar on wooden table top view ; grocery bag chocolate bar


---

## La vérité

**p079** · 6:05.6 · `titre` · revelation · transition fondu
> (sans voix)
- À l'écran : CARTE TITRE « La vérité » / « Qui a pris la différence ? » · sons : impact@0.2
- Rush visé : dark chocolate bar dramatic light ; chocolate bar black background ; dark chocolate pieces smoke

**p080** · 6:08.0 · `schema` · revelation
> NARRATRICE : Sur un euro, il ne reste qu'un morceau pour celui qui fait pousser le cacao.
- À l'écran : DECOUPE « 1 € de chocolat noir (2018) » : Marque 37, Supermarché 32, TVA 5, Négociant 7, Broyeur 6, Sucre… 2, Planteur 11 [héros] · source : BASIC 2020, données 2018, tablette noire ; TVA 5,5 % calculée · sons : riser@0, impact@4.2
- Rush visé : dark chocolate bar isolated white background ; chocolate bar flat lay white background ; chocolate bar top view isolated
- Faits : F02, F03, F32

**p081** · 6:14.0 · `rush` · revelation
> NARRATRICE : Onze centimes, pour des mois de travail sous le soleil.
- À l'écran : PUNCH « 11 c » à 0.4 s · couche source « Image d'illustration » · sons : impact@0.4
- Rush visé : cocoa farmer working plantation sun ; cocoa farmer harvesting ; farmer cutting cocoa pods ; cocoa farmer sweat work
- Faits : F02

**p082** · 6:18.0 · `ecran_partage` · revelation
> NARRATRICE : Marques et supermarchés captent soixante-dix pour cent de la valeur,
- À l'écran : LISTE « Marques + supermarchés » : Part de la valeur 70 % [héros] | Part des marges ? · source : BASIC 2020 (moyenne, données 2018) · média réel à gauche
- Rush visé : supermarket chocolate aisle ; chocolate bars shelf store ; chocolate factory line
- Faits : F05

**p083** · 6:22.0 · `schema` · revelation
> NARRATRICE : et quatre-vingt-dix pour cent des marges.
- À l'écran : CHIFFRE 90 % — des marges vont aux marques et aux supermarchés (« ? » jusqu'à 0.4 s) · source : BASIC 2020 (moyenne, données 2018) · sons : impact@0.4
- Rush visé : supermarket checkout busy ; chocolate bars conveyor factory ; supermarket aisle
- Faits : F05

**p084** · 6:24.4 · `mosaique` · tension
> SCEPTIQUE : Ça, c'était en deux mille dix-huit ! Depuis, les planteurs ont touché des prix records !
- À l'écran : mosaïque : — + —
- Rush visé : cocoa beans market Africa ; cocoa farmers sorting beans

**p085** · 6:29.9 · `rush` · tension
> NARRATRICE : Exact : fin deux mille vingt-quatre, le cacao s'envole.
- À l'écran : plein écran réel
- Rush visé : cocoa beans pouring warehouse ; commodity trading screen numbers ; stock market screen rising ; cocoa beans sacks port
- Faits : F12

**p086** · 6:33.2 · `schema` · revelation
> NARRATRICE : Plus de douze mille neuf cents dollars la tonne, cinq fois sa moyenne d'avant.
- À l'écran : CHIFFRE > 12900 $/t — record du cacao, décembre 2024 (« ? » jusqu'à 1.0 s) · source : Barchart, 23/10/2026 ; Trading Economics ; Coface · sons : impact@1.0
- Rush visé : stock market chart screen ; trading screen graph ; commodity prices screen
- Faits : F12, F14

**p087** · 6:38.7 · `ecran_partage` · revelation
> NARRATRICE : Puis il dégringole : le deux mars deux mille vingt-six, deux mille huit cent quarante-six dollars.
- À l'écran : COMPARAISON Record, déc. 2024 12900 / 2 mars 2026 2846 $ (héros : b) · source : Barchart via Yahoo Finance, 23/10/2026 · média réel à droite
- Rush visé : stock chart falling red screen ; trading screen red numbers ; falling chart monitor
- Faits : F12, F16

**p088** · 6:44.6 · `rush` · tension
> NARRATRICE : Deux jours plus tard, la Côte d'Ivoire baisse le prix de ses planteurs.
- À l'écran : surtitre « 4 mars 2026 »
- Rush visé : cocoa farmer sorting beans Africa ; cocoa farmer raking drying beans ; Ghana cocoa farmer ; cocoa farmers village
- Faits : F21

**p089** · 6:49.8 · `ecran_partage` · revelation
> NARRATRICE : De deux mille huit cents à mille deux cents francs C F A le kilo.
- À l'écran : COMPARAISON Octobre 2025 2800 / Depuis mars 2026 1200 (héros : b) · source : Financial Afrik, 02/10/2025 ; RFI via AllAfrica, 04/03/2026 · média réel à gauche · sons : impact@2.6
- Rush visé : cocoa beans in hands ; cocoa beans sack open close up ; cocoa beans weighing
- Faits : F19, F21

**p090** · 6:55.7 · `rush` · emotion
> NARRATRICE : Moins cinquante-sept pour cent d'un coup,
- À l'écran : PUNCH « −57 % » à 0.6 s · couche source « Image d'illustration » · sons : impact@0.6
- Rush visé : cocoa farmer sad plantation ; cocoa farmer sitting sacks ; cocoa farmer holding beans ; cocoa farmer portrait
- Faits : F21

**p091** · 6:58.2 · `mosaique` · emotion
> NARRATRICE : pour une filière qui fait vivre environ cinq millions de personnes.
- À l'écran : mosaïque : Côte d'Ivoire + ≈ 5 millions de personnes · couche source « Image d'illustration »
- Rush visé : cocoa farmers group village ; cocoa farm workers carrying pods
- Faits : F22

**p092** · 7:02.5 · `schema` · tension
> NARRATRICE : Le ministre de l'Agriculture l'assume : ce sont les cours mondiaux qui l'obligent.
- À l'écran : LISTE « Le ministre, 4 mars 2026 » : « Les cours du cacao sur le marché international nous obligent à procéder à un réajustement. » [héros] · source : RFI via AllAfrica, 04/03/2026
- Rush visé : Abidjan skyline ; Abidjan plateau buildings ; Ivory Coast government
- Faits : F21

**p093** · 7:07.3 · `rush` · tension
> NARRATRICE : Reprends ta tablette noire du début, et refaisons le calcul.
- À l'écran : plein écran réel
- Rush visé : dark chocolate bar unwrapping close up ; dark chocolate bar 70 percent ; hand breaking dark chocolate ; dark chocolate bar foil
- Faits : F10

**p094** · 7:11.3 · `schema` · tension
> NARRATRICE : Alors, ta réponse du début : combien touche le planteur sur cette tablette ?
- À l'écran : DEVINETTE « Combien pour le planteur ? » 3 c / 13 c / 50 c (bonne : 13 c) · sons : tick@1.5
- Rush visé : cocoa pods on tree ; cocoa beans hands ; cocoa farmer plantation

**p095** · 7:19.5 · `ecran_partage` · revelation
> NARRATRICE : Environ treize centimes : soixante-dix grammes de cacao, à mille deux cents francs le kilo.
- À l'écran : CHIFFRE ≈ 0.13 € — pour le planteur, sur une tablette à ≈ 2,60 € (« ? » jusqu'à 0.5 s) · source : Calcul : 70 g de cacao (F50) × prix bord champ ivoirien (RFI 04/03/2026 ; Financial Afrik 02/10/2025), tablette ≈ 2,60 € (Que Choisir, mai 2026) · média réel à gauche
- Rush visé : cocoa beans on scale ; weighing cocoa beans ; cocoa beans handful
- Faits : F10, F21, F33, F50

**p096** · 7:25.0 · `rush` · emotion
> NARRATRICE : Au prix record, c'était environ trente centimes : il a perdu plus de la moitié.
- À l'écran : couche source « Image d'illustration »
- Rush visé : cocoa farmer carrying pods basket ; cocoa farmer walking plantation ; cocoa farmer opening pod ; farmer cocoa beans bucket
- Faits : F19, F50

**p097** · 7:30.6 · `schema` · revelation
> NARRATRICE : Sa part du prix passe d'environ onze à cinq pour cent seulement.
- À l'écran : COMPARAISON Au prix record (oct. 2025) 11 / Depuis mars 2026 5 % (héros : b) · source : Calcul : 70 g de cacao (F50) × prix bord champ ivoirien (RFI 04/03/2026 ; Financial Afrik 02/10/2025), tablette ≈ 2,60 € (Que Choisir, mai 2026)
- Rush visé : cocoa plantation ; cocoa pods tree ; cocoa beans close up
- Faits : F10, F19, F21, F50

**p098** · 7:35.3 · `mosaique` · tension
> SCEPTIQUE : Les industriels ont acheté leur cacao au prix fort, il faut bien l'écouler !
- À l'écran : mosaïque : — + —
- Rush visé : cocoa beans warehouse stock ; chocolate factory production

**p099** · 7:40.5 · `ecran_partage` · leger
> NARRATRICE : C'est leur défense, et elle est en partie vraie : le cacao s'achète à l'avance.
- À l'écran : LISTE « Syndicat du chocolat » : « Le cacao destiné à Pâques 2026 a été acheté il y a de nombreux mois » [héros] | Achats à terme 6 mois à 1 an · source : UFC-Que Choisir, 01/04/2026 ; RTBF, 01/04/2026 · média réel à gauche
- Rush visé : cocoa sacks warehouse stacked ; cocoa storage warehouse ; cocoa beans storage
- Faits : F29, F30

**p100** · 7:46.0 · `schema` · tension
> NARRATRICE : Mais début novembre, le cacao est déjà remonté vers cinq mille quatre cents dollars.
- À l'écran : CHIFFRE ≈ 5394 $/t — cours du cacao, 2 novembre 2026 (« ? » jusqu'à 3.4 s) · source : Trading Economics, 02/11/2026
- Rush visé : commodity chart screen ; trading screen numbers ; market chart monitor
- Faits : F16, F18

**p101** · 7:51.6 · `rush` · tension
> NARRATRICE : Et le prix du planteur ivoirien, lui, est resté bloqué à mille deux cents francs.
- À l'écran : surtitre « Campagne 2026-2027 : 1 200 F CFA/kg » · couche source « Image d'illustration »
- Rush visé : cocoa farmer carrying sack ; cocoa farmer village Africa ; farmer carrying sack on head ; cocoa beans sack farmer
- Faits : F22

**p102** · 7:57.5 · `mosaique` · revelation
> NARRATRICE : Quand le cacao monte, ta tablette monte. Quand il baisse, c'est le planteur qui baisse.
- À l'écran : mosaïque : Ta tablette + Le planteur
- Rush visé : chocolate bars supermarket shelf ; cocoa farmer plantation
- Faits : F21, F22, F28

**p103** · 8:03.4 · `schema` · emotion
> NARRATRICE : Premier suspect, le planteur : pas coupable, c'est lui qui a encaissé la baisse.
- À l'écran : FICHE SUSPECT 01 Le planteur — verdict « Victime »
- Rush visé : cocoa farmer portrait plantation ; cocoa farmer holding pod ; cocoa plantation
- Faits : F21


---

## Laurent, puis la fin

**p104** · 8:08.6 · `ecran_partage` · emotion · transition fondu
> NARRATRICE : Je peux enfin te lire les mots de Laurent Koné, cinquante-quatre ans.
- À l'écran : LISTE « Laurent Koné, 54 ans » : Planteur depuis 1996 | Près de Guiglo, ouest ivoirien | Une bâche en guise de toit [héros] · source : AFP, 26/01/2026 (reprise Le360 Afrique) · média réel à gauche · couche source « Image d'illustration »
- Rush visé : rural village Ivory Coast ; village houses West Africa ; cocoa farmer village
- Faits : F34

**p105** · 8:13.3 · `rush` · emotion
> NARRATRICE : Il vit près de Guiglo, dans l'ouest du pays, dans une maison en torchis.
- À l'écran : couche source « Image d'illustration »
- Rush visé : mud house village Africa ; clay house rural West Africa ; mud brick house village ; village path Africa
- Faits : F34

**p106** · 8:18.9 · `mosaique` · emotion
> NARRATRICE : Pas d'électricité, et une simple bâche en guise de toit.
- À l'écran : mosaïque : Image d'illustration + Image d'illustration
- Rush visé : tarp roof house village ; rural house night no electricity Africa
- Faits : F34

**p107** · 8:22.8 · `rush` · emotion
> NARRATRICE : En janvier deux mille vingt-six, au moment du prix record,
- À l'écran : surtitre « Janvier 2026 · prix record : 2 800 F CFA/kg » · couche source « Image d'illustration »
- Rush visé : farmer walking cocoa plantation ; cocoa plantation path ; cocoa farmer back view ; cocoa farmer plantation morning
- Faits : F19, F34

**p108** · 8:26.8 · `mosaique` · emotion
> NARRATRICE : il témoigne auprès de l'Agence France-Presse.
- À l'écran : mosaïque : Image d'illustration + Image d'illustration
- Rush visé : cocoa farmer village house ; cocoa farmer harvesting pods
- Faits : F34

**p109** · 8:29.3 · `ecran_partage` · emotion
> NARRATRICE : « J'ai commencé à planter en mille neuf cent quatre-vingt-seize, et jusqu'à présent,
- À l'écran : LISTE « Laurent Koné » : « J'ai commencé à planter en 1996 et jusqu'à présent je n'ai pas de toit car il n'y a pas l'argent » [héros] · source : AFP, 26/01/2026 (reprise Le360 Afrique, La Gazette France) · média réel à gauche
- Rush visé : cocoa farmer hands ; farmer hands soil ; cocoa pods hands
- Faits : F34

**p110** · 8:34.1 · `rush` · emotion
> NARRATRICE : je n'ai pas de toit, car il n'y a pas l'argent. »
- À l'écran : couche source « Image d'illustration »
- Rush visé : cocoa farmer sitting ; farmer resting plantation ; cocoa plantation evening light ; farmer looking at cocoa trees
- Faits : F34

**p111** · 8:38.4 · `schema` · emotion
> NARRATRICE : Un sac d'engrais coûte vingt-deux mille francs, soit dix-huit kilos de cacao aujourd'hui.
- À l'écran : CHIFFRE ≈ 18 kg — de cacao pour un sac d'engrais (22 000 F CFA) (« ? » jusqu'à 3.6 s) · source : AFP, 26/01/2026 ; calcul
- Rush visé : fertilizer bag farm ; fertilizer sacks ; farmer fertilizer
- Faits : F34, F22

**p112** · 8:43.6 · `rush` · emotion
> NARRATRICE : Et six semaines après ses mots, son prix était coupé de plus de moitié.
- À l'écran : couche source « Image d'illustration »
- Rush visé : cocoa farmer drying beans ; cocoa beans drying farmer ; cocoa farmer silent ; cocoa plantation rain
- Faits : F21, F34

**p113** · 8:49.1 · `ecran_partage` · emotion
> NARRATRICE : Et il a cette phrase : « Je ne veux pas que mes enfants soient planteurs comme moi. »
- À l'écran : LISTE « Laurent Koné » : « Je ne veux pas que mes enfants soient planteurs comme moi » [héros] | « parce que c'est une souffrance » · source : AFP, 26/01/2026 (reprise Le360 Afrique, La Gazette France) · média réel à droite
- Rush visé : cocoa plantation sunset ; cocoa trees evening ; cocoa pod tree sunset
- Faits : F34

**p114** · 8:55.4 · `rush` · emotion
> NARRATRICE : « Parce que c'est une souffrance », ajoute-t-il, tout simplement.
- À l'écran : plein écran réel
- Rush visé : cocoa plantation golden hour ; cocoa tree silhouette sunset ; empty cocoa plantation ; cocoa pods sunset light
- Faits : F34

**p115** · 8:58.7 · `mosaique` · emotion
> (sans voix)
- À l'écran : mosaïque : — + —
- Rush visé : cocoa pod on tree close up slow ; dark chocolate bar on table

**p116** · 9:01.2 · `schema` · tension
> NARRATRICE : Alors, qui a pris la différence ? Les achats à terme, ou les marges ?
- À l'écran : LISTE « Qui a pris la différence ? » : Les achats à terme ? | Les marges ? | À toi de juger [héros] · source : BASIC 2020 ; Syndicat du chocolat via UFC-Que Choisir, 01/04/2026
- Rush visé : chocolate bar pieces dark ; chocolate bar broken ; cocoa beans and chocolate
- Faits : F05, F29

**p117** · 9:06.3 · `rush` · tension
> NARRATRICE : Et la prochaine fois que le cacao baissera, tu crois que ton rayon suivra ?
- À l'écran : plein écran réel
- Rush visé : supermarket chocolate aisle ; hand picking chocolate shelf ; chocolate bars shelf close up ; woman looking at chocolate shelf

**p118** · 9:11.8 · `mosaique` · emotion
> NARRATRICE : Dis-le moi en commentaire, et regarde ta prochaine tablette un peu autrement.
- À l'écran : mosaïque : — + —
- Rush visé : hand holding chocolate bar close up ; person eating chocolate square

**p119** · 9:16.6 · `ecran_partage` · leger
> NARRATRICE : Dans une prochaine vidéo, on ouvre une brique de lait U H T.
- À l'écran : LISTE « Prochaine enquête » : La brique de lait UHT [héros] | Qui touche quoi ? · source : Prochaine enquête (date non fixée) · média réel à droite
- Rush visé : milk carton pouring ; UHT milk cartons supermarket ; milk carton close up

**p120** · 9:21.8 · `titre` · leger
> (sans voix)
- À l'écran : CARTE TITRE « Qui a pris la différence ? » / « Prochaine enquête : le lait UHT »
- Rush visé : milk carton dark background ; dark chocolate bar black background
