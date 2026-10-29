// Animations SVG "schéma" (règle n°6) : expliquer ce qu'une caméra ne peut pas montrer.
// Toujours étiquetées, typographie règle n°8, UNE info en couleur héros (règle n°7, effet d'isolement).
import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {evolvePath} from '@remotion/paths';
import {theme, clamp} from '../theme';
import {MotsQuiMontent, Compteur} from './Texte';

const C = theme.couleurs;
const T = theme.polices;

export type Schema =
  | {type: 'decomposition'; titre?: string; total: number; unite: string; decimales?: number;
      parts: {label: string; valeur?: number | null; heros?: boolean}[]; source?: string}
  | {type: 'processus'; titre?: string; etapes: {label: string; icone?: Icone}[]}
  | {type: 'chiffre'; valeur: number; decimales?: number; prefixe?: string; suffixe?: string; legende?: string; comparaison?: string; source?: string}
  | {type: 'comparaison'; titre?: string; items: {label: string; valeur: number; unite?: string; heros?: boolean}[]; source?: string};

export type Icone = 'bobine' | 'disque' | 'gobelet' | 'canette' | 'camion' | 'magasin' | 'piece' | 'usine' | 'presse' | 'recyclage';

// ---------- Icônes au trait (dessinées en direct) ----------
const CHEMINS: Record<Icone, string[]> = {
  bobine: ['M -60 0 A 60 60 0 1 1 60 0 A 60 60 0 1 1 -60 0', 'M -22 0 A 22 22 0 1 1 22 0 A 22 22 0 1 1 -22 0', 'M 0 -60 L 80 -60'],
  disque: ['M -60 0 A 60 22 0 1 1 60 0 A 60 22 0 1 1 -60 0', 'M -60 0 L -60 8 A 60 22 0 0 0 60 8 L 60 0'],
  gobelet: ['M -46 -30 L -46 40 Q -46 52 -34 52 L 34 52 Q 46 52 46 40 L 46 -30', 'M -46 -30 A 46 14 0 1 0 46 -30 A 46 14 0 1 0 -46 -30'],
  canette: ['M -34 -60 L 34 -60 L 40 -48 L 40 52 Q 40 64 28 64 L -28 64 Q -40 64 -40 52 L -40 -48 Z', 'M -40 -40 L 40 -40', 'M -40 44 L 40 44'],
  camion: ['M -70 30 L -70 -30 L 20 -30 L 20 30 Z', 'M 20 -10 L 50 -10 L 70 10 L 70 30 L 20 30', 'M -45 40 A 12 12 0 1 1 -21 40 A 12 12 0 1 1 -45 40', 'M 33 40 A 12 12 0 1 1 57 40 A 12 12 0 1 1 33 40'],
  magasin: ['M -66 -20 L 66 -20 L 56 -50 L -56 -50 Z', 'M -60 -20 L -60 56 L 60 56 L 60 -20', 'M -18 56 L -18 14 L 18 14 L 18 56'],
  piece: ['M -56 0 A 56 56 0 1 1 56 0 A 56 56 0 1 1 -56 0', 'M -40 0 A 40 40 0 1 1 40 0 A 40 40 0 1 1 -40 0', 'M -8 -18 L 8 -18 M 0 -18 L 0 18 M -8 18 L 8 18'],
  usine: ['M -70 56 L -70 -10 L -30 10 L -30 -10 L 10 10 L 10 -10 L 50 10 L 50 -60 L 70 -60 L 70 56 Z', 'M -50 30 L -36 30 M -10 30 L 4 30 M 30 30 L 44 30'],
  presse: ['M -60 -64 L 60 -64 L 60 -40 L -60 -40 Z', 'M -10 -40 L -10 0 L 10 0 L 10 -40', 'M -40 0 L 40 0 L 40 14 L -40 14 Z', 'M -70 50 L 70 50 L 70 64 L -70 64 Z'],
  recyclage: ['M -40 30 L 0 -40 L 40 30 Z', 'M -16 -12 L 0 -40 L 16 -12', 'M 26 6 L 40 30 L 10 30'],
};

export const IconeTrait: React.FC<{icone: Icone; progres: number; couleur?: string; taille?: number}> = ({icone, progres, couleur = C.texte, taille = 1}) => (
  <g transform={`scale(${taille})`}>
    {CHEMINS[icone].map((d, i) => {
      const p = Math.max(0, Math.min(1, progres * CHEMINS[icone].length - i));
      const ev = evolvePath(p, d);
      return <path key={i} d={d} fill="none" stroke={couleur} strokeWidth={5} strokeLinecap="round" strokeLinejoin="round"
        strokeDasharray={ev.strokeDasharray} strokeDashoffset={ev.strokeDashoffset} />;
    })}
  </g>
);

const Titre: React.FC<{texte?: string}> = ({texte}) =>
  texte ? (
    <div style={{position: 'absolute', left: 150, top: 110, width: 1620}}>
      <MotsQuiMontent texte={texte} taille={84} debut={0} />
    </div>
  ) : null;

