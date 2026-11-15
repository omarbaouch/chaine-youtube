# TASTE.md — profil de goût de la chaîne « Le Vrai Prix » (Omar)

Confirmed-by: Omar (2026-11-15)

> Profil chargé par le skill `find-broll` avant toute recherche d'images. Il remplace le profil d'exemple livré avec le skill
> (celui de Louise de Sadeleer). Les règles d'Omar dans `.claude/skills/monteur-chaine/SKILL.md` passent avant tout le reste.

## Réponses d'Omar à l'onboarding (15/11/2026, validées par « ok »)
1. **Son des images d'illustration** : coupé (`ffmpeg -an`). On n'entend que la voix, la musique et les bruitages du studio.
2. **Photos fixes** : léger zoom avant lent (Ken Burns ~1,5 %/s, centré, plafonné à ~2 %/s).
3. **Crédit de la source** : oui, en petit en bas à droite, couleur `auto` (blanc ou noir selon l'image) ; à gauche si l'image a déjà
   un logo en bas à droite. Nom court de la source (« Pixabay », « Wikimedia Commons », « UFC-Que Choisir »), jamais d'URL.
4. **Animations Remotion** pour les chiffres, schémas et décompositions de prix : oui, dans le projet existant du studio
   (`/home/claude/chaine-youtube` : `src/motion/`, thème `src/theme.ts`). Jamais de nouveau projet Remotion.
5. **Images générées par IA** : non.

## Ce que la chaîne montre (règles n°1 et n°2 de `monteur-chaine`)
- **L'objet réel dont parle la phrase**, reconnaissable : la capsule, le paquet de pâtes, le compteur, la facture. Jamais un symbole
  ou un dessin à la place.
- **Preuves à l'écran** : captures des documents officiels cités (rapport, tableau, page de prix), surlignées.
- **Plans d'Omar** filmés au téléphone : toujours prioritaires sur une banque d'images.
- Rythme : un plan toutes les 3 à 6 s en vidéo longue, environ toutes les 3 s en Short.

## Sources autorisées (licence libre ou document public cité)
- **Pixabay** (vidéos et photos) — banque par défaut, via `scripts/medias.mjs` et `short_vertical.py`.
- **Wikimedia Commons** — photos d'objets, de lieux, d'archives (vérifier la licence de chaque fichier, créditer l'auteur).
- **Captures de documents officiels**, citées comme sources : INSEE, CRE, Observatoire des prix et des marges (OFPM), DGCCRF,
  service-public.gouv.fr, CNC, Commission européenne, UFC-Que Choisir, 60 Millions de consommateurs.
- **Plans filmés par Omar.**

## Interdits
- Aucun extrait de vidéo YouTube, de télé ou de film, même crédité (droits d'auteur, Content ID).
- Aucun mème ni capture de réseau social d'une personne privée.
- Aucune image générée par IA.
- Aucune image hors sujet (thé versé pour parler d'une capsule, volcan pour les cigarettes : erreurs déjà relevées).

## Mode automatique
Le studio tourne sans validation d'Omar (décision du 29/10/2026) : le skill réduit le choix à 2-3 candidats par phrase, puis le
contrôle qualité du studio choisit selon la règle n°1. Omar ne choisit lui-même que s'il le demande.
