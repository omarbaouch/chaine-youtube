import React from 'react';
import {AbsoluteFill, Img, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {Audio, Video} from '@remotion/media';
import type {EpisodeProps, Scene} from './types';
import {SousTitres} from './effets/SousTitres';
import {Surtitre} from './effets/Surtitre';
import {theme} from './theme';
import {Bruit} from './motion/Schemas';
import {CarteChapitre, PlanEcranPartage, PlanMosaique, PlanSchema} from './motion/Formats';
import {CouchesScene} from './motion/Couches2';
import {BandeauTemoin} from './effets/BandeauTemoin';

const Fond: React.FC<{scene: Scene; flou?: boolean; son?: boolean}> = ({scene, flou, son}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = frame / Math.max(1, scene.duree);
  const ease = Easing.inOut(Easing.quad)(Math.min(1, p));
  // Zoom lent "Ken Burns" : donne de la vie même à un plan fixe.
  const estImg = !!scene.media && /\.(jpe?g|png|webp)$/i.test(scene.media);
  // Photos : mouvement plus ample (retour d'Omar « on s'ennuie ») — zoom marqué + panoramique en diagonale.
  const amplitude = estImg ? 0.24 : 0.08;
  const p2 = estImg ? Math.min(1, frame / Math.max(1, scene.duree)) : ease; // vitesse constante : la photo ne "s'arrête" jamais
  const scale =
    scene.zoom === 'aucun' ? 1.06 : scene.zoom === 'arriere' ? 1.04 + amplitude * (1 - p2) : 1.04 + amplitude * p2;
  const sens = scene.id.charCodeAt(scene.id.length - 1) % 2 ? 1 : -1;
  const derive = estImg ? interpolate(p2, [0, 1], [-3.5 * sens, 3.5 * sens]) : 0;
  const deriveY = estImg ? interpolate(p2, [0, 1], [1.5, -1.5]) : 0;
  const style: React.CSSProperties = {
    width: '100%',
    height: '100%',
    transform: `scale(${scale}) translate(${derive}%, ${deriveY}%)`,
    filter: flou ? 'blur(18px) brightness(0.45)' : undefined,
  };
  if (!scene.media) {
    // Fond de secours : dégradé animé (utile pour les cartes titre sans média).
    const angle = 120 + frame * 0.3;
    return <AbsoluteFill style={{background: `linear-gradient(${angle}deg, #0b0f1a, #1b2a4a 55%, #3a1c4a)`}} />;
  }
  if (estImg) {
    return <Img src={staticFile(scene.media)} style={{...style, objectFit: 'cover'}} />;
  }
  return (
    <Video
      name={`Rush ${scene.id}`}
      src={staticFile(scene.media)}
      muted={!son}
      volume={son ? (f: number) => interpolate(f, [0, 6, scene.duree - 8, scene.duree], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : undefined}
      loop={!son}
      objectFit="cover"
      playbackRate={scene.vitesse}
      trimBefore={Math.round(scene.debutMedia * fps)}
      style={style}
    />
  );
};

// Règle n°7 : emphase cinétique — zoom rapide sur le mot ou le chiffre clé, avec impact.
const usePunch = (punch: Scene['punch']) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (!punch) return 1;
  const a = Math.round(punch.a * fps);
  const monte = interpolate(f, [a, a + 4], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
  const redescend = interpolate(f, [a + 4, a + 22], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.quad)});
  return 1 + 0.13 * monte - 0.13 * redescend;
};

const MotPunch: React.FC<{texte: string; a: number}> = ({texte, a}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const debut = Math.round(a * fps);
  const p = spring({frame: f - debut, fps, config: theme.ressort.rebond});
  if (f < debut) return null;
  const sortie = interpolate(f, [debut + fps * 1.4, debut + fps * 1.8], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: theme.courbe.entree});
  if (sortie <= 0) return null;
  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 300, opacity: sortie}}>
      <div style={{fontFamily: theme.polices.titre, fontWeight: 900, fontSize: 130, color: theme.couleurs.heros, textTransform: 'uppercase',
        letterSpacing: '-0.03em', background: 'rgba(11,14,20,0.78)', padding: '6px 40px', borderRadius: 24, whiteSpace: 'nowrap',
        boxShadow: `0 0 60px ${theme.couleurs.lueur}`, opacity: interpolate(p, [0, 0.3], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
        transform: `scale(${interpolate(p, [0, 1], [1.6, 1])}) rotate(-2deg)`}}>
        {texte}
      </div>
    </AbsoluteFill>
  );
};

