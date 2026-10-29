// Scène test (15 s) : "Comment naît une canette" — vraies vidéos d'usine FUSIONNÉES avec le motion design.
// Rushes attendus dans public/ep/test-canette/media/m1..m5.mp4 (téléchargés par le robot GitHub).
import React from 'react';
import {AbsoluteFill, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Audio} from '@remotion/media';
import {evolvePath, interpolatePath, scalePath} from '@remotion/paths';
import {theme, clamp} from '../theme';
import {Etalonnage, Grain, Vignette} from '../motion/Couches';
import {MotsQuiMontent, Etiquette, Compteur, useSortie} from '../motion/Texte';
import {Rush, CarteVideo, Annotation, Visee, Vitre, Flash} from '../motion/MixedMedia';

const C = theme.couleurs;
const M = (id: string) => staticFile(`ep/test-canette/media/${id}.mp4`);

// ---------- Formes de la canette (même structure de commandes → morphing propre) ----------
const profil = (lh: number, lb: number, haut: number, bas: number, col = 0) => {
  const cx = 200, r = Math.min(26, (bas - haut) / 3);
  return [
    `M ${cx - lh} ${haut}`,
    `C ${cx - lh} ${haut + col * 0.3} ${cx - lb} ${haut + col * 0.6} ${cx - lb} ${haut + col}`,
    `L ${cx - lb} ${bas - r}`,
    `C ${cx - lb} ${bas} ${cx - lb + r} ${bas + 6} ${cx} ${bas + 6}`,
    `C ${cx + lb - r} ${bas + 6} ${cx + lb} ${bas} ${cx + lb} ${bas - r}`,
    `L ${cx + lb} ${haut + col}`,
    `C ${cx + lb} ${haut + col * 0.6} ${cx + lh} ${haut + col * 0.3} ${cx + lh} ${haut}`,
    'Z',
  ].join(' ');
};
const DISQUE = profil(165, 165, 500, 512, 0);
const GOBELET = profil(118, 118, 360, 530, 0);
const CANETTE = profil(80, 98, 40, 530, 48);
const ECHELLE = 1.3; // la forme 400×600 est affichée en 520×780

// Une canette-FENÊTRE : sa silhouette découpe un vrai rush d'usine, contour métallique dessiné par-dessus.
const FenetreCanette: React.FC<{src: string; trace: number; ouverture: number; d?: string}> = ({src, trace, ouverture, d = CANETTE}) => {
  const f = useCurrentFrame();
  const chemin = scalePath(d, ECHELLE, ECHELLE);
  const ev = evolvePath(trace, chemin);
  const reflet = interpolate(f % 120, [0, 120], [-0.6, 1.4]);
  return (
    <div style={{position: 'relative', width: 520, height: 780}}>
      <div style={{position: 'absolute', inset: 0, clipPath: `path('${chemin}')`, opacity: ouverture}}>
        <Rush src={src} zoom={[1.25, 1.1]} />
        {/* reflet métallique qui balaie la vidéo : on lit à la fois "canette" et "usine" */}
        <div style={{position: 'absolute', inset: 0, mixBlendMode: 'screen',
          background: `linear-gradient(90deg, rgba(0,0,0,0.55) 0%, transparent 25%, rgba(255,255,255,0.0) ${reflet * 100 - 8}%, rgba(255,255,255,0.35) ${reflet * 100}%, rgba(255,255,255,0) ${reflet * 100 + 8}%, transparent 75%, rgba(0,0,0,0.6) 100%)`}} />
      </div>
      <svg width={520} height={790} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
        <path d={chemin} fill="none" stroke={C.metalClair} strokeWidth={4} strokeDasharray={ev.strokeDasharray} strokeDashoffset={ev.strokeDashoffset}
          style={{filter: `drop-shadow(0 0 14px ${C.accent}88)`}} />
      </svg>
    </div>
  );
};

