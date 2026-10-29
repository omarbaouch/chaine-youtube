// Données calculées par scripts/build-props.mjs à partir de episodes/<slug>/montage.json.
// Ne pas écrire ce fichier à la main : modifier le montage.json, puis relancer le pipeline.

import type {Schema} from './motion/Schemas';

export type Mot = {texte: string; debut: number; fin: number}; // en frames, relatif à la scène
export type Ligne = {debut: number; fin: number; mots: Mot[]};

export type Scene = {
  id: string;
  type: 'video' | 'image' | 'titre';
  duree: number; // frames
  media?: string; // chemin dans public/
  voix?: string; // chemin dans public/
  voixDebut: number; // frame où la voix démarre dans la scène
  titre?: string;
  sousTitre?: string;
  surtitre?: string; // petit texte incrusté en haut à gauche (lieu, date, chiffre...)
  sousTitres: Ligne[];
  transition: 'fondu' | 'glissement' | 'balayage' | 'coupe';
  zoom: 'avant' | 'arriere' | 'aucun';
  vitesse: number;
  debutMedia: number; // secondes à sauter au début du rush
  couches?: Couche[]; // motion design posé sur le rush (positions en % de l'image : x 0-100, y 0-100)
  format?: 'rush' | 'ecran_partage' | 'mosaique' | 'schema'; // règle n°6 : varier
  schema?: Schema; // pour 'schema' et 'ecran_partage'
  medias?: string[]; // pour 'mosaique' (chemins dans public/)
  legendes?: string[];
  etapes?: boolean; // mosaïque numérotée
  cote?: 'gauche' | 'droite'; // écran partagé : côté du média réel
  legende?: string;
};

// Couches animées, écrites dans montage.json (champ "couches" d'une scène). "a" = début en secondes dans la scène.
export type Couche =
  | {type: 'annotation'; x: number; y: number; vers_x: number; vers_y: number; texte: string; a?: number}
  | {type: 'visee'; x: number; y: number; l: number; h: number; a?: number}
  | {type: 'compteur'; vers: number; decimales?: number; prefixe?: string; suffixe?: string; legende?: string; source?: string; a?: number; position?: 'droite' | 'gauche' | 'centre'}
  | {type: 'mots'; texte: string; heros?: string; a?: number; position?: 'centre' | 'gauche' | 'haut'}
  | {type: 'etiquette'; numero: string; texte: string; a?: number}
  | {type: 'carton'; texte: string; sous_texte?: string; a?: number}
  | {type: 'flash'; a: number}
  | {type: 'zoom_punch'; a: number} // emphase cinétique : zoom rapide + impact
  | {type: 'son'; src: string; a: number; volume?: number}; // bruitage de public/sfx/

export type EpisodeProps = {
  titre: string;
  fps: number;
  largeur: number;
  hauteur: number;
  dureeTransition: number; // frames
  musique?: {src: string; volume: number};
  etalonnage: {contraste: number; saturation: number; luminosite: number};
  grain: boolean;
  scenes: Scene[];
};
