// Rendu des "couches" décrites dans montage.json : le motion design posé SUR le rush réel.
import React from 'react';
import {AbsoluteFill, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Audio} from '@remotion/media';
import type {Couche} from '../types';
import {theme, clamp} from '../theme';
import {Annotation, Visee, Vitre, Flash} from './MixedMedia';
import {MotsQuiMontent, Etiquette, Compteur} from './Texte';

const C = theme.couleurs;
const X = (p: number) => (p / 100) * 1920;
const Y = (p: number) => (p / 100) * 1080;

const CompteurVitre: React.FC<{c: Extract<Couche, {type: 'compteur'}>}> = ({c}) => {
  const pos = c.position ?? 'droite';
  const x = pos === 'gauche' ? 120 : pos === 'centre' ? 660 : 1200;
  return (
    <Vitre x={x} y={300} l={640} h={c.source ? 420 : 300} debut={0}>
      <div style={{padding: '40px 46px', fontFamily: theme.polices.texte, color: C.texte}}>
        {c.legende ? <div style={{fontSize: 30, color: C.texteDim, letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: 14}}>{c.legende}</div> : null}
        <div style={{fontFamily: theme.polices.titre, fontWeight: 900, fontSize: 104, lineHeight: 1, whiteSpace: 'nowrap', color: C.heros, textShadow: `0 0 40px ${C.lueur}`}}>
          {c.prefixe ?? ''}<Compteur vers={c.vers} decimales={c.decimales ?? 0} debut={4} />{c.suffixe ?? ''}
        </div>
        {c.source ? <div style={{marginTop: 26, fontSize: 24, color: C.texteDim, lineHeight: 1.35}}>Source : {c.source}</div> : null}
      </div>
    </Vitre>
  );
};

const Carton: React.FC<{c: Extract<Couche, {type: 'carton'}>}> = ({c}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame: f, fps, config: theme.ressort.doux});
  return (
    <AbsoluteFill style={{background: `rgba(11,14,20,${0.55 * p})`, backdropFilter: `blur(${10 * p}px)`, justifyContent: 'center', alignItems: 'center'}}>
      <MotsQuiMontent texte={c.texte} taille={110} debut={2} style={{justifyContent: 'center', textAlign: 'center', maxWidth: 1500}} />
      {c.sous_texte ? (
        <div style={{marginTop: 30, fontFamily: theme.polices.texte, fontSize: 40, color: C.texteDim, opacity: interpolate(f, [14, 26], [0, 1], clamp)}}>{c.sous_texte}</div>
      ) : null}
    </AbsoluteFill>
  );
};

const UneCouche: React.FC<{c: Couche}> = ({c}) => {
  switch (c.type) {
    case 'annotation':
      return <Annotation x={X(c.x)} y={Y(c.y)} vers={[X(c.vers_x), Y(c.vers_y)]} texte={c.texte} debut={0} />;
    case 'visee':
      return <Visee x={X(c.x)} y={Y(c.y)} l={X(c.l)} h={Y(c.h)} debut={0} />;
    case 'compteur':
      return <CompteurVitre c={c} />;
    case 'mots': {
      const pos = c.position ?? 'centre';
      const style: React.CSSProperties =
        pos === 'gauche' ? {left: 150, top: 300, width: 1000} : pos === 'haut' ? {left: 150, top: 120, width: 1620} : {left: 160, top: 380, width: 1600};
      return (
        <AbsoluteFill>
          <div style={{position: 'absolute', ...style}}>
            <MotsQuiMontent texte={c.texte} heros={c.heros} taille={120} debut={0} style={pos === 'centre' ? {justifyContent: 'center', textAlign: 'center'} : undefined} />
          </div>
        </AbsoluteFill>
      );
    }
    case 'etiquette':
      return (
        <AbsoluteFill style={{padding: '90px 150px'}}>
          <Etiquette numero={c.numero} texte={c.texte} debut={0} />
        </AbsoluteFill>
      );
    case 'carton':
      return <Carton c={c} />;
    case 'flash':
      return <Flash a={[0]} />;
    case 'zoom_punch':
      return <Audio src={staticFile('sfx/impact.wav')} volume={0.55} />;
    case 'son':
      return <Audio src={staticFile(`sfx/${c.src}.wav`)} volume={c.volume ?? 0.7} />;
    default:
      return null;
  }
};

export const CouchesScene: React.FC<{couches: Couche[]}> = ({couches}) => {
  const {fps} = useVideoConfig();
  return (
    <>
      {couches.map((c, i) => (
        <Sequence key={i} from={Math.round((c.a ?? 0) * fps)} name={`couche ${c.type}`}>
          <UneCouche c={c} />
        </Sequence>
      ))}
    </>
  );
};
