import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {POLICE} from '../police';

// Petite étiquette en haut à gauche (lieu, date, chiffre clé) qui glisse depuis la gauche.
export const Surtitre: React.FC<{texte: string}> = ({texte}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const e = spring({frame: frame - 6, fps, config: {damping: 200}, durationInFrames: 18});
  return (
    <AbsoluteFill style={{padding: 70}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 18, opacity: e, transform: `translateX(${interpolate(e, [0, 1], [-40, 0])}px)`}}>
        <div style={{width: 8, height: 56, background: '#FFD400', borderRadius: 4}} />
        <div
          style={{
            fontFamily: POLICE,
            fontWeight: 800,
            fontSize: 40,
            color: 'white',
            textTransform: 'uppercase',
            letterSpacing: 2,
            background: 'rgba(0,0,0,.45)',
            padding: '8px 18px',
            borderRadius: 6,
          }}
        >
          {texte}
        </div>
      </div>
    </AbsoluteFill>
  );
};
