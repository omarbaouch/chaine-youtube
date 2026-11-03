// Transforme episodes/<slug>/montage.json + médias + voix en public/ep/<slug>/props.json (la timeline exacte).
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync, spawnSync} from 'node:child_process';

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
const fichiersMedia = fs.existsSync(dossierMedia) ? fs.readdirSync(dossierMedia).filter((f) => !f.endsWith('.ref')) : [];
const estImage = (f) => /\.(jpe?g|png|webp)$/i.test(f);

const formatDe = (s, media, medias) => {
  if (s.temoignage) return 'temoignage';
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
  const aVoix = !s.temoignage && fs.existsSync(voixWav);
  // Voix « continue » (bloc lu d'un seul souffle, voix.py) : la respiration naturelle est déjà dans le morceau.
  // On n'ajoute que ce qu'il faut pour que deux plans ne se chevauchent pas pendant un fondu.
  const voixJson = voixWav.replace(/\.wav$/, '.json');
  const continu = aVoix && fs.existsSync(voixJson) && JSON.parse(fs.readFileSync(voixJson, 'utf8')).continu === true;
  const fonduAvant = i > 0 && (s.transition ?? montage.transition_defaut ?? 'fondu') !== 'coupe';
  const suivant = montage.scenes[i + 1];
  const fonduApres = suivant && (suivant.transition ?? montage.transition_defaut ?? 'fondu') !== 'coupe';
  const avantDefaut = continu ? (fonduAvant ? dureeTransition / 2 / fps : 0) : (i === 0 ? 0.15 : 0.3);
  const respDefaut = continu ? (fonduApres ? dureeTransition / 2 / fps : 0.02) : (montage.respiration ?? 0.35);
  const voixDebut = aVoix ? Math.round((s.avant_voix ?? avantDefaut) * fps) : 0;
  const dVoix = aVoix ? Math.ceil(dureeAudio(voixWav) * fps) : 0;
  const minimum = Math.round((s.duree_min ?? (s.type === 'titre' ? 2.5 : 2)) * fps);
  const duree = Math.max(minimum, voixDebut + dVoix + Math.round((s.respiration ?? respDefaut) * fps), dureeTransition * 2 + 2);
  // Devinette lue par la voix : le compte à rebours démarre quand la voix a fini de poser la question.
  if (s.schema?.type === 'devine') {
    const depart = voixDebut + dVoix + Math.round(0.2 * fps);
    s.schema = {...s.schema, depart: depart / fps};
  }
  const dureeDevine = s.schema?.type === 'devine' ? Math.round((s.schema.depart + (s.schema.secondes ?? 3) + 1.6) * fps) : 0;
  // Témoignage : une vraie personne parle (son d'origine du clip). Durée = extrait [debut_media, fin] ; sous-titres = citation.
  const tem = s.temoignage;
  const dClip = tem ? Math.max(1, (tem.fin ?? (s.debut_media ?? 0) + 8) - (s.debut_media ?? 0)) : 0;
  const segments = tem
    ? (tem.citation ? [{texte: tem.citation, debut: tem.parole_debut ?? 0.2, fin: tem.parole_fin ?? dClip - 0.2}] : [])
    : aVoix ? JSON.parse(fs.readFileSync(voixWav.replace(/\.wav$/, '.json'), 'utf8')).segments : [];
  const sousTitres = s.sous_titres === false || montage.sous_titres?.actifs === false ? [] : lignes(minuterMots(segments));
  const transition = i === 0 ? 'coupe' : (s.transition ?? montage.transition_defaut ?? 'fondu');
  // retour d'Omar (31/10/2026) : le souffle « whoosh » (le « shiiit ») est banni partout
  const sons = (s.sons ?? []).filter((x) => x.nom !== 'whoosh');
  // (plus de souffle « whoosh » sur les transitions : retour d'Omar du 31/10/2026)
  return {
    id: s.id,
    type: media && estImage(media) && s.type !== 'titre' ? 'image' : s.type ?? 'video',
    format: formatDe(s, media, medias),
    duree: tem ? Math.round((dClip + 0.3) * fps) : Math.max(duree, dureeDevine),
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
    qui: s.voix,
    ambiance: s.ambiance,
    temoin: tem ? {nom: tem.nom, role: tem.role, source: tem.source} : undefined,
  };
});

