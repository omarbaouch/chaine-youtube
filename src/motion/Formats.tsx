// Les formats de plan de la règle n°6 : écran partagé, mosaïque, schéma, carte de chapitre.
// Toujours une vraie image ET une couche animée (règle n°3) ; zone basse (y > 790) laissée aux sous-titres.
import React from 'react';
import {AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Video} from '@remotion/media';
import type {Media, Scene} from '../types';
import {theme, clamp} from '../theme';
import {FondVivant} from './Couches';
import {SchemaAnime, Bruit} from './Schemas';

const C = theme.couleurs;

// Média réel (vidéo ou photo) qui remplit son cadre, toujours en mouvement (Ken Burns).
export const MediaReel: React.FC<{m: Media; duree: number; sens?: 1 | -1; flou?: number; lumiere?: number; debut?: number; vitesse?: number}> = ({
  m, duree, sens = 1, flou = 0, lumiere = 1, debut = 0, vitesse = 1,
}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = interpolate(f, [0, Math.max(1, duree)], [0, 1], {...clamp, easing: theme.courbe.entreSortie});
  const amp = m.image ? 0.12 : 0.06;
  const s = sens === 1 ? 1.03 + amp * p : 1.03 + amp * (1 - p);
  const dx = m.image ? interpolate(p, [0, 1], [-1.6 * sens, 1.6 * sens]) : 0;
  const style: React.CSSProperties = {width: '100%', height: '100%', objectFit: 'cover',
    transform: `scale(${s}) translateX(${dx}%)`, filter: flou || lumiere !== 1 ? `blur(${flou}px) brightness(${lumiere})` : undefined};
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      {m.image ? (
        <Img src={staticFile(m.src)} style={style} />
      ) : (
        <Video src={staticFile(m.src)} muted loop objectFit="cover" trimBefore={Math.round(debut * fps)} playbackRate={vitesse} style={style} />
      )}
    </AbsoluteFill>
  );
};

const Pastille: React.FC<{texte: string; debut: number}> = ({texte, debut}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const e = spring({frame: f - debut, fps, config: theme.ressort.vif});
  return (
    <div style={{position: 'absolute', left: 22, bottom: 22, opacity: e, transform: `translateY(${interpolate(e, [0, 1], [16, 0])}px)`,
      padding: '10px 20px', borderRadius: 12, background: 'rgba(11,14,20,0.88)', borderLeft: `6px solid ${C.accent}`,
      fontFamily: theme.polices.titre, fontWeight: 800, fontSize: 36, color: C.texte, whiteSpace: 'nowrap'}}>
      {texte}
    </div>
  );
};

// Carte : le média réel entre par un volet, coins arrondis, ombre, léger flottement.
export const CarteMedia: React.FC<{m: Media; x: number; y: number; l: number; h: number; debut?: number; duree: number; sens?: 1 | -1; k?: number}> = ({
  m, x, y, l, h, debut = 0, duree, sens = 1, k = 0,
}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame: f - debut, fps, config: theme.ressort.doux});
  const volet = interpolate(f - debut, [0, 20], [100, 0], {...clamp, easing: theme.courbe.sortie});
  const flotte = Math.sin((f + k * 17) / 26) * 4;
  return (
    <div style={{position: 'absolute', left: x, top: y + flotte, width: l, height: h, borderRadius: 26, overflow: 'hidden',
      clipPath: sens === 1 ? `inset(0 ${volet}% 0 0 round 26px)` : `inset(0 0 0 ${volet}% round 26px)`,
      transform: `scale(${interpolate(p, [0, 1], [0.94, 1])})`, boxShadow: '0 50px 100px -30px rgba(0,0,0,0.8)',
      border: '1px solid rgba(255,255,255,0.12)', background: '#000'}}>
      <MediaReel m={m} duree={duree} sens={sens} />
      <AbsoluteFill style={{background: 'linear-gradient(180deg, transparent 60%, rgba(0,0,0,0.4))'}} />
      {m.legende ? <Pastille texte={m.legende} debut={debut + 14} /> : null}
    </div>
  );
};

