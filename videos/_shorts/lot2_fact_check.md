# Fact-check — Shorts lot 2 (14 scripts)

Fact-checker « Le Vrai Prix », 9 novembre 2026. Fichiers : `videos/_shorts/lot2/*.json`. Aucun JSON modifié.

## Bilan
- **État pour la production** : JAUNE, à produire **après les corrections obligatoires** (aucun Short à refaire en entier).
- **Résumé** : tous les chiffres collent à la recherche et tous les calculs tombent juste (à 1 centime près, arrondis). Les problèmes : 1) le sigle « TVA » est écrit en lettres collées dans 5 Shorts (règle de prononciation) ; 2) l'année manque à deux endroits (pâtes, cinéma) ; 3) quatre généralisations, dans le lait, l'encre (deux) et le soda ; 4) le timbre : La Poste a annoncé le 27/07/2026 les tarifs du 01/01/2027, il faut le dire ; 5) « marge brute » n'est jamais dit dans le jambon ni dans le steak haché.
- **Exactitude** : 70 chiffres contrôlés. 66 conformes, 4 à corriger : 3,5 ml dit pour 3,4 ml affiché ; « trois fois » dit pour × 3,3 ; l'assiette de la TSA non confirmée ; le tarif du timbre bientôt périmé.

### Revérifications web (9/11/2026)
| Chiffre | Résultat | Source |
|---|---|---|
| Doliprane 1000 mg ×8 : 2,18 € = 1,16 € + 1,02 € d'honoraire | CONFIRMÉ (Selectra, 21/10/2026 ; la base publique des médicaments n'a pas pu être ouverte, le proxy l'a bloquée) | https://selectra.info/assurance/actualites/marche/doliprane-sans-ordonnance-prix-plein-65-pourcent |
| Lettre verte 1,52 €, recommandée 6,11 € (2026) | CONFIRMÉ, **mais au 01/01/2027 : lettre verte 1,67 €, recommandée 6,47 €** (+6,73 % en moyenne) | https://www.service-public.gouv.fr/particuliers/actualites/A16283 (28/07/2026) ; https://www.caissedesdepots.fr/sites/ms-cdc-fr/files/2026-07/CP_La_Poste_tarifs_au_010127.pdf (communiqué La Poste, 27/07/2026) |
| Taxe soda 2026 : 4,07 / 21,38 / 35,63 € par hl, forfait par tranche, plus de 8 kg/hl = 35,63 € | CONFIRMÉ (Weblex, qui cite BOI-BAREME-000038) | https://www.weblex.fr/chiffres-cles/contribution-sur-les-boissons-non-alcooliques-pour-2026 |
| FDJ, 1 € misé en point de vente (2025) : 68,3 % joueurs, 20 % État, 6,4 % FDJ, 5,3 % détaillants | CONFIRMÉ (page officielle) | https://www.fdj.fr/transparence/Transparence.html |
| TSA 10,72 % | CONFIRMÉ (CNC). **Assiette (HT ou TTC) non précisée par le CNC** : 0,75 € si hors TVA, 0,80 € si TTC, donc dire « environ » | https://www.cnc.fr/cinema/etudes-et-rapports/plaquettes/la-taxe-sur-les-entrees-en-salles-de-spectacles-cinematographiques-tsa_211700 |
| TVA billet de cinéma 5,5 % | Conforme (taux réduit en vigueur, recherche lot 1) | lot1_recherche.md §5 |

---

