import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {theme} from '../theme';

// Petite étiquette en haut à droite (lieu, date, chiffre clé) qui glisse depuis la droite (règle n°8 : 36 px, fond sombre).
export const Surtitre: React.FC<{texte: string}> = ({texte}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const e = spring({frame: frame - 6, fps, config: theme.ressort.doux});
  return (
    <AbsoluteFill style={{padding: '60px 90px', alignItems: 'flex-end'}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 16, opacity: e, transform: `translateX(${interpolate(e, [0, 1], [40, 0])}px)`,
        background: 'rgba(11,14,20,0.78)', padding: '10px 22px', borderRadius: 12}}>
        <div style={{width: 6, height: 40, background: theme.couleurs.accent, borderRadius: 3}} />
        <div style={{fontFamily: theme.polices.titre, fontWeight: 800, fontSize: 36, color: theme.couleurs.texte, textTransform: 'uppercase', letterSpacing: '0.06em'}}>
          {texte}
        </div>
      </div>
    </AbsoluteFill>
  );
};
