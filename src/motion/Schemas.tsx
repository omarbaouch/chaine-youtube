// Schémas animés (format "schema" et moitié schéma de "ecran_partage") — règle n°6 et n°7 d'Omar.
// Ils expliquent ce qu'une caméra ne montre pas : un prix décomposé, des étapes, un ordre de grandeur.
// Chaque schéma tient dans une boîte de largeur `l` ; tailles de texte selon la règle n°8.
import React from 'react';
import {AbsoluteFill, Img, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
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
  const montee = spring({frame: f - revele, fps, config: {damping: 26, stiffness: 150, mass: 0.8}});
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
        const e = spring({frame: f - li.d, fps, config: {damping: 24, stiffness: 140, mass: 0.8}});
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
              <div style={{fontFamily: theme.polices.titre, fontWeight: 900, fontSize: el.valeur.length > 14 ? 34 : 48, color: el.heros ? C.heros : C.texte, maxWidth: '55%', textAlign: 'right', lineHeight: 1.1}}>{el.valeur}</div>
            ) : null}
          </div>
        );
      })}
      <Source texte={s.source} debut={10 + n * ecart} />
      {s.elements.map((_, i) => <Bruit key={i} nom="tick" a={10 + i * ecart} volume={0.28} />)}
    </div>
  );
};


