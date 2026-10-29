// Briques "mixed media" : vraies vidéos fusionnées avec le motion design.
import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Video} from '@remotion/media';
import {theme, clamp} from '../theme';

const C = theme.couleurs;

// Rush réel : Ken Burns + étalonnage, flou/assombri en option (pour servir de fond).
export const Rush: React.FC<{src: string; zoom?: [number, number]; flou?: number; lumiere?: number; debut?: number; vitesse?: number; duree?: number}> = ({
  src, zoom = [1.05, 1.15], flou = 0, lumiere = 1, debut = 0, vitesse = 1, duree = 120,
}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = interpolate(f, [0, duree], zoom, {...clamp, easing: theme.courbe.entreSortie});
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${s})`, filter: `blur(${flou}px) brightness(${lumiere}) contrast(1.08) saturate(0.9)`}}>
        <Video src={src} muted loop objectFit="cover" trimBefore={Math.round(debut * fps)} playbackRate={vitesse} style={{width: '100%', height: '100%'}} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// Carte vidéo : se révèle par un volet, coins arrondis, ombre portée, léger flottement.
export const CarteVideo: React.FC<{src: string; x: number; y: number; l: number; h: number; debut?: number; children?: React.ReactNode}> = ({
  src, x, y, l, h, debut = 0, children,
}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame: f - debut, fps, config: theme.ressort.doux});
  const volet = interpolate(f - debut, [0, 22], [100, 0], {...clamp, easing: theme.courbe.sortie});
  const flotte = Math.sin(f / 26) * 4;
  return (
    <div style={{position: 'absolute', left: x, top: y + flotte, width: l, height: h, borderRadius: 28, overflow: 'hidden',
      clipPath: `inset(0 ${volet}% 0 0 round 28px)`, transform: `scale(${interpolate(p, [0, 1], [0.94, 1])})`,
      boxShadow: '0 50px 100px -30px rgba(0,0,0,0.75)', border: '1px solid rgba(255,255,255,0.10)'}}>
      <Rush src={src} />
      <AbsoluteFill style={{background: 'linear-gradient(180deg, transparent 55%, rgba(0,0,0,0.45))'}} />
      {children}
    </div>
  );
};

// Annotation façon documentaire : point pulsant + trait qui se dessine + étiquette.
export const Annotation: React.FC<{x: number; y: number; vers: [number, number]; texte: React.ReactNode; debut?: number}> = ({x, y, vers, texte, debut = 0}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const point = spring({frame: f - debut, fps, config: theme.ressort.rebond});
  const trait = interpolate(f - debut, [6, 24], [0, 1], {...clamp, easing: theme.courbe.sortie});
  const etiq = spring({frame: f - debut - 18, fps, config: theme.ressort.vif});
  const pulse = 1 + 0.5 * ((f - debut) % 40) / 40;
  const [x2, y2] = vers;
  return (
    <>
      <svg width={1920} height={1080} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
        <circle cx={x} cy={y} r={22 * pulse} fill="none" stroke={C.heros} strokeWidth={2} opacity={point * (1.5 - pulse)} />
        <circle cx={x} cy={y} r={9 * point} fill={C.heros} style={{filter: `drop-shadow(0 0 10px ${C.heros})`}} />
        <line x1={x} y1={y} x2={x + (x2 - x) * trait} y2={y + (y2 - y) * trait} stroke="white" strokeWidth={2.5} opacity={0.9} />
      </svg>
      <div style={{position: 'absolute', left: x2 + 14, top: y2 - 30, opacity: etiq, transform: `translateY(${interpolate(etiq, [0, 1], [14, 0])}px)`,
        padding: '12px 20px', borderRadius: 12, background: 'rgba(11,14,20,0.62)', backdropFilter: 'blur(12px)', border: '1px solid rgba(255,255,255,0.14)',
        fontFamily: theme.polices.texte, fontSize: 30, fontWeight: 600, color: C.texte, whiteSpace: 'nowrap'}}>
        {texte}
      </div>
    </>
  );
};

// Coins de visée (HUD) autour d'une zone du rush, qui "verrouillent" la cible.
export const Visee: React.FC<{x: number; y: number; l: number; h: number; debut?: number; choc?: number}> = ({x, y, l, h, debut = 0, choc = 0}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame: f - debut, fps, config: theme.ressort.vif});
  const e = interpolate(p, [0, 1], [60, 0]) - choc * 14;
  const c = 46;
  const coin = (cx: number, cy: number, sx: number, sy: number) => (
    <path d={`M ${cx + sx * c} ${cy} L ${cx} ${cy} L ${cx} ${cy + sy * c}`} fill="none" stroke={C.accent} strokeWidth={4} strokeLinecap="round" />
  );
  return (
    <svg width={1920} height={1080} style={{position: 'absolute', inset: 0, opacity: p}}>
      {coin(x - e, y - e, 1, 1)}
      {coin(x + l + e, y - e, -1, 1)}
      {coin(x - e, y + h + e, 1, -1)}
      {coin(x + l + e, y + h + e, -1, -1)}
      <line x1={x + l / 2 - 14} x2={x + l / 2 + 14} y1={y + h / 2} y2={y + h / 2} stroke={C.accent} strokeWidth={2} opacity={0.7} />
      <line y1={y + h / 2 - 14} y2={y + h / 2 + 14} x1={x + l / 2} x2={x + l / 2} stroke={C.accent} strokeWidth={2} opacity={0.7} />
    </svg>
  );
};

// Panneau vitré (flou d'arrière-plan) pour poser schémas et chiffres SUR la vidéo.
export const Vitre: React.FC<{x: number; y: number; l: number; h: number; debut?: number; children: React.ReactNode; rayon?: number}> = ({
  x, y, l, h, debut = 0, children, rayon = 24,
}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame: f - debut, fps, config: theme.ressort.doux});
  return (
    <div style={{position: 'absolute', left: x, top: y, width: l, height: h, borderRadius: rayon, overflow: 'hidden', opacity: p,
      transform: `translateY(${interpolate(p, [0, 1], [30, 0])}px) scale(${interpolate(p, [0, 1], [0.96, 1])})`,
      background: 'rgba(11,14,20,0.55)', backdropFilter: 'blur(22px) saturate(1.2)', border: '1px solid rgba(255,255,255,0.12)',
      boxShadow: '0 30px 80px -30px rgba(0,0,0,0.8)'}}>
      {children}
    </div>
  );
};

// Flash d'impact (2-3 images) synchronisé avec un bruitage.
export const Flash: React.FC<{a: number[]; force?: number}> = ({a, force = 0.22}) => {
  const f = useCurrentFrame();
  const o = a.reduce((m, t) => Math.max(m, interpolate(f, [t, t + 1, t + 5], [0, force, 0], clamp)), 0);
  return <AbsoluteFill style={{background: 'white', opacity: o, mixBlendMode: 'overlay', pointerEvents: 'none'}} />;
};
