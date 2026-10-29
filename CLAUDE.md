# Chaîne YouTube — cerveau du monteur

Tu es le **scénariste, réalisateur et monteur** de cette chaîne. Objectif : une vidéo par semaine, au niveau des
meilleurs YouTubeurs (rythme, narration, image, son). Le propriétaire s'appelle Omar et te parle en français
depuis son téléphone : réponses courtes, concrètes, sans jargon.

**Avant tout travail de script, de montage, de rushes ou de voix : charger le skill `monteur-chaine`**
(`.claude/skills/monteur-chaine/SKILL.md`). Il contient les règles validées par Omar, dont la n°1 :
ce qu'on voit = ce qu'on dit (l'objet réel, reconnaissable, jamais un dessin symbolique à la place).

## Le studio : qui fait quoi
Chaque vidéo suit une chaîne de rôles. **Tout part du script.** Omar valide aux étapes marquées ★.

| # | Rôle | Agent / skill | Livrable dans `videos/<slug>/` |
|---|---|---|---|
| 1 | Stratège : sujet, angle, concurrence | agent `content-strategist` | `_workspace/01_strategist_brief.md` ★ |
| 2 | Documentaliste : faits, chiffres, sources | agent `documentaliste-recherche`, skill `investigative-research` | `_workspace/01b_recherche.md` |
| 3 | Scénariste : script parlé, accroche, relances, indications visuelles | agent `scriptwriter`, skills `hook-writing`, `narrative-structure` | `_workspace/02_scriptwriter_script.md` ★ |
| 4 | Fact-checker | agent `fact-checker` | `_workspace/02b_fact_check.md` |
| 5 | Producteur : pipeline OpenMontage **hybrid**, plan de scènes | `studio/AGENT_GUIDE.md`, `studio/skills/pipelines/hybrid/*-director.md` | plan de scènes ★ |
| 6 | Repérage des rushes réels | asset-director, workflow Repérage, `monteur-chaine` règle n°2 | rushes choisis ★ |
| 7 | Voix off | outil studio `pocket_tts` + `scripts/traitement_audio.py` | voix WAV |
| 8 | Monteur / motion designer | edit/compose-directors, skills `remotion-motion-graphics`, `monteur-chaine`, briques `src/motion/` | rendu MP4 |
| 9 | Contrôle qualité | `studio/skills/meta/reviewer.md`, `monteur-chaine` règle n°5 | planche + rapport |
| 10 | Packaging : miniature, titre, description, chapitres | agents `thumbnail-designer`, `seo-optimizer` | `_workspace/03_*`, `04_*` ★ |
| 11 | Relecteur final | agent `production-reviewer` | `_workspace/05_review_report.md` |

- Rôles 1-4 et 10-11 : sous-agents (Omar a demandé une équipe). Leur passer le slug, le dossier et les livrables précédents.
- Rôles 5-9 : OpenMontage dans `studio/` (licence AGPL). Lire `studio/AGENT_GUIDE.md`, `studio/pipeline_defs/hybrid.yaml`
  et le *director* de chaque étape avant de la travailler.
- Exécution des outils OpenMontage : sur GitHub Actions (workflow **Studio**), choix d'Omar du 29/10/2026. Écrire les appels
  dans `videos/<slug>/appels/<etape>.json` ; résultats dans `videos/<slug>/resultats/`, médias dans la Release
  `studio-<slug>-<etape>-N`.
- En cas de conflit : 1) règles d'Omar (`monteur-chaine`), 2) ce fichier, 3) OpenMontage, 4) Harness.
  Voix = `pocket_tts` ; tout gratuit (budget 0 $) ; ce qu'on voit = ce qu'on dit.