// ---------- Plan 1 : l'accroche ----------
const Accroche: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const trace = interpolate(f, [4, 40], [0, 1], {...clamp, easing: theme.courbe.entreSortie});
  const ouverture = interpolate(f, [24, 44], [0, 1], {...clamp, easing: theme.courbe.sortie});
  const entree = spring({frame: f - 4, fps, config: theme.ressort.doux});
  const sortie = useSortie(100);
  return (
    <AbsoluteFill style={sortie}>
      <Rush src={M('m1')} flou={16} lumiere={0.32} zoom={[1.2, 1.1]} duree={100} />
      <AbsoluteFill style={{background: `linear-gradient(90deg, ${C.fond}EE 0%, ${C.fond}99 45%, transparent 75%)`}} />
      <div style={{position: 'absolute', left: 150, top: 300, width: 900}}>
        <MotsQuiMontent texte="Une canette" debut={4} taille={170} heros="canette" />
        <div style={{marginTop: 34}}>
          <MotsQuiMontent texte="naît en moins d'une seconde." debut={24} ecart={2} taille={56}
            style={{fontFamily: theme.polices.texte, fontWeight: 500, letterSpacing: '-0.01em', color: C.texteDim}} />
        </div>
      </div>
      <div style={{position: 'absolute', right: 230, top: 140 + Math.sin(f / 18) * 6,
        transform: `rotate(${interpolate(entree, [0, 1], [-8, 4])}deg) scale(${interpolate(entree, [0, 1], [0.9, 1])})`}}>
        <FenetreCanette src={M('m1')} trace={trace} ouverture={ouverture} />
      </div>
    </AbsoluteFill>
  );
};

// ---------- Plan 2 : la bobine (rush réel en carte + annotations + schéma) ----------
const Bobine: React.FC = () => {
  const f = useCurrentFrame();
  const sortie = useSortie(95);
  return (
    <AbsoluteFill style={sortie}>
      <Rush src={M('m2')} flou={22} lumiere={0.22} duree={95} />
      <div style={{position: 'absolute', left: 150, top: 250, width: 700}}>
        <Etiquette numero="01" texte="LA BOBINE" debut={2} />
        <div style={{height: 34}} />
        <MotsQuiMontent texte="Tout commence par une bobine d'aluminium" debut={8} taille={92} heros="aluminium" />
      </div>
      <CarteVideo src={M('m2')} x={930} y={170} l={860} h={640} debut={4} />
      <Annotation x={1330} y={520} vers={[1460, 300]} debut={30}
        texte={<span>épaisseur ≈ <Compteur vers={0.3} decimales={2} debut={44} suffixe=" mm" style={{color: C.heros}} /></span>} />
      {/* mini-schéma de bobine dans un panneau vitré, posé sur la vidéo */}
      <Vitre x={860} y={700} l={230} h={230} debut={40} rayon={115}>
        <svg viewBox="-120 -120 240 240" style={{width: '100%', height: '100%'}}>
          <g transform={`rotate(${f * 3})`}>
            {Array.from({length: 12}).map((_, i) => (
              <circle key={i} r={86 - i * 6} fill="none" stroke={i % 2 ? C.metalMoyen : C.metalClair} strokeWidth={2.5} opacity={0.4 + 0.5 * (1 - i / 12)} />
            ))}
          </g>
          <line x1={0} y1={-86} x2={120} y2={-86} stroke={C.metalClair} strokeWidth={4} />
        </svg>
      </Vitre>
    </AbsoluteFill>
  );
};

// ---------- Plan 3 : la découpe (rush plein écran + HUD + schéma synchronisé) ----------
const COUPS = [16, 38, 60];
const Decoupe: React.FC = () => {
  const f = useCurrentFrame();
  const sortie = useSortie(95);
  const choc = COUPS.reduce((m, c) => Math.max(m, interpolate(f, [c, c + 2, c + 10], [0, 1, 0], clamp)), 0);
  const secousse = choc * 7 * Math.sin(f * 3.1);
  const descente = COUPS.reduce((m, c) => Math.max(m, interpolate(f, [c - 6, c, c + 8], [0, 1, 0], {...clamp, easing: theme.courbe.choc})), 0);
  const nb = COUPS.filter((c) => f >= c).length;
  return (
    <AbsoluteFill style={sortie}>
      <AbsoluteFill style={{transform: `translate(${secousse}px, ${secousse * 0.6}px)`}}>
        <Rush src={M('m3')} lumiere={0.85} zoom={[1.08, 1.2]} duree={95} />
      </AbsoluteFill>
      <AbsoluteFill style={{background: `linear-gradient(90deg, ${C.fond}F2 0%, ${C.fond}AA 38%, transparent 62%)`}} />
      <Flash a={COUPS} />
      <Visee x={1120} y={330} l={460} h={380} debut={6} choc={choc} />
      <div style={{position: 'absolute', left: 150, top: 250, width: 700}}>
        <Etiquette numero="02" texte="LA DÉCOUPE" debut={2} />
        <div style={{height: 34}} />
        <MotsQuiMontent texte="Découpée en disques, à la chaîne" debut={8} taille={92} heros="disques" />
        <div style={{marginTop: 44, fontFamily: theme.polices.texte, fontSize: 36, color: C.texteDim}}>
          disques découpés : <span style={{color: C.texte, fontWeight: 700, fontSize: 52, fontVariantNumeric: 'tabular-nums',
            display: 'inline-block', transform: `scale(${1 + 0.25 * choc})`}}>{nb}</span>
        </div>
      </div>
      {/* schéma du poinçon, synchronisé avec les coups visibles dans la vidéo */}
      <Vitre x={1380} y={760} l={420} h={230} debut={20}>
        <svg viewBox="0 0 420 230" style={{width: '100%', height: '100%'}}>
          <rect x={30} y={160} width={360} height={26} fill={C.metalMoyen} />
          <g transform={`translate(210 ${interpolate(descente, [0, 1], [40, 150])})`}>
            <rect x={-14} y={-200} width={28} height={200} fill={C.metalSombre} />
            <rect x={-50} y={-14} width={100} height={14} rx={4} fill={C.heros} />
          </g>
          <text x={20} y={40} fill={C.texteDim} style={{fontFamily: theme.polices.texte, fontSize: 18, letterSpacing: 3}}>SCHÉMA · POINÇON</text>
        </svg>
      </Vitre>
    </AbsoluteFill>
  );
};

