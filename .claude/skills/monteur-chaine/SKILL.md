---
name: monteur-chaine
description: Règles de montage de la chaîne YouTube d'Omar (vidéos "comment c'est fait", mixed media vraies images + motion design, voix off française). À charger AVANT d'écrire un script, un montage.json, une scène Remotion, de choisir des rushes ou de toucher à la voix. Contient les leçons validées par Omar.
---

# Monteur de la chaîne — règles validées par Omar

Ces règles viennent des retours d'Omar sur les premiers tests. Elles passent AVANT le goût personnel.
Pour la technique d'animation, charger aussi `remotion-motion-graphics` (courbes, ressorts, couches, vérification).

## Règle n°1 — Ce qu'on voit = ce qu'on dit
Retour d'Omar : « la bobine, on ne voit pas de quoi tu parles, tu as dessiné une bobine mais ce n'est pas parlant ».
- Chaque fois que la voix nomme une chose (une bobine d'aluminium, une presse, une canette), l'écran montre
  **cette chose réelle, reconnaissable en moins d'une seconde**. Un dessin symbolique ne remplace jamais l'objet.
- Le dessin/schéma sert UNIQUEMENT à expliquer ce qu'une caméra ne peut pas montrer (l'intérieur d'une machine,
  une coupe, une épaisseur, un ordre de grandeur, un flux). Il arrive APRÈS (ou À CÔTÉ de) l'image réelle, et il
  porte une étiquette en clair ("Schéma : le poinçon découpe un disque").
- Un schéma doit ressembler à l'objet : proportions réalistes, matière (dégradé métal), légendes et flèches.
  Des cercles concentriques ne "disent" pas bobine ; la photo d'une bobine + une flèche "bande d'aluminium 0,3 mm" oui.
- **Test du son coupé** : pour chaque plan, si on coupe le son, comprend-on ce qu'on regarde ? Sinon le plan est faux.

