# Brief stratège : test « canette » (20 s)

**Slug :** `test-canette-20s` · **Format :** 16:9, 1920×1080, 30 i/s · **Durée :** environ 20 s (environ 50 mots de voix off)
**Rôle de cette vidéo :** tester toute la chaîne du studio (script, repérage Pixabay, voix Pocket TTS, motion, rendu).
C'est aussi la bande-annonce d'une future vidéo complète sur la canette.

---

## 1. Angle et promesse

- **Angle :** la canette est un chef-d'œuvre industriel, fabriqué à la chaîne à une vitesse folle. Pourtant, vide, elle ne vaut presque rien. L'écart entre ce qu'elle coûte et ce que tu paies est le vrai sujet.
- **Promesse au spectateur :** « En 20 secondes, tu vois naître une canette et tu apprends combien elle coûte vraiment. Ensuite, tu as envie de savoir où va le reste de ton argent. »
- **Type :** teaser / « fait choc » (accroche → fabrication accélérée → révélation → boucle ouverte).
- **Public visé :** les 18–40 ans curieux, qui regardent des contenus « comment c'est fait » et qui aiment les chiffres qui surprennent.
- **Émotion visée :** fascination (la machine), puis surprise (le prix), puis frustration positive (« alors où va mon argent ? »).

---

## 2. Trois accroches (moins de 3 s)

| # | Accroche (voix) | Ce qu'on voit | Verdict |
|---|---|---|---|
| A | « Devine combien coûte cette canette. Vide. » | Gros plan sur des canettes qui défilent sur une ligne d'usine | **Choisie** |
| B | « Cette usine crache des canettes plus vite que tu ne peux les compter. » | Plan large d'une ligne de canettes en pleine vitesse | Bonne image, mais pas d'argent dedans, donc hors du thème de la chaîne |
| C | « Le moins cher dans ta canette, c'est… la canette. » | Canette tenue en main | Rejetée : il faudrait prouver que la boisson coûte plus cher, et on n'a pas de source solide |

**Pourquoi A :**
1. C'est une question directe, en tutoiement : le spectateur fait une estimation dans sa tête, donc il reste pour vérifier.
2. Le thème de la chaîne (« combien ça coûte vraiment ») est là dès le premier mot.
3. Elle passe le test du son coupé : « cette canette » est montrée à l'écran pendant qu'on la nomme (règle n°1).
4. Elle fait 6 mots, soit environ 2 s de voix. La réponse arrive vers 10 s, ce qui tient l'attention jusqu'au milieu.
5. Le « Vide. » isolé crée une petite chute à l'oral : la voix IA marque une pause naturelle sur le point.

---

## 3. Structure (4 temps, environ 20 s)

> La voix est écrite comme elle se prononce (Pocket TTS). Un changement de plan toutes les 2 à 4 s, c'est voulu pour un teaser.

| Temps | Durée | Voix off | À l'écran (rush réel + couche animée) |
|---|---|---|---|
| **1. Accroche** | 0–3 s | « Devine combien coûte cette canette. Vide. » | Rush : canettes vides alignées qui défilent sur un convoyeur, en gros plan. Couche : `Visee` qui se verrouille sur UNE canette, puis `Etiquette` « ? € ». |
| **2. Fabrication accélérée** | 3–10 s | « Une bande d'aluminium entre d'un côté. De l'autre, des canettes sortent à la chaîne, sans jamais s'arrêter. » | Plan 2a (environ 3 s) : vraie bobine ou bande d'aluminium qui se déroule, avec `Annotation` « bande d'aluminium ≈ 0,3 mm ». Plan 2b (environ 4 s) : ligne de canettes à pleine vitesse, accélérée (vitesse 1,5–2), `Flash` et bruitage sur une coupe. |
| **3. Révélation** | 10–15 s | « La fabriquer coûte moins de quatre centimes. De dollar. » | Rush : une canette qui sort de la ligne, plan serré. Couche : `Vitre` + `Compteur` qui descend vers **< 0,04 $**. Surtitre en petit : « Estimation : Economic Policy Institute, via CNN, mars 2025 ». |
| **4. Chute / boucle ouverte** | 15–20 s | « Alors, où passe tout le reste de ce que tu paies ? On suit l'argent, centime par centime. » | Rush : rayon de supermarché rempli de canettes, ou main qui prend une canette au rayon. Couche : `MotsQuiMontent` « Où va le reste ? », puis carton final « Bientôt : la vidéo complète ». |

