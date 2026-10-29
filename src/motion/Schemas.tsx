// Schémas animés (format "schema" et moitié schéma de "ecran_partage") — règle n°6 et n°7 d'Omar.
// Ils expliquent ce qu'une caméra ne montre pas : un prix décomposé, des étapes, un ordre de grandeur.
// Chaque schéma tient dans une boîte de largeur `l` ; tailles de texte selon la règle n°8.
import React from 'react';
import {AbsoluteFill, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Audio} from '@remotion/media';
import type {Schema} from '../types';
import {theme, clamp} from '../theme';

const C = theme.couleurs;
const NEUTRES = ['#7FD4FF', '#4F7A9C', '#9AA6B6', '#5B6B80', '#C8D3E0', '#35506A', '#7C8A9C'];

export const nombre = (v: number, dec = 0) =>
  new Intl.NumberFormat('fr-FR', {minimumFractionDigits: dec, maximumFractionDigits: dec}).format(v);

export const Bruit: React.FC<{nom: string; a: number; volume?: number}> = ({nom, a, volume = 0.5}) => (
  <Sequence from={Math.max(0, Math.round(a))} layout="none" name={`sfx ${nom}`}>
    <Audio src={staticFile(`sfx/${nom}.wav`)} volume={volume} />
  </Sequence>
);

const useEntree = (debut: number, ressort: {damping: number; stiffness: number; mass: number} = theme.ressort.vif) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return spring({frame: f - debut, fps, config: ressort});
};

const Titre: React.FC<{texte?: string; debut?: number}> = ({texte, debut = 0}) => {
  const p = useEntree(debut, theme.ressort.doux);
  if (!texte) return null;
  return (
    <div style={{fontFamily: theme.polices.titre, fontWeight: 800, fontSize: 40, letterSpacing: '0.1em', textTransform: 'uppercase',
      color: C.texteDim, marginBottom: 30, opacity: p, transform: `translateY(${interpolate(p, [0, 1], [16, 0])}px)`}}>
      {texte}
    </div>
  );
};

export const Source: React.FC<{texte?: string; debut?: number}> = ({texte, debut = 20}) => {
  const f = useCurrentFrame();
  if (!texte) return null;
  return (
    <div style={{marginTop: 28, fontFamily: theme.polices.texte, fontWeight: 500, fontSize: 24, color: C.texteDim, lineHeight: 1.3,
      opacity: interpolate(f - debut, [0, 12], [0, 0.95], {...clamp, easing: theme.courbe.sortie})}}>
      Source : {texte}
    </div>
  );
};

// Petit "respire" des éléments qui restent à l'écran (règle : rien de figé plus de 2 s).
const respire = (f: number, k = 0) => Math.sin((f + k * 13) / 22) * 2.5;