// ---------- Plan 4 : formage, puis la forme dessinée "s'ouvre" sur la vraie chaîne ----------
const Formage: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const emb = interpolate(f, [6, 22], [0, 1], {...clamp, easing: theme.courbe.choc});
  const eti = interpolate(f, [34, 54], [0, 1], {...clamp, easing: theme.courbe.entreSortie});
  const d = eti > 0 ? interpolatePath(eti, GOBELET, CANETTE) : interpolatePath(emb, DISQUE, GOBELET);
  const ouverture = interpolate(f, [54, 64], [0, 1], {...clamp, easing: theme.courbe.sortie});
  // raccord : la canette remplit tout l'écran et devient la vidéo du plan suivant
  const plonge = interpolate(f, [66, 85], [1, 9], {...clamp, easing: theme.courbe.entree});
  const entree = spring({frame: f, fps, config: theme.ressort.doux});
  const texteOut = interpolate(f, [62, 72], [1, 0], clamp);
  return (
    <AbsoluteFill>
      <Rush src={M('m4')} flou={18} lumiere={0.25} duree={85} />
      <div style={{position: 'absolute', left: 150, top: 250, width: 700, opacity: texteOut}}>
        <Etiquette numero="03" texte="LE FORMAGE" debut={2} />
        <div style={{height: 34}} />
        <MotsQuiMontent texte={eti > 0.02 ? 'Puis étirée vers le haut' : 'Emboutie en gobelet'} debut={eti > 0.02 ? 32 : 6} taille={92}
          heros={eti > 0.02 ? 'étirée' : 'gobelet'} key={eti > 0.02 ? 'b' : 'a'} />
      </div>
      <div style={{position: 'absolute', left: 1100, top: 150, opacity: entree,
        transform: `scale(${interpolate(entree, [0, 1], [0.85, 1]) * plonge})`, transformOrigin: '260px 520px'}}>
        <div style={{position: 'relative', width: 520, height: 780}}>
          {/* corps métallique dessiné (disque → gobelet → canette) */}
          <svg width={520} height={790} style={{position: 'absolute', inset: 0, overflow: 'visible', opacity: 1 - ouverture}}>
            <defs>
              <linearGradient id="metal4" x1="0" x2="1">
                <stop offset="0" stopColor={C.metalSombre} /><stop offset="0.3" stopColor={C.metalClair} />
                <stop offset="0.55" stopColor={C.metalMoyen} /><stop offset="1" stopColor="#252B36" />
              </linearGradient>
            </defs>
            <path d={scalePath(d, ECHELLE, ECHELLE)} fill="url(#metal4)" stroke={C.metalClair} strokeWidth={3} />
          </svg>
          {/* ...qui s'ouvre sur la vraie chaîne de production */}
          {ouverture > 0 ? <AbsoluteFill><FenetreCanette src={M('m4')} trace={1} ouverture={ouverture} /></AbsoluteFill> : null}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------- Plan 5 : le résultat (vraie vidéo + chiffres en panneaux vitrés) ----------
const Resultat: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const b1 = spring({frame: f - 16, fps, config: theme.ressort.doux});
  const b2 = spring({frame: f - 24, fps, config: theme.ressort.doux});
  const anneau = interpolate(f, [26, 56], [0, 1], {...clamp, easing: theme.courbe.entreSortie});
  const ev = evolvePath(anneau, 'M 0 -120 A 120 120 0 1 1 -0.1 -120');
  const fin = interpolate(f, [66, 75], [1, 0], {...clamp, easing: theme.courbe.entree});
  const barre = (p: number, l: number, coul: string, titre: string, v: number) => (
    <div style={{marginBottom: 34, opacity: p}}>
      <div style={{display: 'flex', justifyContent: 'space-between', fontFamily: theme.polices.texte, fontSize: 30, color: C.texteDim, marginBottom: 12}}>
        <span>{titre}</span><span style={{color: C.texte, fontWeight: 600}}>≈ <Compteur vers={v} decimales={2} debut={16} suffixe=" mm" /></span>
      </div>
      <div style={{height: 22, borderRadius: 11, background: 'rgba(255,255,255,0.08)'}}>
        <div style={{width: `${l * p}%`, height: 22, borderRadius: 11, background: coul, boxShadow: coul === C.heros ? `0 0 26px ${C.lueur}` : undefined}} />
      </div>
    </div>
  );
  return (
    <AbsoluteFill style={{opacity: fin}}>
      <Rush src={M('m4')} lumiere={0.7} zoom={[1.0, 1.1]} duree={75} />
      <AbsoluteFill style={{background: `linear-gradient(90deg, ${C.fond}E6 0%, ${C.fond}88 50%, transparent 80%)`}} />
      <div style={{position: 'absolute', left: 150, top: 190, width: 900}}>
        <Etiquette numero="→" texte="RÉSULTAT" debut={0} />
        <div style={{height: 30}} />
        <MotsQuiMontent texte="Une paroi fine comme un cheveu" debut={4} taille={92} heros="cheveu" />
      </div>
      <Vitre x={150} y={640} l={760} h={280} debut={12}>
        <div style={{padding: '40px 44px'}}>
          {barre(b1, 100, C.heros, 'Paroi de la canette', 0.1)}
          {barre(b2, 70, C.metalMoyen, 'Cheveu humain', 0.07)}
        </div>
      </Vitre>
      <Vitre x={1330} y={380} l={330} h={330} debut={20} rayon={165}>
        <svg viewBox="-165 -165 330 330" style={{width: '100%', height: '100%'}}>
          <circle r={120} fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth={12} />
          <path d="M 0 -120 A 120 120 0 1 1 -0.1 -120" fill="none" stroke={C.accent} strokeWidth={12} strokeLinecap="round"
            strokeDasharray={ev.strokeDasharray} strokeDashoffset={ev.strokeDashoffset} />
          <text textAnchor="middle" y={26} fill={C.texte} opacity={anneau} style={{fontFamily: theme.polices.titre, fontWeight: 900, fontSize: 74}}>&lt; 1 s</text>
        </svg>
      </Vitre>
    </AbsoluteFill>
  );
};

