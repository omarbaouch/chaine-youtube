// Planche de contrôle : une image au milieu de chaque scène, en mosaïque (pour relire le montage d'un coup d'œil).
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';

const [slug, video] = process.argv.slice(2);
const props = JSON.parse(fs.readFileSync(path.join('public', 'ep', slug, 'props.json'), 'utf8'));
const tmp = fs.mkdtempSync(path.join('out', '.planche-'));
let t = 0;
props.scenes.forEach((s, i) => {
  if (i && s.transition !== 'coupe') t -= props.dureeTransition;
  const milieu = (t + s.voixDebut + Math.min(s.duree - s.voixDebut, 45)) / props.fps; // un peu après le début de la voix : sous-titre visible
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-ss', milieu.toFixed(2), '-i', video, '-frames:v', '1', '-vf',
    `scale=480:-1,drawtext=text='${s.id}':x=w-tw-10:y=h-th-10:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.6`, path.join(tmp, `${String(i).padStart(3, '0')}.jpg`)]);
  t += s.duree;
});
const n = props.scenes.length;
const cols = Math.min(4, n);
const dest = video.replace(/\.mp4$/, '-planche.jpg');
execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-pattern_type', 'glob', '-i', path.join(tmp, '*.jpg'), '-vf', `tile=${cols}x${Math.ceil(n / cols)}:padding=6:margin=6`, '-frames:v', '1', dest]);
fs.rmSync(tmp, {recursive: true});
console.log(`✔ planche : ${dest}`);