## l01-lait
| # | Phrase | Verdict | Remplacement exact | Source |
|---|---|---|---|---|
| 0 | Ta brique de lait, qui garde l'argent ? | OK | | |
| 1 | En deux mille vingt-trois, elle coûte en moyenne un euro sept en grande surface. | OK (1,07 €, 2023, l'année est dite) | | OFPM 2024, gr. 114 : https://observatoire-prixmarges.franceagrimer.fr/sites/default/files/pictures/10_2024_section_5_lait_de_vache_v7.docx_.pdf |
| 2 | La TVA prend six centimes. Le magasin garde trente-six centimes de marge brute. | **À CORRIGER** (sigle) | `La T V A prend six centimes. Le magasin garde trente-six centimes de marge brute.` | idem |
| 3 | L'industriel qui la remplit garde trente-huit centimes. | OK, amélioration recommandée (« qui la remplit » réduit son rôle, et « marge brute » n'est pas dit) | facultatif : `L'industriel laitier, qui traite et conditionne le lait, garde trente-huit centimes.` | idem |
| 4 | Et le lait lui-même ? Vingt-huit centimes seulement. À peine un quart du prix. | **À CORRIGER** : on voit des vaches et un éleveur, mais 0,28 € est la matière première **nette de la crème revendue**. L'éleveur, lui, est payé environ 0,49 €/L (prudence de la recherche). Et 0,28/1,07 = 26 %, donc « un peu plus d'un quart », pas « à peine ». | `Et le lait lui-même ? Vingt-huit centimes, une fois la crème revendue à part. Environ un quart du prix.` | idem |

Calcul : 0,06 + 0,36 + 0,38 + 0,28 = 1,08 € (arrondis OFPM, OK). Affichage « 36 c » : préférer « 0,36 € » (facultatif, même chose pour 38 c et 28 c).

## l02-jambon
| # | Phrase | Verdict | Remplacement exact | Source |
|---|---|---|---|---|
| 0 | Ton jambon, qui garde vraiment l'argent ? | OK | | |
| 1 | En deux mille vingt-trois, le kilo coûte en moyenne quatorze euros cinquante-huit. | OK | | OFPM 2024, gr. 31 : https://observatoire-prixmarges.franceagrimer.fr/sites/default/files/pictures/06_2024_section_1_viande_porcine_et_charcuteriev7_0.pdf |
| 2 | Le magasin garde deux euros vingt-cinq. L'abattoir, un euro sept. | **À CORRIGER** : « garde » laisse penser à un bénéfice, or c'est une marge brute (salaires, loyers…). Le mot n'apparaît nulle part dans le Short. | `Le magasin garde deux euros vingt-cinq de marge brute. L'abattoir, un euro sept.` | idem |
| 3 | La TVA, soixante-seize centimes. Et le cochon lui-même : cinq euros quarante-cinq. | **À CORRIGER** (sigle) | `La T V A, soixante-seize centimes. Et le cochon lui-même : cinq euros quarante-cinq.` | idem |
| 4 | Et l'usine qui le cuit et le tranche ? Cinq euros cinq. Presque autant que le cochon. | OK (5,05 contre 5,45) | | idem |

Calcul : 5,45 + 1,07 + 5,05 + 2,25 + 0,76 = 14,58 € exact. Titre : le prix de 14,58 € date de 2023. Recommandé : `Ton jambon : sur 14,58 € le kilo, qui touche quoi ? #shorts`.

## l03-steak
| # | Phrase | Verdict | Remplacement exact | Source |
|---|---|---|---|---|
| 0 | Ton steak haché, l'éleveur touche combien ? | OK | | |
| 1 | En deux mille vingt-trois, le kilo coûte en moyenne treize euros quatre-vingt-quatorze. | OK | | OFPM, présentation S. Devienne, 27/05/2026 : https://www.academie-agriculture.fr/system/files_force/seances-colloques/20260527presentation4.pdf?download=1 |
| 2 | L'abattoir et le hachage prennent deux euros quatre-vingt-neuf. | OK | | idem |
| 3 | Le magasin, trois euros cinquante-six. La TVA, soixante-treize centimes. | **À CORRIGER** : sigle, et « marge brute » absent du Short | `Le magasin, trois euros cinquante-six de marge brute. La T V A, soixante-treize centimes.` | idem |
| 4 | Et la viande payée à l'éleveur ? Six euros soixante-dix-sept. Presque la moitié du prix. | OK (48,6 %). Nuance recommandée : c'est la valeur des bêtes, pas son bénéfice (prudence de la recherche) | facultatif : `Et la viande, au prix payé pour les bêtes ? Six euros soixante-dix-sept. Presque la moitié du prix.` | idem |

Calcul : 6,77 + 2,89 + 3,56 + 0,73 = 13,95 € (13,94 annoncé, arrondi OK). Note : la recherche attribue les colonnes de la présentation OFPM « d'après les totaux et les commentaires ». La fiabilité est correcte, mais pas parfaite.

