// Repérage : pour chaque scène avec "recherche", une planche des 12 meilleurs rushes candidats Pixabay,
// numérotés par leur id. Claude regarde la planche et écrit "pixabay_id" dans la scène choisie.
// Usage : node scripts/reperage.mjs <chemin/montage.json> <dossier de sortie>
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';

const [fichier, sortie = 'out/reperage'] = process.argv.slice(2);
const CLE = process.env.PIXABAY_API_KEY;
if (!CLE) throw new Error('PIXABAY_API_KEY manquante');
const montage = JSON.parse(fs.readFileSync(fichier, 'utf8'));
fs.mkdirSync(sortie, {recursive: true});
const POLICE = ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', '/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf'].find((f) => fs.existsSync(f));
const resume = [];

for (const s of montage.scenes) {
  if (!s.recherche || s.fichier) continue;
  const requetes = Array.isArray(s.recherche) ? s.recherche : [s.recherche];
  const hits = [];
  for (const q of requetes) {
    const r = await fetch(`https://pixabay.com/api/videos/?${new URLSearchParams({key: CLE, q, per_page: '20', safesearch: 'true'})}`);
    for (const h of (await r.json()).hits ?? []) if (!hits.some((x) => x.id === h.id)) hits.push({...h, q});
  }
  const choix = hits.filter((h) => (h.videos.large?.width ?? h.videos.medium.width) >= h.videos.medium.height).slice(0, 12);
  const tmp = fs.mkdtempSync(path.join(sortie, `.${s.id}-`));
  choix.forEach((h, i) => {
    const v = h.videos.medium ?? h.videos.small;
    const vignette = path.join(tmp, `${String(i).padStart(2, '0')}.jpg`);
    // une image au tiers du rush, directement depuis la vidéo (plus fiable que la vignette)
    try {
      execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-ss', String(Math.max(0.5, h.duration / 3)), '-i', v.url, '-frames:v', '1', '-vf',
        `scale=480:270:force_original_aspect_ratio=increase,crop=480:270${POLICE ? `,drawtext=fontfile=${POLICE}:text='${h.id} · ${h.duration}s · ${h.videos.large?.width || v.width}p':x=8:y=8:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.65` : ''}`,
        vignette], {timeout: 60000});
    } catch {
      execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'color=c=black:s=480x270', '-frames:v', '1', vignette]);
    }
  });
  if (choix.length) {
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-pattern_type', 'glob', '-i', path.join(tmp, '*.jpg'), '-vf',
      `tile=4x${Math.ceil(choix.length / 4)}:padding=4:color=0x222222`, '-frames:v', '1', path.join(sortie, `${s.id}.jpg`)]);
  }
  fs.rmSync(tmp, {recursive: true});
  resume.push({scene: s.id, recherche: requetes, candidats: choix.map((h) => ({id: h.id, duree: h.duration, tags: h.tags, requete: h.q}))});
  console.log(`✔ ${s.id} : ${choix.length} candidats`);
}
fs.writeFileSync(path.join(sortie, 'candidats.json'), JSON.stringify(resume, null, 1));
