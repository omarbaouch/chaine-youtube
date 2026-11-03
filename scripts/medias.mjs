// Récupère les rushes de chaque scène dans public/ep/<slug>/media/
//  - scène avec "fichier"   : copie ton propre média (chemin relatif au dossier de l'épisode)
//  - scène avec "recherche" : cherche et télécharge un rush gratuit sur Pixabay (clé PIXABAY_API_KEY)
// Sans clé (ex. test local), un faux rush est généré pour pouvoir quand même tester le montage.
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';

const slug = process.argv[2];
if (!slug) throw new Error('Usage : node scripts/medias.mjs <slug>');
const dossierEp = path.join('episodes', slug);
const montage = JSON.parse(fs.readFileSync(path.join(dossierEp, 'montage.json'), 'utf8'));
const sortie = path.join('public', 'ep', slug, 'media');
fs.mkdirSync(sortie, {recursive: true});
const CLE = process.env.PIXABAY_API_KEY;
const credits = [];
const dejaPris = new Set();

const motsParSeconde = 2.6;
const dureeVoulue = (s) => Math.max(s.duree_min ?? 0, (s.texte ? s.texte.split(/\s+/).length / motsParSeconde : 3) + 1);

// Pixabay limite le débit (HTTP 429) : on espace les appels et on réessaie avec une attente croissante.
const pause = (ms) => new Promise((r) => setTimeout(r, ms));
const fetchBrut = globalThis.fetch;
let dernier = 0;
globalThis.fetch = async (url, opts) => {
  for (let essai = 0; ; essai++) {
    const attente = dernier + 700 - Date.now();
    if (attente > 0) await pause(attente);
    dernier = Date.now();
    const r = await fetchBrut(url, opts);
    if ((r.status === 429 || r.status >= 500) && essai < 8) {
      const ra = parseFloat(r.headers.get('retry-after') ?? '');
      const ms = Number.isFinite(ra) ? ra * 1000 : Math.min(60000, 4000 * 2 ** essai);
      console.warn(`  … ${r.status}, nouvel essai dans ${(ms / 1000).toFixed(0)} s`);
      await pause(ms);
      continue;
    }
    return r;
  }
};

async function telecharger(url, dest) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`Téléchargement impossible (${r.status}) : ${url}`);
  fs.writeFileSync(dest, Buffer.from(await r.arrayBuffer()));
}

// Rush choisi au repérage (scripts/reperage.mjs) : "pixabay_id" dans la scène → ce rush précis, sans deviner.
async function videoParId(id) {
  const r = await fetch(`https://pixabay.com/api/videos/?${new URLSearchParams({key: CLE, id: String(id)})}`);
  if (!r.ok) throw new Error(`Pixabay a répondu ${r.status} pour l'id ${id}`);
  const h = (await r.json()).hits[0];
  if (!h) throw new Error(`Rush Pixabay ${id} introuvable`);
  return {h, v: h.videos.large?.url ? h.videos.large : h.videos.medium};
}

async function chercherVideo(s) {
  if (s.pixabay_id) return videoParId(s.pixabay_id);
  const requetes = Array.isArray(s.recherche) ? s.recherche : [s.recherche];
  const hits = [];
  for (const q of requetes) {
    const params = new URLSearchParams({key: CLE, q, per_page: '30', safesearch: 'true', video_type: 'film'});
    const r = await fetch(`https://pixabay.com/api/videos/?${params}`);
    if (!r.ok) throw new Error(`Pixabay a répondu ${r.status} pour "${q}"`);
    hits.push(...(await r.json()).hits.filter((h) => !hits.some((x) => x.id === h.id)));
  }
  const besoin = dureeVoulue(s) / (s.vitesse ?? 1);
  const candidats = hits
    .filter((h) => !dejaPris.has(h.id))
    .map((h, rang) => {
      const v = h.videos.large?.url ? h.videos.large : h.videos.medium;
      let score = Math.max(0, 6 - rang * 0.4); // la pertinence Pixabay compte le plus
      if (v.width >= 1920) score += 3;
      else if (v.width >= 1280) score += 1;
      if (v.width > v.height) score += 3; // paysage
      if (h.duration >= besoin) score += 2;
      score += Math.min(1, (h.downloads ?? 0) / 40000); // popularité = souvent plus beau
      return {h, v, score};
    })
    .filter((c) => c.v?.url)
    .sort((a, b) => b.score - a.score);
  return candidats[0];
}

