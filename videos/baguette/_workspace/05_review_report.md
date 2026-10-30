# Rapport de relecture finale : baguette

Slug : `baguette` · Rôle : production-reviewer · Date : 30/10/2026 · Mode automatique (aucune question à Omar)
Lu : brief, recherche, script, fact-check, fiche miniature + `miniature.jpg`, SEO, `plans.json`, `episodes/baguette/montage.json`,
`reglages_monteur.json`. Vérifié sur le rendu `baguette.mp4` (15:40, 493,9 s) : images extraites à l'accroche, aux six cartes
de chapitre, aux plans p100-p105 et à la fin.

## Bilan

- **Prêt pour la mise en ligne** : 🟡 À corriger puis publier. Les ROUGE du SEO sont corrigés. Il reste une décision à prendre sur la vidéo (re-rendre ou non, voir ORANGE n°1).
- **En bref** : la stratégie, le script, la miniature et l'accroche disent la même chose (« 1 €, dont 6 centimes de blé ; où va le reste ? »), et les chiffres concordent partout. Deux chapitres tombaient à côté de leur carte, et le titre recommandé répétait la miniature : les deux points sont corrigés dans `04_seo_metadata.md`.
- **Total** : 3 ROUGE (tous corrigés dans le SEO, aucun dans la vidéo) · 5 ORANGE · 6 VERT.

## Arbitrage du titre

**Titre final : « Prix de la baguette : où va vraiment ton euro ? »** (47 caractères)

- **Pourquoi pas le titre du SEO** (« Prix de la baguette : 1,01 €… dont 6 centimes de blé ») : la miniature affiche déjà « LE BLÉ ? 6 CENTIMES ». Le titre redirait la même information, et on perdrait la moitié de ce qui donne envie de cliquer. Autre défaut : il met « 1,01 € » à côté du « 1 € » de la miniature, donc deux prix pour le même objet.
- **Pourquoi pas le titre du designer tel quel** (« Combien coûte VRAIMENT une baguette ? ») : il a raison sur la complémentarité, mais il perd le mot-clé principal « prix de la baguette », que le brief exige dans le titre (§ notes SEO). Les majuscules sur « VRAIMENT » sonnent aussi racoleur.
- **Le titre retenu** garde le mot-clé du SEO en tête et applique le principe du designer :
  - le titre pose la question (« où va ton euro ? ») ;
  - la miniature donne le premier morceau de réponse (6 c de blé sur 1 €) ;
  - l'accroche reprend les deux à la lettre en 8 s : « Dans une baguette à un euro, le blé coûte… six centimes. […] Alors, où passent les quatre-vingt-quatorze autres centimes ? ».
- **La promesse est tenue** par les parties 05 (la facture de l'observatoire des prix et des marges, l'OFPM) et 06 (la caisse du boulanger). « Ton euro » reprend aussi le chapitre 06. Ce n'est pas un piège à clics.
- **Réserve pour un test A/B** : « Combien coûte vraiment une baguette ? », à essayer si le taux de clic est faible après 48 h.

## Constats

### ROUGE (à corriger obligatoirement)

