# chaine-youtube

Montage vidéo automatisé : Claude écrit et monte, GitHub Actions fabrique la vidéo, tout est gratuit.

**Pour sortir une vidéo**
1. Claude crée ou modifie `episodes/<nom>/montage.json` (script, plans, titres).
2. Le push lance le robot **Rendu vidéo** (onglet *Actions*) : rushes Pixabay, voix naturelle, sous-titres, rendu.
3. La vidéo arrive dans l'onglet **Releases** (MP4 + planche de contrôle + crédits).

**Ta voix** : dépose `assets/voix/reference.wav` (10–20 s, au calme) pour que la voix IA soit clonée sur la tienne,
ou `episodes/<nom>/voix/<scène>.m4a` pour utiliser directement ton enregistrement.

**Musique** : télécharge des titres de la Bibliothèque audio YouTube dans `assets/musique/`.

Secret requis : `PIXABAY_API_KEY` (Settings → Secrets and variables → Actions).
Détails techniques et règles de montage : `CLAUDE.md`.