## Règle n°2 — Jamais de rush choisi au hasard
Retour : la recherche automatique a donné une machine à café pour "presse", des cheminées pour "bobine",
du jus d'orange pour "chaîne de canettes".
1. Dans `montage.json`, donner 3–4 requêtes en anglais par scène (`"recherche": ["aluminum coil", "metal coil factory", ...]`).
2. Lancer le repérage : workflow **Repérage des rushes** (se lance au push d'un montage avec des scènes sans `pixabay_id`,
   ou à la main : `POST /repos/omarbaouch/chaine-youtube/actions/workflows/reperage.yml/dispatches` avec
   `{"ref":"main","inputs":{"montage":"<chemin>"}}` et l'en-tête `Content-Type: application/json`).
3. Télécharger les planches de la release `reperage-N` (API GitHub, `Accept: application/octet-stream`),
   les REGARDER (Read), et écrire l'id choisi : `"pixabay_id": 123456`. Chaque vignette affiche id · durée · définition.
4. Refuser tout rush où l'objet n'est pas exactement celui dont on parle. Si rien ne convient : autres requêtes,
   plan filmé par Omar (`"fichier"`), ou image réelle d'une autre source libre (Wikimedia Commons, avec crédit).
   En dernier recours seulement : un schéma fidèle et étiqueté.
5. Un rush ne sert qu'une fois par vidéo.

## Règle n°3 — Toujours en symbiose : vraie image + couche animée
Ni vidéo nue avec sous-titres, ni animation seule. Chaque plan combine un rush réel ET une couche qui l'explique.
Briques prêtes (`src/motion/`, exemple complet `src/tests/Canette.tsx`) :
| Brique | Quand l'utiliser |
|---|---|
| `Rush` | fond vidéo avec Ken Burns + étalonnage ; flouté/assombri pour servir de décor |
| `CarteVideo` | montrer l'objet réel en grand à côté du texte, entrée par volet |
| `Annotation` | pointer LA chose dont on parle dans la vidéo (point + trait + étiquette, chiffres) |
| `Visee` | verrouiller une zone d'action (presse qui frappe), réagit aux chocs |
| `Vitre` | poser un schéma ou des chiffres SUR la vidéo, panneau vitré flouté |
| Fenêtre-forme (`FenetreCanette`) | la silhouette de l'objet découpe une vidéo réelle : objet + usine en même temps |
| Raccord forme → vidéo | le schéma s'ouvre et plonge dans le vrai plan suivant |
| `Flash` + secousse + bruitage | synchroniser un impact visible dans le rush |
Placer annotations et visées SUR l'objet visible dans le rush (vérifier sa position dans la planche, ne pas deviner).

## Règle n°4 — Voix et son
- **Remplacé par la règle n°9 (31/10/2026) : la voix est Edge Vivienne.** Pocket TTS ne sert plus qu'en secours.
- (Historique) Pocket TTS (Kyutai), modèle `french_24l`, voix `estelle`, 5 étapes de calcul.
- Chaîne de traitement : `scripts/traitement_audio.py` (coupe-bas, débruiteur `afftdn` qui retire les sifflements
  constants du modèle, creux 220/380 Hz, clarté +2,5/+1,5 dB max, dé-esseur, porte de bruit, compression douce,
  limiteur, -16 LUFS en deux passes). Ne jamais remonter la clarté de plus de ~3 dB : ça fait ressortir les artefacts.
- Retours d'Omar à traiter par la mesure, pas au hasard : "son de mauvaise qualité" → spectre (`scripts/analyse_voix.py`) ;
  "bruits parasites" → bruit dans les pauses + spectrogramme ; "tiiit" → `scripts/detecte_tiit.py` puis vérifier que ce
  ne sont pas les harmoniques normales de la voix (rang entier de F0).
- Pour les tests d'écoute, envoyer du **WAV** (le MP3 crée ses propres petits artefacts) et demander à Omar la seconde
  où il entend le défaut, et s'il l'entend aussi sur la version brute.
- Bruitages (`public/sfx/`) calés 2–3 images avant l'action ; nappe musicale basse sous la voix.

## Règle n°5 — Vérifier avant d'envoyer
1. Rendre (faux rushes ici, vrais rushes sur GitHub), extraire une image par plan, les regarder.
2. Pour chaque scène, écrire dans la réponse de travail : narration → ce qu'on voit à l'écran → OK/KO selon la règle n°1.
3. Corriger, re-rendre, puis seulement envoyer à Omar (SendUserFile) avec une phrase de contexte.

## Règle n°6 — Varier les formats, ne jamais lasser
Retour d'Omar (test 20 s) : « une combinaison de tout : des fois des animations SVG, des fois des vidéos, des fois
des images, des fois une composition d'un peu de tout. Je veux que celui qui voit la vidéo ne se lasse pas. »
- Formats disponibles (champ `format` d'une scène, voir CLAUDE.md) : `rush` (vidéo/photo plein écran + couches),
  `ecran_partage` (média réel d'un côté, schéma SVG de l'autre), `mosaique` (2 à 4 médias réels qui s'enchaînent),
  `schema` (animation SVG pure : `decomposition` de prix, `processus` en étapes, `chiffre` géant, `comparaison`).
- **Jamais deux plans consécutifs du même format.** Sur 6 plans : au moins 3 formats différents, dont au moins un
  `schema` et une composition (`ecran_partage` ou `mosaique`).
- Un `schema` reste fidèle à la règle n°1 : il explique ce qu'une caméra ne peut pas montrer (un prix décomposé,
  une épaisseur, un ordre de grandeur), il est étiqueté, et il suit ou entoure un plan réel de l'objet.

## Règle n°7 — Techniques psychologiques de rétention (à appliquer à chaque vidéo)
| Technique | Ce que ça donne au montage |
|---|---|
| Fossé de curiosité / boucle ouverte | poser la question, retarder la réponse ; afficher « ? » à la place de la réponse ; chaque fin de partie ouvre la suivante |
| Rupture de rythme (pattern interrupt) | changer de format toutes les 3–6 s ; un élément neuf à l'écran toutes les ~2 s |
| Effet d'isolement (Von Restorff) | UNE seule information en couleur héros par image (orange) ; le reste en blanc/gris |
| Emphase cinétique | `zoom_punch` (zoom rapide + bruitage) sur le mot ou le chiffre clé, pas plus d'une fois par plan |
| Ancrage et comparaison | un chiffre est toujours comparé à quelque chose de familier (un cheveu, un ticket de métro) |
| Progression visible | numéroter les étapes (01, 02, 03…) : le cerveau veut finir la série |
| Son qui prépare | riser avant une révélation, une demi-seconde de silence juste avant le chiffre clé, impact pile dessus |
| Pic et fin (peak-end) | le plus beau moment visuel à la révélation ; la fin laisse une question ouverte vers la vidéo suivante |

## Règle n°7 bis — Rétention fondée sur la recherche (demande d'Omar, 02/11/2026) — PRIORITAIRE sur les n°7, 9 et 11
Constat sur la baguette (02/11) : environ 30 à 60 s regardées en moyenne sur 8 min. Cause probable vue sur la planche :
la réponse (6 c / 7 c / 83 c / 5 c) est montrée dès 2 s et redite à 16 s ; image noire à 0 s ; carte titre à 6 s ;
digression à 26–30 s ; écran sombre « Partie 01 » à 36 s. Ne jamais refaire ça.

| Résultat de recherche | Règle de montage obligatoire |
|---|---|
| Fossé d'information (Loewenstein 1994) : la curiosité naît d'un manque perçu, et elle est maximale quand on a une intuition sans être sûr (étude IRMf 2009) | L'accroche pose LA question et donne un indice, jamais la réponse. Aucun chiffre-réponse avant sa révélation prévue. L'« avant-première » de la règle n°9 montre l'objet et la question (« ? »), pas le résultat. |
| Curiosité et mémoire (Gruber, Gelman, Ranganath, *Neuron* 2014) : en état de curiosité, le circuit de la récompense (dopamine) et l'hippocampe s'activent ; on retient la réponse ET ce qu'on voit pendant l'attente | Chaque révélation est précédée d'une attente active de 20 à 60 s, remplie d'images fortes. On pose la question suivante AVANT de répondre à la précédente (boucles imbriquées). |
| Intuition avant réponse : la curiosité culmine quand le spectateur a une idée | Les devinettes (2 c / 6 c / 20 c) arrivent tôt (avant 20 s), le spectateur choisit, la réponse vient plus tard. |
| Rythme des coupes (Lang et al. 2000) : plus de coupes dans une même scène → plus d'éveil, d'attention et de mémoire, sans surcharge | Une coupe toutes les 2 à 4 s dans les 60 premières secondes, puis 3 à 6 s. Jamais d'écran vide, noir ou sombre sans voix. |
| Principes de Mayer (multimédia) : cohérence (couper le superflu), signalement (mettre en valeur l'essentiel), contiguïté temporelle (l'image au moment où on en parle), voix humaine plutôt que voix de synthèse | Supprimer toute digression (ex. « baguettes vendues par seconde »). Une seule info en valeur par image. La meilleure amélioration possible : la voix d'Omar (`episodes/<slug>/voix/`). |
| YouTube (aide officielle) : le taux à 30 s mesure si l'intro tient la promesse du titre et de la miniature ; avancer les meilleurs moments | Les 30 premières secondes reprennent mot pour mot la promesse de la miniature. Première image = image forte dès la frame 0. Aucune carte titre ni « Partie 01 » avant 30 s. |

Contrôle avant rendu (à consigner dans `05_review_report.md`) : 1) aucune réponse chiffrée avant sa révélation ; 2) frame 0 non noire ;
3) pas de carte avant 30 s ; 4) au moins 2 questions ouvertes à 30 s ; 5) aucune séquence de plus de 6 s sans changement d'image.