async function chercherImage(s) {
  const q = Array.isArray(s.recherche) ? s.recherche[0] : s.recherche;
  const params = new URLSearchParams({key: CLE, q, per_page: '30', safesearch: 'true', image_type: 'photo', orientation: 'horizontal'});
  const r = await fetch(`https://pixabay.com/api/?${params}`);
  if (!r.ok) throw new Error(`Pixabay a répondu ${r.status} pour "${s.recherche}"`);
  const {hits} = await r.json();
  return hits.find((h) => !dejaPris.has(h.id));
}

// Média choisi au repérage multi-sources : "pv:<id>" vidéo Pixabay, "pi:<id>" photo Pixabay, "wc:File:<titre>" Wikimedia Commons.
const UA = {'User-Agent': 'chaine-youtube-medias/1.0 (github.com/omarbaouch/chaine-youtube)'};
async function telechargerRef(s) {
  const [src, ...reste] = s.media_ref.split(':');
  // "extrait": secondes de début d'un passage précis d'un long reportage Commons (planches scripts/planche_commons.mjs) ; 30 s gardées
  const cleRush = s.extrait != null ? `${s.media_ref}@${s.extrait}` : s.media_ref;
  const suffixe = JSON.stringify([s.extrait_duree, s.recadre]);
  if (dejaPris.has(cleRush)) console.warn(`⚠ ${s.id} : ${cleRush} déjà utilisé dans ce montage (règle : un rush ne sert qu'une fois)`);
  dejaPris.add(cleRush);
  const id = reste.join(':');
  if (src === 'pv') {
    const c = await videoParId(id);
    await telecharger(c.v.url, path.join(sortie, `${s.id}.mp4`));
    credits.push(`${s.id} : https://pixabay.com/videos/id-${id}/ (Pixabay, ${c.h.user})`);
  } else if (src === 'pi') {
    const r = await fetch(`https://pixabay.com/api/?${new URLSearchParams({key: CLE, id})}`);
    const h = (await r.json()).hits?.[0];
    if (!h) throw new Error(`Photo Pixabay ${id} introuvable`);
    await telecharger(h.largeImageURL, path.join(sortie, `${s.id}.jpg`));
    credits.push(`${s.id} : ${h.pageURL} (Pixabay, ${h.user})`);
  } else if (src === 'wc') {
    const p = new URLSearchParams({action: 'query', titles: id, prop: 'imageinfo', iiprop: 'url|mime|extmetadata', iiurlwidth: '2400', format: 'json'});
    const pg = Object.values((await (await fetch(`https://commons.wikimedia.org/w/api.php?${p}`, {headers: UA})).json()).query.pages)[0];
    const ii = pg.imageinfo[0];
    const m = ii.extmetadata ?? {};
    if (ii.mime.startsWith('video/')) {
      const brut = path.join(sortie, `${s.id}.source`);
      const rr = await fetch(ii.url, {headers: UA});
      fs.writeFileSync(brut, Buffer.from(await rr.arrayBuffer()));
      execFileSync('ffmpeg', ['-y', '-loglevel', 'error', ...(s.extrait != null ? ['-ss', String(s.extrait), '-t', String(s.extrait_duree ?? 30)] : []), '-i', brut,
        // "recadre": [x, y, taille] en fractions : garde un cadre 16:9 (enlève logos et sous-titres incrustés d'origine)
        ...(s.recadre ? ['-vf', `crop=iw*${s.recadre[2]}:ih*${s.recadre[2]}:iw*${s.recadre[0]}:ih*${s.recadre[1]},scale=1920:1080`] : []),
        ...(s.temoignage ? ['-c:a', 'aac', '-b:a', '192k'] : ['-an']), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', path.join(sortie, `${s.id}.mp4`)]);
      fs.rmSync(brut);
    } else {
      const rr = await fetch(ii.thumburl ?? ii.url, {headers: UA});
      fs.writeFileSync(path.join(sortie, `${s.id}.jpg`), Buffer.from(await rr.arrayBuffer()));
    }
    const auteur = (m.Artist?.value ?? '').replace(/<[^>]+>/g, '').trim();
    credits.push(`${s.id} : ${ii.descriptionurl ?? `https://commons.wikimedia.org/wiki/${encodeURIComponent(id)}`} (Wikimedia Commons, ${auteur}, ${m.LicenseShortName?.value ?? ''})`);
  } else {
    throw new Error(`media_ref inconnu : ${s.media_ref}`);
  }
  console.log(`✔ ${s.id} : ${s.media_ref}`);
}

function fauxRush(s, dest) {
  const couleurs = ['0x1b2a4a', '0x4a1c3a', '0x1c4a3a', '0x4a3a1c'];
  const c = couleurs[parseInt(s.id.replace(/\D/g, '') || '0', 10) % couleurs.length];
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'lavfi', '-i', `testsrc2=size=1920x1080:rate=30,colorchannelmixer=.5:0:0:0:0:.5:0:0:0:0:.5,drawbox=c=${c}@0.6:t=fill`, '-t', '8', '-pix_fmt', 'yuv420p', dest]);
}

// Cache des rushes : un fichier <id>.ref garde la référence du média ; si le montage change de média, on retélécharge.
const refPath = (id) => path.join(sortie, `${id}.ref`);
// Ancien cache sans .ref : on fait confiance, sauf pour les ids listés dans montage.rushes_a_refaire.
const aRefaire = new Set(montage.rushes_a_refaire ?? []);
const memeRef = (id, cle) => !aRefaire.has(id) && (!fs.existsSync(refPath(id)) || fs.readFileSync(refPath(id), 'utf8') === String(cle));
const noterRef = (id, cle) => fs.writeFileSync(refPath(id), String(cle));
const purger = (id) => { for (const f of fs.readdirSync(sortie)) if (f.startsWith(`${id}.`) && !f.endsWith('.ref')) fs.rmSync(path.join(sortie, f)); };

// Médias multiples (mosaïque, écran partagé) : "medias": [{"media_ref": "pv:…", "legende": "…"}, {"fichier": "…"}]
// → public/ep/<slug>/media/<id>-1.ext, <id>-2.ext…
for (const s of montage.scenes) {
  (s.medias ?? []).forEach((m, k) => (m._id = `${s.id}-${k + 1}`));
}
for (const s of montage.scenes) {
  for (const m of s.medias ?? []) {
    const existant = fs.readdirSync(sortie).find((f) => f.startsWith(`${m._id}.`) && !f.endsWith('.ref'));
    const cle = (m.fichier ?? m.media_ref ?? '') + (m.extrait != null ? `@${m.extrait}` : '') + (m.recadre || m.extrait_duree ? JSON.stringify([m.extrait_duree, m.recadre]) : '');
    if (existant && memeRef(m._id, cle)) { console.log(`↺ ${m._id} : déjà téléchargé`); continue; }
    if (existant) purger(m._id);
    noterRef(m._id, cle);
    if (m.fichier) {
      const src = path.join(dossierEp, m.fichier);
      fs.copyFileSync(src, path.join(sortie, `${m._id}${path.extname(src).toLowerCase()}`));
      continue;
    }
    if (!CLE) {
      if (/^(pi|wc):/.test(m.media_ref ?? '') && !/\.(webm|ogv|mp4|mpg)$/i.test(m.media_ref)) {
        execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'testsrc2=size=1920x1080', '-frames:v', '1', path.join(sortie, `${m._id}.jpg`)]);
      } else fauxRush({id: m._id}, path.join(sortie, `${m._id}.mp4`));
      continue;
    }
    await telechargerRef({id: m._id, media_ref: m.media_ref, extrait: m.extrait, extrait_duree: m.extrait_duree, recadre: m.recadre});
  }
}

