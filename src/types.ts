// Données calculées par scripts/build-props.mjs à partir de episodes/<slug>/montage.json.
// Ne pas écrire ce fichier à la main : modifier le montage.json, puis relancer le pipeline.

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
};

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
