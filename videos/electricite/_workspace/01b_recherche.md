# Recherche : les offres d'électricité (slug `electricite`)

Vérification à la source le **17/11/2026** (run automatique, documentaliste). Chaque point du brief `01_strategist_brief.md` est classé :
**VERT** = confirmé à la source · **ORANGE** = approximatif, formulation sûre proposée · **ROUGE** = faux ou non trouvé, remplacement proposé.

**Limites de ce run** (à noter pour le fact-checker) :
- Le téléchargement direct (curl) vers cre.fr et energie-info.fr est bloqué par le proxy de la session : les PDF de la CRE ont été lus par l'outil de lecture web (texte extrait), pas ouverts en image. Les tableaux ont donc été recoupés par le calcul (HT → TTC) quand c'était possible.
- Deux pages n'ont pas pu être ouvertes (autorisation non donnée à temps) : la page CRE « VNU : estimation des revenus nucléaires d'EDF » (https://www.cre.fr/electricite/marche-de-detail-de-lelectricite/vnu-estimation-des-revenus-nucleaires-dedf.html) et le comparateur lui-même (https://comparateur.energie-info.fr/). Le nombre d'offres sous le tarif bleu **sur le comparateur officiel** n'a donc pas pu être relevé (point n°4 du brief) : à faire à la main au moment de la capture.
- Les pages energie-info.fr affichent en pied de page « Édition Particulier du [jour de consultation] » : ce n'est **pas** la date de publication. On écrit « page consultée le 17/11/2026 ».
- Légifrance n'a pas été ouvert ; le texte de la loi 2025-594 a été lu sur une reproduction du Journal officiel (associatheque.fr) et recoupé par le cabinet CMS et le texte de la loi 2020-901 (site de l'Arcep).

---

## 1. Le tarif bleu en vigueur (novembre 2026)

| Point du brief | Verdict | Ce que dit la source |
|---|---|---|
| Base : 0,2001 €/kWh TTC depuis le 01/08/2026 | **VERT** | CRE, délibération n° 2026-147 du 15/07/2026, annexe B : Base résidentiel **13,61 c€/kWh HT**. Calcul : (13,61 + accise 3,062) × 1,2 = **20,01 c€ TTC**. Selectra (17/07/2026) et Kelwatt (relevé 16/11/2026) affichent 0,2001 €. |
| Abonnement Base 6 kVA | **VERT** (chiffre ajouté) | **190,35 € TTC par an, soit 15,86 € par mois** (Selectra 17/07/2026 ; Kelwatt affiche 190,32 €). Recoupé : prime fixe 6 kVA **143,28 € HT/an** (annexe B) + CTA 15,35 € = 158,63 € × 1,2 = **190,35 €**. |
| Hausse de 2,5 % TTC au 01/08/2026, suivie par le gouvernement le 16/07 | **VERT** | Délibération 2026-147 : « + 3,12 % HT soit + 5,08 €/MWh HT ou + 2,51 % TTC soit + 5,98 €/MWh TTC, pour les tarifs bleus résidentiels ». AFP (Connaissance des énergies, 16/07/2026) : « tarifs réglementés d'électricité relevés de 2,5 % en moyenne au 1er août ». |
| Facture moyenne 1 046 € → 1 072 €/an | **VERT** | AFP, 16/07/2026 : « une facture moyenne passant de 1 046 à 1 072 euros TTC par an » ; « environ 26 euros TTC par an en moyenne ». |
| Heures pleines / heures creuses 6 kVA | **VERT** | Annexe B : HP 14,79 c€ HT, HC 10,18 c€ HT → **HP 0,2142 €, HC 0,1589 € TTC** (calcul identique à Selectra). Abonnement HP/HC = Base (190,35 €/an). |

À dire : « vingt centimes le kilowattheure, et seize euros par mois d'abonnement en six kilovoltampères » (arrondi sûr de 15,86 €).

## 2. Où vont tes 100 € : recalcul sur le tarif bleu du 01/08/2026

**Verdict sur le brief (39 € / 28 € / 33 €) : ORANGE.** Ces chiffres sont exacts mais datés : Connaissance des énergies (page mise à jour le 26/03/2026) les attribue à la CRE, situation « à fin 2025 » (observatoire T4 2025) : « la part fourniture de l'électricité comptait pour environ 39 % », « les coûts de réseaux comptaient pour environ 28 % », « les taxes et contributions comptaient pour environ 33 % ». Sur le tarif du 01/08/2026, le recalcul donne **environ 41 / 28 / 31**.

### Le calcul (foyer type : option Base, 6 kVA, 4 500 kWh par an, le profil utilisé par Selectra et proche de la facture moyenne de l'AFP)
Sources des briques :
- Prix HT du tarif bleu : délibération CRE 2026-147, annexe B (13,61 c€/kWh ; 143,28 €/an).
- Réseau (TURPE 7 HTA-BT au 01/08/2026) : délibération CRE n° 2026-105 du 21/05/2026. Gestion 17,12 €/an + comptage 22,67 €/an + 6 kVA × 10,42 €/kVA/an (version CU 4 plages) = **102,31 €/an**. Part variable de la version CU 4 plages : 7,72 / 4,09 / 1,71 / 1,20 c€/kWh selon la saison et l'heure ; moyenne pondérée **estimée à 4,5 c€/kWh** pour un profil résidentiel (≈ 58 % de la conso en hiver, ≈ 70 % en heures pleines). La version CU 4 plages est confirmée par la CTA : 15 % × 102,31 € = 15,35 €, exactement ce qu'il faut pour retomber sur 190,35 € TTC.
- Accise : 30,62 €/MWh (30,85 €/MWh au 01/02/2026 selon la délibération CRE n° 2026-06, puis « − 0,23 €/MWh » au 01/08/2026 selon la délibération 2026-147 ; Selectra utilise aussi 30,62).
- CTA : « 15 % de la part fixe du TURPE à partir du 1er février 2026 (21,93 % précédemment) » (délibération 2026-06).
- TVA : 20 % sur tout (abonnement compris depuis le 01/08/2025).

