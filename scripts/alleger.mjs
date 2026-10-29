// Allège les rushes après la timeline : coupe chaque vidéo à la durée vraiment utilisée, 1080p max, sans son.
// Les rushes Pixabay "large" font souvent 20-60 Mo : ici ~2-6 Mo, décodage plus rapide au rendu.
// Usage : node scripts/alleger.mjs <slug>
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';

const slug = process.argv[2];
const pub = path.join('public', 'ep', slug);
const props = JSON.parse(fs.readFileSync(path.join(pub, 'props.json'), 'utf8'));
let gain = 0;
const traiter = (src, secondes) => {
  const f = path.join('public', src);
  if (!fs.existsSync(f) || !/\.(mp4|webm|mov)$/i.test(f)) return;
  const avant = fs.statSync(f).size;
  const tmp = f.replace(/\.[^.]+$/, '.leger.mp4');
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', f, '-t', secondes.toFixed(2), '-an',
    '-vf', "scale='min(1920,iw)':-2,fps=30", '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', tmp]);
  fs.renameSync(tmp, f.replace(/\.[^.]+$/, '.mp4'));
  if (!f.endsWith('.mp4')) fs.rmSync(f);
  gain += avant - fs.statSync(f.replace(/\.[^.]+$/, '.mp4')).size;
};
for (const s of props.scenes) {
  // la vidéo boucle si le rush est trop court : on garde assez pour la scène entière
  const besoin = s.debutMedia + (s.duree / props.fps) * (s.vitesse || 1) + 1;
  if (s.media) traiter(s.media, besoin);
  for (const m of s.medias ?? []) traiter(m.src, s.duree / props.fps + 1);
}
console.log(`✔ rushes allégés : ${(gain / 1e6).toFixed(0)} Mo économisés`);