for (const s of montage.scenes) {
  let existant = fs.readdirSync(sortie).find((f) => f.startsWith(`${s.id}.`) && !f.endsWith('.ref'));
  const cle = (s.fichier ?? s.media_ref ?? s.pixabay_id ?? JSON.stringify(s.recherche ?? '')) + (s.extrait != null ? `@${s.extrait}` : '') + (s.recadre || s.extrait_duree ? JSON.stringify([s.extrait_duree, s.recadre]) : '');
  if (existant && !memeRef(s.id, cle)) { purger(s.id); existant = undefined; }
  if (s.recherche || s.pixabay_id || s.media_ref || s.fichier) noterRef(s.id, cle);
  if (s.fichier) {
    const src = path.join(dossierEp, s.fichier);
    const dest = path.join(sortie, `${s.id}${path.extname(src).toLowerCase()}`);
    fs.copyFileSync(src, dest);
    console.log(`✔ ${s.id} : ton média ${s.fichier}`);
    continue;
  }
  if (!s.recherche && !s.pixabay_id && !s.media_ref) continue;
  if (existant) {
    console.log(`↺ ${s.id} : déjà téléchargé (${existant})`);
    continue;
  }
  if (s.media_ref && CLE) {
    await telechargerRef(s);
    continue;
  }
  const estImage = s.type === 'image' || (/^(pi|wc):/.test(s.media_ref ?? '') && !/\.(webm|ogv|mp4|mpg)$/i.test(s.media_ref));
  if (!CLE) {
    console.warn(`⚠ ${s.id} : pas de PIXABAY_API_KEY → faux rush de test`);
    if (estImage) execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'testsrc2=size=1920x1080', '-frames:v', '1', path.join(sortie, `${s.id}.jpg`)]);
    else fauxRush(s, path.join(sortie, `${s.id}.mp4`));
    continue;
  }
  if (estImage) {
    const h = await chercherImage(s);
    if (!h) throw new Error(`Aucune image Pixabay pour "${s.recherche}" (scène ${s.id}) : change la recherche.`);
    dejaPris.add(h.id);
    await telecharger(h.largeImageURL, path.join(sortie, `${s.id}.jpg`));
    credits.push(`${s.id} : ${h.pageURL} (par ${h.user})`);
    console.log(`✔ ${s.id} : image "${s.recherche}" → ${h.pageURL}`);
  } else {
    const c = await chercherVideo(s);
    if (!c) throw new Error(`Aucune vidéo Pixabay pour "${s.recherche}" (scène ${s.id}) : change la recherche.`);
    dejaPris.add(c.h.id);
    await telecharger(c.v.url, path.join(sortie, `${s.id}.mp4`));
    credits.push(`${s.id} : https://pixabay.com/videos/id-${c.h.id}/ (par ${c.h.user})`);
    console.log(`✔ ${s.id} : vidéo "${s.recherche}" ${c.v.width}x${c.v.height}, ${c.h.duration}s`);
  }
}

if (montage.musique?.fichier) {
  const src = path.join(dossierEp, montage.musique.fichier);
  fs.copyFileSync(src, path.join('public', 'ep', slug, `musique${path.extname(src)}`));
  console.log(`✔ musique : ${montage.musique.fichier}`);
}
if (credits.length) fs.appendFileSync(path.join('public', 'ep', slug, 'credits.txt'), credits.join('\n') + '\n');