const Contenu: React.FC<{scene: Scene; filtre: string}> = ({scene, filtre}) => {
  switch (scene.format) {
    case 'titre':
      return <CarteChapitre scene={scene} />;
    case 'schema':
      return <PlanSchema scene={scene} />;
    case 'ecran_partage':
      return <PlanEcranPartage scene={scene} />;
    case 'mosaique':
      return <PlanMosaique scene={scene} />;
    case 'temoignage':
      // une vraie personne parle : son d'origine, image à peine zoomée (pas de Ken Burns marqué sur un visage)
      return (
        <AbsoluteFill style={{filter: filtre}}>
          <Fond scene={{...scene, zoom: 'aucun'}} son />
        </AbsoluteFill>
      );
    default:
      return (
        <>
          <AbsoluteFill style={{filter: filtre}}>
            <Fond scene={scene} />
          </AbsoluteFill>
          <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,.5) 100%)'}} />
        </>
      );
  }
};

export const ScenePlan: React.FC<{scene: Scene; etalonnage: EpisodeProps['etalonnage']}> = ({scene, etalonnage}) => {
  const {fps} = useVideoConfig();
  const filtreBase = `contrast(${etalonnage.contraste}) saturate(${etalonnage.saturation}) brightness(${etalonnage.luminosite})`;
  const filtre = scene.look === 'bijou'
    ? `${filtreBase} contrast(1.14) saturate(1.08) brightness(0.93) sepia(0.16)`
    : scene.look === 'champ'
      ? `${filtreBase} saturate(0.62) contrast(1.06) brightness(0.97) hue-rotate(-6deg)`
      : filtreBase;
  const zoomPunch = usePunch(scene.punch);
  return (
    <AbsoluteFill style={{backgroundColor: '#000', overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${zoomPunch})`}}>
        <Contenu scene={scene} filtre={filtre} />
        {scene.couches?.length ? <CouchesScene couches={scene.couches} /> : null}
      </AbsoluteFill>
      {scene.look === 'champ' ? <AbsoluteFill style={{background: 'rgba(40,80,130,0.13)', mixBlendMode: 'soft-light', pointerEvents: 'none'}} /> : null}
      {scene.look === 'bijou' ? (
        <>
          <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 45%, rgba(0,0,0,.55) 100%)', pointerEvents: 'none'}} />
          {/* bandes cinéma 2,39:1 : image utile 1920 × 803 */}
          <AbsoluteFill style={{pointerEvents: 'none'}}>
            <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 138, background: '#000'}} />
            <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: 138, background: '#000'}} />
          </AbsoluteFill>
        </>
      ) : null}
      {/* dégradé bas pour la lisibilité des sous-titres */}
      <AbsoluteFill style={{background: 'linear-gradient(to bottom, transparent 62%, rgba(0,0,0,.6) 100%)', pointerEvents: 'none'}} />
      {scene.surtitre ? <Surtitre texte={scene.surtitre} /> : null}
      {scene.temoin ? <BandeauTemoin temoin={scene.temoin} /> : null}
      {scene.punch?.texte ? <MotPunch texte={scene.punch.texte} a={scene.punch.a} /> : null}
      {scene.punch ? <Bruit nom="impact" a={Math.round(scene.punch.a * fps) - 1} volume={0.5} /> : null}
      {scene.sons.map((s, i) => <Bruit key={i} nom={s.nom} a={Math.round(s.a * fps)} volume={s.volume ?? 0.45} />)}
      {scene.voix ? (
        <Sequence from={scene.voixDebut} name="Voix" layout="none">
          <Audio src={staticFile(scene.voix)} />
        </Sequence>
      ) : null}
      {scene.sousTitres.length ? (
        <Sequence from={scene.voixDebut} name="Sous-titres">
          <SousTitres lignes={scene.sousTitres} sceptique={scene.qui === 'sceptique'} />
        </Sequence>
      ) : null}
    </AbsoluteFill>
  );
};
