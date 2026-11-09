// Short 100 % animation SVG : « Ta facture d'électricité de 100 € : où va l'argent ? »
// Tout est piloté par le minutage mot à mot de la voix (public/anim/<slug>-mots.json).
import React from 'react';
import {
  AbsoluteFill, Audio, Easing, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, random,
} from 'remotion';
import '@fontsource/montserrat/700.css';
import '@fontsource/montserrat/800.css';
import '@fontsource/montserrat/900.css';

export type Mot = {texte: string; debut: number; fin: number};
export type AnimProps = {slug: string; mots: Mot[]; duree: number};

const C = {
  fond: '#070A12', fond2: '#0F1626', bleu: '#3DA9FF', cyan: '#7FE7FF', orange: '#FF6B2C', jaune: '#FFD23F',
  rouge: '#FF3B4E', vert: '#3BE38B', blanc: '#F4F6FA', gris: '#8A94A6', billet1: '#1E7A5A', billet2: '#2FBF86',
};
const F = "'Montserrat', sans-serif";
const sortie = Easing.bezier(0.16, 1, 0.3, 1);
const W = 1080;

const norm = (s: string) => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]/g, '');

// ---------- outils de minutage ----------
const useTemps = (mots: Mot[], fps: number) => {
  // frame du n-ième mot qui commence par `debut` (après la frame `apres`)
  return (debut: string, apres = 0): number => {
    const k = norm(debut);
    for (const m of mots) {
      const f = Math.round(m.debut * fps);
      if (f >= apres && norm(m.texte).startsWith(k)) return f;
    }
    return apres;
  };
};

const pop = (frame: number, a: number, fps: number, raideur = 180) =>
  spring({frame: frame - a, fps, config: {damping: 12, stiffness: raideur, mass: 0.6}});
const entre = (frame: number, a: number, d = 12) =>
  interpolate(frame, [a, a + d], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: sortie});

// ---------- fond vivant : grille électrique + particules ----------
const Fond: React.FC = () => {
  const f = useCurrentFrame();
  const lignes = [];
  for (let i = 0; i < 14; i++) {
    const y = ((i * 160 + f * 2) % 2240) - 160;
    lignes.push(<line key={'h' + i} x1={0} x2={W} y1={y} y2={y} stroke={C.bleu} strokeOpacity={0.06} strokeWidth={2} />);
  }
  for (let i = 0; i < 8; i++) {
    lignes.push(<line key={'v' + i} x1={i * 160 - 20} x2={i * 160 - 20} y1={0} y2={1920} stroke={C.bleu} strokeOpacity={0.05} strokeWidth={2} />);
  }
  const parts = new Array(40).fill(0).map((_, i) => {
    const x = random('x' + i) * W;
    const y = (random('y' + i) * 1920 - f * (1 + random('v' + i) * 3) + 4000) % 1920;
    const r = 1.5 + random('r' + i) * 3;
    return <circle key={i} cx={x} cy={y} r={r} fill={C.cyan} opacity={0.15 + 0.35 * random('o' + i)} />;
  });
  return (
    <AbsoluteFill>
      <svg width={W} height={1920}>
        <defs>
          <radialGradient id="halo" cx="50%" cy="42%" r="70%">
            <stop offset="0%" stopColor="#14284A" />
            <stop offset="100%" stopColor={C.fond} />
          </radialGradient>
        </defs>
        <rect width={W} height={1920} fill="url(#halo)" />
        {lignes}
        {parts}
      </svg>
    </AbsoluteFill>
  );
};

// ---------- éclair ----------
const Eclair: React.FC<{a: number; x: number; y: number; h?: number; seed?: string}> = ({a, x, y, h = 700, seed = 'e'}) => {
  const f = useCurrentFrame();
  const t = f - a;
  if (t < 0 || t > 10) return null;
  let p = `M ${x + (random(seed + 'x0') - 0.5) * 200} ${y - h}`;
  const n = 9;
  for (let i = 1; i <= n; i++) {
    const xx = x + (random(seed + i) - 0.5) * (i === n ? 0 : 140);
    p += ` L ${xx} ${y - h + (h * i) / n}`;
  }
  const o = interpolate(t, [0, 2, 10], [1, 1, 0]);
  return (
    <svg width={W} height={1920} style={{position: 'absolute'}}>
      <path d={p} stroke={C.cyan} strokeWidth={22} fill="none" opacity={o * 0.35} style={{filter: 'blur(10px)'}} />
      <path d={p} stroke="#fff" strokeWidth={7} fill="none" opacity={o} strokeLinejoin="round" />
    </svg>
  );
};

