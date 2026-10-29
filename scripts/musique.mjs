// Musique de fond "documentaire / enquête" synthétisée (gratuite, libre de droits, déterministe).
// 32 mesures à 96 BPM (80 s) qui bouclent sans couture : nappe, basse, arpège, pulsation légère qui entrent par sections.
// Usage : node scripts/musique.mjs [sortie.wav]   (par défaut public/sfx/musique-enquete.wav)
import fs from 'node:fs';
import path from 'node:path';

const SR = 48000;
const dest = process.argv[2] ?? path.join('public', 'sfx', 'musique-enquete.wav');
if (fs.existsSync(dest)) { console.log(`↺ musique déjà là : ${dest}`); process.exit(0); }
const BPM = 96, TEMPS = 60 / BPM, MESURE = 4 * TEMPS, NB = 32;
const n = Math.round(NB * MESURE * SR);
const L = new Float32Array(n), R = new Float32Array(n);
let seed = 42;
const rnd = () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296) * 2 - 1;
const hz = (midi) => 440 * Math.pow(2, (midi - 69) / 12);

// Am F C G | Am F Dm E (la tension de l'enquête), répété
const ACCORDS = [[57, 60, 64], [53, 57, 60], [55, 60, 64], [55, 59, 62], [57, 60, 64], [53, 57, 60], [50, 53, 57], [52, 56, 59]];
const ajoute = (buf, i0, x) => { buf[(i0 % n + n) % n] += x; };

function note(t0, dur, f, gain, {attaque = 0.01, relache = 0.3, harm = [1], pan = 0, detune = 0, decroit = 0} = {}) {
  const i0 = Math.round(t0 * SR), len = Math.round((dur + relache) * SR);
  const gl = gain * Math.min(1, 1 - pan), gr = gain * Math.min(1, 1 + pan);
  for (let i = 0; i < len; i++) {
    const t = i / SR;
    let env = t < attaque ? t / attaque : 1;
    if (t > dur) env *= Math.max(0, 1 - (t - dur) / relache);
    if (decroit) env *= Math.exp(-t * decroit);
    let s = 0, s2 = 0;
    harm.forEach((a, k) => {
      s += a * Math.sin(2 * Math.PI * f * (k + 1) * t);
      if (detune) s2 += a * Math.sin(2 * Math.PI * f * (1 + detune) * (k + 1) * t + 1.3);
    });
    const v = detune ? (s + s2) / 2 : s;
    ajoute(L, i0 + i, v * env * gl);
    ajoute(R, i0 + i, (detune ? (s2 + s) / 2 : v) * env * gr);
  }
}

for (let b = 0; b < NB; b++) {
  const t = b * MESURE, acc = ACCORDS[b % 8], section = Math.floor(b / 8);
  // nappe : accord tenu, légèrement désaccordé (stéréo large)
  acc.forEach((m, k) => note(t, MESURE, hz(m), 0.11, {attaque: 0.6, relache: 1.2, harm: [1, 0.5, 0.33, 0.25, 0.18, 0.12, 0.08], detune: 0.004, pan: (k - 1) * 0.35}));
  // basse
  note(t, MESURE * 0.92, hz(acc[0] - 24), 0.13, {attaque: 0.05, relache: 0.4, harm: [1, 0.25]});
  // arpège "pluck" en croches à partir de la section 2
  if (section >= 1) {
    const motif = section === 3 ? [0, 2, 1, 2, 0, 2, 1, 3] : [0, 1, 2, 1, 0, 1, 2, 3];
    motif.forEach((k, j) => {
      const m = k === 3 ? acc[0] + 12 : acc[k] + 12;
      const tt = t + j * TEMPS / 2;
      const p = j % 2 ? 0.45 : -0.45;
      note(tt, 0.05, hz(m), 0.12, {attaque: 0.004, relache: 0.4, harm: [1, 0.6, 0.35, 0.2, 0.12], decroit: 6, pan: p});
      note(tt + TEMPS * 0.75, 0.05, hz(m), 0.03, {attaque: 0.004, relache: 0.4, harm: [1, 0.3], decroit: 6, pan: -p}); // écho
    });
  }
  // pulsation discrète (sections 3 et 4) : grosse caisse feutrée sur 1 et 3, charleston sur les contretemps
  if (section >= 2) {
    for (const k of [0, 2]) {
      const i0 = Math.round((t + k * TEMPS) * SR);
      let ph = 0;
      for (let i = 0; i < SR * 0.35; i++) {
        const tt = i / SR; ph += (2 * Math.PI * (45 + 75 * Math.exp(-tt * 30))) / SR;
        const v = Math.sin(ph) * Math.exp(-tt * 9) * 0.16;
        ajoute(L, i0 + i, v); ajoute(R, i0 + i, v);
      }
    }
    for (let k = 0; k < 4; k++) {
      const i0 = Math.round((t + (k + 0.5) * TEMPS) * SR);
      let y = 0;
      for (let i = 0; i < SR * 0.05; i++) {
        const x = rnd(); const hp = x - y; y = x * 0.6 + y * 0.4;
        const v = hp * Math.exp(-(i / SR) * 90) * 0.07;
        ajoute(L, i0 + i, v * 0.8); ajoute(R, i0 + i, v);
      }
    }
  }
}

// passe-bas doux global (chaleur) + normalisation à -3 dBFS
const pb = (buf, fc) => { const a = Math.exp((-2 * Math.PI * fc) / SR); let y = buf[n - 1]; for (let i = 0; i < n; i++) { y = (1 - a) * buf[i] + a * y; buf[i] = y; } };
pb(L, 5200); pb(R, 5200);
let max = 1e-9;
for (let i = 0; i < n; i++) max = Math.max(max, Math.abs(L[i]), Math.abs(R[i]));
const g = 0.707 / max;
const buf = Buffer.alloc(44 + n * 4);
buf.write('RIFF', 0); buf.writeUInt32LE(36 + n * 4, 4); buf.write('WAVE', 8); buf.write('fmt ', 12);
buf.writeUInt32LE(16, 16); buf.writeUInt16LE(1, 20); buf.writeUInt16LE(2, 22); buf.writeUInt32LE(SR, 24);
buf.writeUInt32LE(SR * 4, 28); buf.writeUInt16LE(4, 32); buf.writeUInt16LE(16, 34); buf.write('data', 36); buf.writeUInt32LE(n * 4, 40);
for (let i = 0; i < n; i++) {
  buf.writeInt16LE(Math.round(Math.max(-1, Math.min(1, L[i] * g)) * 32767), 44 + i * 4);
  buf.writeInt16LE(Math.round(Math.max(-1, Math.min(1, R[i] * g)) * 32767), 46 + i * 4);
}
fs.mkdirSync(path.dirname(dest), {recursive: true});
fs.writeFileSync(dest, buf);
console.log(`✔ musique : ${dest} (${(n / SR).toFixed(1)} s, boucle sans couture)`);
