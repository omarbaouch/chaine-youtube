# Fiche miniature : la baguette

**Slug :** `baguette` · **Format :** 1280×720 (16:9) · **Date :** 30/10/2026 · **Statut :** décidé seul (mode automatique)
**Règles appliquées :** `monteur-chaine` n°1 (vraie baguette, pas de dessin), n°7 (une seule info en orange), n°8 (Montserrat 900,
orange héros `#FF6B2C`, blanc `#F2F4F7`) ; brief stratège §« Notes pour le designer de miniature » ; aucune marque, aucun logo.
**Fichier livré :** `miniature.jpg` (1280×720) + `miniature_320.jpg` (contrôle téléphone). Recette : `miniature_sources/`.

---

## Concept A : « La part du blé » (RETENU)
- **Composition :** vraie photo tirée du rendu (≈ 339,8 s, image sans sous-titre) : trois baguettes croisées sur fond noir.
  Le quignon de la baguette du dessus est coupé net (environ 6 % de sa longueur), écarté de 30 px, teinté orange avec un halo,
  ligne de coupe en pointillés blancs. Pastille sombre « 1 € » en blanc sur le corps de la baguette.
  Texte calé en haut à droite, dans la zone sombre.
- **Texte (3 mots) :** « LE BLÉ ? » (blanc, 104 px) / « 6 » (orange, 250 px) / « CENTIMES » (orange, 92 px).
- **Émotion :** curiosité, puis surprise (« c'est tout ? ») ; le spectateur se demande où partent les 94 autres centimes.
- **Contraste :** fond quasi noir contre pain doré ; une seule couleur héros (orange) qui relie le chiffre au quignon coupé ;
  texte blanc et orange avec contour noir et ombre portée. Lisible à 320 px, « 6 » encore lisible à 128 px.
- **Pourquoi lui :** c'est exactement le pic visuel de la vidéo (la baguette découpée selon qui touche quoi) : le clic tient
  sa promesse dès l'accroche (« le blé coûte… six centimes »). Objet réel reconnaissable en moins d'une seconde.

## Concept B : « Le ticket »
- **Composition :** photo de l'accroche (≈ 0,5 s) : baguette sur bois sombre avec épis de blé, à gauche. À droite,
  un ticket de caisse vitré avec une seule ligne « BAGUETTE … 1,10 € » et un tampon « ? » orange.
- **Texte (3 mots) :** « QUI TOUCHE QUOI ? »
- **Émotion :** soupçon (« je me fais avoir ? »), envie de suivre l'argent.
- **Contraste :** bois brun et pain doré, ticket blanc lumineux ; orange réservé au « ? ».
- **Limite :** plus chargé (deux zones), le ticket est un élément graphique ; moins net à 320 px que A.

## Concept C : « Le vrai coût, c'est la nuit »
- **Composition :** rush réel d'un boulanger qui enfourne à la pelle devant les flammes (four à bois), plan serré, ambiance nuit.
  Grand chiffre posé sur un panneau vitré à droite.
- **Texte (3 mots) :** « 83 CENTIMES ICI » (83 en orange).
- **Émotion :** retournement, empathie (« ce n'est pas le boulanger qui se gave »).
- **Contraste :** flammes chaudes sur fond noir ; risque que l'orange des flammes concurrence le chiffre orange.
- **Limite :** on ne voit pas la baguette elle-même au premier coup d'œil : le test des 3 secondes est moins sûr.

---

## Choix : A
Un seul objet, réel, une seule information en orange, et c'est l'image de la révélation de la vidéo (cohérence clic → vidéo).
B et C restent en réserve pour un test A/B si le taux de clic est faible après 48 h.

## Validation titre et miniature
| Titre candidat (brief) | Miniature A | Miniature B | Remarque |
|---|---|---|---|
| Combien coûte VRAIMENT une baguette ? | **Oui (recommandé)** | Oui | La miniature donne la réponse choc, le titre pose la question : complémentaires. |
| Ta baguette coûte 1 €. Le blé dedans ? 6 centimes. | Non | Oui | Avec A, titre et miniature répètent « 6 centimes ». |
| Où vont les 1,10 € de ta baguette ? | Oui | Moyen | Avec A : 1,10 € dans le titre, 1 € sur la photo ; acceptable, mais préférer le titre 1. |
| La baguette à 29 centimes est-elle possible ? | Moyen | Non | Polémique enseigne : ne pas l'associer à une miniature « qui touche quoi ». |
| Farine, eau, sel, levure : l'ingénierie cachée de la baguette | Moyen | Non | Angle « comment c'est fait » : la miniature A (argent) le complète, mais promet autre chose. |

## Contrôles faits
- 1280×720 JPG, vraie photo de baguette, pas de logo, une seule couleur héros (orange).
- Vu en 320×180 et 128×72 : « LE BLÉ ? » et « 6 CENTIMES » lisibles, la baguette reconnaissable, le quignon orange visible.
- Chiffres conformes au script et au fact-check : blé ≈ 0,06 € pour une baguette à environ 1 € (OFPM 2026, données 2025, ramené à 250 g).

## Refaire la miniature
Police : `montserrat-latin-900-normal.woff` (fontsource) convertie en TTF avec fontTools (`flavor=None`).
```bash
python3 miniature_sources/compose_miniature.py miniature_sources/image_rendu_339-8s.png miniature.jpg <montserrat900.ttf>
```
Si le rush des trois baguettes change au prochain rendu, réextraire une image sans sous-titre et recaler l'axe `A`/`B` du script.
