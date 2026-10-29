// Transforme episodes/<slug>/montage.json + médias + voix en public/ep/<slug>/props.json (la timeline exacte).
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';

const slug = process.argv[2];
if (!slug) throw new Error('Usage : node scripts/construire.mjs <slug>');
const dossierEp = path.join('episodes', slug);
const montage = JSON.parse(fs.readFileSync(path.join(dossierEp, 'montage.json'), 'utf8'));
const pub = path.join('public', 'ep', slug);
const fps = montage.format?.fps ?? 30;
const dureeTransition = montage.duree_transition ?? 12;
const MOTS_MAX = montage.sous_titres?.mots_par_ligne ?? 4;

const dureeAudio = (f) =>
  parseFloat(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).toString());

// Répartit les mots d'une phrase sur sa durée, au prorata de leur longueur (+ petites pauses sur la ponctuation).
function minuterMots(segments) {
  const mots = [];
  for (const seg of segments) {
    // la ponctuation isolée (« ? », « ! », « : ») est collée au mot précédent (sinon un « ? » s'affiche seul)
    const liste = seg.texte.split(/\s+/).filter(Boolean).reduce((acc, m) => {
      if (/^[?!:;.…»]+$/.test(m) && acc.length) acc[acc.length - 1] += '\u00a0' + m;
      else acc.push(m);
      return acc;
    }, []);
    const poids = liste.map((m) => m.replace(/[^\p{L}\p{N}]/gu, '').length + 2 + (/[,;:]$/.test(m) ? 3 : 0) + (/[.!?…]$/.test(m) ? 4 : 0));
    const total = poids.reduce((a, b) => a + b, 0) || 1;
    let t = seg.debut;
    liste.forEach((m, i) => {
      const d = ((seg.fin - seg.debut) * poids[i]) / total;
      mots.push({texte: m, debut: t, fin: t + d, finPhrase: i === liste.length - 1 || /[,;:.!?…]$/.test(m)});
      t += d;
    });
  }
  return mots;
}

function lignes(mots) {
  const res = [];
  let courante = [];
  const pousser = () => {
    if (!courante.length) return;
    res.push({
      debut: Math.round(courante[0].debut * fps),
      fin: Math.round(courante.at(-1).fin * fps),
      mots: courante.map((m) => ({texte: m.texte.replace(/[,;:.…]+$/, ''), debut: Math.round(m.debut * fps), fin: Math.round(m.fin * fps)})),
    });
    courante = [];
  };
  for (const m of mots) {
    courante.push(m);
    if (courante.length >= MOTS_MAX || m.finPhrase) pousser();
  }
  pousser();
  // Pas de trou entre deux lignes rapprochées (évite le clignotement).
  for (let i = 0; i < res.length - 1; i++) if (res[i + 1].debut - res[i].fin < 6) res[i].fin = res[i + 1].debut;
  return res;
}

const dossierMedia = path.join(pub, 'media');
const fichiersMedia = fs.existsSync(dossierMedia) ? fs.readdirSync(dossierMedia) : [];
const estImage = (f) => /\.(jpe?g|png|webp)$/i.test(f);

const formatDe = (s, media, medias) => {
  if (s.format) return s.format;
  if (s.type === 'titre') return 'titre';
  if (medias.length > 1) return 'mosaique';
  if (s.schema) return media || medias.length ? 'ecran_partage' : 'schema';
  return 'rush';
};