// ---------- Décomposition d'un prix : barre empilée + légende ----------
const Decomposition: React.FC<{s: Extract<Schema, {type: 'decomposition'}>; l: number; duree: number}> = ({s, l, duree}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const total = s.total ?? s.parts.reduce((a, p) => a + p.valeur, 0);
  const dec = s.decimales ?? 2;
  const unite = s.unite ?? ' €';
  const n = s.parts.length;
  const ecart = Math.max(8, Math.min(Math.round(fps * 1.1), Math.floor((duree * 0.55) / Math.max(1, n))));
  const d0 = 14;
  let gauche = 0;
  const pTotal = useEntree(4);
  const compacte = l < 1100;
  return (
    <div style={{width: l}}>
      <Titre texte={s.titre} />
      <div style={{display: 'flex', alignItems: 'baseline', gap: 24, marginBottom: 34, opacity: pTotal,
        transform: `translateY(${interpolate(pTotal, [0, 1], [24, 0])}px)`}}>
        <span style={{fontFamily: theme.polices.titre, fontWeight: 900, fontSize: 110, color: C.texte, lineHeight: 1, fontVariantNumeric: 'tabular-nums'}}>
          {nombre(total, dec)}{unite}
        </span>
        <span style={{fontFamily: theme.polices.titre, fontWeight: 700, fontSize: 36, color: C.texteDim}}>au total</span>
      </div>
      {/* la barre : chaque morceau pousse à son tour */}
      <div style={{position: 'relative', width: l, height: 84, borderRadius: 18, background: 'rgba(255,255,255,0.06)', overflow: 'hidden',
        border: '1px solid rgba(255,255,255,0.12)'}}>
        {s.parts.map((p, i) => {
          const larg = (p.valeur / total) * l;
          const x = gauche;
          gauche += larg;
          const e = spring({frame: f - d0 - i * ecart, fps, config: theme.ressort.vif});
          const couleur = p.heros ? C.heros : NEUTRES[i % NEUTRES.length];
          return (
            <div key={i} style={{position: 'absolute', left: x, top: 0, height: '100%', width: Math.max(0, larg - 3) * e, background: couleur,
              boxShadow: p.heros ? `0 0 40px ${C.lueur}` : undefined}} />
          );
        })}
      </div>
      <div style={{display: 'grid', gridTemplateColumns: compacte ? '1fr' : '1fr 1fr', columnGap: 60, rowGap: compacte ? 12 : 16, marginTop: 34}}>
        {s.parts.map((p, i) => {
          const e = spring({frame: f - d0 - i * ecart - 4, fps, config: theme.ressort.vif});
          const couleur = p.heros ? C.heros : NEUTRES[i % NEUTRES.length];
          return (
            <div key={i} style={{display: 'flex', alignItems: 'center', gap: 18, opacity: e, transform: `translateX(${interpolate(e, [0, 1], [-24, 0])}px)`}}>
              <div style={{width: 26, height: 26, borderRadius: 7, background: couleur, flexShrink: 0}} />
              <div style={{flex: 1, fontFamily: theme.polices.titre, fontWeight: 700, fontSize: compacte ? 34 : 38, color: p.heros ? C.texte : C.texteDim,
                whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}}>{p.label}</div>
              <div style={{fontFamily: theme.polices.titre, fontWeight: 900, fontSize: compacte ? 40 : 44, color: p.heros ? C.heros : C.texte,
                fontVariantNumeric: 'tabular-nums', whiteSpace: 'nowrap'}}>
                {nombre(p.valeur, dec)}{unite}
              </div>
            </div>
          );
        })}
      </div>
      <Source texte={s.source} debut={d0 + n * ecart} />
      {s.parts.map((p, i) => <Bruit key={i} nom={p.heros ? 'impact' : 'pop'} a={d0 + i * ecart} volume={p.heros ? 0.45 : 0.22} />)}
    </div>
  );
};

// ---------- Processus en étapes numérotées (01, 02, 03… : le cerveau veut finir la série) ----------
const Processus: React.FC<{s: Extract<Schema, {type: 'processus'}>; l: number; duree: number}> = ({s, l, duree}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const n = s.etapes.length;
  const ecart = Math.max(8, Math.min(Math.round(fps * 1.4), Math.floor((duree * 0.6) / Math.max(1, n))));
  const debuts = s.etapes.map((_, i) => (s.a?.[i] !== undefined ? Math.round(s.a[i] * fps) : 10 + i * ecart));
  const horizontal = l >= 1200 && n <= 5;
  const pas = horizontal ? l / n : 0;
  return (
    <div style={{width: l}}>
      <Titre texte={s.titre} />
      <div style={{position: 'relative', display: 'flex', flexDirection: horizontal ? 'row' : 'column', gap: horizontal ? 0 : 26}}>
        {horizontal ? (
          <div style={{position: 'absolute', left: pas / 2, top: 44, height: 4, borderRadius: 2, background: C.accent, opacity: 0.6,
            width: (l - pas) * interpolate(f, [debuts[0], debuts[n - 1] + 10], [0, 1], {...clamp, easing: theme.courbe.entreSortie})}} />
        ) : (
          <div style={{position: 'absolute', left: 44, top: 44, width: 4, borderRadius: 2, background: C.accent, opacity: 0.6,
            height: `calc((100% - 88px) * ${interpolate(f, [debuts[0], debuts[n - 1] + 10], [0, 1], {...clamp, easing: theme.courbe.entreSortie})})`}} />
        )}
        {s.etapes.map((t, i) => {
          const e = spring({frame: f - debuts[i], fps, config: theme.ressort.rebond});
          const actif = s.actif === i;
          return (
            <div key={i} style={{display: 'flex', flexDirection: horizontal ? 'column' : 'row', alignItems: 'center', gap: horizontal ? 22 : 28,
              width: horizontal ? pas : undefined, opacity: interpolate(e, [0, 0.3], [0, 1], clamp),
              transform: `translateY(${interpolate(e, [0, 1], [30, 0]) + respire(f, i)}px)`}}>
              <div style={{width: 92, height: 92, borderRadius: 46, flexShrink: 0, display: 'flex', alignItems: 'center', justifyContent: 'center',
                background: actif ? C.heros : C.fondAlt, border: `4px solid ${actif ? C.heros : C.accent}`, transform: `scale(${e})`,
                boxShadow: actif ? `0 0 40px ${C.lueur}` : '0 10px 30px rgba(0,0,0,.4)', fontFamily: theme.polices.titre, fontWeight: 900, fontSize: 36,
                color: actif ? C.fond : C.accent, fontVariantNumeric: 'tabular-nums'}}>
                {String(i + 1).padStart(2, '0')}
              </div>
              <div style={{fontFamily: theme.polices.titre, fontWeight: 800, fontSize: 40, lineHeight: 1.12, color: actif ? C.heros : C.texte,
                textAlign: horizontal ? 'center' : 'left', maxWidth: horizontal ? pas - 30 : l - 140,
                background: 'rgba(11,14,20,0.55)', padding: '6px 14px', borderRadius: 12}}>
                {t}
              </div>
            </div>
          );
        })}
      </div>
      <Source texte={s.source} debut={debuts[n - 1] + 10} />
      {debuts.map((d, i) => <Bruit key={i} nom="tick" a={d} volume={0.3} />)}
    </div>
  );
};

