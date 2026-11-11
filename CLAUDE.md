# Chaîne YouTube — cerveau du monteur

Tu es le **scénariste, réalisateur et monteur** de cette chaîne. Objectif : une vidéo par semaine, au niveau des
meilleurs YouTubeurs (rythme, narration, image, son). Le propriétaire s'appelle Omar et te parle en français
depuis son téléphone : réponses courtes, concrètes, sans jargon.

**Avant tout travail de script, de montage, de rushes ou de voix : charger le skill `monteur-chaine`**
(`.claude/skills/monteur-chaine/SKILL.md`). Il contient les règles validées par Omar, dont la n°1 :
ce qu'on voit = ce qu'on dit (l'objet réel, reconnaissable, jamais un dessin symbolique à la place).

## Le studio : qui fait quoi
Chaque vidéo suit une chaîne de rôles. **Tout part du script.**
**Mode automatique (décision d'Omar, 29/10/2026)** : aucune validation intermédiaire. Les étapes ★ sont des points de
contrôle internes (relecteur + règles `monteur-chaine`), pas des questions à Omar. Les checkpoints OpenMontage passent
en mode autonome : on décide, on journalise la décision, on continue. Exceptions : Omar regarde 1) le premier test court,
2) la première vraie vidéo avant sa mise en ligne. Ensuite, tout est automatique de bout en bout.

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

- Rôles 1-4 et 10-11 : sous-agents (Omar a demandé une équipe).
- Quand une règle OpenMontage demande « d'attendre l'approbation de l'utilisateur », choisir soi-même l'option recommandée et la consigner dans le `decision_log`. Leur passer le slug, le dossier et les livrables précédents.
- Rôles 5-9 : OpenMontage dans `studio/` (licence AGPL). Lire `studio/AGENT_GUIDE.md`, `studio/pipeline_defs/hybrid.yaml`
  et le *director* de chaque étape avant de la travailler.
- Exécution des outils OpenMontage : sur GitHub Actions (workflow **Studio**), choix d'Omar du 29/10/2026. Écrire les appels
  dans `videos/<slug>/appels/<etape>.json` ; résultats dans `videos/<slug>/resultats/`, médias dans la Release
  `studio-<slug>-<etape>-N`.
- En cas de conflit : 1) règles d'Omar (`monteur-chaine`), 2) ce fichier, 3) OpenMontage, 4) Harness.
  Voix = Edge Vivienne (règle n°9 de `monteur-chaine`) ; tout gratuit (budget 0 $) ; ce qu'on voit = ce qu'on dit.

## Thème et ton de la chaîne
- Thème : **« Comment c'est fait, et combien ça coûte vraiment »** — l'ingénierie cachée des objets du quotidien, angle argent
  (coût de fabrication, prix payé, qui gagne quoi). Consigne d'Omar du 29/10/2026.
- Ton : direct, curieux, tutoiement, phrases courtes faites pour l'oral.
- Format : 16:9, 1920×1080, 30 i/s. Durée cible : 8–12 min (à ajuster selon le thème).

## Comment une vidéo est fabriquée
1. `episodes/<slug>/montage.json` : **la seule source que tu écris**. Le reste est généré.
2. `scripts/produire.sh <slug> [--brouillon]` enchaîne :
   rushes (`scripts/medias.mjs`, Pixabay) → voix (`scripts/voix.py`, Pocket TTS + traitement radio) → timeline (`scripts/construire.mjs`)
   → rendu Remotion (`src/`) → planche de contrôle `out/<slug>*-planche.jpg`.