| Ligne | € par an | Sur 100 € |
|---|---|---|
| Réseau (TURPE) : 102,31 + 4 500 × 0,045 | 304,81 | **27,9 €** |
| Fourniture (le reste du prix HT) : 40,97 + 4 500 × 0,0911 | 450,92 | **41,3 €** |
| Accise sur l'électricité : 4 500 × 0,03062 | 137,79 | 12,6 € |
| CTA | 15,35 | 1,4 € |
| TVA 20 % | 181,77 | 16,7 € |
| **Total TTC** | **1 090,64** (contrôle : 190,35 + 4 500 × 0,2001 = 1 090,80) | 100 € |
| dont taxes (accise + CTA + TVA) | 334,91 | **30,7 €** |

Sensibilité : si la part variable du réseau vaut 4,0 ou 5,0 c€/kWh au lieu de 4,5, la fourniture fait 43 € ou 39 €, le réseau 26 € ou 30 €. **Les taxes (31 €) ne dépendent pas de cette hypothèse.** À 3 000 kWh/an : fourniture 39,8 €, réseau 30,0 €, taxes 30,3 €.

**Formulation sûre pour la voix** : « Sur cent euros, à peu près quarante paient la fourniture. Une trentaine paient le réseau. Et une trentaine, ce sont des taxes. » Réponse de la devinette n°1 : **environ 40 €** (case « 40 € » = juste). À l'écran : « ≈ 41 € / ≈ 28 € / ≈ 31 € — calcul Le Vrai Prix, tarif bleu Base 6 kVA, 4 500 kWh/an, d'après la CRE ». Variante encore plus sûre : citer la CRE fin 2025 (39 / 28 / 33) avec la date.

« La seule part qui change d'un fournisseur à l'autre » : **VERT**. energie-info.fr, fiche « Prix de l'électricité et du gaz : que payons-nous ? » (consultée le 17/11/2026) : « Il s'agit de la seule composante soumise à la concurrence. » (à propos de la fourniture).

