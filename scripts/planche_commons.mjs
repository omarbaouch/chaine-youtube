// Planches « contact » de vidéos Wikimedia Commons : une image toutes les N secondes, horodatée,
// pour choisir un passage précis (media_ref wc:File:… + debut_media) dans un reportage libre.
// Usage : node scripts/planche_commons.mjs <sortie> "<requête1>|<requête2>" ["wc:File:a.webm|wc:File:b.webm"]
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';

const [sortie, requetes = '', refs = ''] = process.argv.slice(2);
const UA = {'User-Agent': 'chaine-youtube-reperage/1.0 (github.com/omarbaouch/chaine-youtube)'};
const POLICE = ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'].find((f) => fs.existsSync(f));
const pause = (ms) => new Promise((r) => setTimeout(r, ms));
fs.mkdirSync(sortie, {recursive: true});

async function api(params) {
  for (let i = 0; i < 6; i++) {
    await pause(1000);
    const r = await fetch(`https://commons.wikimedia.org/w/api.php?${new URLSearchParams({...params, format: 'json'})}`, {headers: UA});
    const t = await r.text();
    if (r.status === 429 || t.startsWith('You are making')) { await pause(5000 * 2 ** i); continue; }
    return JSON.parse(t);
  }
  throw new Error('429');
}

const titres = new Set(refs.split('|').filter(Boolean).map((r) => r.replace(/^wc:/, '')));
for (const q of requetes.split('|').filter(Boolean)) {
  const j = await api({action: 'query', list: 'search', srsearch: `${q} filetype:video`, srnamespace: '6', srlimit: '10'});
  for (const x of j.query?.search ?? []) titres.add(x.title);
}
const index = [];
let n = 0;
for (const titre of titres) {
  if (n >= 14) break;
  try {
    const j = await api({action: 'query', titles: titre, prop: 'imageinfo|videoinfo', iiprop: 'url|mime|size|extmetadata', viprop: 'url|size|mime|derivatives'});
    const ii = Object.values(j.query.pages)[0].imageinfo?.[0];
    if (!ii || !ii.mime.startsWith('video/')) continue;
    const code = `F${n + 1}`;
    const dest = path.join(sortie, `${code}.jpg`);
    const txt = POLICE ? `,drawtext=fontfile=${POLICE}:text='%{pts\\:hms}':x=6:y=6:fontsize=20:fontcolor=white:box=1:boxcolor=black@0.7` : '';
    const brut = path.join(sortie, `${code}.source`);
    const r = await fetch(ii.url, {headers: UA});
    fs.writeFileSync(brut, Buffer.from(await r.arrayBuffer()));
    const duree = Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', brut]).toString().trim()) || 0;
    if (duree < 8) { fs.rmSync(brut); continue; }
    const pas = Math.max(2, Math.ceil(duree / 60));
    n++;
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', brut, '-vf', `fps=1/${pas},scale=320:180:force_original_aspect_ratio=increase,crop=320:180,setpts=PTS*${pas}${txt},tile=6x10:padding=3:color=0x222222`, '-frames:v', '1', dest], {timeout: 600000});
    fs.rmSync(brut);
    const m = ii.extmetadata ?? {};
    index.push({code, ref: `wc:${titre}`, duree, pas, largeur: ii.width, licence: m.LicenseShortName?.value, auteur: (m.Artist?.value ?? '').replace(/<[^>]+>/g, '').trim().slice(0, 80)});
    console.log(`✔ ${code} ${titre} (${duree} s, une image toutes les ${pas} s)`);
  } catch (e) { console.warn(`  ${titre} : ${e.message}`); }
}
fs.writeFileSync(path.join(sortie, 'index.json'), JSON.stringify(index, null, 1));