const Flash: React.FC<{a: number; couleur?: string}> = ({a, couleur = '#fff'}) => {
  const f = useCurrentFrame();
  const o = interpolate(f - a, [0, 1, 7], [0, 0.55, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <AbsoluteFill style={{background: couleur, opacity: o}} />;
};

// ---------- billet stylisé (dessin original) en 3 morceaux ----------
// parts (en % de la largeur) : courant 39 | taxes 33 | réseau 28
const PARTS = [
  {id: 'courant', w: 0.39},
  {id: 'taxes', w: 0.33},
  {id: 'reseau', w: 0.28},
];
const BW = 900, BH = 430;

export type Expression = {ouvert: number; regard: number; bouche: 'sourire' | 'o' | 'grimace' | 'triste'; sourcils: number; goutte: number; cligne: number};

const Visage: React.FC<{e: Expression}> = ({e}) => {
  const ex1 = BW * 0.12, ex2 = BW * 0.28, ey = 175, mx = BW * 0.2, my = 285;
  const ry = 34 * e.ouvert * (1 - e.cligne);
  const oeil = (x: number) => (
    <g key={x}>
      <ellipse cx={x} cy={ey} rx={30 * Math.max(0.8, e.ouvert * 0.9)} ry={Math.max(3, ry)} fill="#fff" stroke="#0E3B2C" strokeWidth={5} />
      {ry > 6 && <circle cx={x + e.regard * 12} cy={ey + 4} r={13} fill="#0B1A14" />}
      {ry > 6 && <circle cx={x + e.regard * 12 - 4} cy={ey - 2} r={4} fill="#fff" />}
      <path d={`M ${x - 32} ${ey - 52 + (x < mx ? e.sourcils : -e.sourcils) * 10} L ${x + 32} ${ey - 52 - (x < mx ? e.sourcils : -e.sourcils) * 10}`}
        stroke="#0E3B2C" strokeWidth={9} strokeLinecap="round" />
    </g>
  );
  const bouche = {
    sourire: `M ${mx - 55} ${my - 10} Q ${mx} ${my + 45} ${mx + 55} ${my - 10}`,
    o: `M ${mx - 18} ${my} a 18 24 0 1 0 36 0 a 18 24 0 1 0 -36 0`,
    grimace: `M ${mx - 55} ${my} L ${mx - 33} ${my - 14} L ${mx - 11} ${my + 6} L ${mx + 11} ${my - 14} L ${mx + 33} ${my + 6} L ${mx + 55} ${my - 8}`,
    triste: `M ${mx - 50} ${my + 22} Q ${mx} ${my - 28} ${mx + 50} ${my + 22}`,
  }[e.bouche];
  return (
    <g>
      {oeil(ex1)}{oeil(ex2)}
      <path d={bouche} stroke="#0E3B2C" strokeWidth={10} fill={e.bouche === 'o' ? '#0E3B2C' : 'none'} strokeLinecap="round" strokeLinejoin="round" />
      {e.goutte > 0 && <path d={`M ${ex2 + 55} ${ey - 30 + e.goutte * 40} q -16 26 0 34 q 16 -8 0 -34 Z`} fill={C.cyan} opacity={e.goutte} />}
      <circle cx={ex1 - 30} cy={my - 20} r={18} fill="#FF8FA3" opacity={0.35} />
      <circle cx={ex2 + 30} cy={my - 20} r={18} fill="#FF8FA3" opacity={0.35} />
    </g>
  );
};

const MorceauBillet: React.FC<{x0: number; w: number; e: Expression}> = ({x0, w, e}) => {
  const id = 'clip' + Math.round(x0 * 1000);
  return (
    <svg width={BW * w} height={BH} viewBox={`${x0 * BW} 0 ${BW * w} ${BH}`} style={{overflow: 'visible'}}>
      <defs>
        <clipPath id={id}><rect x={x0 * BW} y={0} width={BW * w} height={BH} /></clipPath>
        <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor={C.billet2} />
          <stop offset="100%" stopColor={C.billet1} />
        </linearGradient>
      </defs>
      <g clipPath={`url(#${id})`}>
        <rect x={0} y={0} width={BW} height={BH} rx={28} fill="url(#bg)" stroke="#0E3B2C" strokeWidth={6} />
        {new Array(18).fill(0).map((_, i) => (
          <circle key={i} cx={BW * 0.62} cy={BH / 2} r={30 + i * 22} fill="none" stroke="#fff" strokeOpacity={0.07} strokeWidth={3} />
        ))}
        <rect x={22} y={22} width={BW - 44} height={BH - 44} rx={18} fill="none" stroke="#fff" strokeOpacity={0.35} strokeWidth={3} strokeDasharray="10 8" />
        <text x={BW * 0.42} y={150} fontFamily={F} fontWeight={900} fontSize={120} fill="#fff">100</text>
        <text x={BW * 0.42 + 6} y={210} fontFamily={F} fontWeight={800} fontSize={42} fill="#E9FFF4" letterSpacing={8}>EUROS</text>
        <text x={BW - 70} y={BH - 60} fontFamily={F} fontWeight={900} fontSize={150} fill="#fff" fillOpacity={0.9} textAnchor="end">100</text>
        {/* éclair-logo au centre */}
        <path d={`M ${BW * 0.83} 50 L ${BW * 0.76} 170 L ${BW * 0.83} 170 L ${BW * 0.78} 280 L ${BW * 0.91} 140 L ${BW * 0.84} 140 L ${BW * 0.89} 50 Z`}
          fill={C.jaune} stroke="#8a6a00" strokeWidth={5} />
        <text x={BW * 0.42 + 6} y={BH - 60} fontFamily={F} fontWeight={700} fontSize={28} fill="#E9FFF4" fillOpacity={0.8}>FACTURE D'ÉLECTRICITÉ</text>
        <Visage e={e} />
      </g>
    </svg>
  );
};

// ---------- pylône ----------
const Pylone: React.FC<{x: number; y: number; s?: number; prog: number}> = ({x, y, s = 1, prog}) => {
  const L = 1400;
  const d = `M ${x - 70 * s} ${y} L ${x - 18 * s} ${y - 380 * s} L ${x + 18 * s} ${y - 380 * s} L ${x + 70 * s} ${y}
    M ${x - 70 * s} ${y} L ${x + 50 * s} ${y - 130 * s} M ${x + 70 * s} ${y} L ${x - 50 * s} ${y - 130 * s}
    M ${x - 50 * s} ${y - 130 * s} L ${x + 35 * s} ${y - 260 * s} M ${x + 50 * s} ${y - 130 * s} L ${x - 35 * s} ${y - 260 * s}
    M ${x - 110 * s} ${y - 300 * s} L ${x + 110 * s} ${y - 300 * s} M ${x - 80 * s} ${y - 360 * s} L ${x + 80 * s} ${y - 360 * s}
    M ${x - 18 * s} ${y - 380 * s} L ${x} ${y - 430 * s} L ${x + 18 * s} ${y - 380 * s}`;
  return <path d={d} stroke={C.cyan} strokeWidth={6 * s} fill="none" strokeLinecap="round" strokeLinejoin="round"
    strokeDasharray={L} strokeDashoffset={L * (1 - prog)} style={{filter: `drop-shadow(0 0 10px ${C.bleu})`}} />;
};

const Maison: React.FC<{x: number; y: number; allume: number; prog: number}> = ({x, y, allume, prog}) => {
  const L = 1200;
  return (
    <g>
      <path d={`M ${x - 110} ${y} L ${x - 110} ${y - 150} L ${x} ${y - 250} L ${x + 110} ${y - 150} L ${x + 110} ${y} Z`}
        stroke={C.cyan} strokeWidth={6} fill={C.fond2} fillOpacity={prog} strokeDasharray={L} strokeDashoffset={L * (1 - prog)} />
      <rect x={x - 60} y={y - 130} width={50} height={50} fill={C.jaune} opacity={allume} style={{filter: `drop-shadow(0 0 ${30 * allume}px ${C.jaune})`}} />
      <rect x={x + 10} y={y - 130} width={50} height={50} fill={C.jaune} opacity={allume} style={{filter: `drop-shadow(0 0 ${30 * allume}px ${C.jaune})`}} />
      <rect x={x - 25} y={y - 70} width={50} height={70} fill={C.gris} opacity={prog} />
    </g>
  );
};

// ---------- bâtiment de l'État (dessin générique) ----------
const Etat: React.FC<{x: number; y: number; prog: number; gonfle: number}> = ({x, y, prog, gonfle}) => {
  const L = 2400;
  const cols = [-150, -75, 0, 75, 150].map((dx) => `M ${x + dx} ${y - 40} L ${x + dx} ${y - 250}`).join(' ');
  return (
    <g transform={`translate(${x} ${y}) scale(${1 + 0.06 * gonfle}) translate(${-x} ${-y})`}>
      <path d={`M ${x - 230} ${y} L ${x + 230} ${y} M ${x - 210} ${y - 40} L ${x + 210} ${y - 40} ${cols}
        M ${x - 210} ${y - 250} L ${x + 210} ${y - 250} L ${x} ${y - 360} Z`}
        stroke={C.blanc} strokeWidth={9} fill="none" strokeLinecap="round" strokeLinejoin="round"
        strokeDasharray={L} strokeDashoffset={L * (1 - prog)} />
      <text x={x} y={y - 275} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={40} fill={C.blanc} opacity={prog}>ÉTAT</text>
    </g>
  );
};

const Tampon: React.FC<{a: number; texte: string; x: number; y: number; rot: number; couleur?: string; taille?: number}> =
  ({a, texte, x, y, rot, couleur = C.rouge, taille = 64}) => {
    const f = useCurrentFrame();
    const {fps} = useVideoConfig();
    if (f < a) return null;
    const s = interpolate(pop(f, a, fps, 260), [0, 1], [2.6, 1]);
    const o = entre(f, a, 4);
    return (
      <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) rotate(${rot}deg) scale(${s})`, opacity: o,
        border: `8px solid ${couleur}`, color: couleur, fontFamily: F, fontWeight: 900, fontSize: taille, padding: '6px 26px',
        borderRadius: 14, letterSpacing: 4, background: 'rgba(7,10,18,0.55)', whiteSpace: 'nowrap'}}>{texte}</div>
    );
  };

// ---------- compteur géant ----------
const Compteur: React.FC<{a: number; valeur: number; couleur: string; y: number; legende: string}> = ({a, valeur, couleur, y, legende}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (f < a) return null;
  const v = Math.round(interpolate(f, [a, a + 14], [0, valeur], {extrapolateRight: 'clamp', easing: sortie}));
  const s = interpolate(pop(f, a, fps), [0, 1], [0.4, 1]);
  return (
    <div style={{position: 'absolute', top: y, width: W, textAlign: 'center', transform: `scale(${s})`}}>
      <div style={{fontFamily: F, fontWeight: 900, fontSize: 230, color: couleur, lineHeight: 1,
        textShadow: `0 0 50px ${couleur}88, 0 8px 0 rgba(0,0,0,0.5)`}}>{v} €</div>
      <div style={{fontFamily: F, fontWeight: 800, fontSize: 52, color: C.blanc, letterSpacing: 6, marginTop: 6}}>{legende}</div>
    </div>
  );
};

// ---------- sous-titres mot à mot ----------
const SousTitres: React.FC<{mots: Mot[]}> = ({mots}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  // groupes de 3 mots max, coupés à la ponctuation
  const groupes: Mot[][] = [];
  let g: Mot[] = [];
  mots.forEach((m) => {
    g.push(m);
    if (g.length >= 3 || /[.,?!:;]$/.test(m.texte)) { groupes.push(g); g = []; }
  });
  if (g.length) groupes.push(g);
  const actif = groupes.find((gr, i) => t >= gr[0].debut - 0.05 && t < (groupes[i + 1]?.[0].debut ?? gr[gr.length - 1].fin + 0.6) - 0.05);
  if (!actif) return null;
  const a = Math.round(actif[0].debut * fps);
  const s = interpolate(f, [a - 2, a + 4], [0.85, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: sortie});
  return (
    <div style={{position: 'absolute', top: 1480, width: W, textAlign: 'center', transform: `scale(${s})`, padding: '0 60px', boxSizing: 'border-box'}}>
      {actif.map((m, i) => {
        const on = t >= m.debut - 0.03;
        const courant = on && t < m.fin + 0.05;
        return (
          <span key={i} style={{fontFamily: F, fontWeight: 900, fontSize: 82, margin: '0 12px', textTransform: 'uppercase',
            color: courant ? C.jaune : C.blanc, opacity: on ? 1 : 0.45, WebkitTextStroke: '3px #000', paintOrder: 'stroke',
            textShadow: '0 6px 0 rgba(0,0,0,0.6)', display: 'inline-block', transform: courant ? 'scale(1.08)' : 'none'}}>
            {m.texte.replace(/[.,:;]$/, '')}
          </span>
        );
      })}
    </div>
  );
};

const curseurRegard = (f: number) => Math.sin(f / 6) * 0.9;

// ---------- composition ----------
export const Electricite: React.FC<AnimProps> = ({slug, mots, duree}) => {
  const f = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const T = useTemps(mots, fps);

  const tQuestion = T('combien');
  const tPlus = T('plus', tQuestion);
  const tReseau = T('dabord');
  const tLignes = T('lignes', tReseau);
  const t28 = T('vingt', tReseau);
  const tTaxes = T('ensuite', t28);
  const tAccise = T('laccise', tTaxes);
  const tCta = T('contribution', tTaxes);
  const tTva = T('tva', tTaxes);
  const t33 = T('trente', tTaxes);
  const tCourant = T('et', t33 + 5);
  const t39 = T('trente', tCourant);
  const tMoitie = T('meme', t39);
  const tSix = T('six', tMoitie);
  const tAbo = T('abonne', tSix);

  // --- billet : position et morceaux ---
  const chute = pop(f, 0, fps, 220);
  const billetY0 = interpolate(chute, [0, 1], [380, 560]);
  const versHaut = entre(f, tReseau, 16);
  const billetY = billetY0 + interpolate(versHaut, [0, 1], [0, -310]);
  const echelle = interpolate(versHaut, [0, 1], [1, 0.82]) * interpolate(chute, [0, 1], [1.25, 1]);
  const secousse = f < 12 ? Math.sin(f * 3) * (12 - f) * 2 : 0;

  // départ des morceaux
  const departReseau = entre(f, tLignes - 4, 18);
  const departTaxes = entre(f, tTaxes + 6, 18);
  const centreCourant = entre(f, tCourant, 18);

  const cligne = [40, 150, 330, 470].some((c) => f >= c && f < c + 4) ? 1 : 0;
  let expr: Expression = {ouvert: 1, regard: Math.sin(f / 9) * 0.3, bouche: 'sourire', sourcils: 0, goutte: 0, cligne};
  if (f >= tQuestion) expr = {...expr, bouche: 'o', regard: f >= tPlus + 6 ? (Math.floor((f - tPlus - 6) / 9) % 2 === 0 ? -1 : 1) : curseurRegard(f), sourcils: -0.4};
  if (f >= tLignes - 4) expr = {ouvert: 1.35, regard: 0.9, bouche: 'o', sourcils: -0.8, goutte: entre(f, tLignes, 12), cligne: 0};
  if (f >= tTaxes + 6) expr = {ouvert: 0.75, regard: 0, bouche: 'grimace', sourcils: 0.9, goutte: 1, cligne: 0};
  if (f >= t39 - 2) expr = {ouvert: 0.9, regard: -0.2, bouche: 'triste', sourcils: -0.9, goutte: 0, cligne};
  const respire = 1 + Math.sin(f / 14) * 0.012;
  const atterrit = f < 14 ? interpolate(f, [4, 8, 14], [1, 0.86, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: sortie}) : 1;

  const morceaux = PARTS.map((p, i) => {
    const x0 = PARTS.slice(0, i).reduce((s, q) => s + q.w, 0);
    let dx = 0, dy = 0, rot = 0, sc = 1, op = 1;
    // petit écart quand la découpe apparaît
    const ecart = entre(f, tReseau + 4, 10) * 14;
    if (p.id === 'reseau') {
      dx = ecart + departReseau * 200; dy = departReseau * 420; rot = departReseau * 18; sc = 1 - departReseau * 0.55;
      op = 1 - entre(f, tLignes + 12, 10);
    }
    if (p.id === 'taxes') {
      dy = departTaxes * 520; rot = -departTaxes * 14; sc = 1 - departTaxes * 0.6;
      op = 1 - entre(f, tTaxes + 22, 8);
    }
    if (p.id === 'courant') {
      dx = -ecart + centreCourant * (BW * (1 - p.w) / 2 * 0.82); sc = 1 + centreCourant * 0.25;
      dy = centreCourant * 60;
      op = 1 - entre(f, tSix, 8) * 0.0; dy += entre(f, tSix, 10) * -40; sc *= 1 - entre(f, tSix, 10) * 0.55; dx -= entre(f, tSix, 10) * 0;
      if (f >= tAbo) op = 1 - entre(f, tAbo, 8);
    }
    return (
      <div key={p.id} style={{position: 'absolute', left: (W - BW * echelle) / 2 + x0 * BW * echelle + secousse, top: billetY,
        transform: `translate(${dx}px, ${dy}px) rotate(${rot}deg) scale(${sc * respire}) scaleY(${atterrit})`, transformOrigin: 'center bottom', opacity: op,
        width: BW * p.w * echelle, height: BH * echelle,
        filter: `drop-shadow(0 30px 40px rgba(0,0,0,0.6)) blur(${p.id === 'reseau' ? Math.sin(departReseau * Math.PI) * 5 : p.id === 'taxes' ? Math.sin(departTaxes * Math.PI) * 5 : 0}px)`}}>
        <div style={{transform: `scale(${echelle})`, transformOrigin: 'top left'}}>
          <MorceauBillet x0={x0} w={p.w} e={expr} />
        </div>
      </div>
    );
  });

  // ligne « moitié »
  const moitieVis = entre(f, tQuestion, 10) * (1 - entre(f, tReseau, 8));
  const billetGauche = (W - BW * echelle) / 2;

  // question : boutons plus / moins
  const pb = pop(f, tPlus, fps);
  const boutonsOp = 1 - entre(f, tReseau, 8);
  const curseur = f >= tPlus + 6 ? (Math.floor((f - tPlus - 6) / 9) % 2) : -1;

  // scène réseau
  const reseauOp = entre(f, tReseau, 10) * (1 - entre(f, tTaxes, 10));
  const pyl = entre(f, tReseau + 4, 30);
  const allume = entre(f, t28 - 6, 10);

  // scène taxes
  const taxesOp = entre(f, tTaxes, 10) * (1 - entre(f, tCourant, 10));
  const etatProg = entre(f, tTaxes + 2, 26);
  const gonfle = Math.max(0, 1 - Math.abs(f - (tTaxes + 26)) / 6);

  // scène courant : ampoule
  const courantOp = entre(f, tCourant, 10) * (1 - entre(f, tSix, 10));
  const lumiere = entre(f, t39 - 4, 8);

  // scène finale : 10 pièces
  const finOp = entre(f, tSix, 10) * (1 - entre(f, tAbo, 8));
  const aboOp = entre(f, tAbo, 10);

  // bandeau du haut
  const band = pop(f, -8, fps);

  // fil de vie électrique (progression)
  const prog = f / durationInFrames;

  return (
    <AbsoluteFill style={{background: C.fond, overflow: 'hidden'}}>
      <Fond />

      {/* barre de progression électrique */}
      <div style={{position: 'absolute', top: 0, left: 0, height: 12, width: W * prog, background: `linear-gradient(90deg, ${C.bleu}, ${C.jaune})`,
        boxShadow: `0 0 20px ${C.jaune}`}} />

      {/* bandeau */}
      <div style={{position: 'absolute', top: 120, width: W, textAlign: 'center', transform: `scale(${band})`}}>
        <span style={{fontFamily: F, fontWeight: 900, fontSize: 64, color: C.fond, background: C.jaune, padding: '10px 30px', borderRadius: 16,
          boxShadow: '0 10px 0 rgba(0,0,0,0.4)'}}>FACTURE DE 100 €</span>
        <div style={{fontFamily: F, fontWeight: 900, fontSize: 70, color: C.blanc, marginTop: 34, WebkitTextStroke: '3px #000', paintOrder: 'stroke', opacity: 1 - entre(f, tReseau, 8)}}>
          L'ÉLECTRICITÉ, C'EST COMBIEN ?
        </div>
      </div>

      {/* scène réseau (sous le billet) */}
      <svg width={W} height={1920} style={{position: 'absolute', opacity: reseauOp}}>
        <Pylone x={200} y={1380} prog={pyl} />
        <Pylone x={540} y={1380} s={0.8} prog={pyl} />
        {[0, 1].map((k) => {
          const d = `M 120 ${1090 + k * 60} Q 370 ${1200 + k * 60} 476 ${1140 + k * 50} Q 700 ${1230 + k * 40} 860 ${1200 + k * 20}`;
          return (
            <g key={k}>
              <path d={d} stroke={C.gris} strokeWidth={4} fill="none" strokeDasharray={1200} strokeDashoffset={1200 * (1 - pyl)} />
              <path d={d} stroke={C.jaune} strokeWidth={10} fill="none" strokeDasharray="40 1200"
                strokeDashoffset={-((f - tReseau) * 28 + k * 300) % 1240} opacity={pyl}
                style={{filter: `drop-shadow(0 0 12px ${C.jaune})`}} />
            </g>
          );
        })}
        <Maison x={900} y={1380} allume={allume} prog={pyl} />
        {/* compteur */}
        <g opacity={entre(f, tLignes + 10, 10)}>
          <rect x={835} y={1400} width={130} height={70} rx={10} fill={C.fond2} stroke={C.cyan} strokeWidth={4} />
          <text x={900} y={1448} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={34} fill={C.vert}>{String(1000 + ((f * 7) % 9000)).padStart(5, '0')}</text>
        </g>
      </svg>
      <div style={{opacity: 1 - entre(f, tTaxes, 8)}}><Compteur a={t28} valeur={28} couleur={C.cyan} y={640} legende="LE RÉSEAU" /></div>

      {/* scène taxes */}
      <svg width={W} height={1920} style={{position: 'absolute', opacity: taxesOp}}>
        <Etat x={540} y={1380} prog={etatProg} gonfle={gonfle} />
        {new Array(8).fill(0).map((_, i) => {
          const a0 = tTaxes + 14 + i * 3;
          const p = interpolate(f, [a0, a0 + 14], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.in(Easing.quad)});
          if (p <= 0 || p >= 1) return null;
          return <circle key={i} cx={540 + (random('c' + i) - 0.5) * 300} cy={interpolate(p, [0, 1], [700, 1250])} r={26}
            fill={C.jaune} stroke="#8a6a00" strokeWidth={5} />;
        })}
      </svg>
      {taxesOp > 0 && <>
        <Tampon a={tAccise} texte="ACCISE" x={250} y={1170} rot={-12} />
        <Tampon a={tCta} texte="CTA" x={840} y={1150} rot={10} />
        <Tampon a={tTva} texte="TVA" x={545} y={1290} rot={-4} taille={84} />
      </>}
      <div style={{opacity: 1 - entre(f, tCourant, 8)}}>
        <Compteur a={t33} valeur={33} couleur={C.rouge} y={640} legende="LES TAXES" />
      </div>

      {/* morceaux du billet */}
      {morceaux}

      {/* ligne de découpe pendant la question et au « même pas la moitié » */}
      <svg width={W} height={1920} style={{position: 'absolute', opacity: moitieVis}}>
        <line x1={billetGauche + BW * echelle * 0.5} x2={billetGauche + BW * echelle * 0.5} y1={billetY - 60} y2={billetY + BH * echelle + 60}
          stroke={C.jaune} strokeWidth={8} strokeDasharray="22 16" strokeDashoffset={-f * 3} />
        <text x={billetGauche + BW * echelle * 0.5} y={billetY - 80} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={54} fill={C.jaune}>50 €</text>
      </svg>

      {/* gros « ? » */}
      {f >= tQuestion && f < tReseau && (
        <div style={{position: 'absolute', top: billetY - 40, width: W, textAlign: 'center', fontFamily: F, fontWeight: 900, fontSize: 360,
          color: C.jaune, opacity: 0.92, transform: `scale(${pop(f, tQuestion, fps)}) rotate(${Math.sin(f / 5) * 6}deg)`,
          textShadow: `0 0 60px ${C.jaune}, 0 12px 0 #000`}}>?</div>
      )}

      {/* boutons plus / moins */}
      {f >= tPlus && (
        <div style={{position: 'absolute', top: 1130, width: W, display: 'flex', justifyContent: 'center', gap: 50, opacity: boutonsOp,
          transform: `scale(${pb})`}}>
          {[{t: 'PLUS ▲', c: C.vert}, {t: 'MOINS ▼', c: C.rouge}].map((b, i) => (
            <div key={i} style={{fontFamily: F, fontWeight: 900, fontSize: 64, color: '#fff', background: b.c, padding: '22px 46px', borderRadius: 60,
              boxShadow: curseur === i ? `0 0 0 10px #fff, 0 0 60px ${b.c}` : '0 10px 0 rgba(0,0,0,0.45)',
              transform: curseur === i ? 'scale(1.1)' : 'scale(1)'}}>{b.t}</div>
          ))}
        </div>
      )}

      {/* ampoule */}
      <svg width={W} height={1920} style={{position: 'absolute', opacity: courantOp}}>
        <defs>
          <radialGradient id="lum">
            <stop offset="0%" stopColor={C.jaune} stopOpacity={0.9} />
            <stop offset="100%" stopColor={C.jaune} stopOpacity={0} />
          </radialGradient>
        </defs>
        <circle cx={540} cy={1180} r={330 * lumiere} fill="url(#lum)" opacity={0.6 + 0.1 * Math.sin(f / 2)} />
        <path d="M 540 960 C 420 960 380 1060 400 1130 C 420 1200 470 1230 480 1290 L 600 1290 C 610 1230 660 1200 680 1130 C 700 1060 660 960 540 960 Z"
          fill={lumiere > 0 ? '#FFF6C9' : 'none'} fillOpacity={lumiere * 0.9} stroke={C.blanc} strokeWidth={8} />
        <path d="M 500 1290 L 500 1240 L 520 1170 L 540 1230 L 560 1170 L 580 1240 L 580 1290" stroke={lumiere > 0.5 ? C.orange : C.gris} strokeWidth={7} fill="none" />
        {[0, 1, 2].map((k) => <rect key={k} x={485} y={1300 + k * 26} width={110} height={18} rx={6} fill={C.gris} />)}
        {lumiere > 0 && new Array(10).fill(0).map((_, k) => {
          const ang = (k / 10) * Math.PI * 2;
          const r1 = 240 + 20 * Math.sin(f / 3 + k), r2 = r1 + 60 * lumiere;
          return <line key={k} x1={540 + Math.cos(ang) * r1} y1={1130 + Math.sin(ang) * r1} x2={540 + Math.cos(ang) * r2} y2={1130 + Math.sin(ang) * r2}
            stroke={C.jaune} strokeWidth={8} strokeLinecap="round" />;
        })}
      </svg>
      <div style={{opacity: 1 - entre(f, tSix, 8)}}>
        <Compteur a={t39} valeur={39} couleur={C.orange} y={620} legende="LE COURANT" />
      </div>
      {f >= tMoitie && f < tSix + 8 && <Tampon a={tMoitie} texte="MÊME PAS LA MOITIÉ" x={540} y={1130} rot={-6} couleur={C.rouge} taille={70} />}

      {/* final : 10 pièces */}
      <div style={{position: 'absolute', top: 660, width: W, opacity: finOp}}>
        <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: 34, padding: '0 120px'}}>
          {new Array(10).fill(0).map((_, i) => {
            const a = tSix + 4 + i * 2;
            const s = pop(f, a, fps, 220);
            const pasCourant = i >= 4; // 4 pièces pour le courant, 6 pour le reste
            const bascule = entre(f, tSix + 26 + i, 8);
            const coul = pasCourant ? (bascule > 0.5 ? C.gris : C.jaune) : C.orange;
            return (
              <div key={i} style={{width: 140, height: 140, borderRadius: 70, background: coul, border: '8px solid rgba(0,0,0,0.35)',
                transform: `scale(${s}) scaleX(${Math.abs(Math.cos(bascule * Math.PI)) || 0.02})`, display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontFamily: F, fontWeight: 900, fontSize: 60, color: '#1a1a1a', boxShadow: pasCourant ? 'none' : `0 0 30px ${C.orange}`}}>1 €</div>
            );
          })}
        </div>
        <div style={{textAlign: 'center', marginTop: 70, fontFamily: F, fontWeight: 900, fontSize: 120, color: C.blanc,
          transform: `scale(${pop(f, tSix + 20, fps)})`}}>
          <span style={{color: C.jaune}}>6 €</span> SUR 10
        </div>
        <div style={{textAlign: 'center', marginTop: 10, fontFamily: F, fontWeight: 800, fontSize: 48, color: C.gris, opacity: entre(f, tSix + 30, 10)}}>
          NE PAIENT PAS TON COURANT
        </div>
      </div>

      {/* abonnement */}
      {f >= tAbo && (
        <div style={{position: 'absolute', top: 760, width: W, textAlign: 'center', opacity: aboOp}}>
          <div style={{fontFamily: F, fontWeight: 900, fontSize: 96, color: C.blanc, transform: `scale(${pop(f, tAbo, fps)})`}}>LE VRAI PRIX</div>
          <div style={{display: 'inline-block', marginTop: 50, fontFamily: F, fontWeight: 900, fontSize: 64, padding: '26px 60px', borderRadius: 60,
            color: '#fff', background: f > tAbo + 26 ? '#3A4352' : C.rouge, transform: `scale(${f > tAbo + 22 && f < tAbo + 28 ? 0.9 : 1})`}}>
            {f > tAbo + 26 ? 'ABONNÉ ✓' : "S'ABONNER"}
          </div>
        </div>
      )}

      {/* étalonnage + grain + vignette */}
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,0.25), transparent 22%, transparent 70%, rgba(0,0,0,0.35))', pointerEvents: 'none'}} />
      <AbsoluteFill style={{pointerEvents: 'none', opacity: 0.07, mixBlendMode: 'overlay', backgroundSize: '220px',
        backgroundPosition: `${(f * 7) % 220}px ${(f * 13) % 220}px`,
        backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='220' height='220' filter='url(%23n)' opacity='0.6'/%3E%3C/svg%3E")`}} />
      <AbsoluteFill style={{pointerEvents: 'none', background: 'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.45) 100%)'}} />

      <SousTitres mots={mots} />

      {/* source */}
      <div style={{position: 'absolute', bottom: 70, width: W, textAlign: 'center', fontFamily: F, fontWeight: 700, fontSize: 30, color: C.gris}}>
        Source : CRE — facture moyenne au tarif réglementé, fin 2025
      </div>

      <Eclair a={0} x={540} y={600} seed="a" />
      <Flash a={0} />
      <Eclair a={t28 - 2} x={300} y={1100} h={600} seed="b" />
      <Flash a={t28} couleur={C.cyan} />
      <Flash a={t33} couleur={C.rouge} />
      <Eclair a={t39 - 2} x={540} y={960} h={900} seed="c" />
      <Flash a={t39} couleur={C.jaune} />

      {/* son */}
      <Audio src={staticFile(`anim/${slug}-voix.mp3`)} />
      <Audio src={staticFile('sfx/nappe.wav')} volume={0.1} loop />
      <Sequence from={0}><Audio src={staticFile('sfx/impact.wav')} volume={0.6} /></Sequence>
      <Sequence from={tPlus}><Audio src={staticFile('sfx/pop.wav')} volume={0.5} /></Sequence>
      {[0, 1, 2, 3, 4].map((k) => <Sequence key={'t' + k} from={tPlus + 6 + k * 9}><Audio src={staticFile('sfx/tick.wav')} volume={0.35} /></Sequence>)}
      <Sequence from={tReseau}><Audio src={staticFile('sfx/whoosh.wav')} volume={0.5} /></Sequence>
      <Sequence from={t28}><Audio src={staticFile('sfx/impact.wav')} volume={0.5} /></Sequence>
      <Sequence from={tTaxes}><Audio src={staticFile('sfx/whoosh.wav')} volume={0.5} /></Sequence>
      {[tAccise, tCta, tTva].map((a, k) => <Sequence key={'s' + k} from={a}><Audio src={staticFile('sfx/caisse.wav')} volume={0.35} /></Sequence>)}
      <Sequence from={t33}><Audio src={staticFile('sfx/impact.wav')} volume={0.5} /></Sequence>
      <Sequence from={Math.max(0, t39 - 30)} durationInFrames={30}><Audio src={staticFile('sfx/riser.wav')} volume={0.4} /></Sequence>
      <Sequence from={t39}><Audio src={staticFile('sfx/impact.wav')} volume={0.7} /></Sequence>
      <Sequence from={tMoitie}><Audio src={staticFile('sfx/metal.wav')} volume={0.4} /></Sequence>
      <Sequence from={tSix}><Audio src={staticFile('sfx/whoosh.wav')} volume={0.5} /></Sequence>
      <Sequence from={tAbo + 24}><Audio src={staticFile('sfx/pop.wav')} volume={0.5} /></Sequence>
    </AbsoluteFill>
  );
};
