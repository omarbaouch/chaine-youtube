// Formats composés (règle n°6) : mosaïque de médias réels, écran partagé média réel + schéma SVG.
import React from 'react';
import {AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Video} from '@remotion/media';
import {theme, clamp} from '../theme';
import {SchemaAnime, type Schema} from './Schemas';

const C = theme.couleurs;

// Média réel (vidéo ou photo) avec Ken Burns, rempli dans son cadre.
export const MediaReel: React.FC<{src: string; zoom?: [number, number]; duree?: number}> = ({src, zoom = [1.04, 1.16], duree = 120}) => {
  const f = useCurrentFrame();
  const s = interpolate(f, [0, duree], zoom, {...clamp, easing: theme.courbe.entreSortie});
  const derive = interpolate(f, [0, duree], [0, -2], clamp);
  const style: React.CSSProperties = {width: '100%', height: '100%', transform: `scale(${s}) translateX(${derive}%)`};
  return /\.(mp4|webm|mov)$/i.test(src) ? (
    <Video src={staticFile(src)} muted loop objectFit="cover" style={style} />
  ) : (
    <Img src={staticFile(src)} style={{...style, objectFit: 'cover'}} />
  );
};

const Carte: React.FC<{x: number; y: number; l: number; h: number; debut: number; children: React.ReactNode; legende?: string; numero?: number; rot?: number}> = ({
  x, y, l, h, debut, children, legende, numero, rot = 0,
}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame: f - debut, fps, config: theme.ressort.vif});
  const flotte = Math.sin((f + debut * 3) / 24) * 4;
  return (
    <div style={{position: 'absolute', left: x, top: y + flotte, width: l, height: h, opacity: p,
      transform: `translateY(${interpolate(p, [0, 1], [60, 0])}px) scale(${interpolate(p, [0, 1], [0.85, 1])}) rotate(${rot * p}deg)`}}>
      <div style={{position: 'absolute', inset: 0, borderRadius: 26, overflow: 'hidden', border: '2px solid rgba(255,255,255,0.14)',
        boxShadow: '0 40px 90px -25px rgba(0,0,0,0.85)'}}>{children}</div>
      {numero ? (
        <div style={{position: 'absolute', left: -18, top: -18, width: 64, height: 64, borderRadius: 32, background: C.accent, color: '#0B0E14',
          display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: theme.polices.titre, fontWeight: 900, fontSize: 30,
          boxShadow: '0 10px 30px rgba(0,0,0,.5)'}}>{String(numero).padStart(2, '0')}</div>
      ) : null}
      {legende ? (
        <div style={{position: 'absolute', left: 0, right: 0, bottom: -64, textAlign: 'center', fontFamily: theme.polices.titre, fontWeight: 800,
          fontSize: 36, color: C.texte, textShadow: '0 4px 14px rgba(0,0,0,.8)'}}>{legende}</div>
      ) : null}
    </div>
  );
};

// 2 à 4 médias réels qui arrivent l'un après l'autre (numérotés si "etapes") ; fond = premier média flouté.
export const Mosaique: React.FC<{medias: string[]; legendes?: string[]; etapes?: boolean; duree: number}> = ({medias, legendes = [], etapes, duree}) => {
  const n = Math.min(4, medias.length);
  const ecart = Math.max(6, Math.round((duree * 0.45) / Math.max(1, n)));
  const l = n <= 2 ? 760 : n === 3 ? 540 : 400;
  const h = Math.round(l * 0.68);
  const gap = n <= 2 ? 80 : 44;
  const total = n * l + (n - 1) * gap;
  const x0 = (1920 - total) / 2;
  const y = 330 - (n <= 2 ? 40 : 0);
  return (
    <AbsoluteFill style={{background: C.fond}}>
      <AbsoluteFill style={{filter: 'blur(26px) brightness(0.28) saturate(1.2)', transform: 'scale(1.15)'}}>
        <MediaReel src={medias[0]} duree={duree} />
      </AbsoluteFill>
      {medias.slice(0, n).map((m, i) => (
        <Carte key={i} x={x0 + i * (l + gap)} y={y} l={l} h={h} debut={4 + i * ecart} legende={legendes[i]} numero={etapes ? i + 1 : undefined} rot={i % 2 ? 1.5 : -1.5}>
          <MediaReel src={m} duree={duree} />
        </Carte>
      ))}
    </AbsoluteFill>
  );
};