## Règle n°7 ter — Scotcher le spectateur jusqu'à la fin (étude du 03/11/2026, `etude-retention.md`) — OBLIGATOIRE
Lire `etude-retention.md` (14 études + données YouTube) avant d'écrire. Les codes E1…E14 renvoient aux études.
**Script**
- Structure d'enquête (E3) : une grande question posée dans les 8 premières secondes, réponse finale après 85 % de la vidéo. Entre les deux,
  les suspects/pistes sont éliminés un par un ; un retournement par partie, de plus en plus fort.
- Boucles imbriquées (E2, E4) : on n'ouvre jamais un « trou » sans suspense. Avant de répondre à une question, on en ouvre une nouvelle.
  Re-hook toutes les 60-90 s (« et ce n'est même pas le plus fou »).
- Devinettes à 3 choix où le spectateur a une intuition (E5), avec le compte à rebours ; au moins une toutes les 2 minutes.
- Émotions à forte activation (E6) : indignation juste, émerveillement devant la fabrication, utilité concrète (« comment payer moins »).
  La tristesse seulement par touches courtes, jamais en dernier.
- Une vraie personne qu'on suit du début à la fin (E8) : présentée avant 60 s, sa situation revient au milieu, son dénouement à la fin.
- Vitesse (E7) : chaque phrase apporte du nouveau ; zéro répétition, zéro détour ; le dernier tiers va plus vite que le premier.
- Ton de copain qui raconte (E12), tutoiement, phrases de 6 à 18 mots.
**Montage**
- Chaque plan impose à tous de regarder la même chose au même moment (E1) : un seul point d'intérêt, en mouvement ou mis en valeur.
- Rythme « respiration » (E9, E10) : séries de plans de 1,5 à 3 s dans l'action, puis un plan de 4 à 6 s pour une révélation ou une émotion.
  Jamais plus de 6 s sans changement visuel.
- Schémas qui se construisent à l'écran, élément par élément, en même temps que la voix (E12, E14).
- Un visage humain aux moments clés (témoin, planteur, boulangère) (E11).
- L'image de la miniature apparaît dans les 5 premières secondes.
**Son**
- La musique annonce l'émotion une seconde avant l'image (E11) : montée de tension avant chaque révélation, coupure nette (0,5 s de silence)
  juste avant le chiffre clé, impact pile dessus. Changer d'ambiance à chaque partie ; jamais la même nappe plate du début à la fin.
- Voix lue d'un seul souffle (règle 9), intonation qui monte sur les questions ; la voix d'Omar si possible (E13).
**Emballage (titre, miniature, publication)**
- YouTube recommande au temps de visionnage, pas au clic (E15) : la miniature et le titre promettent exactement ce que montrent les
  30 premières secondes. Jamais de promesse que la vidéo ne tient pas.
- Titre (E17) : un problème, une perte ou une injustice concrète (« ta tablette n'a pas baissé »), un chiffre vrai, moins de 60 caractères.
- Pour chaque vidéo : 3 titres et 3 textes de miniature (à générer par Omar avec ChatGPT/Gemini), pour le Test & Compare de YouTube (E16).
- Régularité : une vidéo par semaine, même jour, même heure (E15, fraîcheur).
**Sous-titres et voix**
- Sous-titres toujours (E19), mot actif sur pastille, 3 à 4 mots par ligne. Voix posée, plus lente sur les chiffres (E20).
**Fin**
- Le plus beau moment visuel à la révélation (E18 : on se souvient du pic et de la fin). Dès que la grande question est tranchée :
  20 s maximum, une dernière question ouverte et l'annonce de la vidéo suivante.
**Boucle analytics (avant chaque nouvelle vidéo)**
- Lire `bmo-studio-link/stats/LEVRAIPRIX/dernier.md` : intro (part restante à 30 s), segments plats, pics, creux, rétention relative.
- Pour chaque creux de la vidéo précédente : retrouver la phrase et le plan à cet instant, écrire la cause probable dans
  `videos/<slug>/_workspace/00_lecons_analytics.md`, et la règle appliquée pour ne pas la refaire. Refaire davantage ce qui fait les pics.
- Shorts : garder les formats des Shorts qui dépassent la moyenne de la chaîne (sujet, devinette, durée), abandonner les autres.

## Règle n°8 — Typographie et couleurs (retour d'Omar : tailles et couleurs des polices)
- Échelle unique (1920×1080) : titres 140–170 px (Montserrat 900) ; mots clés plein écran 120 px ; chiffres 110–150 px ;
  sous-titres 78 px (Montserrat 900, MAJUSCULES, contour noir) ; étiquettes d'étape 34 px ; annotations 36 px ;
  sources 24 px minimum. Rien en dessous de 24 px à l'écran.
- Couleurs : texte blanc `#F2F4F7` ; héros orange `#FF6B2C` (le mot ou chiffre clé) ; accent bleu acier `#7FD4FF`
  (traits, cadres, numéros) ; gris `#B4BDC9` seulement pour le secondaire. Le mot actif des sous-titres est sur une
  pastille orange (texte foncé), pas en jaune.
- Tout texte posé sur une image a un fond (pastille ou panneau vitré) ou un contour : lisible sur téléphone.

## Travailler avec Omar
- Il parle depuis son téléphone : réponses courtes, une question à la fois, fichiers envoyés plutôt que décrits.
- Pas d'attente bloquante longue : pousser sur GitHub, programmer une vérification (send_later) et rendre la main.
- Tout doit rester gratuit (GitHub Actions, Pixabay, Pocket TTS, Remotion licence individuelle).

## Règle n°9 — Retours d'Omar sur la vidéo baguette (31/10/2026)
- **Voix :** les voix de synthèse « robotisées » (Pocket TTS, Piper, Kokoro) sont refusées. Voix choisie par Omar :
  Microsoft Edge `fr-FR-VivienneMultilingualNeural` (`"voix": {"moteur": "edge", "locuteur": "fr-FR-VivienneMultilingualNeural", "debit": "+8%"}`).
  Gratuite, mais ses conditions d'utilisation pour une chaîne monétisée sont floues : à surveiller. La vraie solution reste la voix d'Omar.
- **Bruitages :** plus aucun « whoosh » (le « shiiit shiiit » répété). Les impacts et les risers restent rares et discrets.
- **Intro obligatoire :** ouverture choc de 10 à 15 s qui montre le moment fort de la vidéo en avant-première, puis une carte titre animée avec un impact.
- **Ennui :** pas plus d'un tiers de photos fixes ; privilégier les vraies vidéos. Une photo bouge toujours (zoom et panoramique marqués).
  Les respirations sont courtes (0,15 s) et la musique reste présente (0,2 sous la voix, baissée automatiquement).

- **Voix d'un seul souffle (02/11/2026, choix d'Omar : Edge, la plus naturelle possible)** : `scripts/voix.py` lit les plans voisins
  par blocs d'environ 120 mots en UN appel Edge, puis découpe au mot près (minutage WordBoundary). L'intonation suit le sens et les
  pauses ne s'additionnent plus. Ne pas désactiver (`"continu": false` seulement pour déboguer). Pour en profiter :
  transitions `coupe` entre plans d'un même passage (un fondu impose 0,13 s de marge de chaque côté) ; écrire pour l'oreille :
  virgules pour respirer, « … » pour le suspense, phrases de 6 à 18 mots ; réglage `"debit_continu": "+6%"`, hauteur neutre.

## Règle n°10 — Bibliothèques de mouvement installées (31/10/2026)
- `.claude/skills/video-shotcraft/` (Apache 2.0) : 124 « cartes de plans » cinématiques Remotion (caméra, ouverture, transitions,
  typographie, effets d'impact, données). Avant d'écrire une scène animée, piocher une carte dans `references/shots/` et
  l'adapter à nos briques (objet réel d'abord, règle n°1). Sons : `references/sound-design.md`.
- `.claude/skills/emotional-narrative/` (MIT) : principes d'animation pensés pour l'émotion (anticipation, timing, silence).
  À relire avant chaque moment fort (révélation, histoire humaine).

## Règle n°11 — La recette qui a marché (vidéo baguette v6, publiée le 01/11/2026)
Omar veut de l'**émotion** (références : Léo Duff, Money Radar), pas « un enchaînement de paroles, ta ta ta ».
- **Structure enquête** : une question d'argent simple (« qui a pris tes 94 centimes ? »), des **suspects** présentés un par un
  (fiche `suspect` + verdict tamponné INNOCENT / COUPABLE ?), une partie **« La vérité »** qui renverse l'idée reçue.
- **Ouverture choc 10–15 s** (règle n°9) : l'objet réel découpé en morceaux proportionnels (`decoupe`), puis carte titre.
- **Une vraie personne au centre** : une histoire humaine vérifiée (Alexandra Faure, boulangère, facture d'électricité),
  annoncée au début (« je te garde ce qu'elle a dit pour la fin ») et racontée à la fin : boucle ouverte + pic émotionnel.
- **Voix du sceptique** (`"voix": "sceptique"`, Edge Rémy, sous-titres bleus) : il dit tout haut l'idée reçue
  (« c'est le boulanger qui garde tout ! »), la narratrice lui répond. Ça casse la monotonie.
- **Devinettes** (`devine`) lues par la voix, compte à rebours de 3 s APRÈS la question, puis révélation avec impact.
- **Musique par ambiance** (Kevin MacLeod, CC-BY, `scripts/musique_libre.py`) : tension / émotion / révélation / léger,
  fondus enchaînés, baissée sous la voix. Crédits obligatoires dans la description.
- Fin : question ouverte (« qui paie la baguette à 28 c ? ») + annonce de la vidéo suivante.

## Règle n°12 — Pièges techniques déjà rencontrés (ne pas les refaire)
| Problème | Cause | Solution en place |
|---|---|---|
| « centimes » lu en anglais | Vivienne Multilingual bascule en anglais sur les phrases très courtes | `voix.py` fusionne les phrases de moins de 6 mots ; le script évite les phrases isolées de 1–3 mots |
| « No audio was received » (Edge) | limite de débit | 1,2 s entre appels + reprises exponentielles (`voix_edge.py`) |
| Mauvais rush servi (hot-dog pour « baguette ») | cache de rushes par id de scène | fichier `.ref` par scène + `rushes_a_refaire` dans `_episode` |
| Découpe à côté de l'objet | détection automatique ratée | fixer `zone` / `zone_y` à la main après avoir regardé l'image |
| Tranche plantée « Cannot render video x.jpg » | photo traitée comme vidéo | détection par extension partout |
| Quota d'artefacts GitHub plein | — | transfert entre machines par Release temporaire `tmp-rendu-<run>` |
| Écran noir 0,6 s en début de plan | le rush source démarre par un fondu au noir | `blackdetect` sur le rendu final, puis `debut_media` +1 s |
| Citation non retrouvée | citation reprise sans source primaire | ne JAMAIS mettre une phrase entre guillemets sans l'article qui la cite (date + média) |
| Pixabay HTTP 429 | trop de requêtes | espacement 700 ms + reprises |
| Prépa de 56 min au lieu de 15 (capsules, 06/11) | Commons répond 429 → attentes de 600 s | repérer en 4-5 petits lots parallèles (≤ 8 scènes) ; limiter les médias Commons à ~25 par vidéo |
| « The source image cannot be decoded » au rendu | Commons renvoie « Too many thumbnail requests » à la place d'une très grande image (9 000 px+) | `medias.mjs` vérifie le type et prend l'original réduit ; éviter les fichiers Commons > 8 000 px |
Contrôle final obligatoire : `ebur128` (-14 LUFS, crête ≤ -1 dBTP), `blackdetect`, planches toutes les 3 s regardées.

## Règle n°13 — Témoignages : de vraies personnes qui parlent (demande d'Omar, 01/11/2026)
Format `temoignage` : un vrai clip d'une personne qui parle, **son d'origine**, bandeau nom / rôle / source, sous-titres de la citation,
voix off coupée et musique baissée pendant l'extrait.
```jsonc
{"id": "p160", "fichier": "medias/alexandra.mp4", "debut_media": 12.4, "texte": "",
 "temoignage": {"nom": "Alexandra Faure", "role": "Boulangère à Valdahon", "source": "Brut, 30/11/2022",
   "citation": "Là, c'est le coup de grâce.", "fin": 15.6, "parole_debut": 0.3, "parole_fin": 2.9}}
```
Sources autorisées (sinon Content ID / droits d'auteur → vidéo bloquée ou démonétisée) :
1. **Omar ou ses proches filmés au téléphone** (micro-trottoir, artisan rencontré, avec son accord) → `fichier`. Le meilleur.
2. **Vidéos sous licence libre** : Wikimedia Commons (`wc:File:…webm`, son conservé), YouTube filtré « Creative Commons »
   (CC-BY : créditer l'auteur). Déposer le clip dans `episodes/<slug>/medias/`.
3. **Jamais** un extrait de chaîne télé ou de média (Brut, BFM, Europe 1…) ni la vidéo Facebook d'un particulier sans son accord écrit.
   Pour ces histoires : raconter avec la voix off + citation écrite à l'écran (`ecran_partage`), comme dans la baguette.
Un témoignage dure 3 à 12 s, un seul par partie ; on l'annonce (« écoute ce qu'elle dit ») et on réagit juste après.

## Règle n°14 — Publication (chaîne « Le Vrai Prix »)
- Kit dans `videos/<slug>/_workspace/06_publication_*.txt` : titre ≤ 60 caractères avec le mot-clé au début, description < 5 000
  (mot-clé dans la 1re phrase, chapitres mesurés SUR LE RENDU FINAL, sources, crédits musique + médias, « voix off générée par synthèse »),
  tags < 500, commentaire-question à épingler.
- Publication par **BMO Studio Link** (décision d'Omar du 03/11/2026 : plus de Metricool). Dépôt central `omarbaouch/bmo-studio-link`
  (API YouTube officielle, appli Google « BMO Studio Link ») : déposer `publications/<date>-<nom>.json` sur `main` (format dans son README :
  `chaine` = `LEVRAIPRIX`, `video_url`, `titre`, `description`, `tags`, `categorie` 27, `miniature_url`, `commentaire`, `publier_le`, `playlist`).
  Le workflow envoie, met la miniature, poste le premier commentaire, ajoute à la playlist et range la fiche dans `publications/fait/` avec le lien.
  Ne jamais écrire ni afficher les clés : elles sont dans les secrets de ce dépôt.
- Il faut un **lien public** du MP4 : le dépôt public `omarbaouch/le-vrai-prix-medias` sert à ça. Y pousser `videos/<slug>/video.partNN`
  (morceaux de 90 Mo, `split -b 90m`, UN morceau par push sinon le proxy coupe) + `miniature.jpg` + `credits.txt` ; son workflow recolle et
  publie la Release `<slug>` (`https://github.com/omarbaouch/le-vrai-prix-medias/releases/download/<slug>/<slug>.mp4`).
  Les Shorts (< 100 Mo) vont dans `shorts/<slug>/` et se lisent en `https://raw.githubusercontent.com/omarbaouch/le-vrai-prix-medias/main/shorts/<slug>/<fichier>.mp4`.
- **Shorts à chaque sortie** (données du 03/11 : les Shorts font ~98 % des vues de la chaîne) : 8 à 10 extraits verticaux de 15 à 25 s,
  coupés sur des silences, chacun avec UNE devinette posée puis tranchée ou UN chiffre choc (meilleurs : « Le vrai prix du blé » 652 vues,
  « Ton pain cuit à combien de degrés ? » 363, « La baguette à 29 centimes » 334). Ne jamais dévoiler en Short la réponse principale
  de la vidéo longue. Titre en haut sur 2 lignes (blanc + orange, 64-78 px, `expansion=none`), « La vidéo complète est en lien sous ce
  Short » en bas ; description et premier commentaire avec le lien de la vidéo longue ; même `playlist`. Rythme : **2 par jour
  (12 h 30 et 18 h)** jusqu'à la vidéo suivante, plus un à 8 h le lendemain de la sortie.
- **Statistiques** : `bmo-studio-link/stats/LEVRAIPRIX/dernier.md` (mis à jour chaque jour à 6 h : vues, durée moyenne, % regardé, sources
  de trafic, courbe de rétention). Le lire AVANT d'écrire une nouvelle vidéo et corriger ce qui fait partir les gens (règle n°7 bis).
- Miniature : la meilleure jusqu'ici (chocolat) est une image générée par Omar avec ChatGPT/Gemini à partir d'un texte écrit par Claude :
  photo hyperréaliste très contrastée, un objet + une main, une grosse question en blanc (un mot en jaune), un chiffre choc sur pastille rouge.
  Proposer ce texte à Omar ; à défaut, composer à partir d'une image du rendu. Aucune marque, aucun chiffre faux (vérifier, arrondir honnêtement).
- Tant que Google n'a pas audité l'appli, une vidéo peut être repassée en privé par YouTube : le signaler à Omar s'il le faut.
## Règle n°15 — Branches et équipe
- **`main` est la seule version officielle** (décision d'Omar, 01/11/2026) : le travail de `studio-b` y a été recopié.
  On travaille sur `main` ; le rendu `.github/workflows/rendu-rapide.yml` (6 machines) se lance à chaque push sur `episodes/**`.
- Omar a demandé de ne plus faire de passe de fact-checking séparée (trop lente) : vérifier soi-même chaque chiffre
  et chaque citation à la source pendant l'écriture, et le noter dans `episodes/<slug>/sources.md`.

## Règle n°16 — Faire découvrir les vidéos longues (diagnostic du 08/11/2026, PRIORITAIRE)
Constat (stats du 08/11) : 98 % des vues viennent du flux Shorts ; les vidéos longues font 6 à 114 vues ; trafic « Accueil »
(browse) = 0, « Vidéos suggérées » = 89, et le lien Short → vidéo longue n'a servi que **2 fois** (SHORTS_CONTENT_LINKS).
La rétention n'est pas le problème n°1 (cacao : 0,64, au-dessus de la moyenne) : YouTube ne montre presque pas les vidéos longues.
1. **Lien « Vidéo associée » sur chaque Short** : c'est le seul lien cliquable dans le flux Shorts (un lien en description ou en
   commentaire n'est quasi jamais cliqué). L'API ne permet pas de le régler : Omar le met à la main (YouTube Studio, onglet
   Détails → « Vidéo associée », en « version pour ordinateur » sur le navigateur du téléphone si besoin). À chaque fiche de
   Short, écrire la vidéo longue à associer dans `videos/<slug>/_workspace/07_videos_associees.md` et la lui rappeler.
   (08/11 : Omar a déjà relié les Shorts existants ; les clics n'apparaissent dans les stats qu'avec 2 à 3 jours de retard.)
2. **Short « bande-annonce »** : au moins un Short par sortie se termine sur la question non résolue de la vidéo longue
   (« la réponse est dans la vidéo, lien juste au-dessus »), jamais sur la réponse.
3. **Publier la vidéo longue AVANT les Shorts** du même sujet (au moins 24 h), pour que chaque Short ait sa vidéo associée
   dès sa sortie. Pas de Shorts orphelins (cigarettes, iPhone, jean : sans vidéo longue → à associer à la vidéo la plus proche).
4. **Titre + miniature pensés pour l'accueil, pas pour la recherche** : la vidéo longue doit gagner le clic face aux autres
   miniatures (règle n°14 : image générée, un objet + une main, une question + un chiffre). Jamais une capture du rendu.
5. **Intro** : les trois vidéos perdent 20 à 35 points entre 0:09 et 0:14, juste quand on passe de l'accroche à la mise en place
   (« quatre suspects », devinette, voix du sceptique). Avant 15 s : une image forte et nouvelle toutes les 2 s, pas d'annonce
   de plan (« on va suivre… », « quatre suspects »), on entre directement dans le premier suspect.
5 bis. **Mesure du 08/11 (Reporting réparé)** : YouTube MONTRE les vidéos longues mais personne ne clique. Cacao : 3 161 impressions,
   taux de clic 1,3 % ; gazole : 357 impressions, 1,7 % ; baguette : 461, 3,7 %. Norme visée : 4 à 8 %. Les Shorts n'envoient
   que 2 vues par vidéo longue (SHORTS_CONTENT_LINKS). → Le premier chantier est la miniature + le titre, avant le montage.
   Viser > 4 % ; sous 2 % après 1 000 impressions : changer la miniature puis le titre (API videos.update / thumbnails.set,
   avec l'accord d'Omar), une seule chose à la fois, 48 h entre deux changements.
5 ter. **Miniatures v2 (08/11, mises en ligne)** : `scripts/miniatures/miniatures_v2_081126.py` (images tirées du rendu,
   sans sous-titres : recadrer au-dessus de y = 840). Recette : UN contraste visible en 1 s (cacao −60 % | tablette ?,
   baril ↓ | plein ↑, pièce de 1 € | « qui le prend ? »), 3-4 mots en Inter Black avec contour noir, un visage si possible,
   vérifiée à 168 px de large. Anciens taux : cacao 1,3 %, gazole 1,7 %, baguette 3,7 % → comparer à 48-72 h.
   Action `modifier` de bmo-studio-link : `titre` + `miniature_url` (image poussée dans le-vrai-prix-medias/miniatures/).
5 quater. **Mise à jour du 09/11 (stats API de 13 h 59 UTC : 13 abonnés, 9 818 vues, 267 vues pour les 4 vidéos longues)** :
   - **Correction** : dans l'API, la source `SUBSCRIBER` n'est pas « les abonnés » : c'est « Fonctionnalités de navigation »
     (accueil, fil d'abonnements, historique). La baguette a donc eu 101 de ses 114 vues par là (les visionnages d'Omar peuvent
     en faire partie), pas 0 comme écrit plus haut. YouTube l'a testée, les gens sont partis (26 % regardé, rétention relative
     0,36) et il a arrêté. Le cacao a été testé en suggestions (3 555 impressions) et a calé au clic (1,38 %).
   - **Le sujet décide de la diffusion** : le cacao (dans l'actualité) a eu 6 à 10 fois plus d'impressions que les autres.
     Une vidéo longue = un sujet que les gens cherchent ou regardent déjà cette semaine-là. Sinon on ne la fait pas.
   - **Les Shorts n'amènent pas de vues longues** : 7 789 vues de Shorts → 4 clics vers une vidéo longue. Ne pas compter
     dessus ; la vidéo longue doit gagner seule (sujet + clic + 30 premières secondes).
   - **On ne retouche plus titres ni miniatures des 4 vidéos avant le 15/11** : les v2 datent du 08/11 au soir, les taux de
     clic affichés mélangent encore l'ancien et le nouveau. Ensuite une seule chose à la fois.
   - **Une seule vidéo longue par semaine** (4 en 7 jours du 01 au 07/11 : aucune n'a eu le temps d'être mesurée).
6. Mesurer : nombre de clics « vidéo associée » et vues longues venant de SHORTS_CONTENT_LINKS dans `dernier.md`.
   Attention : moins de 100 vues par vidéo = courbes très bruitées (1 personne = 3 à 8 points) ; ne pas surcorriger.

## Règle n°17 — Leviers de découverte (08/11/2026, mis en place) — à appliquer à CHAQUE sortie
1. **Shorts qui ouvrent, pas qui ferment** (remplace « devinette posée puis tranchée » de la règle n°14) : au moins 6 Shorts sur 8
   finissent sur une question liée à la vidéo longue, sans la trancher ; dernier plan : « La réponse est dans la vidéo : touche
   le lien juste en dessous. » Les 2 autres peuvent trancher une devinette secondaire (jamais la réponse principale).
   Constat : ~6 000 vues de Shorts → 2 vues de vidéo longue chacune.
2. **Playlist « Le Vrai Prix — les enquêtes »** (https://www.youtube.com/playlist?list=PLOjdVM6W6N0A), en section n°1 de la
   page d'accueil de la chaîne : chaque nouvelle vidéo longue y entre en tête (fiche `playlist` avec `en_tete`).
   La bande-annonce de la chaîne (non-abonnés) = la vidéo longue au meilleur taux de clic × rétention (fiche `chaine`,
   `bande_annonce`) ; aujourd'hui le cacao.
3. **Description orientée recherche** : 1re ligne = les mots que les gens tapent (« prix gazole », « prix capsule nespresso »…),
   puis « ▶ Enquête suivante / précédente : lien » et « ▶ Toutes les enquêtes : lien playlist », puis chapitres et sources.
   Tags : la limite YouTube de 500 se compte en octets avec les guillemets (le script garde 450).
4. **Caler la sortie sur l'actu** : si le sujet est dans l'actualité (hausse, record, annonce), sortir dans les 24-48 h et le dire
   dans le titre (« en ce moment », un chiffre du jour vérifié). Sinon, sortir le même jour/heure chaque semaine.
5. **Écran de fin** (Studio seulement, à rappeler à Omar à chaque sortie) : vidéo « la plus adaptée au spectateur » + playlist des enquêtes.
6. **Voix d'Omar** : proposer à chaque vidéo d'enregistrer au téléphone l'accroche (30 s) dans `episodes/<slug>/voix/`.

## Règle n°18 — Ce que dit la documentation officielle (vérifié le 08/11/2026) — PRIORITAIRE sur les « astuces » de créateurs
Sources : aide YouTube « Search & Discovery : the Algorithm and Performance FAQs » (support.google.com/youtube/answer/141805),
annonces TeamYouTube / Creator Insider. Les sites d'agences (AIR, OutlierKit, vidIQ…) ne sont que des sources secondaires.
- **Accueil** = performance auprès de spectateurs similaires + historique de chaque spectateur. **Recherche** = titre, description et
  contenu qui collent à la requête, puis l'engagement sur cette recherche → 1re ligne de description = les mots tapés (règle 17).
- **Vidéos longues : c'est le temps de visionnage ABSOLU qui compte** (le relatif compte surtout pour les vidéos courtes). Une vidéo de
  10 min regardée 4 min vaut mieux qu'une de 4 min regardée 2 min → viser 8-12 min SI la rétention tient (règle 7 ter), jamais du remplissage.
- **Le rythme et l'heure de publication n'ont pas d'effet mesuré** (YouTube n'a trouvé aucun lien entre délai entre vidéos et vues).
  Priorité à la qualité ; la régularité sert seulement les habitudes du public (remplace « même jour, même heure » de la règle 7 ter).
- **Les anciennes vidéos repartent** quand une nouvelle vidéo renvoie vers elles → série « Le Vrai Prix », liens « enquête précédente »,
  écran de fin vers une ancienne enquête, mention orale (« dans l'enquête sur le chocolat… »).
- **Titre/miniature** : changer peut aider, mais « ne pas changer ce qui marche » ; toujours fidèles au contenu (le clickbait fait partir).
- **Les abonnés ne regardent pas tout** : ne pas compter sur les notifications ; c'est l'Accueil et les suggestions qui font les vues.
- **Shorts originaux favorisés depuis le 01/10/2026** : nos Shorts sont tirés de nos vidéos (OK) ; varier les formats pour ne pas
  ressembler à un modèle répété (règles de monétisation « contenu inauthentique » précisées le 16/07/2026).
- **Monétisation (annonce du 10/08/2026)** : jusqu'au 31/01/2027, 1 000 abonnés + 4 000 h (365 j) ou 10 M vues Shorts (90 j) ;
  **à partir du 01/02/2027 : 1 000 abonnés + 8 000 h ou 20 M vues Shorts**. Au 08/11 : 13 abonnés, 4,8 h → le seuil de janvier est hors
  d'atteinte ; la voie réaliste est le temps de visionnage des vidéos longues (8 000 h). Les vues Shorts n'y comptent pas.

## Règle n°19 — Outils officiels à exploiter (recherche du 08/11/2026)
1. **Doublage / audio multilingue** : le doublage automatique YouTube (français → anglais, voix « Expressive Speech ») est ouvert à tous
   les créateurs qui ont activé les fonctionnalités avancées ; YouTube dit qu'il ne nuit pas à la découverte, et les créateurs avec des
   pistes multilingues tirent en moyenne plus de 25 % de leur temps de visionnage d'autres langues. Toutes les langues comptent dans les
   8 000 h. → Omar active « Autoriser le doublage automatique » (Studio > Paramètres > Chaîne > Paramètres avancés). Ensuite seulement :
   titres/descriptions traduits (fiche `traduire` de bmo-studio-link). Notre voix étant de la synthèse depuis un script, piste maison
   possible (Edge TTS espagnol / arabe / portugais) téléversée comme piste audio multilingue (Studio seulement, pas d'API).
   Privilégier les sujets universels (cacao, café, iPhone, jean) pour les autres langues ; pas le gazole français.
2. **Test & Compare** (Studio ordinateur) : jusqu'à 3 titres, 3 miniatures ou 3 combinaisons ; gagnant = part du temps de visionnage, pas
   le taux de clic ; 1 à 2 semaines. → Pour chaque vidéo, livrer 3 miniatures + 3 titres dans `videos/<slug>/_workspace/06_test_compare/`.
3. **Hype** : seulement pour les chaînes du Programme Partenaire entre 500 et 500 000 abonnés, vidéos longues de moins de 7 jours.
   Palier intermédiaire visé : programme « étendu » (500 abonnés + 3 000 h ou 3 M vues Shorts), seuil inchangé en 2027.
