# Combien coûte VRAIMENT une canette vide ?

> Durée estimée : environ 20 s (teaser) | Ton : direct, complice, tutoiement | Voix : Pocket TTS `french_24l`, `estelle`, température 0,3
> Slug : `test-canette-20s` · 16:9, 1920×1080, 30 i/s · Brief : `01_strategist_brief.md` (accroche A retenue)

---

## HOOK (0:00–0:03)

**Narration :**
Devine combien coûte cette canette. Vide.

**Indications visuelles :**
- [Rush : gros plan de canettes vides en aluminium qui défilent sur un convoyeur]
- [Couche : `Visee` qui se verrouille sur UNE canette nette, au centre, puis `Etiquette` « Prix : ? »]

> Note de montage : choisir un rush où les canettes avancent lentement ou ralentir à 0,7 pour que la visée suive vraiment la canette (position vérifiée sur la planche). Étiquette « ? » sans devise : la réponse arrive en dollars au plan 4, on ne veut pas annoncer des euros puis répondre en dollars.

---

## Segment 1 : La fabrication accélérée (0:03–0:10)

**Narration :**
Une bande d'aluminium entre d'un côté.
De l'autre, des canettes sortent à la chaîne, sans jamais s'arrêter.

**Indications visuelles :**
- [Rush plan 2 : vraie bobine ou bande d'aluminium clair et brillant qui se déroule]
- [Couche : `Annotation` pointée sur la bande : « Bande d'aluminium ≈ 0,3 mm », source en petit « alcircle.com »]
- [Rush plan 3 : ligne de canettes vides à pleine vitesse, accélérée 1,5 à 2]
- [Couche : `Flash` + secousse légère + choc métallique sur la coupe 2 → 3]

> Note de montage : le plan 2 est le plus risqué au repérage. Si aucune vraie bobine d'aluminium (pas d'acier rouillé, pas de câble), on fusionne les plans 2 et 3 avec la narration de secours : « Sur la ligne, des canettes sortent à la chaîne, sans jamais s'arrêter. » (11 mots, même durée que la phrase supprimée + celle-ci, à recaler).

---

## Transition (0:10)

[Coupe sèche + « tic » de compteur : on passe de la masse (des milliers de canettes) à UNE seule canette. Changement d'échelle = interruption de rythme.]

---

## Segment 2 : La révélation (0:10–0:14)

**Narration :**
La fabriquer coûte moins de quatre centimes. De dollar.

**Indications visuelles :**
- [Rush plan 4 : une canette seule, nette, en plan serré]
- [Couche : `Vitre` + `Compteur` qui descend vers « < 0,04 $ » ; « tic » à chaque palier]
- [Surtitre en petit, bas d'écran : « Estimation : Adam S. Hersh, Economic Policy Institute, via CNN, 2 mars 2025 »]

> Note de montage : garder le point isolé avant « De dollar. » pour la pause. Le compteur s'arrête sur « < 0,04 $ » pile sur « quatre centimes », le « $ » ressort (couleur d'accent) sur « De dollar ».

---

## CTA

Aucun appel à l'abonnement : c'est un teaser de 20 s, la boucle ouverte fait office d'appel (« la vidéo complète arrive »). L'appel à l'abonnement ira dans la vidéo complète, une seule fois, pas au début.

---

## CLOSING (0:14–0:20)

**Narration :**
Alors, où passe tout le reste de ce que tu paies ?
On suit l'argent, centime par centime.

**Indications visuelles :**
- [Rush plan 5 : rayon de supermarché rempli de canettes, idéalement une main qui en prend une]
- [Couche : `MotsQuiMontent` « Où va le reste ? »]
- [Rush plan 6 : paiement en pièces à une caisse, ou pièces de monnaie en gros plan dans une main]
- [Couche : `MotsQuiMontent` « On suit l'argent », puis carton final « Bientôt : la vidéo complète »]

> Note de montage : ton de confidence sur la chute (nappe qui baisse d'un cran). Le carton final reste 1 s après la fin de la voix.

---

## Nombre de mots / durée estimée
- Total : 50 mots parlés (brief : environ 50, max 55)
- Durée estimée : environ 19 à 20 s avec les pauses (« Vide. », « De dollar. »), Pocket TTS ≈ 2,6 mots/s
- Les minutages du découpage sont des estimations : à recaler sur la durée réelle de chaque phrase après génération de la voix.

## Contrôle règle n°1 (ce qu'on voit = ce qu'on dit)
| Mot dit | Ce qu'on voit | Statut |
|---|---|---|
| « cette canette » | une canette vide réelle, verrouillée par la visée | OK |
| « bande d'aluminium » | vraie bobine/bande d'aluminium (sinon texte de secours) | À confirmer au repérage |
| « des canettes sortent à la chaîne » | ligne de canettes vides en aluminium à pleine vitesse | OK |
| « la fabriquer… quatre centimes » | une canette seule + compteur « < 0,04 $ » + source | OK |
| « ce que tu paies » | rayon de magasin avec canettes reconnaissables | OK |
| « l'argent, centime par centime » | pièces de monnaie / paiement en caisse | OK |

## Mots-clés (pour le SEO)
canette, aluminium, fabriquer, coûte, centimes, chaîne → « prix canette aluminium », « fabrication canette », « coût de fabrication canette ».

## Message clé de l'accroche (pour la miniature)
« Devine combien coûte cette canette vide » → miniature : une canette seule sur fond sombre, « 0,04 $ ? ».

---

## Découpage plan par plan (pour le monteur)

```json
{
  "plans": [
    {
      "id": "p1",
      "debut_s": 0,
      "fin_s": 3,
      "narration": "Devine combien coûte cette canette. Vide.",
      "image_reelle": "Gros plan de canettes vides en aluminium (non remplies, sans couvercle) qui défilent en file sur un convoyeur d'usine",
      "recherche": ["aluminum cans conveyor", "empty cans production line", "cans moving conveyor close up"],
      "couche_animee": "Visee qui se verrouille sur une canette nette au centre, puis Etiquette « Prix : ? »",
      "surtitre": ""
    },
    {
      "id": "p2",
      "debut_s": 3,
      "fin_s": 5.5,
      "narration": "Une bande d'aluminium entre d'un côté.",
      "image_reelle": "Bobine ou bande d'aluminium clair et brillant qui se déroule dans une usine (refuser acier sombre ou rouillé, câbles)",
      "recherche": ["aluminum coil unwinding", "aluminium sheet roll factory", "aluminum rolling mill"],
      "couche_animee": "Annotation (point + trait) posée sur la bande : « Bande d'aluminium ≈ 0,3 mm »",
      "surtitre": "Épaisseur : alcircle.com"
    },
    {
      "id": "p3",
      "debut_s": 5.5,
      "fin_s": 10,
      "narration": "De l'autre, des canettes sortent à la chaîne, sans jamais s'arrêter.",
      "image_reelle": "Ligne de fabrication de canettes vides en aluminium à pleine vitesse, plan large ou en enfilade (refuser bouteilles, jus, verre)",
      "recherche": ["can manufacturing line", "beverage cans factory automation", "canning line high speed"],
      "couche_animee": "Vitesse 1,5 à 2 ; Flash + secousse légère + choc métallique calés sur la coupe d'entrée",
      "surtitre": ""
    },
    {
      "id": "p4",
      "debut_s": 10,
      "fin_s": 14,
      "narration": "La fabriquer coûte moins de quatre centimes. De dollar.",
      "image_reelle": "Une seule canette en aluminium, nette, en plan serré (en usine ou sur fond neutre, marque peu visible)",
      "recherche": ["empty aluminum can macro", "single soda can rotating", "aluminum can close up"],
      "couche_animee": "Vitre + Compteur qui descend jusqu'à « < 0,04 $ » (tic à chaque palier, le $ en couleur d'accent sur « De dollar »)",
      "surtitre": "Estimation : Adam S. Hersh, Economic Policy Institute, via CNN, 2 mars 2025"
    },
    {
      "id": "p5",
      "debut_s": 14,
      "fin_s": 17.5,
      "narration": "Alors, où passe tout le reste de ce que tu paies ?",
      "image_reelle": "Rayon de supermarché rempli de canettes reconnaissables, idéalement une main qui en prend une",
      "recherche": ["hand taking can from shelf", "soda cans supermarket shelf", "drinks aisle cans"],
      "couche_animee": "MotsQuiMontent « Où va le reste ? »",
      "surtitre": ""
    },
    {
      "id": "p6",
      "debut_s": 17.5,
      "fin_s": 20.5,
      "narration": "On suit l'argent, centime par centime.",
      "image_reelle": "Pièces de monnaie en gros plan : paiement en pièces à une caisse ou pièces posées dans une main",
      "recherche": ["paying with coins checkout", "coins in hand close up", "counting coins slow motion"],
      "couche_animee": "MotsQuiMontent « On suit l'argent », puis carton final « Bientôt : la vidéo complète »",
      "surtitre": ""
    }
  ]
}
```