const EtiquetteSchema: React.FC<{texte?: string}> = ({texte}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const e = spring({frame: f - 2, fps, config: theme.ressort.doux});
  if (!texte) return null;
  return (
    <div style={{position: 'absolute', left: 100, top: 60, display: 'flex', alignItems: 'center', gap: 16, opacity: e,
      transform: `translateX(${interpolate(e, [0, 1], [-24, 0])}px)`, background: 'rgba(11,14,20,0.72)', padding: '10px 20px', borderRadius: 12,
      fontFamily: theme.polices.titre, fontWeight: 800, fontSize: 34, letterSpacing: '0.12em', textTransform: 'uppercase', color: C.texte}}>
      <span style={{color: C.accent}}>Schéma</span>
      <span style={{width: 40, height: 2, background: C.accent, opacity: 0.7}} />
      <span>{texte}</span>
    </div>
  );
};

// Fond d'un plan "dessiné" : rush flouté et sombre si on en a un (on garde le lien avec le réel), sinon fond vivant.
const FondPlan: React.FC<{scene: Scene}> = ({scene}) => {
  const m = scene.media ? {src: scene.media, image: scene.type === 'image'} : scene.medias[0];
  return (
    <>
      <FondVivant />
      {m ? (
        <AbsoluteFill style={{opacity: 0.55}}>
          <MediaReel m={m} duree={scene.duree} flou={26} lumiere={0.42} debut={scene.debutMedia} />
        </AbsoluteFill>
      ) : null}
    </>
  );
};