## Thème et ton de la chaîne
- Thème : **À DÉFINIR avec Omar** (remplacer cette ligne dès qu'il est choisi).
- Ton : direct, curieux, tutoiement, phrases courtes faites pour l'oral.
- Format : 16:9, 1920×1080, 30 i/s. Durée cible : 8–12 min (à ajuster selon le thème).

## Comment une vidéo est fabriquée
1. `episodes/<slug>/montage.json` : **la seule source que tu écris**. Le reste est généré.
2. `scripts/produire.sh <slug> [--brouillon]` enchaîne :
   rushes (`scripts/medias.mjs`, Pixabay) → voix (`scripts/voix.py`, Pocket TTS + traitement radio) → timeline (`scripts/construire.mjs`)
   → rendu Remotion (`src/`) → planche de contrôle `out/<slug>*-planche.jpg`.
3. Sur GitHub, chaque push qui touche `episodes/**` lance `.github/workflows/rendu.yml` qui publie le MP4,
   la planche et les crédits dans l'onglet **Releases**. Commit avec `[brouillon]` = rendu 540p rapide.
4. Le PC d'Omar n'est jamais nécessaire : tout tourne sur GitHub Actions.

### Dans une session cloud Claude (sans accès Pixabay ni au modèle de voix)
Tester le montage avec de faux rushes et une voix muette :
```bash
npm ci
VOIX_MOTEUR=silence REMOTION_CONCURRENCY=2 \
REMOTION_BROWSER=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell \
bash scripts/produire.sh <slug> --brouillon
```
(adapter le chemin du navigateur : `find /opt -name chrome-headless-shell -type f`). Puis **regarder la planche**
avec Read avant de dire que c'est bon. Le vrai rendu (vrais rushes + vraie voix) se fait en poussant sur GitHub.

## Motion design : vraies images + animation, toujours ensemble
Lire `.claude/skills/remotion-motion-graphics/SKILL.md` avant d'écrire une scène. Briques prêtes dans `src/motion/` :
`Rush` (vidéo + Ken Burns + étalonnage), `CarteVideo`, `Annotation` (point + trait + étiquette sur la vidéo), `Visee` (HUD),
`Vitre` (panneau vitré pour schémas/chiffres posés sur la vidéo), `Flash`, `MotsQuiMontent`, `Etiquette`, `Compteur`,
couches `FondVivant`/`Etalonnage`/`Grain`/`Vignette`. Exemple complet : `src/tests/Canette.tsx`.
Jamais une vidéo nue avec des sous-titres, jamais du dessin seul : chaque plan mélange un rush réel ET une couche animée
(fenêtre en forme d'objet, annotation, schéma vitré, chiffres). Bruitages dans `public/sfx/` (`node scripts/sfx.mjs`).

## Format de `montage.json`
```jsonc
{
  "titre": "Titre de travail",
  "format": {"largeur": 1920, "hauteur": 1080, "fps": 30},
  "transition_defaut": "fondu",           // fondu | glissement | balayage | coupe
  "duree_transition": 12,                 // frames
  "voix": {"modele": "french_24l", "locuteur": "estelle", "temperature": 0.3, "pause_phrase": 0.22},  // Pocket TTS (Kyutai) ; température plus haute = plus expressif
  "musique": {"fichier": "../../assets/musique/xxx.mp3", "volume": 0.12},
  "etalonnage": {"contraste": 1.08, "saturation": 1.1, "luminosite": 1},
  "grain": true,
  "sous_titres": {"actifs": true, "mots_par_ligne": 4},
  "scenes": [
    {"id": "s01", "type": "video", "recherche": "city night aerial", "texte": "Narration…",
     "surtitre": "Paris, 1889", "zoom": "avant", "vitesse": 0.9, "debut_media": 2, "transition": "coupe"},
    {"id": "s02", "type": "titre", "titre": "Chapitre 1", "sous_titre": "…", "recherche": "fond flou", "duree_min": 3},
    {"id": "s03", "type": "image", "fichier": "medias/photo.jpg", "texte": "…"},
    {"id": "s04", "type": "video", "fichier": "medias/plan-omar.mp4", "texte": "…"}
  ]
}
```
- `recherche` : mots-clés **en anglais**, concrets et visuels (« baker kneading dough close up », pas « travail »).
- `fichier` : média fourni par Omar, chemin relatif au dossier de l'épisode. Toujours prioritaire sur Pixabay.
- Voix d'Omar : `episodes/<slug>/voix/<id>.wav|mp3|m4a` remplace la voix IA pour cette scène.
  Le clonage de voix Pocket TTS demande un compte Hugging Face (conditions acceptées + jeton) : pas activé pour l'instant.
- Son de la voix : chaîne d'égalisation mesurée dans `scripts/voix.py` (EGALISATION_IA). Si on change de voix,
  remesurer avec `python3 scripts/analyse_voix.py avant.wav apres.wav --png spectre.png` et réajuster :
  cibles = clarté 2–5 kHz ≈ -20 dB / sifflantes 5–9 kHz sous la clarté / -16 LUFS / crête ≤ -1,5 dBTP.
- La durée d'une scène = durée de sa voix + respiration (`respiration`, 0.4 s par défaut), au minimum `duree_min`.

## Règles d'écriture (la voix est lue par une IA)
- **Hook dans les 5 premières secondes** : une promesse, une question ou une image forte. Jamais « Bonjour à tous ».
- Une idée par phrase. Phrases de 6 à 18 mots. Ponctuation soignée = intonation naturelle.
- Écrire les nombres, sigles et dates **comme ils se prononcent** (« mille huit cent quatre-vingt-neuf »,
  « la S N C F ») pour éviter les erreurs de lecture.
- Relances régulières (« Mais il y a un problème… »), boucle ouverte avant chaque chapitre, appel à l'abonnement
  court et une seule fois, pas au début.
- Faits vérifiés avec sources (les noter dans `episodes/<slug>/sources.md`). Ne jamais inventer un chiffre.

## Règles de montage
- Un changement de plan toutes les **3 à 6 secondes** : découper une longue narration en plusieurs scènes.
- Alterner plans larges / serrés, mouvements `avant` / `arriere`, ne jamais réutiliser le même rush.
- Cartes `titre` pour ouvrir les chapitres (2,5–3,5 s). `surtitre` pour dates, lieux, chiffres clés.
- Transitions : surtout `coupe` et `fondu` ; `glissement` / `balayage` avec parcimonie (changement de partie).
- Musique : Bibliothèque audio YouTube uniquement (droits OK), volume 0,08–0,15 sous la voix.
- Après chaque rendu : ouvrir la planche, vérifier lisibilité des sous-titres, cohérence image/texte, rythme.

## YouTube : règles à respecter
- Contenu original : script, angle et montage propres à chaque vidéo (la politique « contenu inauthentique »
  démonétise les vidéos produites en série sans apport humain). Pas de modèle de titre ou de miniature recopié.
- Cocher la mention « contenu modifié ou synthétique » si une image réaliste générée par IA pourrait tromper.
- Crédits Pixabay : `credits.txt` dans la release, à coller en description (facultatif mais recommandé).

## Ne pas committer
`node_modules/`, `public/ep/`, `out/`, `.cache/` (déjà dans `.gitignore`).
