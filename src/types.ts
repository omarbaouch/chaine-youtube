// Données calculées par scripts/construire.mjs à partir de episodes/<slug>/montage.json.
// Ne pas écrire ce fichier à la main : modifier le montage.json, puis relancer le pipeline.

export type Mot = {texte: string; debut: number; fin: number}; // en frames, relatif à la scène
export type Ligne = {debut: number; fin: number; mots: Mot[]};

// Règle n°6 : formats de plan. Jamais deux plans consécutifs du même format.
//  rush          : un média réel plein écran + couches animées
//  ecran_partage : média réel d'un côté, schéma animé de l'autre
//  mosaique      : 2 à 4 médias réels qui entrent l'un après l'autre
//  schema        : animation SVG/HTML pure (sur fond vivant ou rush flouté)
//  titre         : carte de chapitre
export type Format = 'rush' | 'ecran_partage' | 'mosaique' | 'schema' | 'titre';

export type Media = {src: string; image: boolean; legende?: string};

export type PartPrix = {label: string; valeur: number; heros?: boolean};
export type Schema =
  | {type: 'decomposition'; titre?: string; total?: number; unite?: string; decimales?: number; parts: PartPrix[]; source?: string}
  | {type: 'processus'; titre?: string; etapes: string[]; actif?: number; a?: number[]; source?: string}
  | {type: 'chiffre'; valeur: number; decimales?: number; prefixe?: string; suffixe?: string; legende?: string; comparaison?: string;
      source?: string; revele_a?: number}
  | {type: 'comparaison'; titre?: string; unite?: string; decimales?: number; heros?: 'a' | 'b'; source?: string;
      a: {label: string; valeur: number}; b: {label: string; valeur: number}}
  | {type: 'decoupe'; titre?: string; total?: number; unite?: string; decimales?: number; parts: PartPrix[]; source?: string;
      zone?: [number, number] /* début/fin de l'objet en % de largeur de l'image */; zone_y?: [number, number]; ratio?: number}
  | {type: 'devine'; question: string; choix: string[]; bonne?: number; secondes?: number}
  | {type: 'suspect'; nom: string; accusation?: string; verdict?: string | null; numero?: string}
  | {type: 'piece'; titre?: string; total?: number; unite?: string; decimales?: number; parts: PartPrix[]; source?: string;
      zone?: [number, number]; zone_y?: [number, number]; ratio?: number}
  | {type: 'loupe'; points: {x: number; y: number; texte: string; a?: number}[]; zoom?: number}
  | {type: 'liste'; titre?: string; elements: {texte: string; valeur?: string; heros?: boolean}[]; source?: string};

export type Son = {nom: string; a: number; volume?: number}; // a = secondes dans la scène

export type Scene = {
  id: string;
  type: 'video' | 'image' | 'titre';
  format: Format;
  duree: number; // frames
  media?: string; // chemin dans public/ (format rush, fond de titre/schéma)
  medias: Media[]; // formats mosaique / ecran_partage
  voix?: string; // chemin dans public/
  voixDebut: number; // frame où la voix démarre dans la scène
  titre?: string;
  sousTitre?: string;
  numero?: string; // "01" pour les cartes de chapitre
  surtitre?: string; // petit texte incrusté en haut à gauche (lieu, date, chiffre...)
  sousTitres: Ligne[];
  transition: 'fondu' | 'glissement' | 'balayage' | 'coupe';
  zoom: 'avant' | 'arriere' | 'aucun';
  vitesse: number;
  debutMedia: number; // secondes à sauter au début du rush
  couches?: Couche[]; // motion design posé sur le rush (positions en % de l'image : x 0-100, y 0-100)
  schema?: Schema;
  etiquetteSchema?: string; // "Schéma : …" (règle n°1 : tout dessin est étiqueté)
  cote?: 'gauche' | 'droite'; // ecran_partage : côté du média réel
  punch?: {a: number; texte?: string}; // règle n°7 : emphase cinétique (zoom + impact)
  sons: Son[];
  qui?: string; // 'sceptique' = 2e voix
  ambiance?: string;
};

// Couches animées, écrites dans montage.json (champ "couches" d'une scène). "a" = début en secondes dans la scène.
export type Couche =
  | {type: 'annotation'; x: number; y: number; vers_x: number; vers_y: number; texte: string; a?: number}
  | {type: 'visee'; x: number; y: number; l: number; h: number; a?: number}
  | {type: 'compteur'; vers: number; decimales?: number; prefixe?: string; suffixe?: string; legende?: string; source?: string; a?: number; position?: 'droite' | 'gauche' | 'centre'}
  | {type: 'mots'; texte: string; heros?: string; a?: number; position?: 'centre' | 'gauche' | 'haut'}
  | {type: 'etiquette'; numero: string; texte: string; a?: number}
  | {type: 'carton'; texte: string; sous_texte?: string; a?: number}
  | {type: 'source'; texte: string; a?: number}
  | {type: 'flash'; a: number};

export type EpisodeProps = {
  titre: string;
  fps: number;
  largeur: number;
  hauteur: number;
  dureeTransition: number; // frames
  musique?: {src: string; volume: number};
  voixPlages?: [number, number][];
  musiques?: {src: string; de: number; a: number; decalage: number}[]; // musique par ambiance // frames globales où la voix parle (la musique se baisse)
  etalonnage: {contraste: number; saturation: number; luminosite: number};
  grain: boolean;
  scenes: Scene[];
};
