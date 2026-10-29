// Source unique des couleurs, polices, courbes et ressorts de la chaîne.
// Ne jamais écrire une couleur ou une courbe en dur dans un composant.
import {Easing} from 'remotion';
import '@fontsource/montserrat/700.css';
import '@fontsource/montserrat/800.css';
import '@fontsource/montserrat/900.css';
import '@fontsource/inter/400.css';
import '@fontsource/inter/500.css';
import '@fontsource/inter/600.css';

export const theme = {
  couleurs: {
    fond: '#0B0E14',
    fondAlt: '#141925',
    heros: '#FF6B2C', // orange "métal en fusion" : UN seul élément héros par image
    accent: '#7FD4FF', // bleu acier froid
    metalClair: '#E3E8EF',
    metalMoyen: '#9AA6B6',
    metalSombre: '#3A4352',
    texte: '#F2F4F7',
    texteDim: '#B4BDC9',
    grille: 'rgba(127, 212, 255, 0.07)',
    lueur: 'rgba(255, 107, 44, 0.45)',
  },
  polices: {
    titre: "'Montserrat', sans-serif",
    texte: "'Inter', sans-serif",
  },
  courbe: {
    sortie: Easing.bezier(0.16, 1, 0.3, 1), // entrées
    entreSortie: Easing.bezier(0.83, 0, 0.17, 1), // déplacements
    entree: Easing.bezier(0.7, 0, 0.84, 0), // sorties uniquement
    choc: Easing.bezier(0.55, 0, 1, 0.45), // coup de presse
  },
  ressort: {
    vif: {damping: 14, stiffness: 160, mass: 0.6},
    doux: {damping: 20, stiffness: 90, mass: 1},
    rebond: {damping: 11, stiffness: 170, mass: 0.7},
  },
} as const;

export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