export const PlanSchema: React.FC<{scene: Scene}> = ({scene}) => (
  <AbsoluteFill>
    <FondPlan scene={scene} />
    <EtiquetteSchema texte={scene.etiquetteSchema} />
    <AbsoluteFill style={{left: 150, right: 150, top: 150, bottom: 300, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
      {scene.schema ? <SchemaAnime s={scene.schema} l={1620} duree={scene.duree} /> : null}
    </AbsoluteFill>
  </AbsoluteFill>
);

export const PlanEcranPartage: React.FC<{scene: Scene}> = ({scene}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const m = scene.medias[0] ?? (scene.media ? {src: scene.media, image: scene.type === 'image'} : undefined);
  const gauche = (scene.cote ?? 'gauche') === 'gauche';
  const xMedia = gauche ? 80 : 1000;
  const xSchema = gauche ? 1000 : 80;
  const p = spring({frame: f - 8, fps, config: theme.ressort.doux});
  return (
    <AbsoluteFill>
      <FondVivant />
      {m ? (
        <AbsoluteFill style={{opacity: 0.35}}>
          <MediaReel m={m} duree={scene.duree} flou={30} lumiere={0.35} />
        </AbsoluteFill>
      ) : null}
      {m ? <CarteMedia m={m} x={xMedia} y={110} l={840} h={660} duree={scene.duree} sens={gauche ? 1 : -1} debut={scene.debutMedia ? 0 : 0} /> : null}
      <div style={{position: 'absolute', left: xSchema, top: 110, width: 840, height: 660, borderRadius: 26, overflow: 'hidden',
        background: 'rgba(11,14,20,0.62)', backdropFilter: 'blur(20px)', border: '1px solid rgba(255,255,255,0.12)',
        opacity: p, transform: `translateY(${interpolate(p, [0, 1], [30, 0])}px)`, display: 'flex', flexDirection: 'column', padding: '30px 50px'}}>
        <div style={{fontFamily: theme.polices.titre, fontWeight: 800, fontSize: 30, letterSpacing: '0.12em',
          textTransform: 'uppercase', color: C.accent, marginBottom: 10}}>
          {scene.etiquetteSchema ? `Schéma · ${scene.etiquetteSchema}` : 'Schéma'}
        </div>
        <div style={{flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{scene.schema ? <SchemaAnime s={scene.schema} l={740} duree={scene.duree} /> : null}</div>
      </div>
    </AbsoluteFill>
  );
};

const DISPOSITIONS: Record<number, [number, number, number, number][]> = {
  1: [[160, 100, 1600, 690]],
  2: [[80, 120, 860, 650], [980, 120, 860, 650]],
  3: [[80, 100, 1060, 690], [1170, 100, 670, 335], [1170, 455, 670, 335]],
  4: [[80, 90, 870, 345], [970, 90, 870, 345], [80, 450, 870, 345], [970, 450, 870, 345]],
};

export const PlanMosaique: React.FC<{scene: Scene}> = ({scene}) => {
  const {fps} = useVideoConfig();
  const n = Math.min(4, Math.max(1, scene.medias.length));
  const cases = DISPOSITIONS[n];
  const ecart = Math.max(8, Math.min(Math.round(fps * 1.3), Math.floor((scene.duree * 0.5) / n)));
  return (
    <AbsoluteFill>
      <FondVivant />
      {scene.medias.slice(0, 4).map((m, i) => {
        const [x, y, l, h] = cases[i];
        return <CarteMedia key={i} m={m} x={x} y={y} l={l} h={h} debut={4 + i * ecart} duree={scene.duree} sens={i % 2 ? -1 : 1} k={i} />;
      })}
      {scene.medias.slice(0, 4).map((_, i) => <Bruit key={i} nom="whoosh" a={4 + i * ecart} volume={0.18} />)}
    </AbsoluteFill>
  );
};

// Carte de chapitre : "PARTIE 01" + titre 150 px + trait orange, sur le rush flouté.
export const CarteChapitre: React.FC<{scene: Scene}> = ({scene}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const num = spring({frame: f - 2, fps, config: theme.ressort.doux});
  const barre = spring({frame: f - 10, fps, config: theme.ressort.doux});
  const sous = spring({frame: f - 18, fps, config: theme.ressort.doux});
  const sortie = interpolate(f, [scene.duree - 10, scene.duree], [1, 0], {...clamp, easing: theme.courbe.entree});
  const mots = (scene.titre ?? '').split(' ');
  return (
    <AbsoluteFill>
      <FondPlan scene={scene} />
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', opacity: sortie, transform: `scale(${1 + 0.02 * (1 - sortie)})`}}>
        {scene.numero ? (
          <div style={{fontFamily: theme.polices.titre, fontWeight: 800, fontSize: 36, letterSpacing: '0.3em', color: C.accent, marginBottom: 26,
            opacity: num, transform: `translateY(${interpolate(num, [0, 1], [20, 0])}px)`}}>
            PARTIE {scene.numero}
          </div>
        ) : null}
        <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'center', columnGap: 38, maxWidth: 1600, textAlign: 'center'}}>
          {mots.map((m, i) => {
            const p = spring({frame: f - 6 - i * 3, fps, config: theme.ressort.vif});
            return (
              <span key={i} style={{display: 'inline-block', overflow: 'hidden', paddingBottom: 12}}>
                <span style={{display: 'inline-block', fontFamily: theme.polices.titre, fontWeight: 900, fontSize: 150, lineHeight: 1.02,
                  letterSpacing: '-0.035em', textTransform: 'uppercase', color: C.texte, opacity: p,
                  transform: `translateY(${interpolate(p, [0, 1], [110, 0])}px)`, textShadow: '0 12px 40px rgba(0,0,0,.6)'}}>{m}</span>
              </span>
            );
          })}
        </div>
        <div style={{width: 260 * barre, height: 10, background: C.heros, marginTop: 30, borderRadius: 5, boxShadow: `0 0 30px ${C.lueur}`}} />
        {scene.sousTitre ? (
          <div style={{fontFamily: theme.polices.titre, fontWeight: 700, fontSize: 46, color: C.texteDim, marginTop: 30, maxWidth: 1400, textAlign: 'center',
            opacity: sous, transform: `translateY(${interpolate(sous, [0, 1], [18, 0])}px)`}}>
            {scene.sousTitre}
          </div>
        ) : null}
      </AbsoluteFill>
      <Bruit nom="whoosh" a={0} volume={0.35} />
      <Bruit nom="impact" a={8} volume={0.3} />
    </AbsoluteFill>
  );
};