### Et « le courant » au sens strict ? **ORANGE (estimation)**
La CRE ne publie pas le niveau absolu de la brique « énergie » du tarif bleu résidentiel. Ce qu'on sait à la source (délibération 2026-06 du 14/01/2026) : commercialisation **18,11 €/MWh HT, dont 9,80 €/MWh de certificats d'économies d'énergie (CEE)** ; rémunération du fournisseur = 2,5 % du tarif HT ; au 01/08/2026, « + 3,45 €/MWh HT » pour la nouvelle capacité et « − 0,64 €/MWh HT » pour la brique CEE et coûts commerciaux.
- Commercialisation + CEE ≈ 17,5 €/MWh × 4,5 MWh ≈ 79 € HT par an ≈ **7 € sur 100 €** (chiffre solide, sourcé CRE).
- En retirant aussi la rémunération (≈ 2 €) et la capacité (≈ 2 €, estimation), il reste **environ 30 € sur 100 € pour l'électricité elle-même**. C'est une estimation à ± 3 €, pas un chiffre publié.
- **Formulation sûre** : « Et sur ces quarante euros, tout n'est pas du courant : environ sept euros paient la commercialisation et les certificats d'économies d'énergie. Le courant lui-même, c'est une trentaine d'euros. » À l'écran : « ≈ 30 € (estimation d'après la CRE) ». Ne pas mettre « 30 € » sur la miniature.

## 3. Prix de gros, fin de l'ARENH, VNU, février 2027

| Point du brief | Verdict | Source et formulation |
|---|---|---|
| Prix de gros ≈ 266 €/MWh du 1er au 10/11, ≈ 4 fois novembre 2025 (65,8 €/MWh) | **ORANGE** | C'est un **relevé Selectra** des prix spot (« Du 1er au 10 novembre », 266,31 €/MWh ; « contre 65,8 en novembre 2025 »), Selectra 11/11/2026. Pas de source primaire EPEX/RTE lue. Recoupements : marché spot France (EPEX) **188,36 €/MWh** en moyenne la semaine du 12 au 18/10 contre 139,60 la semaine d'avant (TotalEnergies, Point marché hebdo du 20/10/2026, « la flambée des prix du gaz, alimentée par les tensions géopolitiques ») ; 259 €/MWh le 07/11 (EconomieMatin d'après Selectra). **Dire** : « Début novembre, l'électricité s'échangeait sur le marché environ quatre fois plus cher qu'un an plus tôt. » Source à l'écran : « relevé Selectra des prix spot, 11/11/2026 ». |
| Livrable 2027 : ~50 → 128 €/MWh (30/10) ; 109,61 le 16/10 | **ORANGE** | Selectra 10/11/2026 : « 128 €/MWh » à la clôture du 30/10. TotalEnergies 20/10/2026 : Cal-27 clôturé à **109,81 €/MWh** le 19/10. **Dire** : « Le courant livrable l'an prochain a plus que doublé depuis janvier. » |
| Attention à la phrase de sortie du brief « cette partie-là vient de quadrupler » | **ROUGE** | Faux pour ta facture : la fourniture du tarif bleu n'a **pas** quadruplé (+2,5 % au 01/08). La CRE achète l'énergie du tarif bleu « de manière lissée sur 24 mois » (délibération 2026-06). **Remplacer par** : « Et le prix de cette partie-là, sur les marchés, vient d'être multiplié par quatre. Le tarif bleu, lui, amortit le choc. Pas toutes les offres. » |
| Fin de l'ARENH au 31/12/2025 | **VERT** | Délibération CRE 2026-06 : l'ARENH a pris fin le 31/12/2025, les fournisseurs achètent désormais tous leurs volumes sur les marchés ou à leur propre production. |
| VNU : aucun reversement en 2027 (revenus 65,50 €/MWh < seuil 78 €/MWh) | **ORANGE** | Estimation CRE au **1er octobre 2026**, rapportée par Selectra (01/11/2026) et Hello Watt (15/10/2026) : revenus nucléaires d'EDF « 65,50 €/MWh », mécanisme qui « ne s'enclenche qu'au-delà de 78 €/MWh », remise « à 0 € pour l'instant ». Base légale : article 17 de la loi de finances pour 2025. La CRE met l'estimation à jour chaque mois : la page CRE n'a pas pu être ouverte. **Dire** : « Selon la dernière estimation de la C R E, ce mécanisme ne te rendrait rien en deux mille vingt-sept. » |
| Tarif bleu « gelé » jusqu'au 01/02/2027, proposition CRE mi-janvier, lissage 24 mois | **ORANGE (mot)** | Selectra 14/09/2026 : « Rien ne change avant le 1er février : le tarif réglementé reste celui en vigueur depuis le 1er août » ; « À la mi-janvier, la CRE fera connaître le nouveau tarif qu'elle propose au gouvernement ». Délibération 2026-147 : la CRE « mettra à jour ces composantes au prochain mouvement de février 2027 ». **Éviter « gelé »** (le mot suggère une décision de blocage, il n'y en a pas). **Dire** : « Le tarif bleu ne bouge pas avant le premier février. Après, personne ne sait encore de combien il montera. » |

## 4. Démarchage (à éviter n°5)

**VERT, avec deux nuances.**
- **Loi n° 2025-594 du 30 juin 2025 contre toutes les fraudes aux aides publiques** (JORF du 01/07/2025), article 13 : réécrit l'article L. 223-1 du code de la consommation. Nouveau texte : « Il est interdit de démarcher par téléphone, directement ou par l'intermédiaire d'un tiers agissant pour son compte, » un consommateur qui n'a pas « exprimé préalablement son consentement ». Consentement = « toute manifestation de volonté libre, spécifique, éclairée, univoque et révocable » (CMS). C'est au professionnel de prouver l'accord.
- **Entrée en vigueur** : article 13, III : « Les a à f et le h du 1o du B du II entrent en vigueur le 11 août 2026. » **VERT.**
- **Nullité** : la phrase « Tout contrat conclu avec un consommateur à la suite d'un démarchage téléphonique réalisé en violation des dispositions du présent article est nul » existe dans l'article L. 223-1 **depuis la loi n° 2020-901 du 24 juillet 2020** (article 3). La loi de 2025 change ce qui est interdit (tout appel sans accord), la nullité s'applique donc désormais à ces appels. **Formulation sûre** : « Depuis le onze août, un vendeur n'a plus le droit de t'appeler sans ton accord. Et un contrat signé après un appel interdit est nul. »
- **Amendes** : article L. 242-16, amende administrative jusqu'à **75 000 €** (personne physique) et **375 000 €** (personne morale) (CMS). Dire « jusqu'à trois cent soixante-quinze mille euros pour une entreprise ».
- **Nuance n°1 (à dire)** : exception client. Ton fournisseur actuel peut t'appeler sans accord préalable pour ton contrat en cours (art. L. 223-1, al. 4, d'après CMS). La loi vise les appels des autres.
- **Nuance n°2** : la loi parle du téléphone. Le démarchage **à domicile** n'est pas interdit par ce texte.
- **Faux médiateur** : **VERT**. energie-info.fr, actualité « Démarchage à domicile : certains commerciaux se font passer pour le médiateur national de l'énergie » (consultée le 17/11/2026) : le médiateur « n'effectue aucun démarchage et ne contacte pas les consommateurs pour leur proposer des contrats ». Une autre page vise le téléphone : « Démarchage par téléphone : certains comparateurs se font passer pour le médiateur national de l'énergie ». **Attention** : la page « à domicile » nomme un fournisseur dans son texte → recadrer la capture sur le titre.
- **Chiffre utile ajouté** : baromètre énergie-info 2026 (synthèse) : **36 % des foyers ont signé un contrat d'énergie après un démarchage**, 50 % chez les moins de 35 ans.

## 5. La facture estimée (à éviter n°4) : le couple des Yvelines

Source : Journal du Net, Charles Desthieux, **15/05/2026, 06 h 50**, « "4 000 euros en un mois" : son compteur Linky devient fou, sa facture explose ».

| Point du brief | Verdict | À la source |
|---|---|---|
| Printemps 2024, ≈ 4 000 € pour un mois | **VERT** | Entre mars et mai 2024, le Linky n'envoie plus de relevés ; facturation sur estimation ; 4 000 € réclamés pour mai 2024. |
| Contrat résilié pour impayé, huissier | **VERT** | Résiliation après le non-paiement, accès à l'espace client coupé, puis un commissaire de justice (l'ancien « huissier »). **Dire « un commissaire de justice »** ou « un huissier », les deux sont compris. |
| Association saisie un an plus tard | **VERT** | Mai 2025, le mari contacte l'Adéic. |
| Citation « On ne sait pas » (sur la cause) | **ORANGE (attribution)** | Elle existe, mais c'est le **juriste de l'Adéic**, pas le couple : « Pourquoi le compteur a-t-il cessé de fonctionner ? La question reste sans réponse. "On ne sait pas", admet Matthieu Bertrand Neuser. » À l'écran : « "On ne sait pas." — Matthieu Bertrand Neuser, juriste de l'Adéic (Journal du Net) ». |
| Citation « Ça change tout : ils nous répondent et font attention. » | **ORANGE (attribution et sens)** | Mot pour mot, mais dite par le **juriste** et elle parle de **l'adresse dédiée de l'association chez le fournisseur** : « Nous avons l'avantage d'avoir une adresse dédiée chez [le fournisseur], explique Matthieu Bertrand Neuser. Ça change tout : ils nous répondent et font attention. » Ne pas la mettre dans la bouche du couple. Usage sûr : « Leur association a une adresse directe chez le fournisseur. Son juriste le dit : "Ça change tout : ils nous répondent et font attention." » |
| Dénouement : février 2026, ≈ 3 000 €, ≈ 700 kWh corrigés, geste de 300 €, 30 mensualités ≈ 100 €, nouveau compteur et nouveau fournisseur | **VERT** | Première proposition en novembre 2025, acceptée en février 2026. Le relevé contesté est annulé, ≈ 700 kWh corrigés ; « un 'geste exceptionnel' de 300 euros » ; « on obtient 1 000 euros de remise » (le juriste) ; « la nouvelle facture n'était plus de 4 000 euros, mais de 3 000 euros » ; 30 mensualités d'environ 100 € ; le couple a changé de compteur et de fournisseur. |
| Fournisseur du couple | info | Le JDN le **nomme** (et nomme le gestionnaire de réseau). Règle du brief maintenue : « leur fournisseur » à la voix ; capture recadrée sur titre + date. |
| Photo | info | Image d'illustration de banque d'images (© Adobe Stock) : pas de visage du couple. Utiliser les mains d'Omar et l'enveloppe. |
| Autre citation utile | — | Le juriste : « compteur Linky qui dysfonctionne, ça arrive, mais ça reste exceptionnel. » À placer pour rester juste (ne pas faire peur sur le Linky). |

**Personne de secours (Hérault)** : **VERT**, Selectra 07/11/2025 (mis à jour le 14/01/2026) d'après Midi Libre (date de l'article d'origine non donnée). Une sexagénaire du bassin de Thau, factures « autour de 200 € », prélèvement de « 211.993,09 € » ; cause : « une simple erreur de saisie », 1 556 kWh enregistrés comme 1 001 556 kWh. Citation de la cliente : « J'ai hurlé et même vomi ». Le fournisseur a reconnu par écrit une « erreur de calcul » le 12 octobre (2025). Dire « l'an dernier, dans l'Hérault ».

**Ce que dit le médiateur** (pour l'action concrète) : **VERT**. energie-info.fr, « J'ai une réclamation concernant mon fournisseur ou le gestionnaire de réseau » : réclamation **écrite** d'abord ; « Si le litige n'est toujours pas résolu 2 mois après ma réclamation écrite (et au plus tard 1 an après ma dernière réclamation écrite) », « je peux saisir directement et gratuitement le médiateur national de l'énergie ».

## 6. La remise « −20 % » qui bascule (à éviter n°3)

Source : JeChange, publié le 06/11/2026 à 12 h 55, **mis à jour le 11/11/2026** après un erratum du fournisseur.

| Point du brief | Verdict | À la source |
|---|---|---|
| Fin au 31/12/2026 | **VERT** | Erratum : le prix fixe finit le **31/12/2026** (et non le 31/01/2027) ; nouveau prix au 01/01/2027. Attention : une grille dans l'article est encore datée du 01/02/2027 (premier courrier) → ne pas la montrer. |
| Remise −20 % sur le kWh HT du tarif bleu | **VERT (précision)** | −20 % sur le kWh HT **du tarif réglementé de février 2025**. |
| kWh HT 0,1140 → 0,1747 € (+53 %) | **VERT** | Option Base, HT. |
| Abonnement +47 % | **ORANGE** | 14,38 → 21,12 € par mois, mais c'est l'**option heures pleines / heures creuses**. Dire « l'abonnement, lui, prend près de cinquante pour cent ». |
| Facture ≈ +42 % | **VERT (prudence)** | Facture annuelle TTC +42 % **pour le client dont le courrier circule** ; le pourcentage varie avec la conso (le courrier est personnalisé). Dire « Pour un client, la facture prend quarante-deux pour cent. » |
| « Le silence vaut acceptation » | **VERT** | Écrit dans l'article : sans action, le nouveau prix s'applique. |
| Nouvelle offre | info | Nouvelle offre à prix fixe HT jusqu'au 31/07/2029. Le fournisseur rappelle qu'on peut partir « sans frais ni préavis ». |
| « Remise sur le kWh HT ≠ remise sur la facture » attribué à UFC-Que Choisir | **ROUGE (attribution)** | L'article UFC du 24/09/2026 n'en parle pas. C'est un **calcul** : la remise ne touche ni l'abonnement, ni l'accise, ni la TVA. Exemple Le Vrai Prix (4 500 kWh) : 20 % de 0,1425 € HT = 2,85 c€ × 4 500 = 128 € HT, soit ≈ 154 € TTC sur une facture d'environ 1 100 € → **environ −14 % sur la facture, pas −20 %**. Dire « moins vingt pour cent sur une ligne, ça ne fait pas moins vingt pour cent sur la facture ». |

Recoupement energie-info.fr (« Attention aux messages que vous recevez de votre fournisseur d'énergie », consultée le 17/11/2026) : « certains fournisseurs décident de modifier leur grille tarifaire à la hausse ou de changer l'indexation de votre contrat » ; le fournisseur « doit vous communiquer au minimum un mois à l'avance les modifications envisagées » ; « vous pouvez changer de fournisseur à tout moment et sans frais ». Conseil : vérifier les spams.

## 7. Les niveaux A-B-C-D et les offres indexées / dynamiques (à éviter n°2)

- **Niveaux de certitude : VERT**, mais **deux sources à distinguer** :
  - CRE, fiche « Niveau de certitude » (PDF non daté, https://cre.fr/fileadmin/Documents/Autres/Niveau_de_certitude.pdf) : **A** vert foncé « L'estimation repose sur un prix entièrement fixe garanti, couvrant l'ensemble des coûts pour la durée du contrat » ; **B** vert moyen « Les prix restent globalement stables mais peuvent être ajustés en fonction de changements réglementaires » ; **C** vert clair « L'ensemble du prix évolue suivant une formule préalablement définie, susceptible de varier à la hausse ou à la baisse » ; **D** jaune « Les prix sont entièrement ou partiellement soumis à des facteurs externes ». Ne vaut que pour la 1re année du contrat. « à l'initiative de la CRE et des fournisseurs ».
  - La formule du brief pour D, « évolution aléatoire ou imprévisible », vient des **Lignes directrices de la CRE**, annexe 3 (version du 10/07/2024 mise à jour le 06/11/2025), niveaux numérotés 1 à 4 : niveau 4 « est présumée évoluer de façon aléatoire ou imprévisible ». Mesure 3 : le fournisseur doit « associer systématiquement à cette estimation un niveau de confiance » ; mesures 7 et 12 : même nomenclature en cours de contrat et au renouvellement.
  - Engagement : 13 lignes directrices annoncées le 11/07/2024 ; « 24 fournisseurs nationaux et plus de 50 fournisseurs locaux » engagés, plus de 99 % des clients résidentiels (CRE, communiqué du 08/10/2024).
  - Bilan CRE n° 2026-110 du 11/06/2026 : certains fournisseurs ont omis le niveau de certitude dans leurs courriers de renouvellement. → « Si ton courrier ne donne pas la lettre, demande-la. »
- **Le niveau figure-t-il sur le comparateur officiel ? VERT** : energie-info.fr, « Le comparateur du médiateur national de l'énergie évolue : découvrez ses nouveautés » (consultée le 17/11/2026) : un indicateur de stabilité des prix noté de A à D, « A : très bonne stabilité, peu de risque de hausse » ; le comparateur est « un outil public, gratuit, neutre et indépendant ».
- **UFC-Que Choisir, 24/09/2026 (Alexandre Loukil)** : note D pour les offres dont le prix « varie chaque jour en fonction des cours boursiers ». **VERT.** (Le brief dit « critère n°1 » : le 1er critère de l'article est « Classement des offres selon le prix », le 2e « Durée de blocage des prix » → dire « parmi les cinq critères ».)
- **Offres dynamiques, energie-info.fr** (« Offres à tarification dynamique : informations pratiques et alerte… », consultée le 17/11/2026) : « le prix de l'énergie fluctue tous les jours et toutes les heures » ; « un risque de factures plus élevées pour les consommateurs non avertis » ; prix les plus hauts « en hiver, lors de la pointe de consommation du soir ». **VERT.**
- energie-info.fr (« Offre de fourniture… que faut-il regarder ? ») : « les offres à prix indexé peuvent aboutir à des augmentations importantes en cours de contrat ». **VERT.**
- **kWh dynamique 0,3563 € contre 0,2001 € (+78 %) : ORANGE.** Calcul Selectra (11/11/2026) : « (prix de gros + 30,62 €/MWh d'accise) x 1,2 de TVA », **hors réseau, abonnement et marge**. Le vrai kWh dynamique serait donc encore plus cher, mais la comparaison n'est pas à base égale. **Dire** : « Début novembre, rien que l'électricité du marché et les taxes coûtaient déjà trente-six centimes le kilowattheure. Le tarif bleu, réseau compris : vingt centimes. » Source à l'écran : « calcul Selectra, 1er au 10 novembre 2026 ».

## 8. Le vieux contrat jamais comparé (à éviter n°1) : l'étude CRE

Source primaire : CRE, **Rapport n° 2026-06 « Cohérence des offres », 03/06/2026**, prix analysés au **1er décembre 2025**. Relais : UFC-Que Choisir, Fabrice Pouliquen, 18/06/2026.

| Point du brief | Verdict | À la source |
|---|---|---|
| 11,6 millions de clients en offre de marché | **ORANGE** | CRE : « environ 11,6 millions de consommateurs particuliers d'électricité en offre de marché », soit 75 % du marché couvert par l'étude. Ce n'est pas le total : l'observatoire CRE compte **15,84 millions** de foyers en offre de marché au 30/06/2026 (Kelwatt, 05/10/2026). Dire « dans l'étude de la C R E ». |
| Près de 10 % paient plus de 10 % au-dessus du tarif bleu | **ORANGE** | Dans UFC (« Près de 10 % de ces 11,6 millions de clients résidentiels ont actuellement une offre » à plus de 10 % au-dessus), **pas trouvé dans le rapport**. Le rapport dit : « 1,9 millions de consommateurs sont en offre à prix fixe dont le prix est supérieur au TRVE de plus de 5 % » et environ 70 % paient au plus le tarif bleu + 5 %. **Dire** : « Selon la C R E, un million neuf cent mille foyers ont un prix fixe plus de cinq pour cent au-dessus du tarif bleu. » |
| « un million de foyers paient plus de 10 % trop cher » (ton du brief) | **ORANGE** | Déduit de UFC (10 % × 11,6 M). Remplacer par le chiffre CRE ci-dessus. |
| Jusqu'à 591 €/an | **ORANGE (deux mots à ajouter)** | CRE : pour le 1 % des contrats les plus chers, « les économies potentielles pour le consommateur moyen atteignent **au moins 591 €/an HT** pour les offres à prix fixe d'électricité ». C'est « au moins », **hors taxes**, prix du 01/12/2025. **Dire** : « Pour le un pour cent des contrats les plus chers, la C R E calcule au moins cinq cent quatre-vingt-onze euros d'économie par an, hors taxes. » Miniature : « 591 € » reste juste (« jusqu'à » est même prudent ; écrire « 591 €/an » sans autre mot). |
| 150 € | **ORANGE** | Pas « 150 € » : économie moyenne **157 €/an HT** si l'on passe à l'offre la plus compétitive. |
| Offres « vertes » 5 à 10 % au-dessus | **ORANGE** | CRE : 78 % des contrats entre le tarif bleu et +5 % sont verts, **91 %** des contrats au-delà de +5 %. UFC : 97 % des 14 % de clients entre +5 et +10 %. Dire « presque toutes ces offres chères sont des offres "vertes" ». Le label VertVolt de l'ADEME n'a pas été vérifié ce jour : ne pas le citer ou le faire vérifier. |
| Citation d'Emmanuelle Wargon | **ORANGE (citation incomplète)** | Rapportée par UFC-Que Choisir (18/06/2026), pas dans le rapport : « Nous allons prendre contact avec les quelques fournisseurs qui maintiennent ces offres à prix fixe **très onéreuses** ». Citer en entier, source « via Que Choisir ». Le rapport lui-même dit que la CRE enverra un courrier aux fournisseurs dont les offres présentent des écarts. |

## 9. Heures creuses et Tempo (à prendre n°3)

- **Baromètre énergie-info 2026** du médiateur, publié le 03/11/2026, 2 000 foyers interrogés en ligne du 2 au 15/09/2026 (synthèse PDF) : **VERT**
  - « 86 % » des foyers : les factures pèsent de façon importante, **« le plus haut niveau depuis 2007 »** (la synthèse dit « stable par rapport à 2025 », elle n'écrit pas « record » → **ORANGE sur le mot**, dire « du jamais vu depuis deux mille sept »).
  - 37 % des foyers en offre de marché préfèrent un prix fixe même plus cher (électricité, +10 points).
  - 52 % ont l'option heures pleines / heures creuses ; **15 %** d'entre eux ne connaissent pas leurs horaires (21 % des moins de 35 ans, 9 % des 65 ans et plus).
  - 34 % ont eu du mal à payer une facture d'électricité ou de gaz (18 % en 2020).
- **Réforme des heures creuses : ORANGE.** « 8 h creuses par jour, surtout la nuit » n'est pas écrit tel quel. Sources : Enedis déplace une partie des heures creuses depuis le 01/11/2025 ; au moins « cinq heures creuses consécutives la nuit » (23 h-7 h) et « jusqu'à trois heures creuses peuvent être déplacées vers la plage 11 h - 17 h l'été » ; « plus de 11 millions de foyers » concernés (Selectra 20/07/2026, d'après la délibération CRE 2026-147). Depuis le 01/08/2026, l'option est ouverte en 3 kVA. Annexe B : « 16 heures pleines et 8 heures creuses ». **Dire** : « Tu as huit heures creuses par jour, la plupart la nuit. Et l'été, une partie passe en début d'après-midi. »
- **Tempo : VERT.** 22 jours rouges, 43 blancs, 300 bleus ; jours rouges entre le 1er novembre et le 31 mars, jamais un samedi, un dimanche ou un jour férié ; couleur connue la veille (Selectra). Prix TTC au 01/08/2026 (annexe B CRE en HT, recalculés) : jour rouge heures pleines **0,7295 €** (57,73 c€ HT), heures creuses 0,1615 € ; jour bleu 0,1654 / 0,1356 € ; jour blanc 0,1921 / 0,1536 € ; abonnement 6 kVA 189,63 €/an. Dire « soixante-treize centimes le kilowattheure, presque quatre fois le tarif de base ». Le nombre de jours rouges déjà tombés cet hiver n'a pas été vérifié.

## 10. Le tarif bleu (à prendre n°2)

- 19,20 millions de foyers, **54,8 %** des sites résidentiels au 30/06/2026 (observatoire CRE du T2 2026, publié le 30/09/2026, rapporté par Kelwatt le 05/10/2026). AFP : 19,37 millions au 31/03/2026. **VERT** (observatoire CRE non ouvert directement). Dire « dix-neuf millions de foyers ».
- 52 % des offres ouvertes fin juin moins chères que le tarif bleu (46 % fin mars) : **VERT** (même source).
- Achats lissés sur 24 mois : **VERT** (délibération 2026-06 : un « ruban d'énergie (produits calendaires Base et Peak) de manière lissée sur 24 mois »). Selectra (14/09) : pour 2027, 20 mois sur 24 étaient déjà achetés fin août.
- Baromètre : 41 % des clients au tarif bleu citent la stabilité des prix comme 1re raison de le garder.

## 11. La bonne offre (à prendre n°1) et la devinette 10:05

- Changement de fournisseur : « une quinzaine de minutes », numéro « à 14 chiffres », « à tout moment et sans frais », « aucuns frais de résiliation » (UFC 24/09/2026). **VERT.** « Zéro coupure » n'est pas dans l'article UFC : formulation sûre « le courant ne s'arrête pas, c'est le même réseau » (fait général : le réseau reste géré par le gestionnaire de réseau) → à garder mais sans l'attribuer à UFC.
- **Classement des litiges du médiateur : ROUGE sur « 5 étoiles ».** La page du médiateur (energie-info.fr, « Qualité de service clients ») note de **1 à 4 étoiles** un **taux de saisines pour 100 000 contrats** : 4 étoiles si ≤ 25 ; 3 étoiles de 26 à 90 ; 2 étoiles de 91 à 200 ; 1 étoile au-delà. Période 01/07/2025-30/06/2026, mise à jour tous les six mois. (UFC parle de 5 étoiles : on suit le médiateur.) **Dire** « regarde les étoiles du médiateur : quatre, c'est le maximum ».
- Rapport du médiateur 2025 (UFC 04/06/2026) : 28 076 litiges reçus, 10 475 saisines (−10 % sur un an), deux « cartons rouges ». Non utilisé à la voix (noms de fournisseurs).
- **Devinette « 8 sur 29 »** : **ORANGE**. Selectra 10/11/2026 (relevé du 09/11, Base 6 kVA, 4 500 kWh/an) : « 15 offres sur 44 » sous le tarif bleu, « 8 sur 29 » à prix fixe, meilleures offres « 74 € de moins » par an, 15 offres en hausse en un mois. Le chiffre du comparateur officiel n'a pas pu être relevé (page bloquée dans cette session). **Option** : garder « 8 sur 29 » avec « relevé Selectra, 9 novembre » à l'écran, ou relever le chiffre sur comparateur.energie-info.fr au moment de la capture et l'écrire dans `sources.md`. Le brief évoque « Trois fournisseurs ont arrêté de prendre de nouveaux clients » : Selectra les nomme → à la voix, « trois fournisseurs ne prennent plus de nouveaux clients », sans nom.

## 12. Ce qui n'a pas été vérifié (ne pas utiliser sans nouvelle vérification)
- Le label VertVolt de l'ADEME.
- Le nombre de jours rouges Tempo déjà passés en novembre 2026.
- Une baisse de taxe sur l'électricité au 01/02/2027 (évoquée par Selectra le 14/09, sans détail).
- Le prix spot moyen de novembre 2025 (65,8 €/MWh) à une source primaire (EPEX ou CRE).

## 13. Documents à capturer à l'écran (15)
Recadrer sur la phrase, jamais une page entière ; 3 à 6 s ; date visible quand elle existe.

| # | Document | URL | Phrase à mettre en valeur | Plan |
|---|---|---|---|---|
| 1 | Comparateur officiel du médiateur | https://comparateur.energie-info.fr/ | page d'accueil + résultat Base 6 kVA 4 500 kWh avec la lettre A-D d'une offre (sans nom de fournisseur lisible) ; relever le nombre d'offres sous le tarif bleu | n°1, 11:00 |
| 2 | energie-info : nouveautés du comparateur | https://www.energie-info.fr/le-comparateur-du-mediateur-national-de-lenergie-evolue-decouvrez-ses-nouveautes/ | « un outil public, gratuit, neutre et indépendant » + « A : très bonne stabilité, peu de risque de hausse » | n°1 |
| 3 | CRE, fiche « Niveau de certitude » | https://cre.fr/fileadmin/Documents/Autres/Niveau_de_certitude.pdf | les 4 pastilles A (vert foncé) → D (jaune) et « prix entièrement fixe garanti » | n°2 |
| 4 | CRE, délibération 2026-147, annexe B | https://www.cre.fr/fileadmin/Documents/Deliberations/2026/260715_2026-147_TRVE_Annexe_B.pdf | ligne Base résidentiel 13,61 c€/kWh HT, ligne 6 kVA 143,28 €/an ; ligne Tempo rouge 57,73 | ch. 1 et n°3 |
| 5 | AFP / Connaissance des énergies, 16/07/2026 | https://www.connaissancedesenergies.org/afp/electricite-le-gouvernement-suit-lavis-du-regulateur-cre-dune-hausse-de-25-des-tarifs-reglementes-260716 | « une facture moyenne passant de 1 046 à 1 072 euros TTC par an » | n°2 tarif bleu |
| 6 | energie-info, « Prix de l'électricité : que payons-nous ? » | https://www.energie-info.fr/fiche_pratique/prix-de-lelectricite-et-du-gaz-que-payons-nous/ | « Il s'agit de la seule composante soumise à la concurrence. » | ch. 1 |
| 7 | CRE, rapport Cohérence des offres 2026 | https://www.cre.fr/fileadmin/Documents/Rapports_et_etudes/2026/Rapport_Coherence_des_offres_2026.pdf | « au moins 591 €/an HT pour les offres à prix fixe d'électricité » | à éviter n°1 |
| 8 | UFC-Que Choisir, 18/06/2026 | https://www.quechoisir.org/actualite-gaz-et-electricite-des-centaines-d-euros-a-economiser-en-faisant-jouer-la-concurrence-n176850/ | titre + date + citation d'Emmanuelle Wargon | à éviter n°1 |
| 9 | Loi n° 2025-594 (Légifrance, JORF du 01/07/2025) | adresse Légifrance **non relevée** (site non ouvert ce jour) : sur legifrance.gouv.fr, rechercher « loi n° 2025-594 du 30 juin 2025 », ou l'article L. 223-1 du code de la consommation ; texte relu sur la reproduction du JO https://www.associatheque.fr/fr/fichiers/actualite/loi-2025-594-NOR-ECOX2432287L.pdf | « Il est interdit de démarcher par téléphone, directement ou par l'intermédiaire d'un tiers… » et « entrent en vigueur le 11 août 2026 » | à éviter n°5 |
| 10 | energie-info, faux médiateur | https://www.energie-info.fr/demarchage-a-domicile-certains-commerciaux-se-font-passer-pour-le-mediateur-national-de-lenergie/ | titre seulement (le texte nomme un fournisseur) | à éviter n°5 |
| 11 | Journal du Net, 15/05/2026 | https://www.journaldunet.com/magazine/1550239-cd1-compteur-linky-4000-euros/ | titre « "4 000 euros en un mois" » + date ; puis « "On ne sait pas", admet Matthieu Bertrand Neuser » | accroche, n°4, dénouement |
| 12 | JeChange, fin d'une offre −20 % | https://www.jechange.fr/energie/electricite/news/primeo-energie-fin-offre-fixe-20-hausse-42-fevrier-2027 | le passage « +42 % » et « le silence vaut acceptation » ; mention « mis à jour le 11/11/2026 » ; **ne pas montrer la grille datée du 01/02/2027** ; recadrer hors nom du fournisseur si possible | à éviter n°3 |
| 13 | energie-info, « Attention aux messages de votre fournisseur » | https://www.energie-info.fr/attention-aux-messages-que-vous-recevez-de-votre-fournisseur-denergie/ | « vous pouvez changer de fournisseur à tout moment et sans frais » | à éviter n°3 |
| 14 | energie-info, offres dynamiques | https://www.energie-info.fr/offres-a-tarification-dynamique-informations-pratiques-et-alerte-pour-sensibiliser-sur-leur-complexite/ | « le prix de l'énergie fluctue tous les jours et toutes les heures » | à éviter n°2 |
| 15 | Synthèse du baromètre énergie-info 2026 | https://www.banquedesterritoires.fr/sites/default/files/2026-11/Synthese_Barometre_Energie-Info_2026.pdf (ou la page du médiateur https://www.energie-mediateur.fr/le-mediateur/publications/barometre/) | « 15 % » des foyers en heures creuses ne connaissent pas leurs horaires ; « 86 % » | à prendre n°3 |
| (bonus) | energie-info, qualité de service | https://www.energie-info.fr/qualite-de-service-clients/ | la légende des étoiles « ≤ 25 » saisines pour 100 000 contrats (sans le tableau des noms) | n°1 |

## 14. Notes pour le scénariste et le fact-checker
- **Retournement du ch. 1 confirmé** : ≈ 40 € de fourniture, dont ≈ 7 € de commercialisation et de CEE ; le courant lui-même ≈ 30 € (estimation, à dire « une trentaine »).
- **Bonne nouvelle à dire honnêtement** : le tarif bleu amortit la flambée (lissage 24 mois) ; c'est pour ça qu'il reste un bon repli cet hiver.
- **Démarchage** : ajouter l'exception « ton fournisseur actuel peut t'appeler pour ton contrat » et « la loi parle du téléphone, pas de la porte ».
- **Couple des Yvelines** : toutes les citations sont du **juriste de l'association**, aucune du couple. Les lui attribuer à l'écran.
- **Rien sur les noms** : JDN, JeChange, Selectra et une page energie-info nomment des fournisseurs ; recadrer.