## l04-pates
| # | Phrase | Verdict | Remplacement exact | Source |
|---|---|---|---|---|
| 0 | Tes pâtes : combien vaut le blé dedans ? | OK | | |
| 1 | Un paquet de cinq cents grammes coûte en moyenne quatre-vingt-quinze centimes. | **À CORRIGER** : l'année manque (prix 2025), et 1,91 ÷ 2 = 0,955, d'où « environ » | `En deux mille vingt-cinq, un paquet de cinq cents grammes coûte environ quatre-vingt-quinze centimes.` | OFPM 2026, gr. 184 : https://observatoire-prixmarges.franceagrimer.fr/sites/default/files/pictures/13_2026_section_8_pates_alimentaires_v4.pdf |
| 2 | Depuis deux mille vingt et un, son prix en rayon a pris trente-neuf pour cent. | OK (2021-2025, synthèse 2026, même édition que gr. 184) | | https://observatoire-prixmarges.franceagrimer.fr/sites/default/files/pictures/2026_ofpm_synthese.pdf (gr. 18) |
| 3 | Pourtant, le blé dur a baissé : de cinquante-six à trente-neuf centimes par kilo de pâtes. | **À CORRIGER** : 0,56 → 0,39 couvre 2023 → 2025, pas 2021 → 2025 comme la phrase d'avant. Sans l'année, on croit que le blé a baissé pendant toute la hausse. | `Pourtant, depuis deux mille vingt-trois, le blé dur a baissé : de cinquante-six à trente-neuf centimes par kilo de pâtes.` | OFPM 2026, gr. 184 |
| 4 | Dans ton paquet, le blé vaut environ vingt centimes. Le reste, c'est surtout l'usine et le magasin. | OK (0,39 ÷ 2 = 0,195 ; marges aval 74 %, non séparées en 2025, d'où « surtout l'usine et le magasin », juste) | | idem |