// ---------- LE pic visuel : l'objet réel découpé en tronçons proportionnels à « qui touche quoi » ----------
const Decoupe: React.FC<{s: Extract<Schema, {type: 'decoupe'}>; l: number; duree: number; media?: string}> = ({s, l, duree, media}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const total = s.total ?? s.parts.reduce((a, p) => a + p.valeur, 0);
  const dec = s.decimales ?? 2;
  const unite = s.unite ?? ' €';
  const [z0, z1] = s.zone ?? [3, 97];
  const [y0, y1] = s.zone_y ?? [30, 70];
  const ratio = s.ratio ?? 3;
  const n = s.parts.length;
  const espace = 40; // écart entre tronçons à la fin
  const largeurUtile = l - espace * (n - 1);
  const imgL = (largeurUtile * 100) / (z1 - z0); // largeur de l'image entière à cette échelle
  const imgH = imgL / ratio;
  const h = Math.min(260, Math.max(90, (imgH * (y1 - y0)) / 100)); // hauteur de la bande visible (l'objet)
  const marge = Math.max(0, (h - (imgH * (y1 - y0)) / 100) / 2);
  const t0 = 8;
  const tCoupe = t0 + Math.round(fps * 0.9);
  const tEcart = tCoupe + Math.round(fps * 0.5);
  const ecart = Math.max(6, Math.min(Math.round(fps * 0.45), Math.floor((duree * 0.35) / n)));
  const pObj = spring({frame: f - t0, fps, config: theme.ressort.doux});
  const pEcart = spring({frame: f - tEcart, fps, config: {damping: 16, stiffness: 90, mass: 1}});
  const coupes: number[] = [];
  let acc = 0;
  s.parts.forEach((p) => { coupes.push(acc / total); acc += p.valeur; });
  // étiquettes : deux rangées quand les tronçons sont trop serrés
  const centres = s.parts.map((p, i) => i * espace + largeurUtile * (coupes[i] + p.valeur / total / 2));
  const rangs: number[] = [];
  centres.forEach((c, i) => { rangs.push(i && c - centres[i - 1] < 240 && rangs[i - 1] === 0 ? 1 : 0); });
  const haut = 190; // place pour deux rangées d'étiquettes au-dessus
  return (
    <div style={{width: l}}>
      <Titre texte={s.titre} />
      <div style={{position: 'relative', width: l, height: haut + h + 30}}>
        {s.parts.map((p, i) => {
          const a = coupes[i];
          const b = coupes[i] + p.valeur / total;
          const ga = z0 + (z1 - z0) * a;
          const x = interpolate(pEcart, [0, 1], [largeurUtile * a, i * espace + largeurUtile * a]);
          const lift = p.heros ? interpolate(pEcart, [0, 1], [0, -18]) : 0;
          const pLab = spring({frame: f - tEcart - 6 - i * ecart, fps, config: theme.ressort.vif});
          const larg = largeurUtile * (b - a);
          const yLab = rangs[i] ? 0 : 92;
          return (
            <React.Fragment key={i}>
              <div style={{position: 'absolute', left: x, top: haut + lift, width: larg, height: h, overflow: 'hidden', opacity: pObj,
                filter: p.heros ? `drop-shadow(0 0 26px ${C.lueur})` : 'drop-shadow(0 18px 24px rgba(0,0,0,.6))'}}>
                {media ? (
                  <Img src={staticFile(media)} style={{position: 'absolute', width: imgL, height: imgH, maxWidth: 'none', left: -(imgL * ga) / 100, top: marge - (imgH * y0) / 100}} />
                ) : (
                  <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(180deg,#E9B46A,#B9763A)'}} />
                )}
                {p.heros ? <div style={{position: 'absolute', inset: 0, background: C.heros, mixBlendMode: 'color', opacity: 0.8 * pEcart}} /> : null}
              </div>
              {/* trait qui relie l'étiquette au tronçon */}
              <div style={{position: 'absolute', left: x + larg / 2 - 1, top: yLab + 84, width: 2, height: haut - yLab - 90 + lift, background: p.heros ? C.heros : C.accent, opacity: 0.7 * pLab}} />
              <div style={{position: 'absolute', left: x + larg / 2, top: yLab, transform: `translateX(-50%) translateY(${interpolate(pLab, [0, 1], [14, 0])}px)`,
                opacity: pLab, textAlign: 'center', whiteSpace: 'nowrap', background: 'rgba(11,14,20,0.78)', borderRadius: 14, padding: '6px 18px',
                border: `2px solid ${p.heros ? C.heros : 'rgba(255,255,255,0.12)'}`}}>
                <div style={{fontFamily: theme.polices.titre, fontWeight: 900, fontSize: p.heros ? 50 : 42, lineHeight: 1.05, color: p.heros ? C.heros : C.texte,
                  fontVariantNumeric: 'tabular-nums'}}>{nombre(p.valeur, dec)}{unite}</div>
                <div style={{fontFamily: theme.polices.titre, fontWeight: 800, fontSize: 26, color: C.texteDim, letterSpacing: '0.04em', textTransform: 'uppercase'}}>{p.label}</div>
              </div>
            </React.Fragment>
          );
        })}
        <svg width={l} height={haut + h + 30} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible', opacity: 1 - pEcart}}>
          {coupes.slice(1).map((c, i) => {
            const x = largeurUtile * c;
            const tr = interpolate(f - tCoupe - i * 4, [0, 10], [0, 1], {...clamp, easing: theme.courbe.sortie});
            return <line key={i} x1={x} x2={x} y1={haut - 16} y2={haut - 16 + (h + 32) * tr} stroke={C.texte} strokeWidth={4} strokeDasharray="14 10" />;
          })}
        </svg>
      </div>
      <Source texte={s.source} debut={tEcart + n * ecart} />
      {coupes.slice(1).map((_, i) => <Bruit key={`c${i}`} nom="tick" a={tCoupe + i * 4} volume={0.35} />)}
      {s.parts.map((p, i) => <Bruit key={i} nom={p.heros ? 'impact' : 'pop'} a={tEcart + 6 + i * ecart} volume={p.heros ? 0.45 : 0.2} />)}
    </div>
  );
};


// ---------- DEVINETTE : 3 choix, compte à rebours, puis la bonne réponse s'allume ----------
const Devine: React.FC<{s: Extract<Schema, {type: 'devine'}>; l: number; duree: number}> = ({s, l, duree}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const sec = s.secondes ?? 3;
  const t0 = s.depart !== undefined ? Math.round(s.depart * fps) : 8; // après la voix
  const tRev = Math.min(duree - Math.round(fps * 0.9), t0 + sec * fps + 6);
  const pQ = spring({frame: f, fps, config: theme.ressort.doux});
  const reste = Math.max(0, Math.ceil(sec - (f - t0) / fps));
  const enCours = f >= t0 && f < tRev;
  const tick = (f - t0) % fps;
  const pouls = enCours ? 1 + 0.12 * Math.exp(-tick / 5) : 1;
  const revele = f >= tRev;
  const lettres = ['A', 'B', 'C', 'D'];
  return (
    <div style={{width: l, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
      <div style={{fontFamily: theme.polices.titre, fontWeight: 900, fontSize: 64, color: C.texte, textAlign: 'center', lineHeight: 1.1, maxWidth: l,
        opacity: pQ, transform: `translateY(${interpolate(pQ, [0, 1], [24, 0])}px)`}}>{s.question}</div>
      <div style={{display: 'flex', gap: 36, marginTop: 50}}>
        {s.choix.map((c, i) => {
          const e = spring({frame: f - 4 - i * 4, fps, config: theme.ressort.rebond});
          const bon = revele && i === s.bonne;
          const faux = revele && i !== s.bonne;
          return (
            <div key={i} style={{minWidth: 280, padding: '26px 34px', borderRadius: 22, textAlign: 'center', opacity: e * (faux ? 0.35 : 1),
              transform: `scale(${interpolate(e, [0, 1], [0.7, 1]) * (bon ? 1.12 : 1)})`,
              background: bon ? C.heros : 'rgba(11,14,20,0.75)', border: `3px solid ${bon ? C.heros : C.accent}`,
              boxShadow: bon ? `0 0 60px ${C.lueur}` : '0 20px 40px rgba(0,0,0,.4)'}}>
              <div style={{fontFamily: theme.polices.titre, fontWeight: 800, fontSize: 30, color: bon ? C.fond : C.accent}}>{lettres[i]}</div>
              <div style={{fontFamily: theme.polices.titre, fontWeight: 900, fontSize: 72, color: bon ? C.fond : C.texte, lineHeight: 1.05}}>{c}</div>
            </div>
          );
        })}
      </div>
      <div style={{marginTop: 50, height: 150, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        {enCours ? (
          <div style={{width: 140, height: 140, borderRadius: 70, border: `6px solid ${C.heros}`, display: 'flex', alignItems: 'center', justifyContent: 'center',
            transform: `scale(${pouls})`, fontFamily: theme.polices.titre, fontWeight: 900, fontSize: 84, color: C.heros}}>{reste}</div>
        ) : f < t0 ? null : (
          <div style={{fontFamily: theme.polices.titre, fontWeight: 900, fontSize: 56, color: C.heros}}>Réponse {lettres[s.bonne ?? 0]}</div>
        )}
      </div>
      {Array.from({length: sec}).map((_, k) => <Bruit key={k} nom="tick" a={t0 + k * fps} volume={0.5} />)}
      <Bruit nom="impact" a={tRev} volume={0.55} />
    </div>
  );
};

// ---------- FICHE SUSPECT (avec photo réelle) puis verdict tamponné ----------
const Suspect: React.FC<{s: Extract<Schema, {type: 'suspect'}>; l: number; media?: string}> = ({s, l, media}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const pF = spring({frame: f, fps, config: theme.ressort.doux});
  const tT = Math.round(fps * 0.9);
  const pT = spring({frame: f - tT, fps, config: {damping: 9, stiffness: 220, mass: 0.6}});
  const coupable = s.verdict && /coupable/i.test(s.verdict);
  const couleurTampon = coupable ? '#FF3B3B' : C.accent;
  return (
    <div style={{width: l, display: 'flex', gap: 60, alignItems: 'center', opacity: pF, transform: `translateY(${interpolate(pF, [0, 1], [30, 0])}px) rotate(${interpolate(pF, [0, 1], [-2, -1])}deg)`}}>
      <div style={{width: 520, height: 600, borderRadius: 12, overflow: 'hidden', background: '#222', boxShadow: '0 40px 80px rgba(0,0,0,.6)', border: '10px solid #E9E4D8', flexShrink: 0, position: 'relative'}}>
        {media ? <Img src={staticFile(media)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: s.verdict ? 'none' : 'grayscale(0.7) contrast(1.1)'}} /> : null}
        {s.numero ? <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,.75)', padding: '10px 18px', fontFamily: theme.polices.titre, fontWeight: 800, fontSize: 30, color: C.texte, letterSpacing: '0.2em'}}>SUSPECT N° {s.numero}</div> : null}
      </div>
      <div style={{flex: 1, position: 'relative'}}>
        <div style={{fontFamily: theme.polices.titre, fontWeight: 800, fontSize: 34, letterSpacing: '0.25em', color: C.accent}}>{s.verdict ? 'VERDICT' : 'SUSPECT'}</div>
        <div style={{fontFamily: theme.polices.titre, fontWeight: 900, fontSize: 110, color: C.texte, lineHeight: 1, marginTop: 10, textTransform: 'uppercase'}}>{s.nom}</div>
        {s.accusation && !s.verdict ? <div style={{fontFamily: theme.polices.titre, fontWeight: 800, fontSize: 52, color: C.heros, marginTop: 30, opacity: spring({frame: f - 10, fps, config: theme.ressort.doux})}}>{s.accusation}</div> : null}
        {s.verdict ? (
          <div style={{marginTop: 40, display: 'inline-block', padding: '14px 34px', border: `8px solid ${couleurTampon}`, borderRadius: 14, color: couleurTampon,
            fontFamily: theme.polices.titre, fontWeight: 900, fontSize: 64, textTransform: 'uppercase', letterSpacing: '0.05em', maxWidth: l - 620,
            opacity: f >= tT ? 1 : 0, transform: `scale(${interpolate(pT, [0, 1], [2.4, 1])}) rotate(-8deg)`, background: 'rgba(11,14,20,.6)'}}>{s.verdict}</div>
        ) : null}
      </div>
      {s.verdict ? <Bruit nom="impact" a={tT} volume={0.7} /> : <Bruit nom="metal" a={2} volume={0.25} />}
    </div>
  );
};

// ---------- PIÈCE : la vraie pièce découpée en parts de camembert qui s'écartent ----------
const Piece: React.FC<{s: Extract<Schema, {type: 'piece'}>; l: number; duree: number; media?: string}> = ({s, l, duree, media}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const total = s.total ?? s.parts.reduce((a, p) => a + p.valeur, 0);
  const R = 300;
  const n = s.parts.length;
  const tEcart = Math.round(fps * 0.9);
  const ecart = Math.max(6, Math.min(Math.round(fps * 0.5), Math.floor((duree * 0.4) / n)));
  const pIn = spring({frame: f, fps, config: theme.ressort.doux});
  let a0 = -Math.PI / 2;
  const parts = s.parts.map((p, i) => {
    const ang = (p.valeur / total) * Math.PI * 2;
    const r = {p, i, a: a0, b: a0 + ang, mid: a0 + ang / 2};
    a0 += ang;
    return r;
  });
  const arc = (a: number, b: number) => {
    const large = b - a > Math.PI ? 1 : 0;
    return `M ${R} ${R} L ${R + R * Math.cos(a)} ${R + R * Math.sin(a)} A ${R} ${R} 0 ${large} 1 ${R + R * Math.cos(b)} ${R + R * Math.sin(b)} Z`;
  };
  return (
    <div style={{width: l, display: 'flex', alignItems: 'center', gap: 70}}>
      <div style={{position: 'relative', width: 2 * R, height: 2 * R, flexShrink: 0, transform: `scale(${interpolate(pIn, [0, 1], [0.6, 1])}) rotate(${interpolate(pIn, [0, 1], [-30, 0])}deg)`, opacity: pIn}}>
        {parts.map(({p, i, a, b, mid}) => {
          const e = spring({frame: f - tEcart - i * ecart, fps, config: theme.ressort.vif});
          const d = (p.heros ? 70 : 34) * e;
          const id = `pc${i}`;
          return (
            <svg key={i} width={2 * R} height={2 * R} style={{position: 'absolute', inset: 0, overflow: 'visible', transform: `translate(${Math.cos(mid) * d}px, ${Math.sin(mid) * d}px)`,
              filter: p.heros ? `drop-shadow(0 0 30px ${C.lueur})` : 'drop-shadow(0 16px 24px rgba(0,0,0,.6))'}}>
              <defs><clipPath id={id}><path d={arc(a, b)} /></clipPath></defs>
              {media ? (() => {
                // l'objet détecté (la pièce) remplit exactement le cercle
                const [z0, z1] = s.zone ?? [0, 100], [y0, y1] = s.zone_y ?? [0, 100], ratio = s.ratio ?? 1;
                const iw = (2 * R * 100) / Math.max(1, z1 - z0), ih = iw / ratio;
                const ix = -(iw * z0) / 100, iy = -(ih * y0) / 100 + (2 * R - (ih * (y1 - y0)) / 100) / 2;
                return <image href={staticFile(media)} x={ix} y={iy} width={iw} height={ih} preserveAspectRatio="none" clipPath={`url(#${id})`} />;
              })() : <path d={arc(a, b)} fill="#C9A44A" />}
              {p.heros ? <path d={arc(a, b)} fill={C.heros} opacity={0.65 * e} style={{mixBlendMode: 'color'}} /> : null}
              <path d={arc(a, b)} fill="none" stroke="rgba(0,0,0,.6)" strokeWidth={3} />
            </svg>
          );
        })}
      </div>
      <div style={{flex: 1}}>
        <Titre texte={s.titre} />
        {parts.map(({p, i}) => {
          const e = spring({frame: f - tEcart - i * ecart - 3, fps, config: theme.ressort.vif});
          return (
            <div key={i} style={{display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', gap: 30, padding: '10px 0', opacity: e,
              transform: `translateX(${interpolate(e, [0, 1], [30, 0])}px)`, borderBottom: '1px solid rgba(255,255,255,.08)'}}>
              <span style={{fontFamily: theme.polices.titre, fontWeight: 800, fontSize: 40, color: p.heros ? C.texte : C.texteDim}}>{p.label}</span>
              <span style={{fontFamily: theme.polices.titre, fontWeight: 900, fontSize: p.heros ? 64 : 46, color: p.heros ? C.heros : C.texte, fontVariantNumeric: 'tabular-nums'}}>
                {nombre(p.valeur, s.decimales ?? 2)}{s.unite ?? ' €'}</span>
            </div>
          );
        })}
        <Source texte={s.source} debut={tEcart + n * ecart} />
      </div>
      {parts.map(({p, i}) => <Bruit key={i} nom={p.heros ? 'impact' : 'pop'} a={tEcart + i * ecart} volume={p.heros ? 0.45 : 0.2} />)}
    </div>
  );
};

// ---------- LOUPE : une loupe ronde se déplace sur la vraie photo et grossit des détails ----------
export const Loupe: React.FC<{s: Extract<Schema, {type: 'loupe'}>; media?: string; duree: number}> = ({s, media, duree}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const z = s.zoom ?? 2.5;
  const W = 1920, H = 1080, r = 210;
  const pts = s.points.map((p, i) => ({...p, t: Math.round((p.a ?? 0.6 + i * ((duree / fps - 1) / Math.max(1, s.points.length))) * fps)}));
  let x = pts[0].x, y = pts[0].y;
  for (let i = 0; i < pts.length; i++) {
    const avant = i ? pts[i - 1] : pts[0];
    const k = interpolate(f, [pts[i].t - 14, pts[i].t], [0, 1], {...clamp, easing: theme.courbe.entreSortie});
    if (f >= pts[i].t - 14) { x = avant.x + (pts[i].x - avant.x) * k; y = avant.y + (pts[i].y - avant.y) * k; }
  }
  const cx = (x / 100) * W, cy = (y / 100) * H;
  const pIn = spring({frame: f - pts[0].t + 10, fps, config: theme.ressort.rebond});
  const actif = [...pts].reverse().find((p) => f >= p.t);
  const pLab = actif ? spring({frame: f - actif.t, fps, config: theme.ressort.vif}) : 0;
  return (
    <AbsoluteFill>
      {media ? <Img src={staticFile(media)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', filter: 'brightness(0.55) saturate(0.9)'}} /> : null}
      <div style={{position: 'absolute', left: cx - r, top: cy - r, width: 2 * r, height: 2 * r, borderRadius: r, overflow: 'hidden', transform: `scale(${pIn})`,
        border: `6px solid ${C.texte}`, boxShadow: `0 0 0 4px ${C.heros}, 0 30px 80px rgba(0,0,0,.7)`}}>
        {media ? <Img src={staticFile(media)} style={{position: 'absolute', width: W * z, height: H * z, maxWidth: 'none', objectFit: 'cover', left: -(cx * z - r), top: -(cy * z - r)}} /> : null}
      </div>
      <div style={{position: 'absolute', left: cx + r * 0.75, top: cy + r * 0.75, width: 70, height: 26, borderRadius: 13, background: C.texte, transform: 'rotate(45deg)', transformOrigin: 'left center', opacity: pIn}} />
      {actif ? (
        <div style={{position: 'absolute', ...(cx > W / 2 ? {right: W - cx + r + 30} : {left: cx + r + 30}), top: cy - 40, opacity: pLab,
          transform: `translateY(${interpolate(pLab, [0, 1], [16, 0])}px)`, padding: '14px 26px', borderRadius: 14, background: 'rgba(11,14,20,0.9)',
          borderLeft: `6px solid ${C.heros}`, fontFamily: theme.polices.titre, fontWeight: 800, fontSize: 44, color: C.texte, maxWidth: 700}}>{actif.texte}</div>
      ) : null}
      {pts.map((p, i) => <Bruit key={i} nom="pop" a={p.t} volume={0.3} />)}
    </AbsoluteFill>
  );
};

export const SchemaAnime: React.FC<{s: Schema; l: number; duree: number; media?: string}> = ({s, l, duree, media}) => {
  switch (s.type) {
    case 'decoupe':
      return <Decoupe s={s} l={l} duree={duree} media={media} />;
    case 'devine':
      return <Devine s={s} l={l} duree={duree} />;
    case 'suspect':
      return <Suspect s={s} l={l} media={media} />;
    case 'piece':
      return <Piece s={s} l={l} duree={duree} media={media} />;
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