**Script complet de la voix (environ 50 mots, environ 19 s) :**
> Devine combien coûte cette canette. Vide.
> Une bande d'aluminium entre d'un côté. De l'autre, des canettes sortent à la chaîne, sans jamais s'arrêter.
> La fabriquer coûte moins de quatre centimes. De dollar.
> Alors, où passe tout le reste de ce que tu paies ? On suit l'argent, centime par centime.

**Contrôle de la règle n°1 (ce qu'on voit = ce qu'on dit) :**
- « cette canette » → une canette réelle, nette, au centre. OK.
- « bande d'aluminium » → une vraie bobine ou une vraie tôle d'aluminium. Si le repérage ne trouve **aucune** vraie bobine d'aluminium (et non de l'acier), on remplace la phrase par « Des milliers de canettes sortent de la ligne… » plutôt que de montrer un faux.
- « canettes à la chaîne » → une ligne de canettes **vides en aluminium**. On refuse les bouteilles, le jus d'orange et le verre (déjà vus au repérage).
- « ce que tu paies » → un rayon de magasin ou un achat, où la canette est reconnaissable.
- On ne dit pas « presse » à voix haute : on n'est pas sûrs de trouver gratuitement une vraie presse à canettes. Si le repérage en trouve une (`can bodymaker`), on peut l'ajouter en plan muet dans le temps 2.

---

## 4. Ton

- Direct, complice, en tutoiement. Le spectateur est mis au défi (« Devine »).
- Rythme rapide sur les temps 1 et 2. Léger ralentissement et pause avant « De dollar. ». Ton de confidence sur la chute.
- Voix Pocket TTS `estelle`, température 0,3. On garde les points isolés (« Vide. », « De dollar. ») pour obtenir les pauses.
- Musique : nappe pulsée et industrielle, discrète (volume 0,10). Bruitages : chocs métalliques calés sur les coupes du temps 2, « tic » de compteur au temps 3.

---

## 5. Images réelles nécessaires (Pixabay / Pexels, mots-clés en anglais)

| Plan | Ce qu'on DOIT voir | Requêtes (3–4) | À refuser |
|---|---|---|---|
| 1 | Canettes vides en aluminium qui défilent sur un convoyeur, en gros plan | `aluminum cans conveyor`, `empty cans production line`, `beverage can factory`, `cans moving conveyor close up` | Bouteilles, jus, verre, canettes déjà remplies et bouchées si on ne les distingue pas |
| 2a | Bobine ou bande d'aluminium (métal clair, brillant) | `aluminum coil`, `aluminium sheet roll factory`, `metal coil unwinding`, `aluminum rolling mill` | Bobines d'acier rouillées ou sombres, câbles, cheminées |
| 2b | Ligne de canettes à pleine vitesse (plan large ou en enfilade) | `can manufacturing line`, `canning line high speed`, `beverage cans factory automation`, `cans production plant` | Machines à café, embouteillage de plastique |
| 3 | Une canette seule, nette, en plan serré (en usine ou sur fond neutre) | `aluminum can close up`, `single soda can rotating`, `empty aluminum can macro`, `can factory close up` | Canettes écrasées, marques trop visibles |
| 4 | Rayon de magasin avec canettes, ou main qui prend une canette | `soda cans supermarket shelf`, `hand taking can from shelf`, `drinks aisle cans`, `buying soda can` | Plans où l'on ne reconnaît pas de canettes |
| bonus (muet) | Vraie presse ou bodymaker de canettes | `can bodymaker machine`, `metal press stamping cans`, `can making machine` | Toute presse qui ne fabrique pas de canettes |

Chaque rush ne sert qu'une fois. Le choix se fait **en regardant les planches** du workflow Repérage (règle n°2), jamais au hasard.

