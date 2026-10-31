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
- Voix : Pocket TTS (Kyutai), modèle `french_24l`, voix `estelle`, **5 étapes de calcul**. Accent validé par Omar.
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

## Règle n°10 — Bibliothèques de mouvement installées (31/10/2026)
- `.claude/skills/video-shotcraft/` (Apache 2.0) : 124 « cartes de plans » cinématiques Remotion (caméra, ouverture, transitions,
  typographie, effets d'impact, données). Avant d'écrire une scène animée, piocher une carte dans `references/shots/` et
  l'adapter à nos briques (objet réel d'abord, règle n°1). Sons : `references/sound-design.md`.
- `.claude/skills/emotional-narrative/` (MIT) : principes d'animation pensés pour l'émotion (anticipation, timing, silence).
  À relire avant chaque moment fort (révélation, histoire humaine).