// Média réel dans une grande carte d'un côté, schéma SVG animé de l'autre.
export const EcranPartage: React.FC<{media: string; schema?: Schema; cote?: 'gauche' | 'droite'; legende?: string; duree: number}> = ({
  media, schema, cote = 'gauche', legende, duree,
}) => {
  const f = useCurrentFrame();
  const glisse = interpolate(f, [0, 16], [cote === 'gauche' ? -80 : 80, 0], {...clamp, easing: theme.courbe.sortie});
  return (
    <AbsoluteFill style={{background: C.fond}}>
      <AbsoluteFill style={{filter: 'blur(30px) brightness(0.25)', transform: 'scale(1.2)'}}>
        <MediaReel src={media} duree={duree} />
      </AbsoluteFill>
      <div style={{position: 'absolute', top: 0, bottom: 0, width: 900, [cote === 'gauche' ? 'left' : 'right']: 0, transform: `translateX(${glisse}px)`}}>
        <Carte x={90} y={100} l={760} h={640} debut={0} legende={legende}>
          <MediaReel src={media} duree={duree} />
        </Carte>
      </div>
      {schema ? (
        <div style={{position: 'absolute', top: 100, width: 860, height: 700, [cote === 'gauche' ? 'left' : 'right']: 970}}>
          <SchemaCompact schema={schema} />
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

// Version "demi-écran" des schémas : mêmes animations, typographie à taille réelle (règle n°8).
const SchemaCompact: React.FC<{schema: Schema}> = ({schema}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const T = theme.polices;
  const titre = 'titre' in schema && schema.titre ? (
    <div style={{fontFamily: T.titre, fontWeight: 900, fontSize: 64, lineHeight: 1.05, color: C.texte, marginBottom: 46, letterSpacing: '-0.02em',
      opacity: interpolate(f, [2, 14], [0, 1], clamp), transform: `translateY(${interpolate(f, [2, 14], [24, 0], clamp)}px)`}}>{schema.titre}</div>
  ) : null;
  const source = 'source' in schema && schema.source ? (
    <div style={{marginTop: 30, fontFamily: T.texte, fontSize: 24, color: C.texteDim, opacity: interpolate(f, [24, 36], [0, 1], clamp)}}>Source : {schema.source}</div>
  ) : null;
  if (schema.type === 'comparaison') {
    const max = Math.max(...schema.items.map((i) => i.valeur));
    return (
      <div style={{padding: '30px 10px'}}>
        {titre}
        {schema.items.map((it, i) => {
          const p = spring({frame: f - 8 - i * 8, fps, config: theme.ressort.doux});
          return (
            <div key={i} style={{marginBottom: 44, opacity: p}}>
              <div style={{display: 'flex', justifyContent: 'space-between', fontFamily: T.titre, fontWeight: 800, fontSize: 42,
                color: it.heros ? C.heros : C.texte, marginBottom: 14}}>
                <span>{it.label}</span>
                <span style={{fontVariantNumeric: 'tabular-nums'}}>{(it.valeur * p).toFixed(it.valeur < 1 ? 2 : 0).replace('.', ',')}{it.unite ? ` ${it.unite}` : ''}</span>
              </div>
              <div style={{height: 40, borderRadius: 20, background: 'rgba(255,255,255,0.10)'}}>
                <div style={{width: `${(it.valeur / max) * 100 * p}%`, height: 40, borderRadius: 20, background: it.heros ? C.heros : C.metalMoyen,
                  boxShadow: it.heros ? `0 0 30px ${C.lueur}` : undefined}} />
              </div>
            </div>
          );
        })}
        {source}
      </div>
    );
  }
  if (schema.type === 'chiffre') {
    const p = spring({frame: f - 4, fps, config: theme.ressort.rebond});
    return (
      <div style={{padding: '60px 10px'}}>
        {schema.legende ? <div style={{fontFamily: T.titre, fontWeight: 800, fontSize: 38, color: C.texteDim, textTransform: 'uppercase', letterSpacing: '0.1em'}}>{schema.legende}</div> : null}
        <div style={{fontFamily: T.titre, fontWeight: 900, fontSize: 170, color: C.heros, whiteSpace: 'nowrap', textShadow: `0 0 50px ${C.lueur}`,
          transform: `scale(${interpolate(p, [0, 1], [0.7, 1])})`, transformOrigin: 'left center'}}>
          {schema.prefixe ?? ''}{(schema.valeur * Math.min(1, p)).toFixed(schema.decimales ?? 0).replace('.', ',')}{schema.suffixe ?? ''}
        </div>
        {schema.comparaison ? <div style={{fontFamily: T.titre, fontWeight: 800, fontSize: 44, color: C.texte, marginTop: 10}}>{schema.comparaison}</div> : null}
        {source}
      </div>
    );
  }
  // autres schémas : version plein écran réduite
  return (
    <div style={{position: 'absolute', left: -530, top: -190, width: 1920, height: 1080, transform: 'scale(0.45)', transformOrigin: 'center center'}}>
      <SchemaAnime schema={schema} />
    </div>
  );
};
