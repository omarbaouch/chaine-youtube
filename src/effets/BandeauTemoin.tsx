import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {theme} from '../theme';
import type {Temoin} from '../types';

// Bandeau « qui parle » d'un témoignage (format temoignage) : nom en blanc, rôle en orange, source en petit.
// En haut à gauche pour laisser la place aux sous-titres de la citation en bas.
export const BandeauTemoin: React.FC<{temoin: Temoin}> = ({temoin}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const e = spring({frame: f - 8, fps, config: theme.ressort.doux});
  return (
    <AbsoluteFill style={{padding: '70px 90px', alignItems: 'flex-start'}}>
      <div style={{display: 'flex', gap: 18, opacity: e, transform: `translateX(${interpolate(e, [0, 1], [-50, 0])}px)`,
        background: 'rgba(11,14,20,0.82)', padding: '16px 28px 16px 20px', borderRadius: 14}}>
        <div style={{width: 8, background: theme.couleurs.heros, borderRadius: 4}} />
        <div>
          <div style={{fontFamily: theme.polices.titre, fontWeight: 900, fontSize: 48, color: theme.couleurs.texte, lineHeight: 1.05}}>{temoin.nom}</div>
          {temoin.role ? <div style={{fontFamily: theme.polices.titre, fontWeight: 800, fontSize: 32, color: theme.couleurs.heros, marginTop: 4}}>{temoin.role}</div> : null}
          {temoin.source ? <div style={{fontFamily: theme.polices.texte, fontSize: 24, color: theme.couleurs.texteDim, marginTop: 6}}>Source : {temoin.source}</div> : null}
        </div>
      </div>
    </AbsoluteFill>
  );
};
