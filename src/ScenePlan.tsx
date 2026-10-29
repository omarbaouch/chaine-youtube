import React from 'react';
import {AbsoluteFill, Img, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {Audio, Video} from '@remotion/media';
import type {EpisodeProps, Scene} from './types';
import {SousTitres} from './effets/SousTitres';
import {Surtitre} from './effets/Surtitre';
import {POLICE} from './police';

const Fond: React.FC<{scene: Scene; flou?: boolean}> = ({scene, flou}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = frame / Math.max(1, scene.duree);
  const ease = Easing.inOut(Easing.quad)(Math.min(1, p));
  // Zoom lent "Ken Burns" : donne de la vie même à un plan fixe.
  const amplitude = scene.type === 'image' ? 0.14 : 0.07;
  const scale =
    scene.zoom === 'aucun' ? 1.02 : scene.zoom === 'arriere' ? 1 + amplitude * (1 - ease) + 0.02 : 1.02 + amplitude * ease;
  const derive = scene.type === 'image' ? interpolate(ease, [0, 1], [-1.5, 1.5]) : 0;
  const style: React.CSSProperties = {
    width: '100%',
    height: '100%',
    transform: `scale(${scale}) translateX(${derive}%)`,
    filter: flou ? 'blur(18px) brightness(0.45)' : undefined,
  };
  if (!scene.media) {
    // Fond de secours : dégradé animé (utile pour les cartes titre sans média).
    const angle = 120 + frame * 0.3;
    return <AbsoluteFill style={{background: `linear-gradient(${angle}deg, #0b0f1a, #1b2a4a 55%, #3a1c4a)`}} />;
  }
  if (scene.type === 'image') {
    return <Img src={staticFile(scene.media)} style={{...style, objectFit: 'cover'}} />;
  }
  return (
    <Video
      name={`Rush ${scene.id}`}
      src={staticFile(scene.media)}
      muted
      loop
      objectFit="cover"
      playbackRate={scene.vitesse}
      trimBefore={Math.round(scene.debutMedia * fps)}
      style={style}
    />
  );
};

const CarteTitre: React.FC<{scene: Scene}> = ({scene}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const entree = spring({frame, fps, config: {damping: 200}, durationInFrames: 25});
  const sortie = interpolate(frame, [scene.duree - 12, scene.duree], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const barre = spring({frame: frame - 8, fps, config: {damping: 200}, durationInFrames: 20});
  const sous = spring({frame: frame - 14, fps, config: {damping: 200}, durationInFrames: 22});
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', opacity: sortie, fontFamily: POLICE}}>
      <div
        style={{
          color: 'white',
          fontSize: 120,
          fontWeight: 900,
          letterSpacing: interpolate(entree, [0, 1], [24, -2]),
          textTransform: 'uppercase',
          textAlign: 'center',
          lineHeight: 1.02,
          maxWidth: '85%',
          opacity: entree,
          transform: `translateY(${interpolate(entree, [0, 1], [30, 0])}px)`,
          textShadow: '0 10px 40px rgba(0,0,0,.55)',
        }}
      >
        {scene.titre}
      </div>
      <div style={{width: 220 * barre, height: 8, background: '#FFD400', marginTop: 28, borderRadius: 4}} />
      {scene.sousTitre ? (
        <div
          style={{
            color: 'rgba(255,255,255,.88)',
            fontSize: 46,
            fontWeight: 600,
            marginTop: 26,
            opacity: sous,
            transform: `translateY(${interpolate(sous, [0, 1], [20, 0])}px)`,
            textAlign: 'center',
            maxWidth: '75%',
          }}
        >
          {scene.sousTitre}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

export const ScenePlan: React.FC<{scene: Scene; etalonnage: EpisodeProps['etalonnage']}> = ({scene, etalonnage}) => {
  const filtre = `contrast(${etalonnage.contraste}) saturate(${etalonnage.saturation}) brightness(${etalonnage.luminosite})`;
  return (
    <AbsoluteFill style={{backgroundColor: '#000', overflow: 'hidden'}}>
      {/* Couche image : même étalonnage sur tous les rushes pour un rendu homogène "film". */}
      <AbsoluteFill style={{filter: filtre}}>
        <Fond scene={scene} flou={scene.type === 'titre'} />
      </AbsoluteFill>
      {/* Vignettage + dégradé bas pour la lisibilité des sous-titres */}
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,.55) 100%)'}} />
      <AbsoluteFill style={{background: 'linear-gradient(to bottom, transparent 55%, rgba(0,0,0,.65) 100%)'}} />
      {scene.type === 'titre' ? <CarteTitre scene={scene} /> : null}
      {scene.surtitre ? <Surtitre texte={scene.surtitre} /> : null}
      {scene.voix ? (
        <Sequence from={scene.voixDebut} name="Voix" layout="none">
          <Audio src={staticFile(scene.voix)} />
        </Sequence>
      ) : null}
      {scene.sousTitres.length ? (
        <Sequence from={scene.voixDebut} name="Sous-titres">
          <SousTitres lignes={scene.sousTitres} />
        </Sequence>
      ) : null}
    </AbsoluteFill>
  );
};