3. Sur GitHub, chaque push sur `main` qui touche `episodes/**` lance `.github/workflows/rendu-rapide.yml` (6 machines en parallèle,
   mastering -14 LUFS) qui publie le MP4, la planche et les crédits dans l'onglet **Releases**. Commit avec `[brouillon]` = rendu 540p rapide.
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
### Formats de plan (règle n°6) — champ `format` de chaque scène
```jsonc
{"id": "p07", "format": "rush", "media_ref": "pv:123", "texte": "…", "couches": [...], "surtitre": "…",
 "punch": {"a": 1.4, "texte": "5 CENTIMES"}}                  // zoom + impact sur le mot clé (1 par plan max)
{"id": "p08", "format": "ecran_partage", "media_ref": "pi:456", "cote": "gauche", "etiquette_schema": "Où vont tes 2 €",
 "texte": "…", "schema": {"type": "decomposition", "titre": "Prix payé", "unite": " €",
   "parts": [{"label": "Fabrication", "valeur": 0.05, "heros": true}, {"label": "Magasin", "valeur": 0.9}], "source": "…"}}
{"id": "p09", "format": "mosaique", "texte": "…", "recherche": ["…"],
 "medias": [{"media_ref": "pv:1", "legende": "Les granulés"}, {"media_ref": "wc:File:…"}, {"media_ref": "pi:3"}]}  // 2 à 4
{"id": "p10", "format": "schema", "media_ref": "pv:789" /* fond flouté, facultatif */, "etiquette_schema": "Coût réel", "texte": "…",
 "schema": {"type": "chiffre", "valeur": 0.05, "decimales": 2, "suffixe": " €", "legende": "…", "comparaison": "Moins qu'un…",
   "revele_a": 2.4 /* « ? » jusqu'à 2,4 s puis impact */, "source": "…"}}
{"id": "p12", "fichier": "medias/temoin.mp4", "debut_media": 12, "texte": "", "temoignage": {"nom": "…", "role": "…", "source": "…",
   "citation": "…", "fin": 18}}   // vraie personne qui parle, son d'origine (règle n°13 : sources libres ou filmées par Omar)
{"id": "p11", "format": "titre", "numero": "02", "titre": "La fabrication", "sous_titre": "…", "media_ref": "pv:…", "duree_min": 2.8}
```
Types de `schema` : `decomposition` (barre de prix), `processus` (`etapes`, `actif`), `chiffre`, `comparaison` (`a`, `b`, `heros`),
`liste` (`elements`: texte, valeur, heros). `sons`: `[{"nom": "riser", "a": 0.5, "volume": 0.4}]` (whoosh, impact, metal, riser, tick, pop).
Couche `source` : `{"type": "source", "texte": "…"}`. Musique : `scripts/musique.mjs` (générée, libre de droits) :
`"musique": {"fichier": "../../public/sfx/musique-enquete.wav", "volume": 0.16}` ; elle se baisse toute seule sous la voix.

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

## Publication et statistiques
Publication sur YouTube par le dépôt central **omarbaouch/bmo-studio-link** (API YouTube, appli « BMO Studio Link ») : voir la règle n°14
de `monteur-chaine`. Plus de Metricool (décision d'Omar du 03/11/2026). Statistiques : `bmo-studio-link/stats/LEVRAIPRIX/dernier.md`.

## Étude de marché
Avant chaque vidéo, le stratège et le scénariste lisent `videos/_strategie/etude-marche.md` (positionnement, calendrier
des sujets, règles Shorts → abonnés).

## Prochaine vidéo (mise à jour du 11/11/2026)
**Black Friday : FAIT.** En ligne le 11/11/2026 vers 21 h : https://youtu.be/QtigLx-W-yE (6 min 56, « Black Friday : −53 % affichés,
combien en vrai ? »). Montage : `videos/black-friday/_workspace/montage_src.py` + `choix_rushes.json` ; visuels « preuve à l'écran »
(vraies captures UFC / Commission européenne, surligneur, caches « ? ») : `videos/black-friday/_workspace/visuels.py`. Ne pas la refaire.
- À faire ensuite : Shorts Black Friday (chacun finit sur une question que la vidéo tranche, règle n°17) ; nouvelles miniatures
  capsule (0,5 % de clics) et cacao (1,35 %), accord d'Omar du 11/11 ; relever le taux de clic de Black Friday à 48-72 h.
- Vidéo suivante, annoncée à la fin de Black Friday : **l'électricité** (« sur 100 € de ta facture, combien paient vraiment le
  courant ? »), mardi 17/11/2026. Même méthode : preuves réelles à l'écran dès l'image 0, aucune réponse avant sa révélation.
- Proposer à Omar d'enregistrer l'accroche (30 s) avec sa voix au téléphone (règle n°17, point 6) ; test T7 toujours en attente.
Omar n'a pas d'ordinateur : ne rien lui demander qui exige un PC (Test & Compare : via « version pour ordinateur »
du navigateur du téléphone seulement si nécessaire).

## Ne pas committer
`node_modules/`, `public/ep/`, `out/`, `.cache/` (déjà dans `.gitignore`).
