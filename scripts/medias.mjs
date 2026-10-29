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

async function telecharger(url, dest) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`Téléchargement impossible (${r.status}) : ${url}`);
  fs.writeFileSync(dest, Buffer.from(await r.arrayBuffer()));
}

async function chercherVideo(s) {
  const params = new URLSearchParams({key: CLE, q: s.recherche, per_page: '30', safesearch: 'true', video_type: 'film'});
  const r = await fetch(`https://pixabay.com/api/videos/?${params}`);
  if (!r.ok) throw new Error(`Pixabay a répondu ${r.status} pour "${s.recherche}"`);
  const {hits} = await r.json();
  const besoin = dureeVoulue(s) / (s.vitesse ?? 1);
  const candidats = hits
    .filter((h) => !dejaPris.has(h.id))
    .map((h) => {
      const v = h.videos.large?.url ? h.videos.large : h.videos.medium;
      let score = 0;
      if (v.width >= 1920) score += 3;
      else if (v.width >= 1280) score += 1;
      if (v.width > v.height) score += 3; // paysage
      if (h.duration >= besoin) score += 2;
      score += Math.min(2, (h.downloads ?? 0) / 20000); // popularité = souvent plus beau
      return {h, v, score};
    })
    .filter((c) => c.v?.url)
    .sort((a, b) => b.score - a.score);
  return candidats[0];
}

async function chercherImage(s) {
  const params = new URLSearchParams({key: CLE, q: s.recherche, per_page: '30', safesearch: 'true', image_type: 'photo', orientation: 'horizontal'});
  const r = await fetch(`https://pixabay.com/api/?${params}`);
  if (!r.ok) throw new Error(`Pixabay a répondu ${r.status} pour "${s.recherche}"`);
  const {hits} = await r.json();
  return hits.find((h) => !dejaPris.has(h.id));
}

function fauxRush(s, dest) {
  const couleurs = ['0x1b2a4a', '0x4a1c3a', '0x1c4a3a', '0x4a3a1c'];
  const c = couleurs[parseInt(s.id.replace(/\D/g, '') || '0', 10) % couleurs.length];
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'lavfi', '-i', `testsrc2=size=1920x1080:rate=30,colorchannelmixer=.5:0:0:0:0:.5:0:0:0:0:.5,drawbox=c=${c}@0.6:t=fill`, '-t', '8', '-pix_fmt', 'yuv420p', dest]);
}

for (const s of montage.scenes) {
  const existant = fs.readdirSync(sortie).find((f) => f.startsWith(`${s.id}.`));
  if (s.fichier) {
    const src = path.join(dossierEp, s.fichier);
    const dest = path.join(sortie, `${s.id}${path.extname(src).toLowerCase()}`);
    fs.copyFileSync(src, dest);
    console.log(`✔ ${s.id} : ton média ${s.fichier}`);
    continue;
  }
  if (!s.recherche) continue;
  if (existant) {
    console.log(`↺ ${s.id} : déjà téléchargé (${existant})`);
    continue;
  }
  const estImage = s.type === 'image';
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
