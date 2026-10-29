import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {theme, clamp} from '../theme';

// Mots qui montent un par un (ressort), avec un mot héros optionnel.
export const MotsQuiMontent: React.FC<{texte: string; debut?: number; ecart?: number; taille?: number; heros?: string; style?: React.CSSProperties}> = ({
  texte, debut = 0, ecart = 3, taille = 150, heros, style,
}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <div style={{display: 'flex', flexWrap: 'wrap', columnGap: taille * 0.26, rowGap: 0, fontFamily: theme.polices.titre, fontWeight: 900,
      fontSize: taille, lineHeight: 1.02, letterSpacing: '-0.035em', color: theme.couleurs.texte, ...style}}>
      {texte.split(' ').map((mot, i) => {
        const p = spring({frame: f - debut - i * ecart, fps, config: theme.ressort.vif});
        const estHeros = heros && mot.replace(/[^\p{L}]/gu, '') === heros;
        return (
          <span key={i} style={{display: 'inline-block', overflow: 'hidden', paddingBottom: taille * 0.08}}>
            <span style={{display: 'inline-block', opacity: p, transform: `translateY(${interpolate(p, [0, 1], [taille * 0.7, 0])}px)`,
              color: estHeros ? theme.couleurs.heros : undefined, textShadow: estHeros ? `0 0 40px ${theme.couleurs.lueur}` : undefined}}>
              {mot}
            </span>
          </span>
        );
      })}
    </div>
  );
};

// Étiquette d'étape "01 · LA BOBINE" avec trait qui se dessine.
export const Etiquette: React.FC<{numero: string; texte: string; debut?: number}> = ({numero, texte, debut = 0}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame: f - debut, fps, config: theme.ressort.doux});
  const trait = interpolate(f - debut, [4, 26], [0, 1], {...clamp, easing: theme.courbe.sortie});
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: 22, opacity: p, transform: `translateX(${interpolate(p, [0, 1], [-30, 0])}px)`,
      fontFamily: theme.polices.texte, fontWeight: 600, fontSize: 30, letterSpacing: '0.18em', color: theme.couleurs.texteDim}}>
      <span style={{color: theme.couleurs.accent, fontVariantNumeric: 'tabular-nums'}}>{numero}</span>
      <div style={{width: 90 * trait, height: 2, background: theme.couleurs.accent, opacity: 0.7}} />
      <span>{texte}</span>
    </div>
  );
};

// Compteur animé (chiffres tabulaires, pas de tremblement).
export const Compteur: React.FC<{vers: number; debut?: number; decimales?: number; suffixe?: string; style?: React.CSSProperties}> = ({
  vers, debut = 0, decimales = 0, suffixe = '', style,
}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const v = interpolate(spring({frame: f - debut, fps, config: {damping: 30, stiffness: 60}}), [0, 1], [0, vers]);
  return <span style={{fontVariantNumeric: 'tabular-nums', ...style}}>{v.toFixed(decimales).replace('.', ',')}{suffixe}</span>;
};

// Sortie de scène (plus rapide que l'entrée) : à appliquer à un conteneur.
export const useSortie = (fin: number, duree = 12) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [fin - duree, fin], [0, 1], {...clamp, easing: theme.courbe.entree});
  return {opacity: 1 - p, transform: `translateY(${-50 * p}px) scale(${1 - 0.04 * p})`, filter: `blur(${6 * p}px)`};
};