// Schéma "decoupe" : l'objet réel est découpé en tronçons. On mesure l'image (ratio) et, si l'objet est posé sur
// un fond sombre, on détecte tout seul sa boîte englobante (cropdetect) pour couper pile dans l'objet.
for (const s of scenes) {
  if (!['decoupe', 'piece'].includes(s.schema?.type) || !s.media || s.type !== 'image') continue;
  const f = path.join('public', s.media);
  const [w, h] = execFileSync('ffprobe', ['-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', f]).toString().trim().split(',').map(Number);
  s.schema = {...s.schema, ratio: w / h};
  if (!s.schema.zone || !s.schema.zone_y) {
    // profil de luminance (image réduite à 320 px) : l'objet = ce qui ressort nettement du fond
    const W = 320, H = Math.max(2, Math.round((320 * h) / w));
    const brut = spawnSync('ffmpeg', ['-v', 'error', '-i', f, '-vf', `scale=${W}:${H},format=gray`, '-f', 'rawvideo', '-']).stdout;
    const px = (x, y) => brut[y * W + x];
    // fond = médiane des pixels du bord de l'image (marche sur fond noir comme sur fond clair)
    const bord = [];
    for (let x = 0; x < W; x++) bord.push(px(x, 0), px(x, H - 1));
    for (let y = 0; y < H; y++) bord.push(px(0, y), px(W - 1, y));
    bord.sort((u, v) => u - v);
    const fond = bord[Math.floor(bord.length / 2)];
    const objet = (x, y) => Math.abs(px(x, y) - fond) > 38;
    const etendue = (n, frac, seuil) => {
      let a = 0, b = n - 1;
      while (a < b && frac(a) < seuil) a++;
      while (b > a && frac(b) < seuil) b--;
      return [a, b + 1];
    };
    const fracLigne = (y) => { let c = 0; for (let x = 0; x < W; x++) c += objet(x, y); return c / W; };
    const [ya, yb] = etendue(H, fracLigne, 0.2);
    const fracCol = (x) => { let c = 0; for (let y = ya; y < yb; y++) c += objet(x, y); return c / Math.max(1, yb - ya); };
    const [xa, xb] = etendue(W, fracCol, 0.35);
    const zoneX = [(xa / W) * 100, (xb / W) * 100], zoneY = [(ya / H) * 100, (yb / H) * 100];
    s.schema.zone ??= zoneX;
    s.schema.zone_y ??= zoneY;
    console.log(`✔ ${s.id} : objet détecté x ${s.schema.zone.map((v) => v.toFixed(1)).join('–')} %, y ${s.schema.zone_y.map((v) => v.toFixed(1)).join('–')} %`);
  }
}

// Sound design automatique (règle n°7) : petit souffle à chaque changement de format,
// riser qui monte dans la dernière seconde et demie avant chaque carte de chapitre.
scenes.forEach((s, i) => {
  if (scenes[i + 1]?.format === 'titre' && s.duree > fps * 2)
    s.sons.push({nom: 'riser', a: Math.max(0, s.duree / fps - 1.6), volume: 0.22});
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
// Musique par ambiance (champ "ambiance" des scènes) : un morceau par ambiance, fondus enchaînés entre segments.
// montage.musiques = {"tension": "public/musique/tension.mp3", ...} (fichiers téléchargés par scripts/musique_libre.py)
let musiques;
if (montage.musiques && scenes.some((s) => s.ambiance)) {
  const debuts = [];
  { let t = 0; scenes.forEach((s, i) => { if (i && s.transition !== 'coupe') t -= dureeTransition; debuts.push(t); t += s.duree; }); }
  const segs = [];
  let cour = null;
  scenes.forEach((s, i) => {
    const amb = s.ambiance ?? cour?.amb ?? Object.keys(montage.musiques)[0];
    if (!cour || amb !== cour.amb) { cour = {amb, de: debuts[i]}; segs.push(cour); }
    cour.a = debuts[i] + s.duree;
  });
  // segments trop courts (< 20 s) absorbés par le précédent : la musique ne doit pas zapper
  const fus = [];
  for (const g of segs) { if (fus.length && g.a - g.de < 20 * fps) fus.at(-1).a = g.a; else fus.push({...g}); }
  for (let i = 1; i < fus.length; i++) fus[i].de = fus[i - 1].a;
  const decal = {};
  musiques = fus.filter((g) => montage.musiques[g.amb]).map((g) => {
    const src = montage.musiques[g.amb].replace(/^public\//, '');
    // on reprend le morceau là où on l'avait laissé, modulo sa durée (sinon Remotion refuse de boucler : « empty range »)
    const fichier = path.join('public', src);
    const dMorceau = fs.existsSync(fichier) ? Math.floor(dureeAudio(fichier) * fps) : 0;
    const off = dMorceau > fps ? (decal[g.amb] ?? 0) % dMorceau : 0;
    decal[g.amb] = off + (g.a - g.de);
    return {src, de: g.de, a: g.a, decalage: off};
  });
  console.log('musique :', musiques.map((m) => `${path.basename(m.src)} ${(m.de / fps).toFixed(0)}-${(m.a / fps).toFixed(0)} s`).join(' | '));
}


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
  musiques,
  scenes,
};
fs.writeFileSync(path.join(pub, 'props.json'), JSON.stringify(props, null, 1));
const total = scenes.reduce((a, s) => a + s.duree, 0) - scenes.filter((s, i) => i && s.transition !== 'coupe').length * dureeTransition;
console.log(`✔ timeline : ${scenes.length} scènes, ${(total / fps).toFixed(1)} s → ${path.join(pub, 'props.json')}`);