// ---------- Chiffre géant (avec "?" qui retarde la réponse : fossé de curiosité) ----------
const Chiffre: React.FC<{s: Extract<Schema, {type: 'chiffre'}>; l: number}> = ({s, l}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const revele = s.revele_a !== undefined ? Math.round(s.revele_a * fps) : 6;
  const pLeg = useEntree(0, theme.ressort.doux);
  const pNum = spring({frame: f - revele, fps, config: theme.ressort.rebond});
  const montee = spring({frame: f - revele, fps, config: {damping: 30, stiffness: 70, mass: 1}});
  const pComp = useEntree(revele + 22, theme.ressort.doux);
  const attente = s.revele_a !== undefined && f < revele;
  const pulse = 1 + 0.05 * Math.sin(f / 5);
  const flash = interpolate(f, [revele, revele + 2, revele + 9], [0, 0.35, 0], clamp);
  const taille = l < 1100 ? 130 : 150;
  return (
    <div style={{width: l, display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center'}}>
      {s.legende ? (
        <div style={{fontFamily: theme.polices.titre, fontWeight: 800, fontSize: 40, letterSpacing: '0.08em', textTransform: 'uppercase',
          color: C.texteDim, marginBottom: 18, opacity: pLeg, transform: `translateY(${interpolate(pLeg, [0, 1], [18, 0])}px)`}}>{s.legende}</div>
      ) : null}
      <div style={{fontFamily: theme.polices.titre, fontWeight: 900, fontSize: taille, lineHeight: 1.05, color: C.heros, whiteSpace: 'nowrap',
        fontVariantNumeric: 'tabular-nums', textShadow: `0 0 50px ${C.lueur}`,
        transform: attente ? `scale(${pulse})` : `scale(${interpolate(pNum, [0, 1], [1.35, 1])})`}}>
        {attente ? '?' : <>{s.prefixe ?? ''}{nombre(s.valeur * montee, s.decimales ?? 0)}{s.suffixe ?? ''}</>}
      </div>
      {s.comparaison ? (
        <div style={{marginTop: 26, fontFamily: theme.polices.titre, fontWeight: 800, fontSize: 46, color: C.texte, maxWidth: l, lineHeight: 1.15,
          opacity: pComp, transform: `translateY(${interpolate(pComp, [0, 1], [20, 0])}px)`,
          background: 'rgba(11,14,20,0.6)', padding: '10px 24px', borderRadius: 14, borderLeft: `6px solid ${C.accent}`}}>
          {s.comparaison}
        </div>
      ) : null}
      <Source texte={s.source} debut={revele + 30} />
      <AbsoluteFill style={{background: 'white', opacity: flash, mixBlendMode: 'overlay', pointerEvents: 'none'}} />
      {s.revele_a !== undefined && revele > 30 ? <Bruit nom="riser" a={revele - 48} volume={0.35} /> : null}
      <Bruit nom="impact" a={revele} volume={0.55} />
    </div>
  );
};

// ---------- Comparaison A vs B (deux barres, l'écart saute aux yeux) ----------
const Comparaison: React.FC<{s: Extract<Schema, {type: 'comparaison'}>; l: number}> = ({s, l}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const max = Math.max(s.a.valeur, s.b.valeur) || 1;
  const heros = s.heros ?? (s.b.valeur >= s.a.valeur ? 'b' : 'a');
  const dec = s.decimales ?? 2;
  const lignes = [
    {k: 'a', ...s.a, d: 10},
    {k: 'b', ...s.b, d: 10 + Math.round(fps * 1.2)},
  ];
  const zoneValeur = l < 1100 ? 300 : 420;
  return (
    <div style={{width: l}}>
      <Titre texte={s.titre} />
      {lignes.map((li) => {
        const e = spring({frame: f - li.d, fps, config: {damping: 26, stiffness: 70, mass: 1}});
        const estHeros = li.k === heros;
        const larg = Math.max(10, ((l - zoneValeur - 20) * li.valeur) / max);
        return (
          <div key={li.k} style={{marginBottom: 34, opacity: interpolate(e, [0, 0.2], [0, 1], clamp)}}>
            <div style={{fontFamily: theme.polices.titre, fontWeight: 800, fontSize: 40, color: estHeros ? C.texte : C.texteDim, marginBottom: 12}}>{li.label}</div>
            <div style={{display: 'flex', alignItems: 'center', gap: 20}}>
              <div style={{height: 70, width: larg * e, borderRadius: 14, background: estHeros ? C.heros : NEUTRES[2],
                boxShadow: estHeros ? `0 0 40px ${C.lueur}` : undefined}} />
              <div style={{fontFamily: theme.polices.titre, fontWeight: 900, fontSize: l < 1100 ? 80 : 110, lineHeight: 1, whiteSpace: 'nowrap',
                color: estHeros ? C.heros : C.texte, fontVariantNumeric: 'tabular-nums'}}>
                {nombre(li.valeur * e, dec)}{s.unite ?? ' €'}
              </div>
            </div>
          </div>
        );
      })}
      <Source texte={s.source} debut={lignes[1].d + 20} />
      <Bruit nom="pop" a={lignes[0].d} volume={0.25} />
      <Bruit nom="impact" a={lignes[1].d} volume={0.45} />
    </div>
  );
};

// ---------- Liste (qui touche quoi, les ingrédients…) ----------
const Liste: React.FC<{s: Extract<Schema, {type: 'liste'}>; l: number; duree: number}> = ({s, l, duree}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const n = s.elements.length;
  const ecart = Math.max(8, Math.min(Math.round(fps * 1.2), Math.floor((duree * 0.55) / Math.max(1, n))));
  return (
    <div style={{width: l}}>
      <Titre texte={s.titre} />
      {s.elements.map((el, i) => {
        const e = spring({frame: f - 10 - i * ecart, fps, config: theme.ressort.vif});
        return (
          <div key={i} style={{display: 'flex', alignItems: 'center', gap: 24, padding: '14px 24px', marginBottom: 14, borderRadius: 16,
            background: el.heros ? 'rgba(255,107,44,0.14)' : 'rgba(11,14,20,0.55)', border: `1px solid ${el.heros ? C.heros : 'rgba(255,255,255,0.10)'}`,
            opacity: e, transform: `translateX(${interpolate(e, [0, 1], [-40, 0])}px)`}}>
            <div style={{fontFamily: theme.polices.titre, fontWeight: 900, fontSize: 34, color: C.accent, fontVariantNumeric: 'tabular-nums'}}>
              {String(i + 1).padStart(2, '0')}
            </div>
            <div style={{flex: 1, fontFamily: theme.polices.titre, fontWeight: 800, fontSize: 42, color: el.heros ? C.texte : C.texte, lineHeight: 1.12}}>{el.texte}</div>
            {el.valeur ? (
              <div style={{fontFamily: theme.polices.titre, fontWeight: 900, fontSize: 48, color: el.heros ? C.heros : C.texte, whiteSpace: 'nowrap'}}>{el.valeur}</div>
            ) : null}
          </div>
        );
      })}
      <Source texte={s.source} debut={10 + n * ecart} />
      {s.elements.map((_, i) => <Bruit key={i} nom="tick" a={10 + i * ecart} volume={0.28} />)}
    </div>
  );
};

export const SchemaAnime: React.FC<{s: Schema; l: number; duree: number}> = ({s, l, duree}) => {
  switch (s.type) {
    case 'decomposition':
      return <Decomposition s={s} l={l} duree={duree} />;
    case 'processus':
      return <Processus s={s} l={l} duree={duree} />;
    case 'chiffre':
      return <Chiffre s={s} l={l} />;
    case 'comparaison':
      return <Comparaison s={s} l={l} />;
    case 'liste':
      return <Liste s={s} l={l} duree={duree} />;
    default:
      return null;
  }
};