const scenes = montage.scenes.map((s, i) => {
  const media = fichiersMedia.find((f) => f.startsWith(`${s.id}.`));
  const medias = fichiersMedia
    .filter((f) => f.startsWith(`${s.id}-`) && /^\d+\./.test(f.slice(s.id.length + 1)))
    .sort((a, b) => parseInt(a.slice(s.id.length + 1), 10) - parseInt(b.slice(s.id.length + 1), 10))
    .map((f) => {
      const k = parseInt(f.slice(s.id.length + 1), 10) - 1;
      return {src: `ep/${slug}/media/${f}`, image: estImage(f), legende: s.medias?.[k]?.legende};
    });
  const voixWav = path.join(pub, 'voix', `${s.id}.wav`);
  const aVoix = fs.existsSync(voixWav);
  const voixDebut = aVoix ? Math.round((s.avant_voix ?? (i === 0 ? 0.15 : 0.3)) * fps) : 0;
  const dVoix = aVoix ? Math.ceil(dureeAudio(voixWav) * fps) : 0;
  const minimum = Math.round((s.duree_min ?? (s.type === 'titre' ? 2.5 : 2)) * fps);
  const duree = Math.max(minimum, voixDebut + dVoix + Math.round((s.respiration ?? 0.35) * fps), dureeTransition * 2 + 2);
  const segments = aVoix ? JSON.parse(fs.readFileSync(voixWav.replace(/\.wav$/, '.json'), 'utf8')).segments : [];
  const sousTitres = s.sous_titres === false || montage.sous_titres?.actifs === false ? [] : lignes(minuterMots(segments));
  const transition = i === 0 ? 'coupe' : (s.transition ?? montage.transition_defaut ?? 'fondu');
  const sons = [...(s.sons ?? [])];
  if (transition === 'glissement' || transition === 'balayage') sons.push({nom: 'whoosh', a: 0, volume: 0.35});
  return {
    id: s.id,
    type: media && estImage(media) && s.type !== 'titre' ? 'image' : s.type ?? 'video',
    format: formatDe(s, media, medias),
    duree,
    media: media ? `ep/${slug}/media/${media}` : undefined,
    medias,
    voix: aVoix ? `ep/${slug}/voix/${s.id}.wav` : undefined,
    voixDebut,
    segments,
    titre: s.titre,
    sousTitre: s.sous_titre,
    numero: s.numero,
    surtitre: s.surtitre,
    sousTitres,
    transition,
    zoom: s.zoom ?? (i % 2 ? 'arriere' : 'avant'),
    vitesse: s.vitesse ?? 1,
    debutMedia: s.debut_media ?? 0,
    couches: s.couches ?? [],
    schema: s.schema,
    etiquetteSchema: s.etiquette_schema,
    cote: s.cote,
    punch: s.punch,
    sons,
  };
});

// Plages de voix (frames globales) : la musique se baisse dessous.
const voixPlages = [];
{
  let t = 0;
  scenes.forEach((s, i) => {
    if (i && s.transition !== 'coupe') t -= dureeTransition;
    for (const g of s.segments) voixPlages.push([Math.round(t + s.voixDebut + g.debut * fps), Math.round(t + s.voixDebut + g.fin * fps)]);
    t += s.duree;
  });
}
scenes.forEach((s) => delete s.segments);

// Règle n°6 : jamais deux plans consécutifs du même format.
const doublons = scenes.filter((s, i) => i && s.format === scenes[i - 1].format).map((s) => s.id);
if (doublons.length) console.warn(`⚠ règle n°6 : même format que le plan précédent → ${doublons.join(', ')}`);
const parFormat = scenes.reduce((a, s) => ((a[s.format] = (a[s.format] ?? 0) + 1), a), {});
console.log('formats :', JSON.stringify(parFormat));

const musique = fs.readdirSync(pub).find((f) => f.startsWith('musique.'));
const props = {
  titre: montage.titre,
  fps,
  largeur: montage.format?.largeur ?? 1920,
  hauteur: montage.format?.hauteur ?? 1080,
  dureeTransition,
  musique: musique ? {src: `ep/${slug}/${musique}`, volume: montage.musique?.volume ?? 0.12} : undefined,
  etalonnage: {contraste: 1.08, saturation: 1.1, luminosite: 1, ...(montage.etalonnage ?? {})},
  grain: montage.grain ?? true,
  voixPlages,
  scenes,
};
fs.writeFileSync(path.join(pub, 'props.json'), JSON.stringify(props, null, 1));
const total = scenes.reduce((a, s) => a + s.duree, 0) - scenes.filter((s, i) => i && s.transition !== 'coupe').length * dureeTransition;
console.log(`✔ timeline : ${scenes.length} scènes, ${(total / fps).toFixed(1)} s → ${path.join(pub, 'props.json')}`);
