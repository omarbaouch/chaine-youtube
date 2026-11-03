# Journal des décisions — chocolat (mode automatique, 03/11/2026)
- Sujet : chocolat (annoncé à la fin de la vidéo baguette). Brief : content-strategist.
- Fact-checking : pas de passe séparée (règle n°15 d'Omar, prioritaire sur le prompt programmé) ; la documentaliste a vérifié chaque chiffre et citation à la source (01b_recherche.md, sources.md).
- Citation de Laurent Koné : AFP 26/01/2026, 4 reprises concordantes ; racontée en voix off + citation écrite (règle 13 : pas de clip média).
- Repérage : 120 planches (lots a–e, g1–g2 vidéos seulement) + planches horodatées de reportages Commons (workflow « Planches Commons », nouveau).
  Correctif reperage.mjs : pauses + reprises sur 429 (4 repérages parallèles avaient tout bloqué).
- Règle n°9 (≤ 1/3 de photos) NON tenue : ~32 % de vidéos seulement. Le stock libre vidéo sur le cacao est quasi vide
  (Pixabay renvoie café, soja, Nutella). Gain : reportage VOA (domaine public, Côte d'Ivoire) découpé en 12 passages (champ "extrait"),
  fermentation (Commons CC BY), usine de tablettes (Commons). Les photos ont un Ken Burns. Solution durable : plans filmés par Omar.
- p041 : pas de vrai beurre de cacao en stock → écran partagé photo poudre + schéma « La presse » (règle 1 : le schéma explique ce qu'on ne peut pas montrer).
- p080 : pas de tablette entière sur fond uni → barre de décomposition au lieu de la découpe.
- p018 : texte « en tas ou dans des caisses » pour coller à la vidéo de fermentation en caisse.
- Doublons de photos supprimés (passages VOA à la place).
## Contrôle du rendu n°1 (chocolat-final-rapide-18, 7:22) → corrections
- Fiches suspect vides quand le média est une vidéo → Suspect accepte la vidéo (Schemas.tsx, Formats.tsx).
- Compteurs coupés avant la fin (p022, p066, p100, p111) → revele_a avancé + duree_min.
- « 2 800 F CFA/kg » coupé (p028) → unité raccourcie.
- Sous-titres/logos incrustés (fermentation, VOA, reportage CI) → nouveau champ "recadre" (crop 16:9) ; passages VOA limités à 3,5 s ("extrait_duree") + vitesse 0,8 pour ne jamais montrer un interviewé qu'on prendrait pour Laurent.
- p110 « pas de toit » montrait une case avec toit → fèves qui sèchent.
- Carte titre à 0:27,7 (< 30 s) → voix au débit naturel (+0 %) + p009 complété (« en Côte d'Ivoire »).
- Devinettes : compte à rebours 2 s au lieu de 3 (moins de temps sans changement d'image).
- Son rendu n°1 : -13,9 LUFS, crête -1,2 dBTP, aucun noir détecté → OK.