1. **SEO, titre recommandé**
   - Problème : le titre et la miniature se répètent (« 6 centimes de blé » / « LE BLÉ ? 6 CENTIMES »), et le titre donne 1,01 € quand la miniature dit 1 €.
   - Avant : « Prix de la baguette : 1,01 €… dont 6 centimes de blé ».
   - Corrigé : section « 0. Titre final » ajoutée à `04_seo_metadata.md` (voir l'arbitrage ci-dessus). La ligne « Miniature associée au n°1 » décrivait une miniature « 6 c » qui n'existe pas : elle décrit maintenant la miniature réellement livrée.

2. **SEO, chapitre 01 « Le grain »**
   - Problème : à 00:25, on est encore sur la mosaïque de l'accroche (« le moulin, la pâte… »). La carte « Partie 01 » n'apparaît qu'à 29,5 s. YouTube ouvrirait le chapitre au milieu de l'accroche.
   - Avant : 00:25.
   - Corrigé : 00:29, dans la description et dans la section 3.

3. **SEO, chapitre 03 « La pâte »**
   - Problème : à 02:31, la carte est déjà terminée (on est sur le plan du décret, p041). La carte apparaît à 148 s.
   - Avant : 02:31.
   - Corrigé : 02:28.
   - Recalé au passage, d'après la mesure : 02 = 01:29, 04 = 03:55 (à 03:54, on voit encore la fin de p059), 06 = 06:28. Le chapitre 05 (05:07) était juste. L'estimation par nombre de mots est remplacée par la mesure sur le MP4.

### ORANGE (à corriger de préférence)

1. **Vidéo, plans p100 et p103** (signalé seulement, pas corrigé : la vidéo est déjà rendue)
   - Dans le MP4 de 15:40, deux plans enfreignent la règle n°1 (on doit voir l'objet dont on parle) :
     - p100 : la vignette « Baguette » montre un hot-dog autrichien (pain évidé, `Austrian_Hot_Dog.jpg`) ;
     - p103 : la vignette « Farine » montre une aile de moulin à vent en contre-plongée (`pv:784`).
   - `montage.json` a déjà été corrigé à 15:46, après le rendu, via `reglages_monteur.json` (p100 → `pi:923865` ; p103 → `Chef sifting flour.jpg`). Il faut donc relancer le rendu avant la mise en ligne.
   - Les crédits du SEO correspondent au MP4 de 15:40. Ils restent juridiquement sûrs dans les deux cas : la photo de Landon Heredia est dans le domaine public, et Pixabay n'impose pas de crédit. Après le nouveau rendu, appliquer les deux remplacements notés en fin de section 6 de `04_seo_metadata.md`.

2. **Fin de vidéo, annonce du chocolat** (p119 et p120)
   - Problème : la voix dit « La semaine prochaine, on suit l'argent du chocolat ». C'est une promesse datée.
   - Correction proposée : si la vidéo chocolat n'est pas prête dans 7 jours, ne pas la mettre dans l'écran de fin. Mettre plutôt « vidéo la plus adaptée au spectateur », et lancer la vidéo chocolat ensuite comme prévu dans le planning.

3. **Commentaire épinglé et carte de fin « Qui paie la baguette à 28 c ? »**
   - Problème : le fact-check classe ce point ORANGE, à surveiller. La question laisse entendre une vente à perte que rien ne prouve : Leclerc affirme garder une marge.
   - Dans la vidéo, la formule reste une question, ce qui est acceptable. Dans le commentaire épinglé, ne rien ajouter qui y réponde par l'affirmative.
   - Version plus neutre proposée pour le commentaire : « À 28 centimes au supermarché contre 1,12 € en boulangerie : pour toi, c'est la même baguette ? Et chez toi, elle coûte combien ? Donne ta ville et ton prix. »

4. **Crédits CC BY / CC BY-SA**
   - Problème : les liens complets ne sont que dans les commentaires 2 et 3. Un commentaire peut être filtré par YouTube ou supprimé par erreur.
   - Correction proposée : ajouter en fin de description une ligne vers le `credits.txt` de la Release GitHub, si le dépôt est public, ou garder les deux commentaires et vérifier qu'ils restent visibles après publication.

5. **Mots-clés de recherche**
   - Problème : avec le titre final, la requête « combien coûte une baguette » n'est plus ni dans le titre ni dans la description.
   - Correction proposée : commencer la description par « Combien coûte vraiment une baguette ? Le prix de la baguette : 1,01 € en moyenne… ». Elle reste dans les tags.

### VERT (pour information)

1. **Accroche** : la promesse est posée dès la 3e seconde (le zoom sur « 6 CENTIMES » tombe à 3,2 s, avec l'impact sonore). Le schéma affiche bien 0,06 € (on voit « 0,01 € » à 5 s parce que le compteur est en train de monter). La boucle « 94 autres centimes » est ouverte à 8 s.
2. **Chiffres** : ils sont les mêmes dans le script, `plans.json`, la miniature et le SEO.
   - Prix et part du blé : 1 € et 1,01 € (OFPM), 6 c de blé, 6 % du prix hors taxes.
   - Découpe de la baguette : 7 c pour le meunier, 5 c de TVA, 83 c après le moulin.
   - Autres prix : 1,12 € en boulangerie, 29 c chez Leclerc en 2022, 28 c en mars 2026.
   - Aucun chiffre « environ » du fact-check n'apparaît dans les métadonnées.
3. **Le mot-clé « prix de la baguette »** est dans le titre, dans la première ligne de la description, dans le chapitre 05 et dans les tags. À l'oral, l'accroche dit « une baguette à un euro » : c'est acceptable, on ne retouche pas la vidéo pour ça.
4. **Leclerc** :
   - Il est nommé pour des faits datés et sourcés (RMC et Pleinchamp, 11/01/2022), et sa propre version est citée.
   - Le ROUGE du fact-check sur la pâte surgelée est corrigé.
   - Les façades et logos Leclerc à l'écran (p111, p112) sont un usage factuel, dans une vidéo documentaire, avec la source à l'écran.
   - Leclerc est absent de la miniature, comme le voulait le brief (décision 10).
   - Aucune marque n'est dénigrée sans source.
5. **Voix de synthèse** : elle est mentionnée dans la description (Pocket TTS, Kyutai). La case « contenu modifié ou synthétique » n'est pas requise : il n'y a aucune image réaliste générée par IA, et la voix n'imite personne. Le quignon orange de la miniature est un effet graphique visible, pas une tromperie.
6. **Sous-titres** : il n'y a pas de fichier SRT. Les sous-titres sont incrustés dans l'image. Plus tard, on pourrait téléverser un SRT tiré de la narration du script pour l'accessibilité et pour une piste en anglais (le brief en parle).

## Tableau de cohérence

| Vérification | État | Remarque |
|---|---|---|
| Stratégie ↔ Script | ✅ | L'angle « comment c'est fait + qui touche quoi » est tenu. Les 6 parties correspondent au brief. La vidéo dure 8:14 pour 8 min visées. |
| Script ↔ Miniature | ✅ | La miniature est l'image réelle de p086 (trois baguettes croisées). Le « 6 CENTIMES » est expliqué entre 0 et 8 s. |
| Script ↔ SEO | ✅ (après correction) | Les chapitres sont recalés sur le MP4. La description et les tags reprennent le script. |
| Titre ↔ Miniature ↔ Accroche | ✅ (après correction) | La question est dans le titre, la première réponse sur la miniature, et l'accroche relie les deux mot pour mot. |
| Crédits / sources | ⚠️ | Les crédits sont complets pour le MP4 de 15:40. Deux lignes changent en cas de nouveau rendu. `sources.md` est présent, et les sources principales sont dans la description. |
| Règles YouTube | ✅ | Pas de titre trompeur, la voix de synthèse est mentionnée, la marque est citée avec sa source. Un seul appel à l'abonnement, après la moitié de la vidéo (p109). |

## Livrables finaux

- [x] Script complet (`02_scriptwriter_script.md`, `plans.json`)
- [x] Miniature (`miniature.jpg`, 1280×720, testée en 320 px)
- [x] Paquet SEO : titre final, description, tags, hashtags (`04_seo_metadata.md`)
- [x] Chapitres (mesurés sur le MP4)
- [ ] Fichier de sous-titres SRT (facultatif, sous-titres incrustés)
- [ ] Nouveau rendu après les corrections p100 et p103 faites dans `montage.json`, puis mise à jour des deux lignes de crédits
