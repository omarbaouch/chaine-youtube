// Repérage multi-sources : pour chaque scène avec "recherche", une planche de candidats réels numérotés.
//   V<n> = vidéo Pixabay · I<n> = photo Pixabay · C<n> = fichier Wikimedia Commons (photo/vidéo, libre avec crédit)
// Claude regarde la planche et écrit dans la scène : "media_ref": "pv:<id>" | "pi:<id>" | "wc:File:<titre>"
// (le code ↔ ref est dans <scene>-candidats.json). Ancien champ "pixabay_id" toujours accepté (= pv:<id>).
// Usage : node scripts/reperage.mjs <chemin/montage.json> <dossier de sortie>
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';

const [fichier, sortie = 'out/reperage'] = process.argv.slice(2);
const CLE = process.env.PIXABAY_API_KEY;
if (!CLE) throw new Error('PIXABAY_API_KEY manquante');
const UA = {'User-Agent': 'chaine-youtube-reperage/1.0 (github.com/omarbaouch/chaine-youtube)'};
const montage = JSON.parse(fs.readFileSync(fichier, 'utf8'));
fs.mkdirSync(sortie, {recursive: true});
const POLICE = ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', '/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf'].find((f) => fs.existsSync(f));
const tous = {};

async function pixabayVideos(q) {
  const r = await fetch(`https://pixabay.com/api/videos/?${new URLSearchParams({key: CLE, q, per_page: '12', safesearch: 'true'})}`);
  return ((await r.json()).hits ?? []).map((h) => ({ref: `pv:${h.id}`, apercu: (h.videos.medium ?? h.videos.small).url, video: true, duree: h.duration,
    info: `${h.duration}s`, tags: h.tags, credit: `Pixabay (${h.user})`}));
}
async function pixabayPhotos(q) {
  const r = await fetch(`https://pixabay.com/api/?${new URLSearchParams({key: CLE, q, per_page: '12', safesearch: 'true', image_type: 'photo', orientation: 'horizontal'})}`);
  return ((await r.json()).hits ?? []).map((h) => ({ref: `pi:${h.id}`, apercu: h.webformatURL, video: false, info: `${h.imageWidth}px`, tags: h.tags, credit: `Pixabay (${h.user})`}));
}
async function commons(q) {
  const p = new URLSearchParams({action: 'query', generator: 'search', gsrsearch: q, gsrnamespace: '6', gsrlimit: '12', prop: 'imageinfo',
    iiprop: 'url|size|mime|extmetadata', iiurlwidth: '960', format: 'json', origin: '*'});
  const r = await fetch(`https://commons.wikimedia.org/w/api.php?${p}`, {headers: UA});
  const pages = Object.values((await r.json()).query?.pages ?? {});
  return pages
    .map((pg) => ({pg, ii: pg.imageinfo?.[0]}))
    .filter(({ii}) => ii && /^(image\/(jpeg|png|webp)|video\/)/.test(ii.mime) && (ii.width ?? 0) >= 1000)
    .map(({pg, ii}) => {
      const m = ii.extmetadata ?? {};
      const auteur = (m.Artist?.value ?? '').replace(/<[^>]+>/g, '').trim().slice(0, 60);
      return {ref: `wc:${pg.title}`, apercu: ii.mime.startsWith('video/') ? ii.url : (ii.thumburl ?? ii.url), video: ii.mime.startsWith('video/'),
        info: `${ii.width}px`, tags: pg.title, credit: `Wikimedia Commons, ${auteur || 'auteur inconnu'}, ${m.LicenseShortName?.value ?? 'licence ?'}`};
    });
}

function vignette(c, code, dest) {
  const texte = `${code} · ${c.info}`.replace(/[':]/g, ' ');
  const filtre = `scale=480:270:force_original_aspect_ratio=increase,crop=480:270${POLICE ? `,drawtext=fontfile=${POLICE}:text='${texte}':x=8:y=8:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.7` : ''}`;
  const args = c.video ? ['-ss', String(Math.max(0.5, (c.duree ?? 6) / 3))] : [];
  try {
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', ...args, '-user_agent', UA['User-Agent'], '-i', c.apercu, '-frames:v', '1', '-vf', filtre, dest], {timeout: 90000});
  } catch {
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'color=c=black:s=480x270', '-frames:v', '1', dest]);
  }
}

for (const s of montage.scenes) {
  if (!s.recherche || s.fichier) continue;
  const requetes = Array.isArray(s.recherche) ? s.recherche : [s.recherche];
  const vus = new Set();
  const groupes = {V: [], I: [], C: []};
  for (const q of requetes) {
    for (const [cle, fn] of [['V', pixabayVideos], ['I', pixabayPhotos], ['C', commons]]) {
      try {
        for (const c of await fn(q)) if (!vus.has(c.ref)) { vus.add(c.ref); groupes[cle].push({...c, q}); }
      } catch (e) { console.warn(`  ${cle} "${q}" : ${e.message}`); }
    }
  }
  // 8 vidéos, 8 photos, 8 Commons au maximum → planche de 24 vignettes
  const choix = [...groupes.V.slice(0, 8).map((c, i) => ({...c, code: `V${i + 1}`})), ...groupes.I.slice(0, 8).map((c, i) => ({...c, code: `I${i + 1}`})),
    ...groupes.C.slice(0, 8).map((c, i) => ({...c, code: `C${i + 1}`}))];
  const tmp = fs.mkdtempSync(path.join(sortie, `.${s.id}-`));
  choix.forEach((c, i) => vignette(c, c.code, path.join(tmp, `${String(i).padStart(2, '0')}.jpg`)));
  if (choix.length) {
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-pattern_type', 'glob', '-i', path.join(tmp, '*.jpg'), '-vf',
      `tile=4x${Math.ceil(choix.length / 4)}:padding=4:color=0x222222`, '-frames:v', '1', path.join(sortie, `${s.id}.jpg`)]);
  }
  fs.rmSync(tmp, {recursive: true});
  tous[s.id] = choix.map(({code, ref, info, tags, credit, q}) => ({code, ref, info, tags, credit, requete: q}));
  console.log(`✔ ${s.id} : ${groupes.V.length} vidéos, ${groupes.I.length} photos, ${groupes.C.length} Commons → ${choix.length} sur la planche`);
}
fs.writeFileSync(path.join(sortie, 'candidats.json'), JSON.stringify(tous, null, 1));
