// Les 5 couches de chaque plan : fond vivant → (contenu) → étalonnage → grain → vignette.
import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {theme, clamp} from '../theme';

export const FondVivant: React.FC<{grille?: boolean}> = ({grille = true}) => {
  const f = useCurrentFrame();
  const d1 = Math.sin(f / 55) * 60;
  const d2 = Math.cos(f / 70) * 45;
  const apparition = interpolate(f, [0, 20], [0, 1], {...clamp, easing: theme.courbe.sortie});
  return (
    <AbsoluteFill style={{background: theme.couleurs.fond}}>
      <div style={{position: 'absolute', width: 1400, height: 1400, borderRadius: '50%', top: -600, left: -350 + d1, filter: 'blur(60px)',
        background: `radial-gradient(circle, ${theme.couleurs.heros}22, transparent 62%)`}} />
      <div style={{position: 'absolute', width: 1100, height: 1100, borderRadius: '50%', bottom: -520, right: -300 - d2, filter: 'blur(80px)',
        background: `radial-gradient(circle, ${theme.couleurs.accent}1F, transparent 65%)`}} />
      {grille ? (
        // Grille "plan d'ingénieur" qui dérive lentement
        <AbsoluteFill style={{opacity: apparition,
          backgroundImage: `linear-gradient(${theme.couleurs.grille} 1px, transparent 1px), linear-gradient(90deg, ${theme.couleurs.grille} 1px, transparent 1px)`,
          backgroundSize: '80px 80px', backgroundPosition: `${-f * 0.4}px ${-f * 0.25}px`,
          maskImage: 'radial-gradient(ellipse at center, black 30%, transparent 80%)'}} />
      ) : null}
    </AbsoluteFill>
  );
};

export const Etalonnage: React.FC = () => (
  <AbsoluteFill style={{pointerEvents: 'none'}}>
    <AbsoluteFill style={{backgroundColor: theme.couleurs.heros, mixBlendMode: 'soft-light', opacity: 0.08}} />
    <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,0.18), transparent 25%, transparent 75%, rgba(0,0,0,0.28))'}} />
  </AbsoluteFill>
);

export const Grain: React.FC = () => {
  const f = useCurrentFrame();
  const bruit = `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='220' height='220' filter='url(%23n)' opacity='0.5'/%3E%3C/svg%3E")`;
  return <AbsoluteFill style={{pointerEvents: 'none', backgroundImage: bruit, backgroundSize: '220px',
    backgroundPosition: `${(f * 7) % 220}px ${(f * 13) % 220}px`, opacity: 0.07, mixBlendMode: 'overlay'}} />;
};

export const Vignette: React.FC = () => (
  <AbsoluteFill style={{pointerEvents: 'none', background: 'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.45) 100%)'}} />
);