---

## 6. Chiffres et sources

### Le chiffre de la vidéo (la seule révélation)
- **Fabriquer une canette (vide) coûte « un peu moins de 4 centimes » de dollar.** C'est l'estimation d'Adam S. Hersh, économiste senior à l'Economic Policy Institute, citée par CNN (Maria Sole Campinoti, 2 mars 2025). Il ajoutait qu'une taxe de 25 % sur l'aluminium ferait monter ce coût à environ 5 centimes.
  - Source (republication CNN Newsource) : https://abc17news.com/money/cnn-business-consumer/2025/03/02/why-trumps-aluminum-tariffs-wont-raise-the-price-of-your-can-of-coke/
  - Autre reprise du même article : https://itiger.com/news/2516022548
  - **Prudence :** c'est une estimation américaine, en dollars, datée de début 2025, donc avant le passage des taxes à 50 % (voir Fortune ci-dessous). C'est pour cela que la voix dit « de dollar » et que la source s'affiche à l'écran. On ne convertit pas en euros, faute de source française équivalente.

### Chiffres de réserve, vérifiés (pour la vidéo complète, pas pour ce test)
- Une ligne fabrique les corps de canettes à **1 500 à 2 700 par minute** par machine (bodymaker). On compte **2 500 à 3 750 gobelets par minute** au découpage-emboutissage. Une bobine d'aluminium pèse environ **25 000 livres** (environ 11 t). Source : https://p2infohouse.org/ref/45/44123/text/manuf.htm
- Tôle d'aluminium laminée à **0,25–0,30 mm** avant mise en forme. Source : https://www.alcircle.com/blog/a-step-by-step-guide-to-aluminium-can-manufacturing-process
- Une canette de 33 cl pèse environ **18 g**. Fabriquer la canette demande environ **10 fois plus d'énergie** que fabriquer la boisson qu'elle contient. Le recyclage économise environ 95 % de l'énergie. Source : https://www.energie-environnement.ch/fichiers/visites-dechets/fiches-enseignant/02_canette_alu.pdf
- Environ **180 milliards** de canettes en aluminium produites par an dans le monde. Source : https://en.wikipedia.org/wiki/Aluminum_can
- Aux États-Unis, une canette recyclée redevient une canette neuve en **moins de 60 jours en moyenne**. Étude RRS commandée par l'Aluminum Association et le Can Manufacturers Institute, mars 2025. Source : https://www.recyclingproductnews.com/article/43040/study-reveals-used-beverage-cans-are-recycled-into-new-cans-in-less-than-60-days
- Hausse des taxes américaines sur l'aluminium à 50 % (2025). AriZona menace son prix historique à 99 cents. Source : https://www.fortune.com/2025/08/11/arizona-iced-tea-price-increase-trump-tariffs-aluminum

À recopier dans `episodes/test-canette-20s/sources.md` au moment du montage.

---

## 7. Trois idées de titre

1. **Combien coûte VRAIMENT une canette vide ?** (question directe, mot-clé « canette » en tête ; c'est mon préféré)
2. **Moins de 4 centimes : le vrai prix d'une canette** (le chiffre dans le titre, effet de surprise immédiat)
3. **Ta canette ne coûte presque rien. Alors où va ton argent ?** (boucle ouverte, plus adapté à la vidéo complète)

---

## Notes pour les rôles suivants

- **Scénariste :** garder environ 50 mots, au maximum 55. Ne rien ajouter qui ne puisse pas se montrer. « Quatre centimes » est écrit en toutes lettres pour la voix.
- **Fact-checker :** vérifier en priorité la citation de Hersh (moins de 4 cents, CNN, 02/03/2025) et la mention « de dollar ».
- **Repérage :** le plan 2a (bobine d'aluminium) est le plus risqué. Prévoir le texte de secours décrit en section 3.
- **Miniature (si publiée) :** une canette seule sur fond sombre, avec en gros « 0,04 $ ? ».
- **SEO :** mot-clé principal « prix canette aluminium ». Mots-clés secondaires : « fabrication canette », « comment est fabriquée une canette », « coût de fabrication canette ».
