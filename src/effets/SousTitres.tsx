import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Ligne} from '../types';
import {theme} from '../theme';

const C = theme.couleurs;

// Sous-titres "style YouTubeur" (règle n°8) : 78 px, MAJUSCULES, contour noir ;
// le mot prononcé passe sur une pastille orange (texte foncé) qui glisse de mot en mot.
export const SousTitres: React.FC<{lignes: Ligne[]}> = ({lignes}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const ligne = lignes.find((l) => frame >= l.debut && frame < l.fin);
  if (!ligne) return null;
  const apparition = spring({frame: frame - ligne.debut, fps, config: {damping: 14, mass: 0.6}, durationInFrames: 10});
  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 96}}>
      <div
        style={{
          fontFamily: theme.polices.titre,
          fontWeight: 900,
          fontSize: 78,
          lineHeight: 1.18,
          textAlign: 'center',
          maxWidth: 1560,
          textTransform: 'uppercase',
          letterSpacing: '-0.01em',
          opacity: apparition,
          transform: `translateY(${interpolate(apparition, [0, 1], [18, 0])}px) scale(${0.9 + 0.1 * apparition})`,
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          columnGap: 18,
        }}
      >
        {ligne.mots.map((m, i) => {
          const actif = frame >= m.debut && frame < m.fin;
          const pop = actif ? spring({frame: frame - m.debut, fps, config: {damping: 12, stiffness: 220}, durationInFrames: 8}) : 0;
          return (
            <span
              key={i}
              style={{
                display: 'inline-block',
                padding: '0 14px',
                borderRadius: 14,
                background: actif ? C.heros : 'transparent',
                color: actif ? '#0B0E14' : C.texte,
                WebkitTextStroke: actif ? '0px transparent' : '10px rgba(0,0,0,.9)',
                paintOrder: 'stroke fill',
                textShadow: actif ? 'none' : '0 6px 18px rgba(0,0,0,.55)',
                boxShadow: actif ? `0 10px 30px ${C.lueur}` : 'none',
                transform: `scale(${1 + 0.06 * pop}) rotate(${actif ? -1.2 : 0}deg)`,
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