## l05-beurre
| # | Phrase | Verdict | Remplacement exact | Source |
|---|---|---|---|---|
| 0 | Ton beurre, pourquoi il coûte si cher ? | OK | | |
| 1 | En deux mille vingt-cinq, le kilo est à dix euros trente-quatre en moyenne. | OK (source B qui cite l'OFPM 2026) | | https://www.transformation-laitiere.fr/ofpm-2026-repartition-prix-produits-laitiers-gms/ |
| 2 | Ta plaquette de deux cent cinquante grammes : environ deux euros soixante. | OK (2,585 €) | | calcul |
| 3 | En un an, la matière grasse du lait a pris dix-sept pour cent. | OK (2025) | | idem |
| 4 | Résultat : hors taxes, soixante-trois pour cent du prix paient la matière grasse du lait. | OK (63 %, synthèse 2026, même édition). « Résultat » est un lien de cause un peu appuyé ; tournure plus claire recommandée | facultatif : `Hors taxes, soixante-trois pour cent du prix servent désormais à payer la matière grasse du lait.` | https://observatoire-prixmarges.franceagrimer.fr/sites/default/files/pictures/2026_ofpm_synthese.pdf (gr. 19) |

Le Short ne mélange pas les éditions (le 45,2 % de 2024 n'est pas utilisé). Conforme.

## l06-doliprane
| # | Phrase | Verdict | Remplacement exact | Source |
|---|---|---|---|---|
| 0 | Ta boîte de Doliprane, qui touche l'argent ? | OK | | |
| 1 | La boîte de huit comprimés de mille milligrammes coûte deux euros dix-huit. | OK (revérifié) | | https://selectra.info/assurance/actualites/marche/doliprane-sans-ordonnance-prix-plein-65-pourcent ; https://base-donnees-publique.medicaments.gouv.fr/medicament/60234100/extrait |
| 2 | Le médicament lui-même compte pour un euro seize, marges du grossiste et de la pharmacie comprises. | OK. Les 1,16 € incluent aussi la TVA de 2,1 % : précision recommandée | facultatif : `Le médicament lui-même compte pour un euro seize, marges et T V A comprises.` | idem |
| 3 | Le reste ? Un euro deux d'honoraire pour le pharmacien, à chaque boîte vendue. | OK (revérifié) | | idem |
| 4 | Presque la moitié du prix paie l'acte du pharmacien, pas le comprimé. | OK (1,02 ÷ 2,18 = 46,8 %, affiché 47 %) | | calcul |

Le Short ne cite ni coût de fabrication ni prix du labo à 0,76 €. Conforme aux prudences.

## l07-lunettes
| # | Phrase | Verdict | Remplacement exact | Source |
|---|---|---|---|---|
| 0 | Tes lunettes, qui les paie vraiment ? | OK | | |
| 1 | Une paire avec deux verres simples coûte en moyenne trois cents euros. | OK (Octika, données mars 2025, source B) | | https://www.octika.com/blog/les-chiffres-de-l-optique-avril-2025-n201 |
| 2 | En France, on a dépensé huit milliards trois cents millions d'euros en optique en un an. | OK. L'année est recommandée | facultatif : `En France, on a dépensé huit milliards trois cents millions d'euros en optique en deux mille vingt-quatre.` | https://drees.solidarites-sante.gouv.fr/sites/default/files/2025-12/CNS%20-%20Fiche%2016%20-%20L%27optique%20m%C3%A9dicale.pdf |
| 3 | Selon Que Choisir, en deux mille treize, l'opticien revendait trois fois son prix d'achat. | **À CORRIGER** : la voix dit « trois fois », l'écran affiche « × 3,3 » ; et la phrase est bancale (« revendait trois fois son prix ») | `Selon Que Choisir, en deux mille treize, l'opticien revendait ses lunettes plus de trois fois leur prix d'achat.` | https://www.quechoisir.org/action-ufc-que-choisir-surcouts-de-l-optique-les-marges-exorbitantes-des-opticiens-n11637/ |
| 4 | Et la Sécu ? Elle ne paie que quatre pour cent. Le reste : ta mutuelle, et toi. | OK (DREES 2024 : 4 / 68 / 28 %). Il s'agit de 4 % des dépenses totales d'optique, pas de ta paire | facultatif : `Et la Sécu ? Elle paie quatre pour cent des dépenses d'optique. Le reste : ta mutuelle, et toi.` | DREES fiche 16 |

Le « coût de fabrication 15 à 40 € » n'est pas utilisé. Conforme.

## l08-encre
| # | Phrase | Verdict | Remplacement exact | Source |
|---|---|---|---|---|
| 0 | Ton encre d'imprimante, combien au litre ? | OK | | |
| 1 | Une petite cartouche noire courante coûte dix-sept euros quatre-vingt-quinze. | OK (prix d'un revendeur relevé le 03/11 ; non revérifié, le proxy bloque LDLC : montrer l'étiquette à l'écran) | | https://www.ldlc.com/fiche/PB00275816.html |
| 2 | Dedans : trois millilitres et demi. Moins qu'une cuillère à café. | **À CORRIGER** : la cartouche contient 3,4 ml (affiché 3,4 ml), pas 3,5 | `Dedans : trois virgule quatre millilitres. Moins qu'une cuillère à café.` | idem |
| 3 | Le parfum, c'est environ mille quatre cents euros le litre, selon une étude britannique. | **À CORRIGER** : « le parfum » généralise ; l'étude compare une eau de parfum haut de gamme, en 2021 | `Un parfum de luxe ? Environ mille quatre cents euros le litre, selon une étude de deux mille vingt et un.` | https://www.quechoisir.org/actualite-encre-d-imprimante-un-produit-de-luxe-n95760/ (cite Which?) |
| 4 | Ton encre : environ cinq mille deux cent quatre-vingts euros le litre. | **À CORRIGER** : le calcul porte sur **cette** cartouche. L'encre de marque moyenne est autour de 2 800 €/L (Which?), et les encres compatibles sont bien moins chères. « Ton encre » généralise. | `Cette encre-là : environ cinq mille deux cent quatre-vingts euros le litre. Près de quatre fois plus.` | calcul 17,95 ÷ 3,4 ml = 5 279 €/L ; 5 280 ÷ 1 400 = 3,8 |

## l09-fdj
| # | Phrase | Verdict | Remplacement exact | Source |
|---|---|---|---|---|
| 0 | Ton ticket F D J : où va l'argent ? | OK | | |
| 1 | Prends dix euros joués en point de vente. | OK | | https://www.fdj.fr/transparence/Transparence.html |
| 2 | Le buraliste garde cinquante-trois centimes. La F D J, soixante-quatre centimes. | OK (revérifié : 5,3 % et 6,4 %). Les « détaillants » ne sont pas tous buralistes (bars, presse) : formulation recommandée | facultatif : `Le point de vente garde cinquante-trois centimes. La F D J, soixante-quatre centimes.` | idem |
| 3 | L'État, lui, prend deux euros. | OK (20 %, prélèvements publics) | | idem |
| 4 | Et les joueurs récupèrent six euros quatre-vingt-trois en gains. En moyenne, tous jeux confondus. | OK (68,3 %, « tous jeux » dit, conforme à la prudence) | | idem |

Calcul : 6,83 + 2 + 0,64 + 0,53 = 10,00 €. Le commentaire « Joue avec modération » est bien présent.

## l10-livre
| # | Phrase | Verdict | Remplacement exact | Source |
|---|---|---|---|---|
| 0 | Ton livre à vingt euros, l'auteur touche combien ? | OK | | |
| 1 | Le libraire garde environ sept euros cinquante. | OK (37,5 %, répartition indicative) | | https://occitanielivre.fr/sites/default/files/2026-03/livret_jeunes_26_num.pdf |
| 2 | La distribution, trois euros quarante. L'éditeur, trois euros. | OK (17 % / 15 %) | | idem |
| 3 | L'imprimeur, trois euros aussi. La TVA, environ un euro. | **À CORRIGER** (sigle) | `L'imprimeur, trois euros aussi. La T V A, environ un euro.` | idem ; TVA exacte 1,04 € (calcul) |
| 4 | Et l'auteur ? Environ un euro quatre-vingt-dix pour un roman. Moins d'un euro sur dix. | OK (10 % médian de 18,96 € HT = 1,90 € ; 9,5 % du prix TTC) | | https://fill-livrelecture.org/wp-content/uploads/2025/04/10e_Barometre_AuteursEditeurs_08-04-25.pdf |

Note : la TVA réelle (1,04 €) et l'auteur au taux HT (1,90 €) remplacent les 1,10 € et 2,00 € du livret. Les parts font donc 19,84 €, pas 20 €. Avec « environ », c'est acceptable.

## l11-eau
| # | Phrase | Verdict | Remplacement exact | Source |
|---|---|---|---|---|
| 0 | Ta bouteille d'eau, combien de fois plus chère ? | OK | | |
| 1 | Au robinet, un mètre cube coûte en moyenne quatre euros quatre-vingt-neuf, assainissement compris. | OK. La date est recommandée (prix au 01/01/2025) | facultatif : `Au robinet, début deux mille vingt-cinq, un mètre cube coûte en moyenne quatre euros quatre-vingt-neuf, assainissement compris.` | https://ofb.gouv.fr/sites/ofb-gouv-fr/files/2026-07/cp_sispea_2024_0.pdf |
| 2 | Un mètre cube, c'est mille litres. Ton litre du robinet coûte donc un demi-centime. | OK (0,49 centime) | | calcul |
| 3 | En bouteille, c'est environ trente centimes le litre en moyenne. | OK (CIEAU via Selectra, B) | | https://selectra.info/energie/actualites/marche/eau-bouteille-robinet-prix-canicule-2026 |
| 4 | Soit environ soixante fois plus cher. Et jusqu'à trois cents fois pour les marques chères. | OK (0,30 ÷ 0,00489 = 61 ; 1,50 ÷ 0,00489 = 307). Conforme à la prudence (« marques chères ») | | calcul |

## l12-cinema
| # | Phrase | Verdict | Remplacement exact | Source |
|---|---|---|---|---|
| 0 | Ta place de ciné, ton argent va où ? | OK | | |
| 1 | En moyenne, une entrée rapporte sept euros quarante-deux, selon le C N C. | **À CORRIGER** : c'est le chiffre de 2024, il faut dire l'année (prudence lot 1 : le chiffre 2025 n'est pas trouvé) | `En deux mille vingt-quatre, une entrée rapportait en moyenne sept euros quarante-deux, selon le C N C.` | https://www.quechoisir.org/enquete-salles-obscures-les-prix-font-leur-cinema-n175090/ |
| 2 | La TVA prend environ trente-neuf centimes. | **À CORRIGER** (sigle) ; chiffre OK (5,5 % : 0,387 €) | `La T V A prend environ trente-neuf centimes.` | calcul |
| 3 | Une taxe qui finance le cinéma français prend soixante-quinze centimes. | **À CORRIGER** : le CNC ne dit pas si les 10,72 % portent sur le prix HT (0,75 €) ou TTC (0,80 €). Ajouter « environ » | `Une taxe qui finance le cinéma français prend environ soixante-quinze centimes.` | https://www.cnc.fr/cinema/etudes-et-rapports/plaquettes/la-taxe-sur-les-entrees-en-salles-de-spectacles-cinematographiques-tsa_211700 |
| 4 | Le reste est coupé en deux, à peu près : une moitié pour la salle, l'autre pour le film. | OK (« à peu près », conforme) | | lot1_recherche.md §5 |

Affichage plan 3 : `≈ 0,75 €` recommandé (au lieu de `0,75 €`).

## l13-timbre
Le tarif 2026 est juste, mais **La Poste a annoncé le 27/07/2026 : lettre verte à 1,67 € et recommandée à 6,47 € au 1er janvier 2027**. Le Short sort sept semaines avant cette hausse. « Passe à un euro cinquante-deux » se lit comme une annonce, alors que c'est déjà le prix actuel. On remplace la recommandée par l'annonce 2027.

| # | Phrase | Verdict | Remplacement exact | Source |
|---|---|---|---|---|
| 0 | Ton timbre a pris combien en quinze ans ? | **À CORRIGER** (la durée change avec 2027) | `Ton timbre a pris combien depuis deux mille onze ?` | |
| 1 | Au premier janvier deux mille vingt-six, la lettre verte passe à un euro cinquante-deux. | **À CORRIGER** (temps du verbe) | `Depuis le premier janvier deux mille vingt-six, la lettre verte coûte un euro cinquante-deux.` | https://www.lapostegroupe.com/assets/media/le-groupe-laposte/aIeE8FGsbswqTWUN_CPLaPoste-Tarifscourriercolis2026_.pdf |
| 2 | Une lettre recommandée : six euros onze. | **À CORRIGER** : vrai aujourd'hui, mais il faut l'annonce 2027 | texte : `Et au premier janvier deux mille vingt-sept, elle passera à un euro soixante-sept.` ; chiffre : `1,67 €` ; chiffre_mot : `un` | https://www.service-public.gouv.fr/particuliers/actualites/A16283 ; https://www.caissedesdepots.fr/sites/ms-cdc-fr/files/2026-07/CP_La_Poste_tarifs_au_010127.pdf |
| 3 | En deux mille onze, à sa création, la lettre verte coûtait cinquante-sept centimes. | OK | | https://en.wikipedia.org/wiki/Evolution_of_stamp_prices_in_France |
| 4 | Presque trois fois plus cher en quinze ans. | **À CORRIGER** (1,67 ÷ 0,57 = 2,93) | texte : `Presque trois fois plus cher qu'en deux mille onze.` ; chiffre : `× 2,9` | calcul |

Titre et accroche : toujours vrais aujourd'hui (1,52 €). Recommandé : `Lettre verte à 1,67 € en 2027 : le timbre a pris combien ? #shorts` et `TIMBRE À 1,67 € EN 2027 : IL A PRIS COMBIEN ?`. Sources : ajouter les deux URL 2027.

## l14-soda
| # | Phrase | Verdict | Remplacement exact | Source |
|---|---|---|---|---|
| 0 | Ta canette de soda cache quelle taxe ? | OK | | |
| 1 | En France, une taxe frappe le sucre ajouté des boissons. Elle grimpe avec la dose. | OK (barème par tranches) | | https://www.weblex.fr/chiffres-cles/contribution-sur-les-boissons-non-alcooliques-pour-2026 |
| 2 | Au-delà de huit kilos de sucre par hectolitre, c'est trente-cinq euros soixante-trois l'hectolitre. | OK (revérifié, forfait par tranche) | | idem ; https://selectra.info/assurance/actualites/marche/taxe-soda-bareme-coca-cola-combien-et-ou-va-argent |
| 3 | Ta canette classique fait trente-trois centilitres. | **À CORRIGER** : les 12 centimes ne valent que pour une boisson au-dessus de 8 g de sucre pour 100 ml, comme un cola classique (10,6 g). Un soda moins sucré paie 4 ou 21 € l'hectolitre. « Ta canette » généralise. | `Ta canette de cola classique fait trente-trois centilitres. Et elle dépasse ce seuil.` | lot1_recherche.md §10 (10,6 g/100 ml) |
| 4 | Ça fait environ douze centimes de taxe, rien que pour le sucre. | OK (0,33 × 35,63 = 11,8 c) | | calcul |

---

## Grille de cohérence
| Point vérifié | État | Notes |
|---|---|---|
| Exactitude des faits | ALERTE | 4 chiffres à corriger (encre 3,4 ml, lunettes × 3,3, TSA « environ », timbre 2027) |
| Fiabilité des sources | OK | OFPM, DREES, FDJ, CNC, La Poste, service-public : A. Octika, Selectra, transformation-laitiere : B, et ils citent une source primaire |
| Équilibre et neutralité | OK | Ton factuel. Il manquait des nuances (« marge brute », crème du lait), ajoutées dans les corrections |
| Recherche et script | ALERTE | Années oubliées (pâtes plan 3, cinéma) ; généralisations (lait, encre, soda) |
| Juridique et éthique | OK | Marques citées de façon factuelle (Doliprane, FDJ) ; mention « Joue avec modération » sur la FDJ ; les chiffres Que Choisir sont attribués |
| Prononciation | ALERTE | « TVA » à écrire « T V A » (5 Shorts) ; tous les chiffres sont en toutes lettres |

---

## Corrections obligatoires

Index des plans : 0 = premier. Champ = `plans[i].texte`, sauf mention contraire.

1. **l01-lait.json**, plan 2, texte
   - ancien : `La TVA prend six centimes. Le magasin garde trente-six centimes de marge brute.`
   - nouveau : `La T V A prend six centimes. Le magasin garde trente-six centimes de marge brute.`
2. **l01-lait.json**, plan 4, texte
   - ancien : `Et le lait lui-même ? Vingt-huit centimes seulement. À peine un quart du prix.`
   - nouveau : `Et le lait lui-même ? Vingt-huit centimes, une fois la crème revendue à part. Environ un quart du prix.`
3. **l02-jambon.json**, plan 2, texte
   - ancien : `Le magasin garde deux euros vingt-cinq. L'abattoir, un euro sept.`
   - nouveau : `Le magasin garde deux euros vingt-cinq de marge brute. L'abattoir, un euro sept.`
4. **l02-jambon.json**, plan 3, texte
   - ancien : `La TVA, soixante-seize centimes. Et le cochon lui-même : cinq euros quarante-cinq.`
   - nouveau : `La T V A, soixante-seize centimes. Et le cochon lui-même : cinq euros quarante-cinq.`
5. **l03-steak.json**, plan 3, texte
   - ancien : `Le magasin, trois euros cinquante-six. La TVA, soixante-treize centimes.`
   - nouveau : `Le magasin, trois euros cinquante-six de marge brute. La T V A, soixante-treize centimes.`
6. **l04-pates.json**, plan 1, texte
   - ancien : `Un paquet de cinq cents grammes coûte en moyenne quatre-vingt-quinze centimes.`
   - nouveau : `En deux mille vingt-cinq, un paquet de cinq cents grammes coûte environ quatre-vingt-quinze centimes.`
7. **l04-pates.json**, plan 3, texte
   - ancien : `Pourtant, le blé dur a baissé : de cinquante-six à trente-neuf centimes par kilo de pâtes.`
   - nouveau : `Pourtant, depuis deux mille vingt-trois, le blé dur a baissé : de cinquante-six à trente-neuf centimes par kilo de pâtes.`
8. **l07-lunettes.json**, plan 3, texte
   - ancien : `Selon Que Choisir, en deux mille treize, l'opticien revendait trois fois son prix d'achat.`
   - nouveau : `Selon Que Choisir, en deux mille treize, l'opticien revendait ses lunettes plus de trois fois leur prix d'achat.`
9. **l08-encre.json**, plan 2, texte
   - ancien : `Dedans : trois millilitres et demi. Moins qu'une cuillère à café.`
   - nouveau : `Dedans : trois virgule quatre millilitres. Moins qu'une cuillère à café.`
10. **l08-encre.json**, plan 3, texte
    - ancien : `Le parfum, c'est environ mille quatre cents euros le litre, selon une étude britannique.`
    - nouveau : `Un parfum de luxe ? Environ mille quatre cents euros le litre, selon une étude de deux mille vingt et un.`
11. **l08-encre.json**, plan 4, texte
    - ancien : `Ton encre : environ cinq mille deux cent quatre-vingts euros le litre.`
    - nouveau : `Cette encre-là : environ cinq mille deux cent quatre-vingts euros le litre. Près de quatre fois plus.`
12. **l10-livre.json**, plan 3, texte
    - ancien : `L'imprimeur, trois euros aussi. La TVA, environ un euro.`
    - nouveau : `L'imprimeur, trois euros aussi. La T V A, environ un euro.`
13. **l12-cinema.json**, plan 1, texte
    - ancien : `En moyenne, une entrée rapporte sept euros quarante-deux, selon le C N C.`
    - nouveau : `En deux mille vingt-quatre, une entrée rapportait en moyenne sept euros quarante-deux, selon le C N C.`
14. **l12-cinema.json**, plan 2, texte
    - ancien : `La TVA prend environ trente-neuf centimes.`
    - nouveau : `La T V A prend environ trente-neuf centimes.`
15. **l12-cinema.json**, plan 3, texte
    - ancien : `Une taxe qui finance le cinéma français prend soixante-quinze centimes.`
    - nouveau : `Une taxe qui finance le cinéma français prend environ soixante-quinze centimes.`
16. **l12-cinema.json**, plan 3, chiffre
    - ancien : `0,75 €`
    - nouveau : `≈ 0,75 €`
17. **l13-timbre.json**, plan 0, texte
    - ancien : `Ton timbre a pris combien en quinze ans ?`
    - nouveau : `Ton timbre a pris combien depuis deux mille onze ?`
18. **l13-timbre.json**, plan 1, texte
    - ancien : `Au premier janvier deux mille vingt-six, la lettre verte passe à un euro cinquante-deux.`
    - nouveau : `Depuis le premier janvier deux mille vingt-six, la lettre verte coûte un euro cinquante-deux.`
19. **l13-timbre.json**, plan 2, texte
    - ancien : `Une lettre recommandée : six euros onze.`
    - nouveau : `Et au premier janvier deux mille vingt-sept, elle passera à un euro soixante-sept.`
20. **l13-timbre.json**, plan 2, chiffre
    - ancien : `6,11 €`
    - nouveau : `1,67 €`
21. **l13-timbre.json**, plan 2, chiffre_mot
    - ancien : `six`
    - nouveau : `un`
22. **l13-timbre.json**, plan 4, texte
    - ancien : `Presque trois fois plus cher en quinze ans.`
    - nouveau : `Presque trois fois plus cher qu'en deux mille onze.`
23. **l13-timbre.json**, plan 4, chiffre
    - ancien : `× 2,7`
    - nouveau : `× 2,9`
24. **l13-timbre.json**, sources (ajout en fin de liste)
    - ancien : (rien)
    - nouveau : `Service-public.fr, 28/07/2026 (tarifs au 1er janvier 2027 : lettre verte 1,67 €) : https://www.service-public.gouv.fr/particuliers/actualites/A16283`
25. **l14-soda.json**, plan 3, texte
    - ancien : `Ta canette classique fait trente-trois centilitres.`
    - nouveau : `Ta canette de cola classique fait trente-trois centilitres. Et elle dépasse ce seuil.`

Chaque nouveau texte contient toujours le `chiffre_mot` du plan. Pour l13 plan 2, le `chiffre_mot` change (correction n° 21).
