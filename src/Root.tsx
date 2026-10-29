import React from 'react';
import {Composition} from 'remotion';
import {Episode, dureeTotale} from './Episode';
import type {EpisodeProps} from './types';

// Props par défaut : une carte titre seule, pour que le Studio s'ouvre même sans épisode construit.
// Pour un vrai épisode : npm run produire -- <slug>  (crée public/ep/<slug>/props.json)
const parDefaut: EpisodeProps = {
  titre: 'Aperçu',
  fps: 30,
  largeur: 1920,
  hauteur: 1080,
  dureeTransition: 12,
  etalonnage: {contraste: 1.08, saturation: 1.1, luminosite: 1},
  grain: true,
  scenes: [
    {
      id: 's01',
      type: 'titre',
      duree: 90,
      voixDebut: 0,
      titre: 'Ma chaîne',
      sousTitre: 'Lance un épisode pour voir le vrai montage',
      sousTitres: [],
      transition: 'coupe',
      zoom: 'avant',
      vitesse: 1,
      debutMedia: 0,
    },
  ],
};

export const RemotionRoot: React.FC = () => (
  <Composition
    id="Episode"
    component={Episode}
    durationInFrames={90}
    fps={30}
    width={1920}
    height={1080}
    defaultProps={parDefaut}
    calculateMetadata={({props}) => ({
      durationInFrames: dureeTotale(props),
      fps: props.fps,
      width: props.largeur,
      height: props.hauteur,
    })}
  />
);