const Source: React.FC<{texte?: string}> = ({texte}) => {
  const f = useCurrentFrame();
  return texte ? (
    <div style={{position: 'absolute', left: 150, bottom: 230, fontFamily: T.texte, fontSize: 24, color: C.texteDim, opacity: interpolate(f, [20, 35], [0, 1], clamp)}}>
      Source : {texte}
    </div>
  ) : null;
};

// ---------- Décomposition d'un prix (ticket) : les parts inconnues restent des « ? » (fossé de curiosité) ----------
const Decomposition: React.FC<{s: Extract<Schema, {type: 'decomposition'}>}> = ({s}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const L = 1520, X0 = 200, Y0 = 470, H = 120;
  const connus = s.parts.reduce((a, p) => a + (p.valeur ?? 0), 0);
  const inconnus = s.parts.filter((p) => p.valeur == null).length;
  const reste = Math.max(0, s.total - connus);
  let x = X0;
  return (
    <AbsoluteFill>
      <Titre texte={s.titre} />
      <svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>
        <rect x={X0} y={Y0} width={L * interpolate(f, [0, 18], [0, 1], {...clamp, easing: theme.courbe.sortie})} height={H} rx={18} fill="rgba(255,255,255,0.06)" stroke="rgba(255,255,255,0.18)" />
        {s.parts.map((p, i) => {
          const v = p.valeur ?? reste / Math.max(1, inconnus);
          const larg = Math.max(18, (v / s.total) * L);
          const e = spring({frame: f - 14 - i * 7, fps, config: theme.ressort.vif});
          const xi = x;
          x += larg;
          const coul = p.heros ? C.heros : p.valeur == null ? 'rgba(255,255,255,0.10)' : C.metalMoyen;
          return (
            <g key={i} opacity={e}>
              <rect x={xi + 3} y={Y0 + 3} width={Math.max(0, (larg - 6) * e)} height={H - 6} rx={14} fill={coul}
                stroke={p.valeur == null ? 'rgba(255,255,255,0.35)' : 'none'} strokeDasharray={p.valeur == null ? '10 8' : undefined}
                style={p.heros ? {filter: `drop-shadow(0 0 18px ${C.lueur})`} : undefined} />
              <text x={xi + larg / 2} y={Y0 + H / 2 + 16} textAnchor="middle" fill={p.heros ? '#0B0E14' : C.texte}
                style={{fontFamily: T.titre, fontWeight: 900, fontSize: p.valeur == null ? 54 : 34}}>{p.valeur == null ? '?' : ''}</text>
              <text x={xi + 8} y={i % 2 ? Y0 + H + 58 : Y0 - 26} fill={p.heros ? C.heros : C.texte}
                style={{fontFamily: T.titre, fontWeight: 800, fontSize: 34}}>
                {p.label}{p.valeur != null ? ` · ${p.valeur.toFixed(s.decimales ?? 2).replace('.', ',')} ${s.unite}` : ''}
              </text>
            </g>
          );
        })}
        <text x={X0 + L} y={Y0 - 90} textAnchor="end" fill={C.texte} opacity={interpolate(f, [6, 18], [0, 1], clamp)}
          style={{fontFamily: T.titre, fontWeight: 900, fontSize: 64}}>
          {`Total : ${s.total.toFixed(s.decimales ?? 2).replace('.', ',')} ${s.unite}`}
        </text>
      </svg>
      <Source texte={s.source} />
    </AbsoluteFill>
  );
};

