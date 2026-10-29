// Kit de bruitages synthétisés (déterministes, libres de droits) → public/sfx/*.wav
// whoosh, impact, metal (choc métallique d'usine), riser, tick, pop, nappe (ambiance 20 s).
import fs from 'node:fs';
import path from 'node:path';

const SR = 48000;
const OUT = path.join('public', 'sfx');
fs.mkdirSync(OUT, {recursive: true});

let seed = 1234567;
const rnd = () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296) * 2 - 1;

function ecrire(nom, L, R = L) {
  const n = L.length;
  const buf = Buffer.alloc(44 + n * 4);
  buf.write('RIFF', 0); buf.writeUInt32LE(36 + n * 4, 4); buf.write('WAVE', 8); buf.write('fmt ', 12);
  buf.writeUInt32LE(16, 16); buf.writeUInt16LE(1, 20); buf.writeUInt16LE(2, 22); buf.writeUInt32LE(SR, 24);
  buf.writeUInt32LE(SR * 4, 28); buf.writeUInt16LE(4, 32); buf.writeUInt16LE(16, 34); buf.write('data', 36); buf.writeUInt32LE(n * 4, 40);
  let max = 1e-9;
  for (let i = 0; i < n; i++) max = Math.max(max, Math.abs(L[i]), Math.abs(R[i]));
  const g = 0.89 / max; // normalise à -1 dBFS
  for (let i = 0; i < n; i++) {
    buf.writeInt16LE(Math.round(Math.max(-1, Math.min(1, L[i] * g)) * 32767), 44 + i * 4);
    buf.writeInt16LE(Math.round(Math.max(-1, Math.min(1, R[i] * g)) * 32767), 46 + i * 4);
  }
  fs.writeFileSync(path.join(OUT, `${nom}.wav`), buf);
}

// Filtre biquad (RBJ) passe-bande / passe-bas, coefficients recalculés à la volée.
function biquad() {
  let x1 = 0, x2 = 0, y1 = 0, y2 = 0;
  return (x, type, f, q = 0.9) => {
    const w = (2 * Math.PI * Math.min(f, SR * 0.45)) / SR, a = Math.sin(w) / (2 * q), c = Math.cos(w);
    let b0, b1, b2;
    if (type === 'bp') { b0 = a; b1 = 0; b2 = -a; } else { b0 = (1 - c) / 2; b1 = 1 - c; b2 = (1 - c) / 2; }
    const a0 = 1 + a, a1 = -2 * c, a2 = 1 - a;
    const y = (b0 * x + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2) / a0;
    x2 = x1; x1 = x; y2 = y1; y1 = y;
    return y;
  };
}
const N = (s) => Math.round(s * SR);

{ // whoosh : bruit filtré dont la fréquence balaie, avec panoramique gauche → droite
  const n = N(0.7), L = new Float32Array(n), R = new Float32Array(n), f1 = biquad(), f2 = biquad();
  for (let i = 0; i < n; i++) {
    const t = i / n, env = Math.sin(Math.PI * Math.pow(t, 0.6)) ** 2;
    const f = 300 + 2600 * Math.sin(Math.PI * Math.pow(t, 0.8));
    const s = f2(f1(rnd(), 'bp', f, 1.2), 'bp', f * 1.1, 1.4) * env;
    L[i] = s * (1 - 0.6 * t); R[i] = s * (0.4 + 0.6 * t);
  }
  ecrire('whoosh', L, R);
}
{ // impact : coup sourd grave + transitoire
  const n = N(0.9), L = new Float32Array(n), lp = biquad();
  let ph = 0;
  for (let i = 0; i < n; i++) {
    const t = i / SR, f = 48 + 70 * Math.exp(-t * 18);
    ph += (2 * Math.PI * f) / SR;
    const corps = Math.tanh(Math.sin(ph) * 2.2) * Math.exp(-t * 5.5);
    const clic = lp(rnd(), 'lp', 2500) * Math.exp(-t * 60) * 0.8;
    L[i] = corps + clic;
  }
  ecrire('impact', L);
}
{ // metal : choc de presse, partiels inharmoniques
  const n = N(1.2), L = new Float32Array(n), R = new Float32Array(n), hp = biquad();
  const partiels = [[412, 6], [987, 7], [1531, 9], [2244, 11], [3170, 14], [4410, 18]];
  for (let i = 0; i < n; i++) {
    const t = i / SR;
    let s = 0;
    partiels.forEach(([f, d], k) => (s += Math.sin(2 * Math.PI * f * t + k) * Math.exp(-t * d) / (k + 1.5)));
    s += hp(rnd(), 'bp', 3500, 0.7) * Math.exp(-t * 40) * 0.9;
    const corps = Math.sin(2 * Math.PI * 70 * t) * Math.exp(-t * 9) * 0.7;
    L[i] = s + corps; R[i] = s * 0.92 + corps;
  }
  ecrire('metal', L, R);
}
{ // riser : montée de tension (bruit + sinus qui monte), pour les transitions de partie
  const n = N(1.6), L = new Float32Array(n), R = new Float32Array(n), bp = biquad();
  let ph = 0;
  for (let i = 0; i < n; i++) {
    const t = i / n, env = Math.pow(t, 2.2) * (t > 0.97 ? (1 - t) / 0.03 : 1);
    const f = 180 * Math.pow(7, t);
    ph += (2 * Math.PI * f) / SR;
    const s = (bp(rnd(), 'bp', 400 + 5000 * t, 0.8) * 0.8 + Math.sin(ph) * 0.35) * env;
    L[i] = s; R[i] = s * 0.95;
  }
  ecrire('riser', L, R);
}
{ // tick
  const n = N(0.06), L = new Float32Array(n);
  for (let i = 0; i < n; i++) { const t = i / SR; L[i] = Math.sin(2 * Math.PI * 2100 * t) * Math.exp(-t * 90); }
  ecrire('tick', L);
}
{ // pop
  const n = N(0.16), L = new Float32Array(n);
  let ph = 0;
  for (let i = 0; i < n; i++) { const t = i / n; ph += (2 * Math.PI * (760 - 420 * t)) / SR; L[i] = Math.sin(ph) * Math.exp(-t * 8); }
  ecrire('pop', L);
}
{ // nappe : ambiance sombre et douce (ré mineur), 20 s, fondu entrée/sortie
  const d = 20, n = N(d), L = new Float32Array(n), R = new Float32Array(n), lpL = biquad(), lpR = biquad();
  const notes = [73.42, 110, 146.83, 174.61, 220];
  for (let i = 0; i < n; i++) {
    const t = i / SR;
    let l = 0, r = 0;
    notes.forEach((f, k) => {
      l += Math.sin(2 * Math.PI * f * 0.998 * t + k) + 0.3 * Math.sin(4 * Math.PI * f * t);
      r += Math.sin(2 * Math.PI * f * 1.002 * t + 2 * k) + 0.3 * Math.sin(4 * Math.PI * f * 1.001 * t);
    });
    const env = Math.min(1, t / 2.5) * Math.min(1, (d - t) / 3) * (0.85 + 0.15 * Math.sin(2 * Math.PI * 0.1 * t));
    L[i] = lpL(l, 'lp', 900) * env; R[i] = lpR(r, 'lp', 900) * env;
  }
  ecrire('nappe', L, R);
}
console.log('✔ bruitages →', OUT, fs.readdirSync(OUT).join(', '));
