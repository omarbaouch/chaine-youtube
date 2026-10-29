import React from 'react';
import {AbsoluteFill, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Ligne} from '../types';
import {POLICE} from '../police';

// Sous-titres "style YouTubeur" : 2-6 mots à la fois, le mot prononcé passe en jaune avec un petit "pop".
export const SousTitres: React.FC<{lignes: Ligne[]}> = ({lignes}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const ligne = lignes.find((l) => frame >= l.debut && frame < l.fin);
  if (!ligne) return null;
  const apparition = spring({frame: frame - ligne.debut, fps, config: {damping: 14, mass: 0.6}, durationInFrames: 10});
  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 120}}>
      <div
        style={{
          fontFamily: POLICE,
          fontWeight: 900,
          fontSize: 68,
          lineHeight: 1.15,
          textAlign: 'center',
          maxWidth: '78%',
          textTransform: 'uppercase',
          transform: `scale(${0.85 + 0.15 * apparition})`,
          WebkitTextStroke: '10px rgba(0,0,0,.85)',
          paintOrder: 'stroke fill',
          textShadow: '0 6px 18px rgba(0,0,0,.5)',
        }}
      >
        {ligne.mots.map((m, i) => {
          const actif = frame >= m.debut && frame < m.fin;
          const pop = actif ? spring({frame: frame - m.debut, fps, config: {damping: 10}, durationInFrames: 8}) : 0;
          return (
            <span
              key={i}
              style={{
                display: 'inline-block',
                margin: '0 0.28em',
                color: actif ? '#FFD400' : 'white',
                // Petit saut vers le haut plutôt qu'un agrandissement : les mots longs ne mordent plus sur l'espace.
                transform: `translateY(${-8 * pop * (1 - pop) * 4}px) scale(${1 + 0.04 * pop})`,
              }}
            >
              {m.texte}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