// ---------- Processus en étapes numérotées (progression visible) ----------
const Processus: React.FC<{s: Extract<Schema, {type: 'processus'}>}> = ({s}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const n = s.etapes.length;
  const pas = 1620 / n;
  const cy = 560;
  return (
    <AbsoluteFill>
      <Titre texte={s.titre} />
      <svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>
        {s.etapes.map((e, i) => {
          const debut = 8 + i * 16;
          const p = spring({frame: f - debut, fps, config: theme.ressort.doux});
          const trace = interpolate(f, [debut, debut + 22], [0, 1], {...clamp, easing: theme.courbe.entreSortie});
          const cx = 150 + pas * i + pas / 2;
          const actif = f >= debut && (i === n - 1 || f < debut + 16);
          const fl = interpolate(f, [debut + 10, debut + 22], [0, 1], clamp);
          return (
            <g key={i}>
              {i < n - 1 ? (
                <g opacity={fl}>
                  <line x1={cx + 110} x2={cx + 110 + (pas - 220) * fl} y1={cy} y2={cy} stroke={C.accent} strokeWidth={5} strokeLinecap="round" />
                  <path d={`M ${cx + pas - 122} ${cy - 14} L ${cx + pas - 108} ${cy} L ${cx + pas - 122} ${cy + 14}`} fill="none" stroke={C.accent} strokeWidth={5} strokeLinecap="round" opacity={fl > 0.95 ? 1 : 0} />
                </g>
              ) : null}
              <g transform={`translate(${cx} ${cy}) scale(${interpolate(p, [0, 1], [0.6, 1])})`} opacity={p}>
                <circle r={100} fill={actif ? 'rgba(255,107,44,0.14)' : 'rgba(255,255,255,0.05)'} stroke={actif ? C.heros : 'rgba(255,255,255,0.22)'} strokeWidth={3} />
                {e.icone ? <IconeTrait icone={e.icone} progres={trace} couleur={actif ? C.heros : C.texte} taille={0.95} /> : null}
                <text y={-122} textAnchor="middle" fill={C.accent} style={{fontFamily: T.titre, fontWeight: 900, fontSize: 30}}>{String(i + 1).padStart(2, '0')}</text>
                <text y={156} textAnchor="middle" fill={C.texte} style={{fontFamily: T.titre, fontWeight: 800, fontSize: 36}}>{e.label}</text>
              </g>
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};

// ---------- Chiffre géant (pic émotionnel) ----------
const Chiffre: React.FC<{s: Extract<Schema, {type: 'chiffre'}>}> = ({s}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame: f - 4, fps, config: theme.ressort.rebond});
  const onde = interpolate(f, [6, 30], [0, 1], {...clamp, easing: theme.courbe.sortie});
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
      <svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>
        {[0, 1, 2].map((k) => (
          <circle key={k} cx={960} cy={500} r={180 + onde * (300 + k * 140)} fill="none" stroke={C.heros} strokeWidth={3} opacity={(1 - onde) * (0.5 - k * 0.12)} />
        ))}
      </svg>
      {s.legende ? (
        <div style={{fontFamily: T.titre, fontWeight: 800, fontSize: 40, letterSpacing: '0.12em', textTransform: 'uppercase', color: C.texteDim,
          opacity: interpolate(f, [0, 12], [0, 1], clamp), marginBottom: 10}}>{s.legende}</div>
      ) : null}
      <div style={{fontFamily: T.titre, fontWeight: 900, fontSize: 230, lineHeight: 1, color: C.heros, whiteSpace: 'nowrap',
        textShadow: `0 0 60px ${C.lueur}`, transform: `scale(${interpolate(p, [0, 1], [0.6, 1])})`, opacity: Math.min(1, p * 1.4)}}>
        {s.prefixe ?? ''}<Compteur vers={s.valeur} decimales={s.decimales ?? 0} debut={4} />{s.suffixe ?? ''}
      </div>
      {s.comparaison ? (
        <div style={{marginTop: 26, fontFamily: T.titre, fontWeight: 800, fontSize: 46, color: C.texte, background: 'rgba(11,14,20,0.7)',
          padding: '12px 28px', borderRadius: 14, opacity: interpolate(f, [26, 40], [0, 1], clamp)}}>{s.comparaison}</div>
      ) : null}
      <Source texte={s.source} />
    </AbsoluteFill>
  );
};

// ---------- Comparaison en barres (ancrage) ----------
const Comparaison: React.FC<{s: Extract<Schema, {type: 'comparaison'}>}> = ({s}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const max = Math.max(...s.items.map((i) => i.valeur));
  return (
    <AbsoluteFill>
      <Titre texte={s.titre} />
      <div style={{position: 'absolute', left: 200, top: 360, width: 1520}}>
        {s.items.map((it, i) => {
          const p = spring({frame: f - 10 - i * 8, fps, config: theme.ressort.doux});
          return (
            <div key={i} style={{marginBottom: 54, opacity: p}}>
              <div style={{display: 'flex', justifyContent: 'space-between', fontFamily: T.titre, fontWeight: 800, fontSize: 40, color: it.heros ? C.heros : C.texte, marginBottom: 14}}>
                <span>{it.label}</span>
                <span><Compteur vers={it.valeur} decimales={it.valeur < 1 ? 2 : 0} debut={10 + i * 8} suffixe={it.unite ? ` ${it.unite}` : ''} /></span>
              </div>
              <div style={{height: 38, borderRadius: 19, background: 'rgba(255,255,255,0.08)'}}>
                <div style={{width: `${(it.valeur / max) * 100 * p}%`, height: 38, borderRadius: 19, background: it.heros ? C.heros : C.metalMoyen,
                  boxShadow: it.heros ? `0 0 30px ${C.lueur}` : undefined}} />
              </div>
            </div>
          );
        })}
      </div>
      <Source texte={s.source} />
    </AbsoluteFill>
  );
};

export const SchemaAnime: React.FC<{schema: Schema}> = ({schema}) => {
  switch (schema.type) {
    case 'decomposition': return <Decomposition s={schema} />;
    case 'processus': return <Processus s={schema} />;
    case 'chiffre': return <Chiffre s={schema} />;
    case 'comparaison': return <Comparaison s={schema} />;
    default: return null;
  }
};