// ---------- Assemblage + son ----------
const Son: React.FC<{src: string; a: number; volume?: number}> = ({src, a, volume = 0.8}) => (
  <Sequence from={a} layout="none" name={src}>
    <Audio src={staticFile(`sfx/${src}.wav`)} volume={volume} />
  </Sequence>
);

export const TestCanette: React.FC = () => (
  <AbsoluteFill style={{background: C.fond}}>
    <Sequence from={0} durationInFrames={100} name="1 Accroche"><Accroche /></Sequence>
    <Sequence from={100} durationInFrames={95} name="2 Bobine"><Bobine /></Sequence>
    <Sequence from={195} durationInFrames={95} name="3 Découpe"><Decoupe /></Sequence>
    <Sequence from={290} durationInFrames={85} name="4 Formage"><Formage /></Sequence>
    <Sequence from={375} durationInFrames={75} name="5 Résultat"><Resultat /></Sequence>
    <Etalonnage />
    <Grain />
    <Vignette />
    <Audio src={staticFile('sfx/nappe.wav')} volume={(f) => interpolate(f, [0, 20, 420, 450], [0, 0.5, 0.5, 0], clamp)} />
    <Son src="impact" a={2} volume={0.7} />
    <Son src="whoosh" a={98} />
    <Son src="pop" a={100 + 28} volume={0.4} />
    <Son src="whoosh" a={193} />
    {COUPS.map((c) => <Son key={c} src="metal" a={195 + c - 2} volume={0.65} />)}
    <Son src="whoosh" a={288} />
    <Son src="impact" a={290 + 20} volume={0.8} />
    <Son src="whoosh" a={290 + 34} volume={0.7} />
    <Son src="riser" a={290 + 40} volume={0.55} />
    <Son src="impact" a={373} volume={0.7} />
    {[0, 6, 12, 18, 24].map((k) => <Son key={k} src="tick" a={375 + 28 + k} volume={0.35} />)}
  </AbsoluteFill>
);
