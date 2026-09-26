# Out There — cinematic anime-style short (~61 s, no voice, calm piano)
# Run: streamlit run out_there.py   (no API key needed)
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Out There", page_icon="🌅", layout="wide")
st.markdown("""
<style>
.stApp { background: #07070a; color: #efe9df; }
.stApp label, .stApp p, .stApp span, [data-testid="stWidgetLabel"] *, [data-testid="stMarkdownContainer"] *,
header[data-testid="stHeader"] * { color: #efe9df !important; }
header[data-testid="stHeader"] { background: transparent; }
</style>
""", unsafe_allow_html=True)

st.title("Out There")
size = st.radio("Video size", ["TikTok 9:16", "YouTube 16:9"], horizontal=True)
FORMAT = "916" if size.startswith("TikTok") else "169"

HTML_ANIMATION = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Out There</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,500&family=Inter:wght@500;600&display=swap">
<style>
  [hidden] { display: none !important; }
  :root { color-scheme: dark; --bg: #07070a; --panel: #131318; --garis: #26262e; --teks: #efe9df; --redup: #9b958c; --kuning: #ffd84a; }
  html, body { background: var(--bg); color: var(--teks); }
  body { margin: 0; font-family: Inter, system-ui, sans-serif; padding-inline: 16px; padding-block: 16px 24px; }
  .wadah { width: min(100%, 1100px, calc((100vh - 150px) * 16 / 9)); min-width: 260px; margin: 0 auto; display: flex; flex-direction: column; gap: 10px; }
  .v916 .wadah { width: min(100%, 460px, calc((100vh - 150px) * 9 / 16)); }
  .atas { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; justify-content: space-between; }
  h1 { margin: 0; font: italic 500 26px/1 "Cormorant Garamond", Georgia, serif; letter-spacing: .02em; }
  .pilih { display: inline-flex; background: var(--panel); border-radius: 999px; padding: 3px; box-shadow: inset 0 0 0 1px var(--garis); }
  .pilih button { font: 600 13px/1 Inter, sans-serif; color: var(--redup); background: none; border: 0; border-radius: 999px; padding: 8px 12px; cursor: pointer; }
  .pilih button[aria-pressed="true"] { background: var(--teks); color: #111; }
  .panggung { position: relative; width: 100%; max-width: 100%; aspect-ratio: 16 / 9; border-radius: 10px; overflow: hidden; background: #000; box-shadow: 0 0 0 1px var(--garis); }
  .v916 .panggung { aspect-ratio: 9 / 16; }
  canvas { position: absolute; inset: 0; width: 100%; height: 100%; display: block; }
  .mulai { position: absolute; inset: 0; display: grid; place-content: center; background: rgba(0,0,0,.45); }
  .mulai button { font: 600 16px/1 Inter, sans-serif; background: var(--teks); color: #141210; border: 0; border-radius: 999px; padding: 14px 26px; cursor: pointer; }
  .kontrol { display: flex; gap: 10px; align-items: center; }
  .ikon { width: 38px; height: 38px; border-radius: 50%; border: 0; background: var(--panel); color: var(--teks); box-shadow: inset 0 0 0 1px var(--garis); cursor: pointer; font-size: 14px; flex: none; }
  .bar { flex: 1; height: 5px; border-radius: 3px; background: var(--garis); cursor: pointer; position: relative; }
  .bar div { position: absolute; inset: 0 auto 0 0; width: 0; border-radius: 3px; background: var(--kuning); }
  .waktu { font: 500 12px Inter, sans-serif; color: var(--redup); font-variant-numeric: tabular-nums; min-width: 76px; text-align: right; }
  button:focus-visible { outline: 2px solid var(--teks); outline-offset: 2px; }
</style>
<div class="wadah">
  <div class="atas">
    <h1>Out There</h1>
    <div class="pilih" role="group" aria-label="Video size">
      <button data-format="916" aria-pressed="true">TikTok 9:16</button>
      <button data-format="169" aria-pressed="false">YouTube 16:9</button>
    </div>
  </div>
  <div class="panggung">
    <canvas id="c" aria-label="Anime-style cinematic short: a girl leaves her room and travels — mountains, lantern streets, snow villages, a swing by Mount Fuji, the sea"></canvas>
    <div class="mulai" id="mulai"><button id="bMulai">▶ Play (sound on)</button></div>
  </div>
  <div class="kontrol">
    <button class="ikon" id="bMain" aria-label="Play">▶</button>
    <button class="ikon" id="bUlang" aria-label="Restart">↺</button>
    <div class="bar" id="bar" role="slider" aria-label="Position" tabindex="0"><div id="isi"></div></div>
    <span class="waktu" id="waktu">0.0 / 76.0</span>
  </div>
</div>
<script>
(() => {
'use strict';
const KONFIG_AWAL = { format: '916' };
const C = document.getElementById('c'), L = C.getContext('2d');
const buf = document.createElement('canvas'), B = buf.getContext('2d');       // scene A
const buf2 = document.createElement('canvas'), B2 = buf2.getContext('2d');    // scene B (crossfade)
const kecil = document.createElement('canvas'), K = kecil.getContext('2d');   // bloom
let g = B;
const TAU = Math.PI * 2, PI = Math.PI, DUR = 76;
let VW = 720, VH = 1280, W = 720, H = 1280, FORMAT = '916', DPR = 1, T = 0, main = false, waktuNyata = 0;
const klem = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
const lerp = (a, b, t) => a + (b - a) * t;
const eio = t => { t = klem(t); return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
const halus = t => { t = klem(t); return t * t * (3 - 2 * t); };
const u = (t, a, b) => klem((t - a) / (b - a));
const muncul = (t, a, b, m = .6, k = .6) => t < a || t > b ? 0 : Math.min(1, (t - a) / m, (b - t) / k);
function rng(s) { return () => { s |= 0; s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const n1 = (x, s) => Math.sin(x * 1.3 + s) * .5 + Math.sin(x * 2.9 + s * 1.7) * .25 + Math.sin(x * 6.1 + s * 2.3) * .13 + Math.sin(x * 13.7 + s * 3.1) * .06 + Math.sin(x * 29 + s * 5.3) * .03;
const hx = h => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
const mixC = (a, b, t) => { const A = hx(a), Bc = hx(b); return '#' + A.map((v, i) => Math.round(v + (Bc[i] - v) * klem(t)).toString(16).padStart(2, '0')).join(''); };
const rgba = (h, a) => { const c = hx(h); return `rgba(${c[0]},${c[1]},${c[2]},${a})`; };

function ukur() {
  const r = C.getBoundingClientRect(); DPR = Math.min(devicePixelRatio || 1, 2);
  C.width = Math.round(r.width * DPR); C.height = Math.round(r.height * DPR);
  for (const cv of [buf, buf2]) { cv.width = C.width; cv.height = C.height; }
  kecil.width = Math.max(1, Math.round(C.width / 6)); kecil.height = Math.max(1, Math.round(C.height / 6));
}
new ResizeObserver(ukur).observe(C);

// =====================================================================
//  PAINTING HELPERS (g = current context; W, H = frame size in css px)
// =====================================================================
function gradV(y0, y1, stops) { const gr = g.createLinearGradient(0, y0, 0, y1); stops.forEach(([o, c]) => gr.addColorStop(o, c)); return gr; }
function langit(stops) { g.fillStyle = gradV(0, H, stops); g.fillRect(-50, -50, W + 100, H + 100); }
function cahaya(x, y, r, warna, a = 1, mode = 'lighter') { g.save(); g.globalCompositeOperation = mode; const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, rgba(warna, a)); gr.addColorStop(.35, rgba(warna, a * .35)); gr.addColorStop(1, rgba(warna, 0)); g.fillStyle = gr; g.fillRect(x - r, y - r, r * 2, r * 2); g.restore(); }
function punggung(baseY, amp, freq, seed, fill, geser = 0, tajam = 0) {
  g.beginPath(); g.moveTo(-20, H + 20);
  for (let x = -20; x <= W + 20; x += Math.max(3, W / 180)) { const n = n1((x + geser) * freq / W * 10, seed); const y = baseY - amp * (tajam ? (1 - Math.abs(n)) * 1.2 - .3 : n); g.lineTo(x, y); }
  g.lineTo(W + 20, H + 20); g.closePath(); g.fillStyle = fill; g.fill();
}
function kabut(y, tinggi, warna, a, t, kec = 8, seed = 1) {
  g.save(); g.fillStyle = gradV(y - tinggi, y + tinggi, [[0, rgba(warna, 0)], [.5, rgba(warna, a)], [1, rgba(warna, 0)]]); g.fillRect(-20, y - tinggi, W + 40, tinggi * 2);
  const r = rng(seed); for (let i = 0; i < 7; i++) { const x = ((r() * (W + 600) + t * kec * (.6 + r())) % (W + 600)) - 300, yy = y + (r() - .5) * tinggi, rr = tinggi * (1.2 + r() * 1.4);
    const gr = g.createRadialGradient(x, yy, 0, x, yy, rr); gr.addColorStop(0, rgba(warna, a * .8)); gr.addColorStop(1, rgba(warna, 0)); g.fillStyle = gr; g.save(); g.translate(x, yy); g.scale(2.4, 1); g.translate(-x, -yy); g.fillRect(x - rr, yy - rr, rr * 2, rr * 2); g.restore(); }
  g.restore();
}
function awan(x, y, s, seed, atas, bawah, a = 1, rim) {
  s = Math.min(s, Math.min(W, H) * .5);
  const r = rng(seed); g.save(); g.globalAlpha *= a; g.filter = `blur(${Math.max(1, s / 90)}px)`;
  const bola = [];
  for (let i = 0; i < 30; i++) { const f = r(), px = x + (f - .5) * s * 1.9, puncak = Math.max(0, 1 - Math.abs(f - .5) * 2.1), py = y - puncak * s * (.25 + r() * .3) + r() * s * .06, rr = s * (.08 + r() * .13) * (.6 + puncak * .7); bola.push([px, py, rr]); }
  bola.sort((p, q) => q[1] - p[1]);
  for (const [px, py, rr] of bola) { const gr = g.createRadialGradient(px - rr * .2, py - rr * .5, rr * .05, px, py + rr * .2, rr * 1.15); gr.addColorStop(0, atas); gr.addColorStop(.55, atas); gr.addColorStop(.9, bawah); gr.addColorStop(1, rgba(bawah, 0)); g.fillStyle = gr; g.beginPath(); g.arc(px, py, rr, 0, TAU); g.fill(); }
  g.fillStyle = rgba(bawah, .6); g.beginPath(); g.ellipse(x, y + s * .05, s * .95, s * .07, 0, 0, TAU); g.fill();
  if (rim) { g.globalCompositeOperation = 'lighter'; for (const [px, py, rr] of bola) { if (py > y - s * .05) continue; const gr = g.createRadialGradient(px, py - rr * .7, 0, px, py - rr * .7, rr * .7); gr.addColorStop(0, rgba(rim, .28)); gr.addColorStop(1, rgba(rim, 0)); g.fillStyle = gr; g.beginPath(); g.arc(px, py - rr * .5, rr * .7, 0, TAU); g.fill(); } }
  g.restore();
}
function sinarDewa(x, y, n, panjang, warna, a, t, lebar = .06, arah = PI / 2, sebar = 1.2) {
  g.save(); g.globalCompositeOperation = 'lighter';
  for (let i = 0; i < n; i++) { const an = arah + (i / (n - 1) - .5) * sebar + Math.sin(t * .3 + i) * .02, w = lebar * (0.6 + .8 * ((i * 37) % 10) / 10), al = a * (.5 + .5 * Math.sin(t * .7 + i * 1.7));
    const gr = g.createLinearGradient(x, y, x + Math.cos(an) * panjang, y + Math.sin(an) * panjang); gr.addColorStop(0, rgba(warna, al)); gr.addColorStop(1, rgba(warna, 0));
    g.fillStyle = gr; g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(an - w) * panjang, y + Math.sin(an - w) * panjang); g.lineTo(x + Math.cos(an + w) * panjang, y + Math.sin(an + w) * panjang); g.closePath(); g.fill(); }
  g.restore();
}
function bokeh(list, t, skala = 1) {
  g.save(); g.globalCompositeOperation = 'lighter';
  for (const b of list) { const x = b.x * W + Math.sin(t * .2 + b.f) * 6, y = b.y * H, r = b.r * skala * Math.min(W, H) / 720; const a = b.a * (.7 + .3 * Math.sin(t * b.v + b.f));
    const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, rgba(b.c, a)); gr.addColorStop(.7, rgba(b.c, a * .8)); gr.addColorStop(1, rgba(b.c, 0)); g.fillStyle = gr; g.beginPath(); g.arc(x, y, r, 0, TAU); g.fill(); }
  g.restore();
}
const buatBokeh = (n, seed, warna, ymin, ymax, rmin, rmax, amin = .25, amax = .6) => { const r = rng(seed); return Array.from({ length: n }, () => ({ x: r(), y: ymin + r() * (ymax - ymin), r: rmin + r() * (rmax - rmin), c: warna[Math.floor(r() * warna.length)], a: amin + r() * (amax - amin), f: r() * 9, v: .5 + r() * 1.5 })); };
function burung(x, y, s, t, a = .7, warna = '#1a1420') { g.save(); g.globalAlpha *= a; g.strokeStyle = warna; g.lineWidth = Math.max(1, s * .12); g.lineCap = 'round'; const k = Math.sin(t * 9) * .5; g.beginPath(); g.moveTo(x - s, y - s * k * .6); g.quadraticCurveTo(x - s * .4, y - s * (.35 + k * .2), x, y); g.quadraticCurveTo(x + s * .4, y - s * (.35 + k * .2), x + s, y - s * k * .6); g.stroke(); g.restore(); }
function pinus(x, baseY, h, warna, salju) {
  g.fillStyle = warna; g.beginPath(); g.moveTo(x, baseY - h);
  for (let i = 0; i <= 5; i++) { const yy = baseY - h + h * i / 5, w = h * .09 + h * .075 * i; g.lineTo(x + w, yy + h * .12); g.lineTo(x + w * .45, yy + h * .1); }
  g.lineTo(x + h * .03, baseY); g.lineTo(x - h * .03, baseY);
  for (let i = 5; i >= 0; i--) { const yy = baseY - h + h * i / 5, w = h * .09 + h * .075 * i; g.lineTo(x - w * .45, yy + h * .1); g.lineTo(x - w, yy + h * .12); }
  g.closePath(); g.fill();
  if (salju) { g.fillStyle = salju; for (let i = 0; i <= 5; i++) { const yy = baseY - h + h * i / 5, w = h * .09 + h * .075 * i; g.beginPath(); g.moveTo(x - w * .8, yy + h * .1); g.quadraticCurveTo(x, yy - h * .02, x + w * .8, yy + h * .1); g.lineTo(x + w * .5, yy + h * .085); g.quadraticCurveTo(x, yy + h * .02, x - w * .5, yy + h * .085); g.fill(); } }
}


// =====================================================================
//  ANIME GIRL — cel-shaded (base + shadow + highlight + outline + rim)
// =====================================================================
const WR = {
  kulit: '#ffe6d8', kulitB: '#f2bba6', kulitG: '#dd9483', garis: '#3f2629',
  rambut: '#2b2336', rambutB: '#18131f', rambutT: '#54477a', rambutK: '#9b8ccf',
  iris1: '#2a1512', iris2: '#8a4a2a', iris3: '#f0b067',
  jaket: '#2f3d63', jaketB: '#1e2744', jaketT: '#4c5f93', dalam: '#efe3d2', dalamB: '#cdb9a2',
  syal: '#c26a55', syalB: '#944a3d', syalT: '#e0937a', ransel: '#6f7a4a', ranselB: '#4c5432', ranselT: '#8e9a63',
  celana: '#41577f', celanaB: '#2c3c5c', sepatu: '#f3eee6', sepatuB: '#c9c0b3',
};
let TK = { t: 0, rim: null, rimSisi: 1 }; // per-frame: time, rim light colour, rim side (1 = right)
function isiTepi(p, isi, garis, lw) { g.fillStyle = isi; g.fill(p); if (garis) { g.strokeStyle = garis; g.lineWidth = lw; g.stroke(p); } }
function bayangDi(klip, bentuk, warna) { g.save(); g.clip(klip); g.fillStyle = warna; g.fill(bentuk); g.restore(); }
const jalur = f => { const p = new Path2D(); f(p); return p; };
// limbs: segments [[x0,y0,x1,y1,w,colour]], outlines first then fills => clean joints
function anggota(seg, lw) {
  g.lineCap = 'round'; g.lineJoin = 'round';
  for (const [a, b, c, d, w] of seg) { g.strokeStyle = WR.garis; g.lineWidth = w + lw * 2; g.beginPath(); g.moveTo(a, b); g.lineTo(c, d); g.stroke(); }
  for (const [a, b, c, d, w, k] of seg) { g.strokeStyle = k; g.lineWidth = w; g.beginPath(); g.moveTo(a, b); g.lineTo(c, d); g.stroke(); }
}
function rimDi(paths, lebar) { // soft back light along given right-side contours (mirrored when the light is on the left)
  if (!TK.rim) return; g.save(); g.filter = 'blur(1.2px)'; if (TK.rimSisi < 0) g.scale(-1, 1);
  g.globalCompositeOperation = 'lighter'; g.lineCap = 'round'; g.strokeStyle = rgba(TK.rim, .2); g.lineWidth = lebar * 2.2; for (const p of paths) g.stroke(p);
  g.strokeStyle = rgba(TK.rim, .45); g.lineWidth = lebar; for (const p of paths) g.stroke(p); g.restore();
}

// ---------- anime eye (local coords, sd = side)
function mataAnime(sd, o, kf) {
  const buka = kf * (o.bukaMata ?? (o.mata === 'sayu' ? .62 : o.mata === 'tutup' ? 0 : 1)), lx = o.lirikX || 0, ly = o.lirikY || 0;
  g.save(); g.scale(sd, 1);
  if (o.mata === 'senyum') {
    g.strokeStyle = WR.garis; g.lineWidth = .055; g.beginPath(); g.moveTo(-.14, .05); g.quadraticCurveTo(.01, -.1, .16, .03); g.stroke();
    g.lineWidth = .025; g.beginPath(); g.moveTo(.15, .02); g.lineTo(.21, .0); g.stroke(); g.restore(); return;
  }
  if (buka < .08) {
    g.strokeStyle = WR.garis; g.lineWidth = .05; g.beginPath(); g.moveTo(-.14, .03); g.quadraticCurveTo(.01, .11, .17, .01); g.stroke();
    g.lineWidth = .022; for (let k = 0; k < 3; k++) { g.beginPath(); g.moveTo(.06 + k * .045, .07 - k * .02); g.lineTo(.08 + k * .055, .11 - k * .015); g.stroke(); }
    g.restore(); return;
  }
  const up = y => lerp(.03, y, buka);
  const skl = jalur(p => { p.moveTo(-.14, .03); p.bezierCurveTo(-.11, up(-.13), .1, up(-.16), .17, up(-.04)); p.bezierCurveTo(.16, .12, -.07, .17, -.14, .03); p.closePath(); });
  g.fillStyle = '#fffaf5'; g.fill(skl);
  g.save(); g.clip(skl); g.scale(sd, 1); // unmirror: highlights on the same side for both eyes
  const cx = .015 * sd + lx * .05, cy = .045 + ly * .03;
  const ir = g.createLinearGradient(0, cy - .14, 0, cy + .13); ir.addColorStop(0, WR.iris1); ir.addColorStop(.5, WR.iris2); ir.addColorStop(1, WR.iris3);
  g.fillStyle = ir; g.beginPath(); g.ellipse(cx, cy, .1, .135, 0, 0, TAU); g.fill();
  g.strokeStyle = rgba(WR.iris1, .9); g.lineWidth = .014; g.stroke();
  g.strokeStyle = rgba(WR.iris1, .35); g.lineWidth = .008; for (let k = 0; k < 14; k++) { const a = k / 14 * TAU; g.beginPath(); g.moveTo(cx + Math.cos(a) * .05, cy + Math.sin(a) * .07); g.lineTo(cx + Math.cos(a) * .092, cy + Math.sin(a) * .125); g.stroke(); }
  g.fillStyle = '#140a09'; g.beginPath(); g.ellipse(cx, cy - .005, .045, .068, 0, 0, TAU); g.fill();
  g.strokeStyle = rgba('#ffd9a0', .55); g.lineWidth = .016; g.beginPath(); g.ellipse(cx, cy + .02, .07, .085, 0, PI * .2, PI * .8); g.stroke();
  g.fillStyle = 'rgba(40,20,30,.32)'; g.beginPath(); g.ellipse(0, up(-.13), .3, .09, 0, 0, TAU); g.fill(); // lid shadow
  const kil = Math.sin(TK.t * 2.1) * .006; g.fillStyle = '#fff'; g.beginPath(); g.ellipse(cx - .035 + kil, cy - .05, .036, .048, -.4, 0, TAU); g.fill();
  g.beginPath(); g.arc(cx + .045, cy + .06, .016, 0, TAU); g.fill();
  g.globalAlpha = .7; g.beginPath(); g.arc(cx + .05, cy - .06, .01, 0, TAU); g.fill(); g.globalAlpha = 1;
  g.restore();
  // lashes
  g.strokeStyle = '#1c0f11'; g.lineWidth = .05; g.beginPath(); g.moveTo(-.15, .035); g.bezierCurveTo(-.11, up(-.13), .1, up(-.165), .18, up(-.045)); g.stroke();
  g.fillStyle = '#1c0f11'; g.beginPath(); g.moveTo(.14, up(-.08)); g.lineTo(.24, up(-.1)); g.lineTo(.18, up(-.02)); g.closePath(); g.fill();
  g.lineWidth = .016; g.beginPath(); g.moveTo(.16, .07); g.quadraticCurveTo(.08, .15, -.02, .15); g.stroke();
  if (buka > .7) { g.strokeStyle = rgba(WR.garis, .45); g.lineWidth = .014; g.beginPath(); g.moveTo(-.09, -.15); g.quadraticCurveTo(.05, -.21, .17, -.12); g.stroke(); }
  g.restore();
}

// ---------- bust (front), for close-ups; head ≈ 2 units tall, chin at y≈.68, jacket to y 3.3
// o: tol, miring, mata ('buka'|'tutup'|'senyum'|'sayu'), bukaMata 0-1, mulut ('datar'|'senyum'|'lebar'|'kecil'|'buka'),
//    merah, angin, arahAngin, lirikX, lirikY, tudung, lambai 0-1, syal, cermin, napas
function gadisDada(x, y, s, o = {}) {
  const t = TK.t, ang = o.angin || 0, ar = o.arahAngin || 1;
  const sw = k => ang * ar * k * (.7 + .3 * Math.sin(t * 2.3 + k * 6)) + Math.sin(t * 1.1 + k * 3) * .012 * k;
  const lw = 2.3 / s, dx = (o.tol || 0) * .1, ns = Math.sin(t * 1.6) * .015 * (o.napas ?? 1);
  g.save(); g.translate(x, y); g.scale(o.cermin ? -s : s, s); g.lineJoin = 'round'; g.lineCap = 'round';
  const kepala = () => { g.translate(0, .62); g.rotate((o.miring || 0) + Math.sin(t * .7) * .012 * (o.goyang ?? 1)); g.translate(0, -.62); };
  const gRambut = (y0, y1, a = '#241d2e', b = '#3f355a') => { const gr = g.createLinearGradient(0, y0, 0, y1); gr.addColorStop(0, a); gr.addColorStop(.5, WR.rambut); gr.addColorStop(1, b); return gr; };
  // ---- hood when up (behind everything)
  let tudungLuar = null;
  if (o.tudung) { tudungLuar = jalur(p => { p.moveTo(-1.0, 1.25); p.bezierCurveTo(-1.25, .2, -1.05, -1.3, 0, -1.32); p.bezierCurveTo(1.05, -1.3, 1.25, .2, 1.0, 1.25); p.closePath(); });
    g.save(); kepala(); isiTepi(tudungLuar, WR.jaketB, WR.garis, lw); g.restore(); }
  // ---- back hair
  const rb = jalur(p => {
    p.moveTo(.64, -.5); p.bezierCurveTo(.3, -1.12, -.3, -1.12, -.64, -.5);
    p.bezierCurveTo(-.86, -.1, -.84 + sw(.1), .5, -.9 + sw(.3), 1.0); p.bezierCurveTo(-.94 + sw(.5), 1.3, -.98 + sw(.7), 1.5, -.92 + sw(.8), 1.7);
    for (let i = 1; i <= 8; i++) { const xx = lerp(-.92, .92, i / 8) + sw(.85); if (i % 2) p.quadraticCurveTo(xx - .1, 1.72, xx, 1.9 + Math.sin(i * 2.1) * .06); else p.quadraticCurveTo(xx - .06, 1.8, xx, 1.62); }
    p.bezierCurveTo(.98 + sw(.7), 1.5, .94 + sw(.5), 1.3, .9 + sw(.3), 1.0); p.bezierCurveTo(.84 + sw(.1), .5, .86, -.1, .64, -.5); p.closePath();
  });
  if (!o.tudung) { g.save(); kepala(); isiTepi(rb, gRambut(-1, 1.9, '#120e18', '#2c2440'), WR.garis, lw); g.restore(); }
  // ---- neck + body
  g.save(); g.translate(0, ns);
  const leher = jalur(p => { p.moveTo(-.16, .4); p.lineTo(-.19, 1.05); p.lineTo(.19, 1.05); p.lineTo(.16, .4); p.closePath(); });
  isiTepi(leher, WR.kulit, WR.garis, lw); bayangDi(leher, jalur(p => { p.moveTo(-.3, .4); p.quadraticCurveTo(0, .95, .3, .4); p.lineTo(.3, 1.2); p.lineTo(-.3, 1.2); }), WR.kulitB);
  if (!o.tudung) { const hd = jalur(p => { p.moveTo(-.74, 1.08); p.bezierCurveTo(-.62, .74, .62, .74, .74, 1.08); p.bezierCurveTo(.42, 1.24, -.42, 1.24, -.74, 1.08); p.closePath(); }); isiTepi(hd, WR.jaketB, WR.garis, lw); }
  const kaos = jalur(p => { p.moveTo(-.34, .95); p.quadraticCurveTo(0, 1.12, .34, .95); p.lineTo(.3, 1.6); p.lineTo(-.3, 1.6); p.closePath(); });
  isiTepi(kaos, WR.dalam, WR.garis, lw); bayangDi(kaos, jalur(p => { p.moveTo(-.4, .9); p.quadraticCurveTo(0, 1.2, .4, .9); p.lineTo(.4, 1.12); p.quadraticCurveTo(0, 1.26, -.4, 1.12); }), WR.dalamB);
  const jk = jalur(p => { p.moveTo(-.22, 1.0); p.bezierCurveTo(-.46, 1.04, -.8, 1.06, -.98, 1.26); p.bezierCurveTo(-1.13, 1.42, -1.16, 1.72, -1.18, 2.0); p.lineTo(-1.26, 3.4); p.lineTo(1.26, 3.4); p.lineTo(1.18, 2.0); p.bezierCurveTo(1.16, 1.72, 1.13, 1.42, .98, 1.26); p.bezierCurveTo(.8, 1.06, .46, 1.04, .22, 1.0); p.lineTo(.04, 1.42); p.lineTo(-.04, 1.42); p.closePath(); });
  isiTepi(jk, WR.jaket, WR.garis, lw);
  const jkB = jalur(p => { p.moveTo(.3, 1.02); p.bezierCurveTo(.7, 1.4, .85, 2.2, .72, 3.5); p.lineTo(1.5, 3.5); p.lineTo(1.5, .9); p.closePath(); }), jkT = jalur(p => { p.moveTo(-1.02, 1.3); p.bezierCurveTo(-.86, 1.14, -.6, 1.09, -.38, 1.1); p.bezierCurveTo(-.6, 1.18, -.84, 1.24, -.98, 1.42); p.closePath(); });
  bayangDi(jk, jkB, WR.jaketB); bayangDi(jk, jkT, WR.jaketT); JAKET = { jk, jkB, jkT, ns };
  g.strokeStyle = rgba(WR.garis, .8); g.lineWidth = lw * .9;
  g.lineWidth = lw * .6; g.beginPath(); g.moveTo(-.55, 2.1); g.quadraticCurveTo(-.45, 2.4, -.5, 2.7); g.moveTo(.5, 1.9); g.quadraticCurveTo(.42, 2.2, .46, 2.5); g.stroke();
  g.strokeStyle = WR.garis; g.lineWidth = lw; g.beginPath(); g.moveTo(0, 1.42); g.lineTo(0, 3.4); g.stroke();
  g.fillStyle = '#c9c3bb'; g.fillRect(-.03, 1.5, .06, .12);
  g.strokeStyle = WR.dalam; g.lineWidth = .028; g.beginPath(); g.moveTo(-.2, 1.08); g.quadraticCurveTo(-.25 + sw(.08), 1.35, -.2 + sw(.15), 1.66); g.moveTo(.2, 1.08); g.quadraticCurveTo(.25 + sw(.08), 1.35, .22 + sw(.15), 1.68); g.stroke();
  if (o.syal) {
    const sy = jalur(p => { p.moveTo(-.7, 1.0); p.bezierCurveTo(-.66, .7, .66, .7, .7, 1.0); p.bezierCurveTo(.72, 1.18, .5, 1.36, .1, 1.38); p.bezierCurveTo(-.3, 1.4, -.68, 1.26, -.7, 1.0); p.closePath(); });
    const uj = jalur(p => { p.moveTo(-.42, 1.2); p.bezierCurveTo(-.46 + sw(.2), 1.6, -.5 + sw(.4), 1.9, -.46 + sw(.5), 2.25); p.lineTo(-.14 + sw(.5), 2.22); p.bezierCurveTo(-.14 + sw(.4), 1.9, -.12 + sw(.2), 1.6, -.1, 1.3); p.closePath(); });
    isiTepi(uj, WR.syal, WR.garis, lw); bayangDi(uj, jalur(p => p.rect(-.32, 1.1, .3, 1.3)), WR.syalB);
    g.strokeStyle = WR.syalB; g.lineWidth = .03; g.beginPath(); for (let k = 0; k < 4; k++) { g.moveTo(-.44 + sw(.5), 2.24 + k * 0); g.lineTo(-.44 + k * .1 + sw(.55), 2.36); } g.stroke();
    isiTepi(sy, WR.syal, WR.garis, lw); bayangDi(sy, jalur(p => { p.moveTo(-.8, 1.05); p.quadraticCurveTo(0, 1.25, .8, 1.05); p.lineTo(.8, 1.5); p.lineTo(-.8, 1.5); }), WR.syalB);
    g.save(); g.clip(sy); g.strokeStyle = rgba(WR.syalB, .7); g.lineWidth = .02; for (let k = -6; k <= 6; k++) { g.beginPath(); g.moveTo(k * .11, .8); g.quadraticCurveTo(k * .12 + .03, 1.1, k * .1, 1.4); g.stroke(); }
    g.strokeStyle = rgba(WR.syalT, .8); g.lineWidth = .04; g.beginPath(); g.moveTo(-.55, .9); g.quadraticCurveTo(-.2, .82, .1, .86); g.stroke(); g.restore();
  }
  rimDi([jalur(p => { p.moveTo(.3, 1.0); p.bezierCurveTo(.5, 1.04, .8, 1.06, .98, 1.26); p.bezierCurveTo(1.13, 1.42, 1.16, 1.72, 1.18, 2.0); p.lineTo(1.26, 3.4); })], .04);
  g.restore();
  // ---- head
  g.save(); kepala();
  const muka = jalur(p => { p.moveTo(-.57, -.25); p.bezierCurveTo(-.58, .1, -.5, .3, -.33 + dx * .6, .48); p.bezierCurveTo(-.2 + dx, .6, -.07 + dx, .68, dx * 1.2, .69); p.bezierCurveTo(.07 + dx, .68, .2 + dx, .6, .33 + dx * .6, .48); p.bezierCurveTo(.5, .3, .58, .1, .57, -.25); p.bezierCurveTo(.55, -.85, -.55, -.85, -.57, -.25); p.closePath(); });
  isiTepi(muka, WR.kulit, WR.garis, lw);
  bayangDi(muka, jalur(p => { p.moveTo(-.7, -.9); p.lineTo(.7, -.9); p.lineTo(.7, -.1); for (let i = 0; i <= 8; i++) p.lineTo(.6 - i * .15, (i % 2 ? -.06 : -.14)); p.closePath(); }), WR.kulitB);
  bayangDi(muka, jalur(p => { p.moveTo(.44 + dx, -.3); p.bezierCurveTo(.52 + dx, .1, .42 + dx, .42, .12 + dx, .66); p.lineTo(.8, .75); p.lineTo(.8, -.3); p.closePath(); }), rgba(WR.kulitB, .75));
  g.save(); g.clip(muka); cahaya(-.2, .1, .5, '#ffffff', .15, 'source-over'); g.restore();
  const kd = (t + (o.fasekedip || 0)) % 4.3, kedip = o.kedip === false ? 1 : kd < .2 ? Math.min(1, Math.abs(kd - .08) / .08) : 1;
  for (const sd of [-1, 1]) { const sk = 1 - Math.max(0, sd * (o.tol || 0)) * .25; g.save(); g.translate(sd * .26 + dx * (sd > 0 ? .8 : 1.2), .08); g.scale(sk, 1); mataAnime(sd, o, kedip); g.restore(); }
  g.strokeStyle = WR.kulitG; g.lineWidth = .022; g.beginPath(); g.moveTo(.03 + dx * 1.3, .3); g.lineTo(0 + dx * 1.3, .345); g.stroke();
  g.fillStyle = rgba('#ffffff', .6); g.beginPath(); g.arc(-.01 + dx * 1.3, .29, .012, 0, TAU); g.fill();
  const mulut = o.mulut || 'datar', mx = .01 + dx * 1.3, my = .49;
  g.strokeStyle = WR.garis; g.lineWidth = .024;
  if (mulut === 'senyum') { g.beginPath(); g.moveTo(mx - .09, my - .015); g.quadraticCurveTo(mx, my + .05, mx + .09, my - .015); g.stroke(); }
  else if (mulut === 'lebar' || mulut === 'buka') {
    const lb = mulut === 'lebar' ? 1 : .6, m = jalur(p => { p.moveTo(mx - .11 * lb, my - .03); p.quadraticCurveTo(mx, my - .005, mx + .11 * lb, my - .03); p.quadraticCurveTo(mx + .02, my + .14 * lb, mx - .11 * lb, my - .03); p.closePath(); });
    g.fillStyle = '#8e2f36'; g.fill(m); g.save(); g.clip(m); g.fillStyle = '#e57f7d'; g.beginPath(); g.ellipse(mx + .01, my + .1 * lb, .07, .045, 0, 0, TAU); g.fill(); if (lb > .8) { g.fillStyle = '#fff'; g.fillRect(mx - .1, my - .04, .2, .035); } g.restore(); g.lineWidth = .02; g.stroke(m);
  }
  else if (mulut === 'kecil') { g.fillStyle = '#b8575a'; g.beginPath(); g.ellipse(mx, my, .028, .02, 0, 0, TAU); g.fill(); }
  else { g.beginPath(); g.moveTo(mx - .055, my); g.quadraticCurveTo(mx, my + .012, mx + .055, my - .004); g.stroke(); }
  const mr = o.merah ?? .5;
  for (const sd of [-1, 1]) { const bx = sd * .32 + dx; g.fillStyle = `rgba(255,120,130,${.32 * mr})`; g.beginPath(); g.ellipse(bx, .29, .12, .055, 0, 0, TAU); g.fill(); g.strokeStyle = `rgba(225,85,100,${.55 * mr})`; g.lineWidth = .014; for (let k = 0; k < 3; k++) { g.beginPath(); g.moveTo(bx - .06 + k * .045, .315); g.lineTo(bx - .035 + k * .045, .265); g.stroke(); } }
  // ---- bangs
  const uj = [[.52, -.26], [.44, -.02], [.34, -.3], [.25, -.07], [.15, -.3], [.06, .05], [-.03, -.28], [-.12, -.05], [-.22, -.3], [-.31, -.1], [-.4, -.28], [-.49, -.01], [-.56, -.24]];
  const po = jalur(p => {
    p.moveTo(-.66, .08); p.bezierCurveTo(-.82, -.72, -.36, -1.12, .02, -1.1); p.bezierCurveTo(.42, -1.12, .82, -.72, .66, .08);
    let prev = [.66, .08];
    uj.forEach(([ux, uy], i) => { const w = sw(.06) * (i % 2 ? 1 : .4); if (i % 2) p.quadraticCurveTo(ux + .05, uy - .12, ux + w, uy); else p.quadraticCurveTo(prev[0] - .03, prev[1] - .12, ux + w, uy); prev = [ux, uy]; });
    p.quadraticCurveTo(-.6, -.1, -.66, .08); p.closePath();
  });
  isiTepi(po, gRambut(-1.1, .1), WR.garis, lw);
  bayangDi(po, jalur(p => { p.moveTo(-.9, -.2); p.bezierCurveTo(-.4, -.42, .4, -.42, .9, -.2); p.lineTo(.9, .3); p.lineTo(-.9, .3); p.closePath(); }), WR.rambutB);
  bayangDi(po, jalur(p => p.rect(.3, -1.2, .6, 1.4)), rgba(WR.rambutB, .5));
  g.save(); g.clip(po);
  g.strokeStyle = WR.rambutT; g.lineWidth = .1; g.beginPath(); g.arc(0, -.2, .68, PI * 1.12, PI * 1.72); g.stroke();
  g.fillStyle = WR.rambutK; for (let i = 0; i < 9; i++) { const a = PI * (1.16 + i * .06), r = .68; const x0 = Math.cos(a) * r, y0 = -.2 + Math.sin(a) * r; g.beginPath(); g.moveTo(x0 - .03, y0 - .02); g.lineTo(x0 + .03, y0 - .02); g.lineTo(x0 + Math.cos(a) * .0, y0 + .09 + (i % 2) * .04); g.closePath(); g.fill(); }
  g.strokeStyle = rgba(WR.rambutB, .9); g.lineWidth = lw * .8;
  for (const [ux, uy] of uj.filter((_, i) => i % 2)) { g.beginPath(); g.moveTo(ux * .4, -1.0); g.quadraticCurveTo(ux * .95, -.5, ux + sw(.06), uy - .04); g.stroke(); }
  g.restore();
  g.strokeStyle = WR.rambut; g.lineWidth = .045; g.beginPath(); g.moveTo(.02, -1.08); g.quadraticCurveTo(.08 + sw(.1), -1.32, .24 + sw(.15), -1.24); g.stroke(); // ahoge
  // side locks
  const sisi = [];
  for (const sd of [-1, 1]) {
    const bx = sd * .6, sl = jalur(p => { p.moveTo(bx - sd * .12, -.45); p.bezierCurveTo(bx + sd * .1, -.05, bx + sd * .07 + sw(.3), .5, bx + sd * .01 + sw(.55), 1.12); p.bezierCurveTo(bx - sd * .06 + sw(.45), .8, bx - sd * .1 + sw(.2), .4, bx - sd * .16, .05); p.bezierCurveTo(bx - sd * .2, -.1, bx - sd * .2, -.3, bx - sd * .12, -.45); p.closePath(); });
    isiTepi(sl, gRambut(-.45, 1.12), WR.garis, lw); bayangDi(sl, jalur(p => p.rect(bx - .3, .35, .6, 1)), WR.rambutB); sisi.push(sl);
    g.strokeStyle = rgba(WR.rambutK, .5); g.lineWidth = .02; g.beginPath(); g.moveTo(bx - sd * .06, -.2); g.quadraticCurveTo(bx + sd * .03 + sw(.2), .3, bx - sd * .02 + sw(.4), .75); g.stroke();
  }
  if (ang > .15) { for (let i = 0; i < 3; i++) { const yy = -.1 + i * .3, x0 = ar * .58, ex = x0 + sw(1.1) + Math.sin(t * 5 + i) * .05, ey = yy + .25 + Math.sin(t * 3 + i) * .08;
    const st = jalur(p => { p.moveTo(x0, yy - .05); p.bezierCurveTo(x0 + sw(.4), yy - .02, ex - sw(.3), ey - .12, ex, ey); p.bezierCurveTo(ex - sw(.4), ey - .04, x0 + sw(.3), yy + .1, x0, yy + .06); p.closePath(); }); isiTepi(st, WR.rambut, WR.garis, lw * .8); } }
  g.globalAlpha = .6; g.strokeStyle = WR.garis; g.lineWidth = .032; for (const sd of [-1, 1]) { g.beginPath(); g.moveTo(sd * .12 + dx, -.19 + (o.alis || 0) * .5); g.quadraticCurveTo(sd * .27 + dx, -.25 + (o.alis || 0), sd * .4 + dx, -.19); g.stroke(); } g.globalAlpha = 1;
  if (o.tudung) { const rim = jalur(p => { p.moveTo(-.86, 1.1); p.bezierCurveTo(-1.02, .1, -.9, -1.18, 0, -1.2); p.bezierCurveTo(.9, -1.18, 1.02, .1, .86, 1.1); p.lineTo(.7, 1.05); p.bezierCurveTo(.84, .1, .74, -1.02, 0, -1.04); p.bezierCurveTo(-.74, -1.02, -.84, .1, -.7, 1.05); p.closePath(); });
    isiTepi(rim, WR.jaket, WR.garis, lw); bayangDi(rim, jalur(p => p.rect(.2, -1.4, 1, 2.6)), WR.jaketB); bayangDi(rim, jalur(p => { p.moveTo(-1, -.4); p.quadraticCurveTo(-.5, -1.3, .2, -1.25); p.lineTo(.1, -1.1); p.quadraticCurveTo(-.6, -1.05, -.9, -.2); p.closePath(); }), WR.jaketT); }
  rimDi(o.tudung ? [jalur(p => { p.moveTo(0, -1.32); p.bezierCurveTo(1.05, -1.3, 1.25, .2, 1.0, 1.25); })] : [jalur(p => { p.moveTo(.02, -1.1); p.bezierCurveTo(.42, -1.12, .82, -.72, .66, .0); }), jalur(p => { p.moveTo(.86, .1); p.bezierCurveTo(.84 + sw(.1), .4, .86 + sw(.2), .7, .88 + sw(.3), .9); }), jalur(p => { p.moveTo(.57, -.1); p.bezierCurveTo(.58, .1, .5, .3, .33, .48); })], .035);
  g.restore();
  poseTangan(o.tangan || (o.lambai !== undefined ? { pose: 'lambai', k: o.lambai } : null), lw, ns, t);
  g.restore();
}
// ---------- anime hand; wrist at (0,0), fingers toward -y. One closed silhouette (thumb + fingers + palm) so every outline joins cleanly.
function lobus(p, [bx, by, tx, ty, w], lembah) {
  const dx = tx - bx, dy = ty - by, d = Math.hypot(dx, dy), ux = dx / d, uy = dy / d, nx = -uy, ny = ux, r = w * .46, cx = tx - ux * r, cy = ty - uy * r;
  const L0 = [bx - nx * w / 2, by - ny * w / 2], R0 = [bx + nx * w / 2, by + ny * w / 2];
  if (lembah) p.quadraticCurveTo(lembah[0], lembah[1], ...L0); else p.lineTo(...L0);
  p.quadraticCurveTo((L0[0] + cx) / 2 - nx * w * .06, (L0[1] + cy) / 2 - ny * w * .06, cx - nx * r, cy - ny * r);
  const a = Math.atan2(-ny, -nx); p.arc(cx, cy, r, a, a + PI, false);
  p.quadraticCurveTo((R0[0] + cx) / 2 + nx * w * .06, (R0[1] + cy) / 2 + ny * w * .06, ...R0);
}
function tanganAnime(x, y, rot, sz, pose, cermin, lw) {
  if (pose === 'genggam') return tanganGenggam(x, y, rot, sz, cermin, lw);
  g.save(); g.translate(x, y); g.rotate(rot); g.scale(cermin ? -sz : sz, sz); g.lineCap = 'round'; g.lineJoin = 'round';
  const L = lw / sz * .9, buka = pose === 'buka';
  const J = buka
    ? [[-.093, -.2, -.15, -.4, .064], [-.031, -.215, -.046, -.46, .066], [.031, -.215, .046, -.45, .064], [.091, -.2, .135, -.37, .058]]
    : [[-.09, -.2, -.1, -.43, .058], [-.03, -.215, -.033, -.49, .06], [.03, -.215, .03, -.475, .058], [.089, -.2, .094, -.4, .054]];
  const jp = buka ? [-.1, -.05, -.215, -.17, .072] : [-.095, -.06, -.155, -.21, .062];
  const tgn = jalur(p => {
    p.moveTo(-.07, .05); p.bezierCurveTo(-.095, .02, -.11, -.01, -.115, -.03);
    lobus(p, jp); p.quadraticCurveTo(-.125, -.14, -.119, -.2);
    J.forEach((j, i) => { const pv = J[i - 1]; lobus(p, j, pv ? [(pv[0] + j[0]) / 2, (pv[1] + j[1]) / 2 + .012] : null); });
    p.bezierCurveTo(.124, -.13, .112, -.03, .078, .05); p.quadraticCurveTo(0, .075, -.07, .05); p.closePath();
  });
  isiTepi(tgn, WR.kulit, WR.garis, L);
  bayangDi(tgn, jalur(p => { p.moveTo(.05, -.6); p.quadraticCurveTo(.075, -.25, .055, .1); p.lineTo(.3, .1); p.lineTo(.3, -.6); p.closePath(); }), rgba(WR.kulitB, .75));
  bayangDi(tgn, jalur(p => p.rect(-.3, -.01, .6, .12)), rgba(WR.kulitB, .55));
  g.strokeStyle = rgba(WR.garis, .45); g.lineWidth = L * .75;
  for (let i = 0; i < 3; i++) { const a = J[i], b = J[i + 1], mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2 + .01, tx = (a[2] + b[2]) / 2, ty = (a[3] + b[3]) / 2; g.beginPath(); g.moveTo(lerp(mx, tx, .08), lerp(my, ty, .08)); g.lineTo(lerp(mx, tx, buka ? .25 : .62), lerp(my, ty, buka ? .25 : .62)); g.stroke(); }
  g.strokeStyle = rgba(WR.kulitG, .55); g.lineWidth = L * .7; g.beginPath();
  if (buka) { g.moveTo(-.06, -.13); g.quadraticCurveTo(0, -.11, .06, -.14); }
  else { g.moveTo(-.06, -.09); g.quadraticCurveTo(-.08, -.03, -.05, .02); }
  g.stroke();
  g.restore();
}
function tanganGenggam(x, y, rot, sz, cermin, lw) {
  g.save(); g.translate(x, y); g.rotate(rot); g.scale(cermin ? -sz : sz, sz); g.lineCap = 'round'; g.lineJoin = 'round';
  const L = lw / sz * .9, kn = [-.087, -.029, .029, .087];
  const kepal = jalur(p => { p.moveTo(-.075, .05); p.bezierCurveTo(-.12, 0, -.13, -.12, -.118, -.2);
    kn.forEach((k, i) => { const r = .031 - (i === 3 ? .004 : 0), yy = -.225 + Math.abs(i - 1.5) * .008; p.arc(k, yy, r, PI, 0, false); });
    p.bezierCurveTo(.13, -.12, .12, -.02, .078, .05); p.quadraticCurveTo(0, .075, -.075, .05); p.closePath(); });
  isiTepi(kepal, WR.kulit, WR.garis, L);
  bayangDi(kepal, jalur(p => { p.moveTo(.05, -.4); p.quadraticCurveTo(.07, -.15, .055, .1); p.lineTo(.3, .1); p.lineTo(.3, -.4); p.closePath(); }), rgba(WR.kulitB, .75));
  g.strokeStyle = rgba(WR.garis, .5); g.lineWidth = L * .75; g.beginPath();
  for (let i = 0; i < 3; i++) { const xx = (kn[i] + kn[i + 1]) / 2; g.moveTo(xx, -.215); g.lineTo(xx + .004, -.14); }
  g.moveTo(-.115, -.14); g.quadraticCurveTo(0, -.115, .118, -.14); g.stroke();
  const jp = jalur(p => { const b = [-.11, -.02, .0, -.13, .064]; p.moveTo(b[0] - .02, b[1] - .025); lobus(p, b); p.quadraticCurveTo(-.08, .01, b[0] - .02, b[1] - .025); p.closePath(); });
  isiTepi(jp, WR.kulit, WR.garis, L); bayangDi(jp, jalur(p => p.rect(-.2, -.06, .3, .1)), rgba(WR.kulitB, .6));
  g.restore();
}
// smooth limb: one continuous tube bending through A→B→C (no joints, no seams); o: capAwal, gembung, mulai (0-1: where the outline starts), terang
let arahLengan = 0, JAKET = null;
function pita(A0, B0, C0, w0, w1, isi, gelap, lw, o = {}) {
  const lembut = o.lembut ?? .5, cx = lerp(2 * B0[0] - (A0[0] + C0[0]) / 2, B0[0], lembut), cy = lerp(2 * B0[1] - (A0[1] + C0[1]) / 2, B0[1], lembut), N = 28, Lp = [], Rp = [], M = [];
  let th0 = 0, th1 = 0;
  for (let i = 0; i <= N; i++) { const t = i / N, mt = 1 - t;
    const x = mt * mt * A0[0] + 2 * mt * t * cx + t * t * C0[0], y = mt * mt * A0[1] + 2 * mt * t * cy + t * t * C0[1];
    let dx = 2 * mt * (cx - A0[0]) + 2 * t * (C0[0] - cx), dy = 2 * mt * (cy - A0[1]) + 2 * t * (C0[1] - cy); const d = Math.hypot(dx, dy) || 1; dx /= d; dy /= d;
    if (i === 0) th0 = Math.atan2(dy, dx); if (i === N) th1 = Math.atan2(dy, dx);
    const w = (lerp(w0, w1, t) + Math.sin(t * PI) * (o.gembung || 0)) / 2;
    Lp.push([x - dy * w, y + dx * w]); Rp.push([x + dy * w, y - dx * w]); M.push([x, y, dx, dy, w]); }
  const rEnd = M[N][4], rStart = M[0][4];
  // drop offset points that fold back on a tight bend (inner elbow) so edges never loop
  const rapikan = P => { const out = [P[0]]; for (let i = 1; i < P.length; i++) { const q = out[out.length - 1], d = [P[i][0] - q[0], P[i][1] - q[1]]; if (d[0] * M[i][2] + d[1] * M[i][3] > 0 || i === P.length - 1) out.push(P[i]); } return out; };
  { const L2 = rapikan(Lp), R2 = rapikan(Rp); Lp.length = 0; Rp.length = 0; const n = Math.max(L2.length, R2.length);
    for (let i = 0; i <= N; i++) { Lp.push(L2[Math.min(L2.length - 1, Math.round(i / N * (L2.length - 1)))]); Rp.push(R2[Math.min(R2.length - 1, Math.round(i / N * (R2.length - 1)))]); } }
  const bentuk = jalur(p => { p.moveTo(...Lp[0]); for (const q of Lp) p.lineTo(...q); if (!o.ujungDatar) p.arc(C0[0], C0[1], rEnd, th1 + PI / 2, th1 - PI / 2, true); for (let i = N; i >= 0; i--) p.lineTo(...Rp[i]); if (o.capAwal) p.arc(A0[0], A0[1], rStart, th0 - PI / 2, th0 + PI / 2, true); p.closePath(); });
  g.fillStyle = isi; g.fill(bentuk);
  g.save(); g.clip(bentuk); g.lineJoin = 'round'; g.lineCap = 'round';
  g.strokeStyle = gelap; g.lineWidth = w0 * .55; g.beginPath(); Rp.forEach((q, i) => i ? g.lineTo(...q) : g.moveTo(...q)); g.lineTo(C0[0] + Math.cos(th1) * rEnd, C0[1] + Math.sin(th1) * rEnd); g.stroke();
  if (o.terang) { g.strokeStyle = o.terang; g.lineWidth = w0 * .12; g.beginPath(); M.forEach(([x, y, dx, dy, w], i) => { const px = x - dy * w * .55, py = y + dx * w * .55; i ? g.lineTo(px, py) : g.moveTo(px, py); }); g.stroke(); }
  g.restore();
  const i0 = Math.round((o.mulai || 0) * N);
  g.strokeStyle = WR.garis; g.lineWidth = lw; g.lineJoin = 'round'; g.lineCap = 'round'; g.beginPath();
  g.moveTo(...Lp[i0]); for (let i = i0; i <= N; i++) g.lineTo(...Lp[i]); if (o.ujungDatar) g.moveTo(...Rp[N]); else g.arc(C0[0], C0[1], rEnd, th1 + PI / 2, th1 - PI / 2, true); for (let i = N; i >= i0; i--) g.lineTo(...Rp[i]);
  g.stroke();
  return M;
}
// jacket sleeve: smooth tube + cuff drawn over the wrist after the hand
function lengan(bahu, siku, pg, lw, tangan, w = 1, lembut = .75) {
  arahLengan = Math.atan2(pg[1] - siku[1], pg[0] - siku[0]) + PI / 2;
  const A = bahu || [siku[0] + (siku[0] - pg[0]) * .6, siku[1] + (siku[1] - pg[1]) * .6];
  const M = pita(A, siku, pg, .44 * w, .34 * w, WR.jaket, WR.jaketB, lw, { mulai: bahu ? .3 : 0, capAwal: !!bahu, gembung: .03, lembut, ujungDatar: true });
  // soft fold lines near the bend
  const N = M.length - 1, m = M[Math.round(N * .5)]; g.strokeStyle = rgba(WR.garis, .35); g.lineWidth = lw * .7; g.lineCap = 'round';
  for (const k of [-.06, .06]) { const i = Math.round(N * (.5 + k)), q = M[i]; g.beginPath(); g.moveTo(q[0] - q[3] * q[4] * .7, q[1] + q[2] * q[4] * .7); g.quadraticCurveTo(q[0] + q[2] * .04, q[1] + q[3] * .04, q[0] - q[3] * q[4] * .1, q[1] + q[2] * q[4] * .1); g.stroke(); }
  if (bahu && JAKET) { g.save(); g.clip(JAKET.jk); const cx = bahu[0] * 1.18, cy = bahu[1] - .1, rr = .42;
    const gr = g.createRadialGradient(cx, cy, rr * .55, cx, cy, rr); gr.addColorStop(0, '#000'); gr.addColorStop(1, 'rgba(0,0,0,0)');
    g.beginPath(); g.arc(cx, cy, rr, 0, TAU); g.clip(); g.fillStyle = WR.jaket; g.fill(JAKET.jk); bayangDi(JAKET.jk, JAKET.jkB, WR.jaketB); bayangDi(JAKET.jk, JAKET.jkT, WR.jaketT); g.restore();
    g.save(); g.beginPath(); g.arc(cx, cy, rr, 0, TAU); g.clip(); g.strokeStyle = WR.garis; g.lineWidth = lw; g.stroke(JAKET.jk); g.restore(); }
  if (tangan) tangan();
  // cuff
  let ia = N, pj = 0; while (ia > 1 && pj < .17 * w) { pj += Math.hypot(M[ia][0] - M[ia - 1][0], M[ia][1] - M[ia - 1][1]); ia--; }
  const a = M[ia], b0 = M[N], b = [b0[0] + b0[2] * .035, b0[1] + b0[3] * .035, b0[2], b0[3], b0[4]], ww = b[4] * 1.08;
  const mn = jalur(p => { p.moveTo(a[0] - a[3] * ww, a[1] + a[2] * ww); p.lineTo(b[0] - b[3] * ww, b[1] + b[2] * ww); p.quadraticCurveTo(b[0] + b[2] * ww * .18, b[1] + b[3] * ww * .18, b[0] + b[3] * ww, b[1] - b[2] * ww); p.lineTo(a[0] + a[3] * ww, a[1] - a[2] * ww); p.quadraticCurveTo(a[0] + a[2] * ww * .2, a[1] + a[3] * ww * .2, a[0] - a[3] * ww, a[1] + a[2] * ww); p.closePath(); });
  isiTepi(mn, WR.jaket, WR.garis, lw); bayangDi(mn, jalur(p => { p.moveTo(a[0] + a[3] * ww * .1, a[1] - a[2] * ww * .1); p.lineTo(b[0] + b[3] * ww * .1, b[1] - b[2] * ww * .1); p.lineTo(b[0] + b[3] * ww * 2, b[1] - b[2] * ww * 2); p.lineTo(a[0] + a[3] * ww * 2, a[1] - a[2] * ww * 2); p.closePath(); }), WR.jaketB);
  g.strokeStyle = rgba(WR.garis, .3); g.lineWidth = lw * .6; g.beginPath(); for (const f of [.45]) { g.moveTo(lerp(a[0], b[0], f) - a[3] * ww * .8, lerp(a[1], b[1], f) + a[2] * ww * .8); g.lineTo(lerp(a[0], b[0], f) + a[3] * ww * .8, lerp(a[1], b[1], f) - a[2] * ww * .8); } g.stroke();
}
function cangkir(x, y, lw, t) {
  g.strokeStyle = WR.garis; g.lineWidth = .1 + lw * 2; g.beginPath(); g.arc(x + .32, y - .02, .14, -1.2, 1.2); g.stroke(); g.strokeStyle = '#efe0c8'; g.lineWidth = .1; g.stroke();
  const b = jalur(p => p.roundRect(x - .32, y - .34, .64, .64, [.04, .04, .14, .14])); isiTepi(b, '#f3e6d2', WR.garis, lw);
  bayangDi(b, jalur(p => p.rect(x + .1, y - .4, .3, .8)), '#d9c6aa'); bayangDi(b, jalur(p => p.rect(x - .4, y - .06, .8, .12)), '#c8765a');
  g.fillStyle = 'rgba(255,255,255,.6)'; g.fillRect(x - .24, y - .28, .05, .45);
  const bib = jalur(p => p.ellipse(x, y - .34, .32, .07, 0, 0, TAU)); isiTepi(bib, '#e9d9c0', WR.garis, lw); g.fillStyle = '#5a3420'; g.beginPath(); g.ellipse(x, y - .335, .26, .05, 0, 0, TAU); g.fill();
  g.save(); g.lineCap = 'round'; for (let i = 0; i < 3; i++) { const f = (t * .35 + i / 3) % 1; g.strokeStyle = `rgba(255,250,240,${.4 * Math.sin(f * PI)})`; g.lineWidth = .05; g.beginPath(); for (let k = 0; k <= 12; k++) { const yy = y - .42 - k * .06 - f * .3, xx = x + (i - 1) * .1 + Math.sin(k * .7 + t * 2 + i) * .06 * (k / 12 + .3); k ? g.lineTo(xx, yy) : g.moveTo(xx, yy); } g.stroke(); } g.restore();
}
function poseTangan(TG, lw, ns, t) {
  const k = TG ? TG.k ?? 1 : 0, P = TG ? TG.pose : null;
  g.save(); g.translate(0, ns); g.beginPath(); g.rect(-4, -4, 8, 7.4); g.clip();
  const istirahat = sd => { g.strokeStyle = rgba(WR.garis, .75); g.lineWidth = lw * .9; g.beginPath(); g.moveTo(sd * .97, 1.52); g.bezierCurveTo(sd * .87, 2.0, sd * .85, 2.6, sd * .89, 3.5); g.stroke();
    g.save(); g.beginPath(); g.moveTo(sd * .97, 1.52); g.bezierCurveTo(sd * .87, 2.0, sd * .85, 2.6, sd * .89, 3.5); g.lineTo(sd * .8, 3.5); g.bezierCurveTo(sd * .76, 2.6, sd * .78, 2.0, sd * .9, 1.5); g.closePath(); g.fillStyle = rgba(WR.jaketB, .55); g.fill(); g.restore(); };
  const pakaiKiri = P === 'syal', pakaiKanan = !!P && P !== 'cangkir';
  if (!pakaiKiri) istirahat(-1);
  if (!pakaiKanan) istirahat(1);
  if (P === 'cangkir') {
    const y = 2.55 - k * .2;
    cangkir(0, y, lw, t);
    lengan(null, [-.98, 3.9], [-.7, y + .16], lw, () => tanganAnime(-.66, y + .1, PI / 2 - .4, 1.45, 'genggam', true, lw));
    lengan(null, [.98, 3.9], [.7, y + .16], lw, () => tanganAnime(.66, y + .1, -(PI / 2 - .4), 1.45, 'genggam', false, lw));
  } else if (P === 'rambut' || P === 'lambai') {
    const ke = eio(k), w = lerp(.8, 1, ke);
    if (P === 'rambut') { const siku = [lerp(1.0, 1.52, ke), lerp(2.4, 2.05, ke)], pg = [lerp(1.0, .98, ke), lerp(3.6, .72, ke)];
      lengan([.78, 1.62], siku, pg, lw, ke > .05 ? () => tanganAnime(pg[0], pg[1], arahLengan * lerp(1, .35, ke) - .08 * ke, 1.5, 'lentik', false, lw) : null, w); }
    else { const ay = Math.sin(t * 7.5) * .1 * ke, siku = [lerp(1.0, 1.62, ke), lerp(2.4, 2.15, ke)], pg = [lerp(1.0, 1.36, ke) + ay * .6, lerp(3.6, .62, ke)];
      lengan([.78, 1.62], siku, pg, lw, ke > .05 ? () => tanganAnime(pg[0], pg[1], lerp(arahLengan - (arahLengan > PI ? TAU : 0), -.12 + ay * 1.4, klem(ke * 1.6)), 1.7, 'buka', true, lw) : null, w, lerp(.75, .15, ke)); }
  } else if (P === 'dagu') {
    const pg = [lerp(.5, .26, k), lerp(3.9, 1.08, k)]; lengan(null, [lerp(.6, .55, k), lerp(4.3, 3.0, k)], pg, lw, () => tanganAnime(pg[0], pg[1], -.22, 1.55, 'genggam', false, lw));
  } else if (P === 'syal') {
    for (const sd of [-1, 1]) { const pg = [sd * .4, lerp(2.6, 1.78, k)]; lengan(null, [sd * .95, 3.0], pg, lw, () => tanganAnime(pg[0], pg[1], sd * -.2, 1.45, 'genggam', sd < 0, lw)); }
  }
  g.restore();
}

// ---------- full body, seen from behind (colored), walking / standing; (x,y) = feet, h = height
// o: jalan, fase, angin, arahAngin, ransel, syal, mantel, mantelB, tengadah, rambutPendek
function gadisBelakang(x, y, h, o = {}) {
  const t = TK.t, fase = o.fase || 0, ang = o.angin || 0, ar = o.arahAngin || 1, jalan = !!o.jalan;
  const bob = jalan ? -.01 * Math.abs(Math.cos(fase)) : Math.sin(t * 1.6) * .002, sway = jalan ? Math.sin(fase) * .006 : 0;
  const wx = k => ang * ar * .07 * k * (1 + .3 * Math.sin(t * 2.6 + k * 4)) + (jalan ? Math.sin(fase - k) * .006 * k : Math.sin(t * 1.3 + k) * .002 * k);
  const lw = 1.5 / h, mantel = o.mantel || WR.jaket, mantelB = o.mantelB || WR.jaketB;
  g.save(); g.translate(x, y); g.scale(h, h); g.lineJoin = 'round'; g.lineCap = 'round';
  if (o.bayangan !== false) { g.save(); g.scale(1, .15); const gr = g.createRadialGradient(0, 0, 0, 0, 0, .2); gr.addColorStop(0, `rgba(10,5,10,${o.bayangan ?? .35})`); gr.addColorStop(1, 'rgba(10,5,10,0)'); g.fillStyle = gr; g.fillRect(-.2, -.2, .4, .4); g.restore(); }
  // legs
  const kaki = [];
  for (const s of [-1, 1]) {
    const p = Math.sin(fase + (s > 0 ? PI : 0)), angkat = jalan ? Math.max(0, p) * .035 : 0, maju = jalan ? p * .012 : 0;
    const pinggul = [s * .045 + sway, -.5 + bob], lutut = [s * .05 + sway * .5 + maju * .3, -.28 - angkat * .5], mata_k = [s * .052 + maju * .2, -.055 - angkat];
    kaki.push({ s, pinggul, lutut, mata_k, angkat });
  }
  kaki.sort((a, b) => b.angkat - a.angkat);
  for (const k of kaki) {
    pita(k.pinggul, k.lutut, k.mata_k, .078, .054, WR.celana, WR.celanaB, lw, { gembung: .004 });
    const sp = jalur(p => { p.moveTo(k.mata_k[0] - .03, k.mata_k[1] - .01); p.lineTo(k.mata_k[0] + .03, k.mata_k[1] - .01); p.quadraticCurveTo(k.mata_k[0] + .036, k.mata_k[1] + .045, k.mata_k[0], k.mata_k[1] + .05 - k.angkat * .3); p.quadraticCurveTo(k.mata_k[0] - .036, k.mata_k[1] + .045, k.mata_k[0] - .03, k.mata_k[1] - .01); p.closePath(); });
    isiTepi(sp, WR.sepatu, WR.garis, lw); bayangDi(sp, jalur(p => p.rect(k.mata_k[0] - .05, k.mata_k[1] + .03 - k.angkat * .3, .1, .05)), WR.sepatuB);
  }
  // torso (hoodie / coat)
  const bawah = o.mantel ? -.3 : -.47, lb = o.mantel ? .135 : .118;
  const jk = jalur(p => { p.moveTo(-.035 + sway, -.848 + bob); p.quadraticCurveTo(-.09, -.84 + bob, -.1 + sway, -.815 + bob); p.quadraticCurveTo(-.122, -.8 + bob, -.118 + sway, -.76 + bob); p.lineTo(-lb + sway + wx(.2), bawah + bob); p.quadraticCurveTo(sway, bawah + .012 + bob, lb + sway + wx(.2), bawah + bob); p.lineTo(.118 + sway, -.76 + bob); p.quadraticCurveTo(.122, -.8 + bob, .1 + sway, -.815 + bob); p.quadraticCurveTo(.09, -.84 + bob, .035 + sway, -.848 + bob); p.closePath(); });
  isiTepi(jk, mantel, WR.garis, lw);
  bayangDi(jk, jalur(p => { p.moveTo(.03, -.9); p.quadraticCurveTo(.06, -.6, .04, -.2); p.lineTo(.2, -.2); p.lineTo(.2, -.9); p.closePath(); }), mantelB);
  g.fillStyle = mantelB; g.fillRect(-lb + sway, bawah - .03 + bob, lb * 2, .03);
  g.strokeStyle = rgba(WR.garis, .7); g.lineWidth = lw * .8; g.beginPath(); g.moveTo(-.05 + sway, -.62 + bob); g.quadraticCurveTo(-.03, -.56, -.06 + sway, -.5 + bob); g.moveTo(.06 + sway, -.66 + bob); g.quadraticCurveTo(.04, -.58, .07 + sway, -.52 + bob); g.stroke();
  // arms
  for (const s of [-1, 1]) {
    const ay = jalan ? Math.sin(fase + (s < 0 ? PI : 0)) * .02 : 0;
    const bahu = [s * .098 + sway, -.8 + bob], siku = [s * .128 + sway + ay * .3, -.655 + bob], tng = [s * .122 + sway + ay, -.525 + bob];
    const tg = jalur(p => p.ellipse(tng[0], tng[1] + .026, .019, .027, 0, 0, TAU)); isiTepi(tg, WR.kulit, WR.garis, lw); bayangDi(tg, jalur(p => p.rect(tng[0] + (s > 0 ? 0 : -.001), tng[1], .03, .06)), WR.kulitB);
    pita([s * .088 + sway, -.765 + bob], [siku[0] + s * .004, siku[1]], tng, .046, .04, mantel, mantelB, lw, { mulai: .25, capAwal: true });
  }
  // hood
  const hd = jalur(p => { p.moveTo(-.07 + sway, -.845 + bob); p.bezierCurveTo(-.085, -.77 + bob, .085, -.77 + bob, .07 + sway, -.845 + bob); p.closePath(); });
  if (!o.mantel) isiTepi(hd, mantelB, WR.garis, lw);
  if (o.ransel) {
    for (const s of [-1, 1]) { g.strokeStyle = WR.ranselB; g.lineWidth = .02; g.beginPath(); g.moveTo(s * .055 + sway, -.83 + bob); g.lineTo(s * .07 + sway, -.76 + bob); g.stroke(); }
    const r = jalur(p => p.roundRect(-.078 + sway, -.785 + bob, .156, .26, [.05, .05, .025, .025])); isiTepi(r, WR.ransel, WR.garis, lw);
    bayangDi(r, jalur(p => p.rect(.03 + sway, -.8 + bob, .1, .3)), WR.ranselB); bayangDi(r, jalur(p => p.rect(-.08 + sway, -.785 + bob, .03, .26)), WR.ranselT);
    const k2 = jalur(p => p.roundRect(-.055 + sway, -.635 + bob, .11, .09, .02)); isiTepi(k2, WR.ranselB, WR.garis, lw);
    g.strokeStyle = WR.garis; g.lineWidth = lw; g.beginPath(); g.moveTo(-.06 + sway, -.73 + bob); g.quadraticCurveTo(sway, -.745 + bob, .06 + sway, -.73 + bob); g.stroke();
  }
  if (o.syal) { const sy = jalur(p => p.roundRect(-.07 + sway, -.865 + bob, .14, .045, .02)); isiTepi(sy, WR.syal, WR.garis, lw); const ek = jalur(p => { p.moveTo(.035 + sway, -.83 + bob); p.lineTo(.06 + wx(1), -.7 + bob); p.lineTo(.025 + wx(1), -.695 + bob); p.lineTo(.005 + sway, -.83 + bob); p.closePath(); }); isiTepi(ek, WR.syal, WR.garis, lw); bayangDi(ek, jalur(p => p.rect(.03 + sway, -.9, .06, .3)), WR.syalB); }
  // head + hair from behind
  const ty = o.tengadah || 0, ky = -.925 + bob, pj = o.rambutPendek ? -.79 : (o.ransel ? -.7 : -.66);
  const rb = jalur(p => {
    p.moveTo(sway, ky - .075 + ty * .01);
    p.bezierCurveTo(.05 + sway, ky - .077, .07 + wx(.05) + sway, ky - .04, .068 + wx(.1) + sway, ky + .01);
    p.bezierCurveTo(.07 + wx(.3) + sway, ky + .07, .085 + wx(.6) + sway, (ky + pj) / 2 + .03, .082 + wx(1) + sway, pj);
    for (let i = 1; i <= 7; i++) { const xx = .082 - i * .164 / 7 + wx(1) + sway; if (i % 2) p.quadraticCurveTo(xx + .02, pj + .01, xx, pj + .03 + (i === 3 ? .012 : 0)); else p.quadraticCurveTo(xx + .012, pj + .01, xx, pj - .01); }
    p.bezierCurveTo(-.085 + wx(.6) + sway, (ky + pj) / 2 + .03, -.07 + wx(.3) + sway, ky + .07, -.068 + wx(.1) + sway, ky + .01);
    p.bezierCurveTo(-.07 + wx(.05) + sway, ky - .04, -.05 + sway, ky - .077, sway, ky - .075 + ty * .01); p.closePath();
  });
  isiTepi(rb, WR.rambut, WR.garis, lw);
  bayangDi(rb, jalur(p => { p.moveTo(.015 + sway, ky - .1); p.quadraticCurveTo(.03, (ky + pj) / 2, .01 + wx(1) + sway, pj + .05); p.lineTo(.2, pj + .05); p.lineTo(.2, ky - .1); p.closePath(); }), WR.rambutB);
  bayangDi(rb, jalur(p => p.rect(-.2, ky + .06, .4, .5)), rgba(WR.rambutB, .45));
  g.save(); g.clip(rb); g.strokeStyle = WR.rambutT; g.lineWidth = .016; g.beginPath(); g.arc(sway, ky + .005, .058, PI * 1.08, PI * 1.72); g.stroke();
  g.strokeStyle = rgba(WR.rambutK, .8); g.lineWidth = .006; g.beginPath(); g.arc(sway, ky + .005, .058, PI * 1.2, PI * 1.5); g.stroke();
  g.strokeStyle = rgba(WR.rambutB, .85); g.lineWidth = .004; for (let i = -3; i <= 3; i++) { g.beginPath(); g.moveTo(i * .012 + sway, ky - .06); g.quadraticCurveTo(i * .024 + wx(.4) + sway, ky + .08, i * .026 + wx(1) + sway, pj); g.stroke(); }
  g.restore();
  if (ang > .15) { g.strokeStyle = WR.rambut; g.lineWidth = .005; for (let i = 0; i < 4; i++) { const yy = ky + .04 + i * .04, x0 = ar * .06 + sway; g.beginPath(); g.moveTo(x0, yy); g.quadraticCurveTo(x0 + wx(1), yy + .03, x0 + wx(1.8) + Math.sin(t * 5 + i) * .006, yy + .05 + Math.sin(t * 4 + i) * .01); g.stroke(); } }
  rimDi([jalur(p => { p.moveTo(sway, ky - .075); p.bezierCurveTo(.05 + sway, ky - .077, .07 + sway, ky - .04, .068 + sway, ky + .01); p.bezierCurveTo(.07 + wx(.3) + sway, ky + .07, .085 + wx(.6) + sway, (ky + pj) / 2 + .03, .082 + wx(1) + sway, pj); }), jalur(p => { p.moveTo(.1 + sway, -.815 + bob); p.quadraticCurveTo(.122, -.8 + bob, .118 + sway, -.76 + bob); p.lineTo(lb + sway, bawah + bob); }), jalur(p => { p.moveTo(.13 + sway, -.66 + bob); p.lineTo(.125 + sway, -.53 + bob); })], .008);
  g.restore();
}

// ---------- on a swing, side view; (x,y) = seat, faces +x (dir -1 flips)
function gadisAyun(x, y, h, o) {
  const t = TK.t, v = o.kec || 0, d = o.dir || 1, k = (v + 1) / 2, lw = 1.6 / h;
  g.save(); g.translate(x, y); g.rotate(o.miring || 0); g.scale(h * d, h); g.lineJoin = 'round'; g.lineCap = 'round';
  const cond = -.12 - v * .12, bahu = [Math.sin(cond) * .36 * -1 - .01, -Math.cos(cond) * .36], kep = [bahu[0] + .015, bahu[1] - .115];
  const lut = [.17, -.025], ank = [lut[0] + lerp(.03, .17, k), lut[1] + lerp(.17, .04, k)];
  // back hair streaming behind
  const ek = -.12 - v * .09, wv = Math.sin(t * 6) * .012;
  const rb = jalur(p => { p.moveTo(kep[0] + .01, kep[1] - .07); p.bezierCurveTo(kep[0] - .07, kep[1] - .08, kep[0] - .09, kep[1] - .02, kep[0] - .08 + ek * .3, kep[1] + .05); p.bezierCurveTo(kep[0] - .08 + ek * .6, kep[1] + .1 + wv, kep[0] - .06 + ek, kep[1] + .14, kep[0] - .04 + ek * 1.25, kep[1] + .19 + wv); p.bezierCurveTo(kep[0] - .03 + ek * .6, kep[1] + .16, kep[0] - .02, kep[1] + .12, kep[0] - .02, kep[1] + .07); p.closePath(); });
  isiTepi(rb, WR.rambutB, WR.garis, lw);
  // far leg (darker), body, near leg
  pita([.02, -.02], [lut[0] - .01, lut[1] - .01], [ank[0] - .02, ank[1] - .01], .062, .048, WR.celanaB, '#1f2b44', lw);
  const bd = jalur(p => { p.moveTo(-.07, .03); p.quadraticCurveTo(-.085 + bahu[0], -.2, bahu[0] - .055, bahu[1] + .02); p.quadraticCurveTo(bahu[0], bahu[1] - .02, bahu[0] + .05, bahu[1] + .02); p.quadraticCurveTo(.07, -.18, .09, .03); p.closePath(); });
  pita([bahu[0] - .02, bahu[1]], [bahu[0] + .05, bahu[1] + .03], [-.006, bahu[1] - .085], .042, .034, WR.jaketB, '#141a30', lw);
  isiTepi(bd, WR.jaket, WR.garis, lw); bayangDi(bd, jalur(p => p.rect(-.2, -.5, .12, .6)), WR.jaketB);
  pita([.02, 0], lut, ank, .068, .052, WR.celana, WR.celanaB, lw);
  const sp = jalur(p => p.ellipse(ank[0] + .025, ank[1] + .012, .045, .022, lerp(1.1, .1, k), 0, TAU)); isiTepi(sp, WR.sepatu, WR.garis, lw);
  // head in profile
  const kp = jalur(p => p.ellipse(kep[0], kep[1], .06, .066, 0, 0, TAU)); isiTepi(kp, WR.kulit, WR.garis, lw);
  g.fillStyle = WR.kulit; g.strokeStyle = WR.garis; g.lineWidth = lw; const hid = jalur(p => { p.moveTo(kep[0] + .055, kep[1] - .005); p.lineTo(kep[0] + .07, kep[1] + .012); p.lineTo(kep[0] + .056, kep[1] + .02); }); g.fill(hid); g.stroke(hid);
  const rd = jalur(p => { p.moveTo(kep[0] - .07, kep[1] + .04); p.bezierCurveTo(kep[0] - .08, kep[1] - .08, kep[0] + .05, kep[1] - .1, kep[0] + .068, kep[1] - .02); p.lineTo(kep[0] + .05, kep[1] - .015); p.lineTo(kep[0] + .035, kep[1] - .03); p.lineTo(kep[0] + .02, kep[1] - .01); p.lineTo(kep[0] - .01, kep[1] - .02); p.quadraticCurveTo(kep[0] - .03, kep[1] + .03, kep[0] - .045, kep[1] + .075); p.closePath(); });
  isiTepi(rd, WR.rambut, WR.garis, lw);
  g.save(); g.clip(rd); g.strokeStyle = WR.rambutT; g.lineWidth = .012; g.beginPath(); g.arc(kep[0], kep[1] + .01, .06, PI * 1.2, PI * 1.7); g.stroke(); g.restore();
  g.fillStyle = WR.iris1; g.beginPath(); g.ellipse(kep[0] + .036, kep[1] + .008, .008, .015, 0, 0, TAU); g.fill(); g.fillStyle = '#fff'; g.beginPath(); g.arc(kep[0] + .034, kep[1] + .002, .003, 0, TAU); g.fill();
  g.strokeStyle = WR.garis; g.lineWidth = .006; g.beginPath(); g.moveTo(kep[0] + .026, kep[1] - .008); g.lineTo(kep[0] + .048, kep[1] - .006); g.stroke();
  g.fillStyle = 'rgba(255,120,130,.45)'; g.beginPath(); g.ellipse(kep[0] + .03, kep[1] + .03, .014, .007, 0, 0, TAU); g.fill();
  // scarf end
  const sy = jalur(p => { p.moveTo(bahu[0] - .02, bahu[1] - .01); p.lineTo(bahu[0] - .1 - v * .05, bahu[1] + .06 + Math.sin(t * 7) * .01); p.lineTo(bahu[0] - .09 - v * .05, bahu[1] + .09); p.lineTo(bahu[0] + .01, bahu[1] + .025); p.closePath(); }); isiTepi(sy, WR.syal, WR.garis, lw);
  const sl = jalur(p => p.roundRect(bahu[0] - .045, bahu[1] - .015, .09, .03, .012)); isiTepi(sl, WR.syal, WR.garis, lw);
  // near arm holding rope
  const siku = [bahu[0] + .075, bahu[1] + .02], tg = [.004, bahu[1] - .085];
  pita(bahu, siku, tg, .046, .038, WR.jaket, WR.jaketB, lw, { mulai: .15 });
  const tgp = jalur(p => p.ellipse(tg[0], tg[1], .02, .022, 0, 0, TAU)); isiTepi(tgp, WR.kulit, WR.garis, lw);
  rimDi([jalur(p => { p.moveTo(kep[0] - .07, kep[1] + .04); p.bezierCurveTo(kep[0] - .08, kep[1] - .08, kep[0] + .05, kep[1] - .1, kep[0] + .068, kep[1] - .02); }), jalur(p => { p.moveTo(-.07, .03); p.quadraticCurveTo(-.085 + bahu[0], -.2, bahu[0] - .055, bahu[1] + .02); })], .01);
  g.restore();
}


// =====================================================================
//  SCENERY HELPERS
// =====================================================================
const potret = () => H > W;
const bulat = (x, y, r) => { g.beginPath(); g.arc(x, y, Math.max(.1, r), 0, TAU); g.fill(); };
function dorong(z, cx = W / 2, cy = H / 2, gx = 0, gy = 0) { g.translate(cx + gx, cy + gy); g.scale(z, z); g.translate(-cx, -cy); }
function saring(f, fn) { g.save(); g.filter = f; fn(); g.restore(); }
function papan(x0, y0, w, h, c1, c2, lebar, seed) { // wooden planks
  g.fillStyle = c1; g.fillRect(x0, y0, w, h); const r = rng(seed);
  for (let x = x0; x < x0 + w; x += lebar) { g.fillStyle = rgba(c2, .15 + r() * .35); g.fillRect(x, y0, lebar, h); g.fillStyle = 'rgba(0,0,0,.35)'; g.fillRect(x, y0, 2, h); g.fillStyle = 'rgba(255,220,180,.07)'; g.fillRect(x + 2, y0, 2, h);
    g.strokeStyle = 'rgba(0,0,0,.08)'; g.lineWidth = 1; for (let k = 0; k < 3; k++) { const xx = x + lebar * (.25 + r() * .5); g.beginPath(); g.moveTo(xx, y0); g.bezierCurveTo(xx + 4, y0 + h * .3, xx - 4, y0 + h * .6, xx + 2, y0 + h); g.stroke(); } }
}
function rimbun(x, y, r, c, gelap, terang, seed, n = 14, pipih = .7) { // leafy canopy
  const R = rng(seed), bl = [];
  for (let i = 0; i < n; i++) { const a = R() * TAU, d = Math.sqrt(R()) * r * .7; bl.push([x + Math.cos(a) * d, y + Math.sin(a) * d * pipih, r * (.28 + R() * .22)]); }
  bl.sort((a, b) => a[1] - b[1]);
  g.fillStyle = gelap; for (const [a, b, rr] of bl) bulat(a, b + rr * .15, rr);
  g.fillStyle = c; for (const [a, b, rr] of bl) bulat(a - rr * .08, b - rr * .06, rr * .85);
  if (terang) { g.fillStyle = terang; for (const [a, b, rr] of bl) bulat(a - rr * .3, b - rr * .32, rr * .38); }
}
function palem(x, y, h, c, gelap, t, seed = 1) {
  const r = rng(seed), lean = (r() - .5) * .3, top = [x + h * lean, y - h];
  g.strokeStyle = gelap; g.lineWidth = h * .035; g.lineCap = 'round'; g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + h * lean * .2, y - h * .5, ...top); g.stroke();
  g.strokeStyle = rgba('#000000', .25); g.lineWidth = h * .01; for (let k = 1; k < 10; k++) { const f = k / 10, px = lerp(x, top[0], f * f), py = lerp(y, top[1], f); g.beginPath(); g.moveTo(px - h * .016, py); g.lineTo(px + h * .016, py - 2); g.stroke(); }
  for (let i = 0; i < 9; i++) { const a = -PI / 2 + (i / 8 - .5) * 3.6 + Math.sin(t * 1.3 + i) * .04, L = h * (.32 + r() * .12);
    const ex = top[0] + Math.cos(a) * L, ey = top[1] + Math.sin(a) * L * .6 + L * .45;
    g.fillStyle = i % 2 ? c : gelap; g.beginPath(); g.moveTo(...top); g.quadraticCurveTo(top[0] + Math.cos(a) * L * .6, top[1] + Math.sin(a) * L * .6 - L * .15 - h * .02, ex, ey); g.quadraticCurveTo(top[0] + Math.cos(a) * L * .5, top[1] + Math.sin(a) * L * .5 - L * .05 + h * .02, ...top); g.fill(); }
}
function rumput(y0, y1, n, c, t, tinggi, seed, lebar = 1.5) {
  const r = rng(seed); g.strokeStyle = c; g.lineWidth = lebar; g.beginPath();
  for (let i = 0; i < n; i++) { const x = r() * (W + 40) - 20, y = lerp(y0, y1, r()), hh = tinggi * (.5 + r()) * (.4 + .6 * (y - y0) / Math.max(1, y1 - y0)), sw = Math.sin(t * 1.8 + x * .02) * hh * .25; g.moveTo(x, y); g.quadraticCurveTo(x + sw * .3, y - hh * .5, x + sw + (r() - .5) * hh * .3, y - hh); }
  g.stroke();
}
// big mountain with ridges, gullies and snow
function gunung(o) {
  const { px, py, kiri, kanan, alas, c1, c2, bayang, salju, saljuB, garisSalju, seed, kasar = 1 } = o;
  const R = rng(seed), N = 90, pts = [];
  for (let i = 0; i <= N; i++) { const f = i / N, x = lerp(kiri, kanan, f); const d = x < px ? (px - x) / (px - kiri) : (x - px) / (kanan - px);
    const y = lerp(py, alas, Math.pow(d, .9)) - n1(f * 8, seed) * (alas - py) * .07 * kasar * Math.sin(d * PI); pts.push([x, y]); }
  const p = new Path2D(); p.moveTo(kiri, alas + 400); pts.forEach(q => p.lineTo(...q)); p.lineTo(kanan, alas + 400); p.closePath();
  g.save(); g.fillStyle = gradV(py, alas, [[0, c1], [1, c2]]); g.fill(p); g.clip(p);
  // shaded faces (right of every ridge spur)
  g.fillStyle = bayang; g.beginPath(); g.moveTo(px, py); for (let i = 0; i < 9; i++) { const f = (i + 1) / 10, x = lerp(px, kanan, f), y = lerp(py, alas, f); g.lineTo(x + (R() - .3) * (kanan - px) * .08, y + (alas - py) * (.05 + R() * .08)); } g.lineTo(kanan, alas + 400); g.lineTo(px + (kanan - px) * .05, alas + 400); g.closePath(); g.fill();
  const baji = (x0, y0, w, Lg, lean, warna) => { g.fillStyle = warna; g.beginPath(); g.moveTo(x0 - w / 2, y0); g.quadraticCurveTo(x0 - w * .3 + lean * .5, y0 + Lg * .5, x0 + lean, y0 + Lg); g.quadraticCurveTo(x0 + w * .3 + lean * .5, y0 + Lg * .5, x0 + w / 2, y0); g.closePath(); g.fill(); };
  g.save(); g.filter = `blur(${Math.max(1, (kanan - kiri) / 900)}px)`;
  for (let i = 0; i < 18; i++) { const x0 = lerp(kiri, kanan, (i + R() * .8) / 18), q = pts[Math.round((x0 - kiri) / (kanan - kiri) * N)], Lg = (alas - q[1]) * (.35 + R() * .5), w = (kanan - kiri) * (.012 + R() * .02), lean = (x0 - px) * .12;
    baji(q[0], q[1] + 2, w, Lg, lean, rgba('#000000', .06 + R() * .06)); baji(q[0] + w * .7, q[1] + 4, w * .5, Lg * .8, lean, rgba('#ffffff', .04)); }
  g.restore();
  if (salju) { const gs = garisSalju;
    g.fillStyle = salju; g.beginPath(); g.moveTo(kiri, -50); pts.forEach(q => g.lineTo(q[0], q[1] - 2)); g.lineTo(kanan, -50); g.closePath();
    g.save(); g.clip(); g.beginPath(); g.moveTo(kiri, gs); for (let x = kiri; x <= kanan; x += 8) g.lineTo(x, gs + n1(x * .02, seed + 3) * (alas - py) * .12 + Math.abs(x - px) * .05); g.lineTo(kanan, -50); g.lineTo(kiri, -50); g.fill();
    g.fillStyle = saljuB; g.beginPath(); g.moveTo(px, py - 5); for (let i = 0; i < 8; i++) { const f = (i + 1) / 9; g.lineTo(lerp(px, kanan, f * .6) + (R() - .3) * 20, lerp(py, gs + 30, f)); } g.lineTo(kanan, gs + 60); g.lineTo(kanan, -50); g.closePath(); g.fill(); g.restore();
    g.save(); g.filter = 'blur(.8px)'; for (let i = 0; i < 16; i++) { const x0 = lerp(kiri + (px - kiri) * .35, kanan - (kanan - px) * .3, (i + R()) / 16), y0 = gs - 10 + R() * 30, Lg = (alas - py) * (.1 + R() * .22), w = (kanan - kiri) * (.0018 + R() * .003);
      g.fillStyle = rgba(salju, .45); g.beginPath(); g.moveTo(x0 - w, y0); g.quadraticCurveTo(x0 - w * .4, y0 + Lg * .6, x0 + (x0 - px) * .05, y0 + Lg); g.quadraticCurveTo(x0 + w * .4, y0 + Lg * .6, x0 + w, y0); g.fill(); } g.restore(); }
  g.restore();
}
function lampion(x, y, rr, t, i = 0, merah = '#e8452e') {
  g.save(); g.translate(x, y); g.rotate(Math.sin(t * 1.3 + i) * .06);
  g.strokeStyle = 'rgba(30,10,10,.8)'; g.lineWidth = Math.max(1, rr * .06); g.beginPath(); g.moveTo(0, -rr * 1.9); g.lineTo(0, -rr * 1.1); g.stroke();
  g.fillStyle = '#2a120c'; g.fillRect(-rr * .45, -rr * 1.2, rr * .9, rr * .25); g.fillRect(-rr * .45, rr * .98, rr * .9, rr * .25);
  const gr = g.createRadialGradient(-rr * .25, -rr * .2, rr * .1, 0, 0, rr * 1.15); gr.addColorStop(0, '#ffd59a'); gr.addColorStop(.45, merah); gr.addColorStop(1, '#8a1a12');
  g.fillStyle = gr; g.beginPath(); g.ellipse(0, 0, rr, rr * 1.12, 0, 0, TAU); g.fill();
  g.strokeStyle = 'rgba(120,20,10,.5)'; g.lineWidth = Math.max(.8, rr * .05); for (const k of [-.55, 0, .55]) { g.beginPath(); g.ellipse(0, 0, rr * Math.abs(k) + .1, rr * 1.1, 0, 0, TAU); g.stroke(); }
  g.fillStyle = 'rgba(255,240,200,.35)'; g.beginPath(); g.ellipse(-rr * .35, -rr * .35, rr * .25, rr * .4, -.3, 0, TAU); g.fill();
  g.strokeStyle = '#c9302a'; g.lineWidth = Math.max(1, rr * .08); g.beginPath(); g.moveTo(0, rr * 1.2); g.lineTo(0, rr * 1.7); g.stroke();
  g.restore();
}
function jendelaGedung(x, y, w, h, kolom, baris, c, a) { g.fillStyle = c; for (let i = 0; i < kolom; i++) for (let j = 0; j < baris; j++) { g.globalAlpha = a * (.5 + .5 * (((i * 7 + j * 13) % 10) / 10)); g.fillRect(x + (i + .15) * w / kolom, y + (j + .2) * h / baris, w / kolom * .7, h / baris * .55); } g.globalAlpha = 1; }
function salju(t, n = 1, kec = 1) { for (const [x, y, s, f] of SALJU.slice(0, Math.round(SALJU.length * n))) { const yy = ((y + t * (.03 + s * .02) * kec) % 1) * H, xx = ((x * W + Math.sin(t * .8 + f) * 20 + t * 8 * s) % W + W) % W; g.fillStyle = `rgba(255,255,255,${.35 + s * .25})`; bulat(xx, yy, s * 1.3 * Math.min(W, H) / 720); } }
function debu(t, warna, n = 1) { g.save(); g.globalCompositeOperation = 'lighter'; for (const [x, y, s, f] of DEBU.slice(0, Math.round(DEBU.length * n))) { const xx = x * W + Math.sin(t * .3 + f) * 30, yy = y * H + Math.cos(t * .25 + f) * 30; g.fillStyle = rgba(warna, .15 + .3 * Math.sin(t + f) ** 2); bulat(xx, yy, s * 1.2); } g.restore(); }
const SALJU = (() => { const r = rng(21); return Array.from({ length: 240 }, () => [r(), r(), .4 + r() * 1.8, r() * 9]); })();
const DEBU = (() => { const r = rng(33); return Array.from({ length: 70 }, () => [r(), r(), .6 + r() * 1.6, r() * 9]); })();
const GELITER = (() => { const r = rng(44); return Array.from({ length: 110 }, () => [r(), r(), r() * 9, .3 + r()]); })();
const BINTANG = (() => { const r = rng(4); return Array.from({ length: 140 }, () => [r(), r() * .6, r() * 1.2 + .3, r() * 9]); })();
const BOK_HANGAT = buatBokeh(26, 12, ['#ffcf8a', '#ffe7b8', '#ffb46b'], 0, 1, 20, 60, .12, .35);
// fairy lights with polaroids of mountains (foreshadowing the trip)
function hiasanDinding(t, x0, x1, y) {
  const M = Math.min(W, H), sag = M * .05, titik = f => [lerp(x0, x1, f), y + Math.sin(f * PI) * sag];
  g.strokeStyle = 'rgba(40,28,18,.85)'; g.lineWidth = 1.3; g.beginPath(); for (let i = 0; i <= 30; i++) { const [x, yy] = titik(i / 30); i ? g.lineTo(x, yy) : g.moveTo(x, yy); } g.stroke();
  for (const [f, a, b] of [[.14, '#8fb6d8', '#f0d09a'], [.38, '#f0a878', '#6d8fb0'], [.62, '#a8c8a0', '#e8e0d0'], [.86, '#c8a0c8', '#ffd0a0']]) {
    const [x, yy] = titik(f), w = M * .07, iw = w * .84, top = M * .014, rot = Math.sin(f * 9) * .12 + Math.sin(t * .8 + f * 5) * .015;
    g.save(); g.translate(x, yy); g.rotate(rot); g.fillStyle = 'rgba(0,0,0,.28)'; g.fillRect(-w / 2 + 3, top + 4, w, w * 1.2);
    g.fillStyle = '#f6f1e6'; g.fillRect(-w / 2, top, w, w * 1.2); const iy = top + w * .08;
    g.fillStyle = gradV(iy, iy + iw, [[0, a], [1, b]]); g.fillRect(-iw / 2, iy, iw, iw);
    g.fillStyle = 'rgba(40,50,70,.6)'; g.beginPath(); g.moveTo(-iw / 2, iy + iw); g.lineTo(-iw * .1, iy + iw * .42); g.lineTo(iw * .12, iy + iw * .68); g.lineTo(iw * .3, iy + iw * .5); g.lineTo(iw / 2, iy + iw); g.fill();
    g.fillStyle = 'rgba(255,255,255,.7)'; g.beginPath(); g.moveTo(-iw * .1, iy + iw * .42); g.lineTo(-iw * .17, iy + iw * .55); g.lineTo(-iw * .03, iy + iw * .52); g.fill();
    g.fillStyle = '#c9a36a'; g.fillRect(-M * .005, 0, M * .01, M * .024); g.restore(); }
  for (let i = 0; i < 16; i++) { const f = (i + .5) / 16, [x, yy] = titik(f), a = .65 + .35 * Math.sin(t * 2 + i * 1.7); g.fillStyle = rgba('#ffe0a8', a); bulat(x, yy + 4, M * .006); cahaya(x, yy + 4, M * .045, '#ffc070', .3 * a); }
}
function rakBuku(x, y, w, t) {
  const M = Math.min(W, H), R = rng(17); let bx = x + w * .04;
  g.fillStyle = 'rgba(0,0,0,.25)'; g.fillRect(x + 4, y + 5, w, M * .016);
  while (bx < x + w * .7) { const bw = M * (.012 + R() * .012), bh = M * (.06 + R() * .04); g.fillStyle = ['#8a3a30', '#3a5a7a', '#c9a36a', '#4a6a4a', '#6a4a7a', '#d8cbb0'][Math.floor(R() * 6)]; g.fillRect(bx, y - bh, bw, bh); g.fillStyle = 'rgba(255,255,255,.18)'; g.fillRect(bx + bw * .2, y - bh * .8, bw * .6, M * .004); bx += bw + 1; }
  g.save(); g.translate(bx + M * .01, y - M * .015); g.rotate(-.35); g.fillStyle = '#7a4a3a'; g.fillRect(0, -M * .07, M * .014, M * .07); g.restore();
  const px = x + w * .86; g.fillStyle = '#b8715a'; g.beginPath(); g.moveTo(px - M * .022, y - M * .04); g.lineTo(px + M * .022, y - M * .04); g.lineTo(px + M * .017, y); g.lineTo(px - M * .017, y); g.fill();
  for (let i = 0; i < 7; i++) { g.save(); g.translate(px, y - M * .04); g.rotate(-1.3 + i * .43 + Math.sin(t * .7 + i) * .04); g.fillStyle = i % 2 ? '#5f8a4a' : '#4a7040'; g.beginPath(); g.ellipse(0, -M * .03, M * .009, M * .03, 0, 0, TAU); g.fill(); g.restore(); }
  g.fillStyle = '#3a2618'; g.fillRect(x, y, w, M * .016); g.fillStyle = 'rgba(255,220,170,.2)'; g.fillRect(x, y, w, 2);
}
function orangSiluet(x, y, h, warna, seed) { const r = rng(seed); g.fillStyle = warna; g.beginPath(); g.arc(x, y - h * .88, h * .08, 0, TAU); g.fill(); g.beginPath(); g.moveTo(x - h * .12, y - h * .76); g.quadraticCurveTo(x, y - h * .82, x + h * .12, y - h * .76); g.lineTo(x + h * (.1 + r() * .04), y - h * .35); g.lineTo(x + h * .06, y); g.lineTo(x - h * .06, y); g.lineTo(x - h * (.1 + r() * .04), y - h * .35); g.closePath(); g.fill(); }
function pakis(x, y, s, warna, t, seed) { const r = rng(seed); g.strokeStyle = warna; g.lineCap = 'round'; for (let k = 0; k < 5; k++) { const a = -PI / 2 + (k - 2) * .45 + Math.sin(t + k + seed) * .05, L = s * (.7 + r() * .4); g.lineWidth = Math.max(1, s * .04); g.beginPath(); g.moveTo(x, y); const ex = x + Math.cos(a) * L, ey = y + Math.sin(a) * L * .8; g.quadraticCurveTo(x + Math.cos(a) * L * .5, y + Math.sin(a) * L * .6 - L * .15, ex, ey); g.stroke(); g.lineWidth = Math.max(1, s * .025); for (let j = 1; j < 7; j++) { const f = j / 7, px = lerp(x, ex, f), py = lerp(y, ey, f) - Math.sin(f * PI) * L * .1, l = s * .16 * (1 - f * .6); g.beginPath(); g.moveTo(px, py); g.lineTo(px - Math.sin(a) * l, py + Math.cos(a) * l * .5); g.moveTo(px, py); g.lineTo(px + Math.sin(a) * l, py - Math.cos(a) * l * .5); g.stroke(); } } }
const SCENES = [];
const adeg = (a, b, f, o = {}) => SCENES.push({ a, b, f, ...o });
// character layer: draw the girl on her own layer, then light her so she sits inside the scene
const lapis = document.createElement('canvas'), LP = lapis.getContext('2d'), topeng = document.createElement('canvas'), TP = topeng.getContext('2d');
function tokoh(fn, e = {}) {
  if (lapis.width !== C.width || lapis.height !== C.height) { lapis.width = topeng.width = C.width; lapis.height = topeng.height = C.height; }
  const utama = g, m = utama.getTransform();
  LP.setTransform(1, 0, 0, 1, 0, 0); LP.globalCompositeOperation = 'source-over'; LP.globalAlpha = 1; LP.filter = 'none'; LP.clearRect(0, 0, lapis.width, lapis.height);
  LP.setTransform(m); g = LP; fn(); g = utama;
  if (e.tint || e.gelap || e.bayang || e.sinar) {
    TP.setTransform(1, 0, 0, 1, 0, 0); TP.globalCompositeOperation = 'copy'; TP.drawImage(lapis, 0, 0);
    LP.save(); const big = [-W * 2, -H * 2, W * 5, H * 5];
    if (e.gelap) { LP.globalCompositeOperation = 'multiply'; LP.fillStyle = rgba(e.gelap[0], e.gelap[1]); LP.fillRect(...big); }
    if (e.bayang) { const [x0, y0, x1, y1, w, a] = e.bayang, gr = LP.createLinearGradient(x0, y0, x1, y1); gr.addColorStop(0, rgba(w, 0)); gr.addColorStop(1, rgba(w, a)); LP.globalCompositeOperation = 'multiply'; LP.fillStyle = gr; LP.fillRect(...big); }
    if (e.tint) { LP.globalCompositeOperation = 'soft-light'; LP.fillStyle = rgba(e.tint[0], e.tint[1]); LP.fillRect(...big); }
    if (e.sinar) { const [x, y, r, w, a] = e.sinar, gr = LP.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, rgba(w, a)); gr.addColorStop(1, rgba(w, 0)); LP.globalCompositeOperation = 'screen'; LP.fillStyle = gr; LP.fillRect(...big); }
    LP.setTransform(1, 0, 0, 1, 0, 0); LP.globalCompositeOperation = 'destination-in'; LP.drawImage(topeng, 0, 0); LP.restore();
  }
  g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha *= e.alpha ?? 1; g.drawImage(lapis, 0, 0); g.restore();
}
// anamorphic lens flare
function suar(x, y, a, warna = '#ffd9a0') {
  if (a <= 0) return; const M = Math.min(W, H); g.save(); g.globalCompositeOperation = 'lighter';
  cahaya(x, y, M * .35, warna, .5 * a); cahaya(x, y, M * .06, '#ffffff', .9 * a);
  const gr = g.createLinearGradient(x - W * .7, 0, x + W * .7, 0); gr.addColorStop(0, rgba(warna, 0)); gr.addColorStop(.5, rgba('#fff4e0', .55 * a)); gr.addColorStop(1, rgba(warna, 0)); g.fillStyle = gr; g.fillRect(x - W * .7, y - M * .003, W * 1.4, M * .006);
  const cx = W / 2, cy = H / 2;
  for (const [f, r, c, al] of [[.45, .025, '#9fd0ff', .25], [.75, .07, '#ffcf8a', .1], [1.25, .018, '#d0a8ff', .3], [1.55, .11, '#8affd0', .06], [1.85, .045, '#ffd9a0', .16]]) {
    const px = x + (cx - x) * f, py = y + (cy - y) * f, rr = M * r, gg = g.createRadialGradient(px, py, rr * .6, px, py, rr); gg.addColorStop(0, rgba(c, al * a * .4)); gg.addColorStop(.85, rgba(c, al * a)); gg.addColorStop(1, rgba(c, 0)); g.fillStyle = gg; bulat(px, py, rr); }
  g.restore();
}
// drifting leaves / petals
const DAUN = (() => { const r = rng(58); return Array.from({ length: 26 }, () => [r(), r(), .6 + r(), r() * 9]); })();
function daun(t, warna, n = 1, blur = 0) {
  g.save(); if (blur) g.filter = `blur(${blur}px)`; const M = Math.min(W, H);
  for (const [x, y, s, f] of DAUN.slice(0, Math.round(DAUN.length * n))) { const xx = ((x * W - t * M * .05 * s + Math.sin(t * .9 + f) * M * .04) % W + W) % W, yy = ((y + t * .045 * s) % 1) * H;
    g.save(); g.translate(xx, yy); g.rotate(t * 1.5 * s + f); g.scale(1, Math.sin(t * 2.2 + f)); g.fillStyle = warna; g.beginPath(); g.ellipse(0, 0, M * .012 * s, M * .006 * s, 0, 0, TAU); g.fill(); g.restore(); }
  g.restore();
}
function bintangJatuh(t, x0, y0, t0) { const f = (t - t0) / .7; if (f < 0 || f > 1) return; const M = Math.min(W, H), x = x0 + f * M * .5, y = y0 + f * M * .2; g.save(); g.globalCompositeOperation = 'lighter'; const gr = g.createLinearGradient(x - M * .15, y - M * .06, x, y); gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(1, `rgba(255,255,255,${Math.sin(f * PI)})`); g.strokeStyle = gr; g.lineWidth = 2; g.beginPath(); g.moveTo(x - M * .15, y - M * .06); g.lineTo(x, y); g.stroke(); g.restore(); }

// ---------- shared: the wooden room (scenes 1, 3, 15)
function dindingKamar(t, o = {}) {
  const P = potret(), M = Math.min(W, H);
  papan(0, 0, W, H, '#6b4630', '#8a5a3c', M * .085, 5);
  g.fillStyle = gradV(0, H, [[0, 'rgba(20,10,5,.1)'], [1, 'rgba(20,10,5,.55)']]); g.fillRect(0, 0, W, H);
  // upper cabinet with a blue curtain peeking
  const ct = P ? H * .17 : H * .2, cx0 = P ? W * .3 : W * .42;
  g.fillStyle = '#2a1a12'; g.fillRect(cx0, 0, W - cx0, ct); g.fillStyle = '#3d281c'; g.fillRect(cx0, ct - M * .02, W - cx0, M * .02);
  g.fillStyle = '#1b2a3f'; g.fillRect(W - M * .22, 0, M * .12, ct * .9); g.fillStyle = 'rgba(80,110,150,.5)'; for (let k = 0; k < 4; k++) g.fillRect(W - M * .22 + k * M * .03, 0, M * .008, ct * .9);
  // wall panel + switches on the left
  const pw = P ? W * .16 : W * .12; g.fillStyle = '#8c8279'; g.fillRect(0, 0, pw, H); g.fillStyle = 'rgba(0,0,0,.25)'; g.fillRect(pw - 4, 0, 4, H);
  for (const [yy, n] of [[.36, 2], [.52, 1]]) { const sy = H * yy, sw = pw * .5; g.fillStyle = '#d8d2c6'; g.beginPath(); g.roundRect(pw * .25, sy, sw, sw * 1.2, 4); g.fill(); g.fillStyle = '#b9b2a6'; for (let k = 0; k < n; k++) g.fillRect(pw * .35 + k * sw * .42, sy + sw * .35, sw * .3, sw * .5); }
  // padded bench behind her
  g.fillStyle = gradV(H * .74, H, [[0, '#c9a27a'], [1, '#7a5a3e']]); g.beginPath(); g.roundRect(pw * .6, H * (P ? .76 : .7), W, H, 18); g.fill();
  g.strokeStyle = 'rgba(80,50,30,.35)'; g.lineWidth = 2; for (let x = pw; x < W; x += M * .03) { g.beginPath(); g.moveTo(x, H * (P ? .77 : .71)); g.lineTo(x + 4, H); g.stroke(); }
  hiasanDinding(t, pw + M * .04, W * .97, P ? H * .2 : H * .25);
  rakBuku(P ? W * .66 : W * .72, P ? H * .5 : H * .56, P ? W * .3 : W * .22, t);
  cahaya(W * .9, H * .06, M * 1.1, '#ffb266', .45 * (o.lampu ?? 1)); cahaya(W * .6, H * .5, M * .5, '#ffcf9a', .12);
}

// 1 — leaning on the wall, eyes closed (0–6.5)
adeg(0, 6.5, t => {
  const P = potret(), M = Math.min(W, H);
  const s = P ? W * .25 : H * .2, x = W * (P ? .56 : .52), y = H - (P ? 3.0 : 3.15) * s;
  const naik = eio(u(t, .3, 3.6)), cy = lerp(y + 2.3 * s, y + .3 * s, naik), z = lerp(P ? 1.5 : 1.7, 1.06, naik) + .03 * t / 6.5;
  g.save(); dorong(z, x, cy, W / 2 - x, H * .5 - cy); g.translate(W / 2, H / 2); g.rotate(lerp(.04, .01, naik)); g.translate(-W / 2, -H / 2);
  dindingKamar(t);
  g.save(); g.globalCompositeOperation = 'lighter'; for (let k = 0; k < 6; k++) { g.fillStyle = `rgba(255,190,120,${.05 + .02 * Math.sin(waktuNyata * .5 + k)})`; g.beginPath(); const x0 = W * (.35 + k * .1); g.moveTo(x0, 0); g.lineTo(x0 + M * .05, 0); g.lineTo(x0 - W * .25 + M * .05, H); g.lineTo(x0 - W * .25, H); g.fill(); } g.restore();
  g.fillStyle = 'rgba(20,8,4,.35)'; g.save(); g.filter = 'blur(18px)'; g.beginPath(); g.ellipse(x - s * .6, y + s * .6, s * 1.4, s * 2.4, 0, 0, TAU); g.fill(); g.restore();
  TK.rim = '#ffc07a'; TK.rimSisi = 1;
  const buka = eio(u(t, 3.9, 5.1));
  tokoh(() => gadisDada(x, y, s, { miring: lerp(-.2, -.1, buka), bukaMata: buka < .06 ? 0 : .7 * buka, merah: .6, lirikX: -.2, napas: 1, tangan: { pose: 'cangkir', k: .5 + .5 * Math.sin(t * .6) } }),
    { sinar: [W * .95, H * .02, M * 1.3, '#ffb266', .28], bayang: [x + s, 0, x - s * 1.6, 0, '#3a1e2a', .45] });
  g.restore(); debu(waktuNyata, '#ffd9a0', .5);
});
// 2 — window: the city outside (6.5–11.5)
adeg(6.5, 11.5, t => {
  const P = potret(), M = Math.min(W, H), z = 1.02 + .05 * t / 5;
  g.save(); dorong(z);
  const win = P ? { x: W * .22, y: H * .2, w: W * .66, h: H * .5 } : { x: W * .3, y: H * .12, w: W * .44, h: H * .68 };
  g.save(); g.beginPath(); g.rect(win.x, win.y, win.w, win.h); g.clip();
  g.fillStyle = gradV(win.y, win.y + win.h, [[0, '#dfe2e4'], [.6, '#eceae4'], [1, '#f4efe4']]); g.fillRect(win.x, win.y, win.w, win.h);
  awan(win.x + win.w * .3, win.y + win.h * .25, win.w * .5, 8, '#f7f6f2', '#d6d8da', .7);
  { const r = rng(71); for (let i = 0; i < 14; i++) { const bx = win.x + r() * win.w, bw = win.w * (.06 + r() * .1), bh = win.h * (.25 + r() * .35); g.fillStyle = mixC('#c9ced2', '#b7bdc2', r()); g.fillRect(bx, win.y + win.h - bh, bw, bh); jendelaGedung(bx, win.y + win.h - bh, bw, bh, 3, 8, '#9aa3aa', .35); }
    g.strokeStyle = '#8a9096'; g.lineWidth = 2; const kx = win.x + win.w * .45; g.beginPath(); g.moveTo(kx, win.y + win.h * .4); g.lineTo(kx, win.y + win.h * .12); g.lineTo(kx + win.w * .25, win.y + win.h * .12); g.moveTo(kx - win.w * .06, win.y + win.h * .12); g.lineTo(kx, win.y + win.h * .12); g.stroke(); }
  // white grid office block
  const ob = { x: win.x - win.w * .05, y: win.y + win.h * .3, w: win.w * .5, h: win.h * .75 };
  g.fillStyle = '#ecebe6'; g.fillRect(ob.x, ob.y, ob.w, ob.h); g.fillStyle = '#d0cfca'; g.fillRect(ob.x + ob.w * .7, ob.y, ob.w * .3, ob.h);
  for (let j = 0; j < 12; j++) for (let i = 0; i < 8; i++) { g.fillStyle = (i + j) % 3 ? '#8e98a2' : '#a9b2ba'; g.fillRect(ob.x + ob.w * (.04 + i * .12), ob.y + ob.h * (.03 + j * .08), ob.w * .08, ob.h * .05); }
  // glass tower with a pointed crown
  const tw = { x: win.x + win.w * .6, y: win.y - win.h * .05, w: win.w * .38, h: win.h * 1.1 };
  g.fillStyle = gradV(tw.y, tw.y + tw.h, [[0, '#9fb0b8'], [.5, '#70848e'], [1, '#56666e']]); g.fillRect(tw.x, tw.y, tw.w, tw.h);
  g.fillStyle = '#b3aa92'; g.beginPath(); g.moveTo(tw.x + tw.w * .1, tw.y + tw.h * .52); g.lineTo(tw.x + tw.w * .5, tw.y + tw.h * .3); g.lineTo(tw.x + tw.w * .9, tw.y + tw.h * .52); g.closePath(); g.fill();
  g.fillStyle = '#8f8670'; g.beginPath(); g.moveTo(tw.x + tw.w * .5, tw.y + tw.h * .3); g.lineTo(tw.x + tw.w * .9, tw.y + tw.h * .52); g.lineTo(tw.x + tw.w * .5, tw.y + tw.h * .52); g.closePath(); g.fill();
  g.strokeStyle = 'rgba(40,55,62,.5)'; g.lineWidth = 1.5; for (let j = 0; j < 30; j++) { const yy = tw.y + j * tw.h / 30; g.beginPath(); g.moveTo(tw.x, yy); g.lineTo(tw.x + tw.w, yy); g.stroke(); }
  for (let i = 1; i < 8; i++) { g.beginPath(); g.moveTo(tw.x + i * tw.w / 8, tw.y); g.lineTo(tw.x + i * tw.w / 8, tw.y + tw.h); g.stroke(); }
  g.fillStyle = 'rgba(255,255,255,.18)'; g.beginPath(); g.moveTo(tw.x, tw.y + tw.h * .1); g.lineTo(tw.x + tw.w * .4, tw.y); g.lineTo(tw.x + tw.w * .6, tw.y); g.lineTo(tw.x, tw.y + tw.h * .3); g.fill();
  // trees + palms
  const tb = win.y + win.h;
  rimbun(win.x + win.w * .15, tb - win.h * .08, win.w * .2, '#3f6b3a', '#284a28', '#6d9a55', 3, 16);
  rimbun(win.x + win.w * .85, tb - win.h * .06, win.w * .22, '#46703c', '#2a4a2a', '#7aa55e', 7, 16);
  palem(win.x + win.w * .38, tb, win.h * .42, '#4d7a3e', '#2c4a26', waktuNyata, 2); palem(win.x + win.w * .62, tb, win.h * .36, '#4d7a3e', '#2c4a26', waktuNyata, 5); palem(win.x + win.w * .93, tb, win.h * .3, '#4d7a3e', '#2c4a26', waktuNyata, 9);
  g.restore();
  // dark room + frame + mullion
  g.fillStyle = '#120c0a'; g.beginPath(); g.rect(0, 0, W, H); g.rect(win.x + win.w, win.y, -win.w, win.h); g.fill('evenodd');
  g.fillStyle = '#1e1511'; g.fillRect(win.x + win.w * .48, win.y, win.w * .05, win.h); g.fillRect(win.x - 8, win.y + win.h, win.w + 16, M * .03);
  g.fillStyle = 'rgba(255,240,220,.12)'; g.fillRect(win.x - 8, win.y + win.h, win.w + 16, 3);
  cahaya(win.x + win.w / 2, win.y + win.h / 2, M * .9, '#dfe6ea', .12);
  { const px = win.x + win.w * .78, py = win.y + win.h; g.fillStyle = '#2a1c16'; g.beginPath(); g.moveTo(px - M * .035, py - M * .06); g.lineTo(px + M * .035, py - M * .06); g.lineTo(px + M * .027, py); g.lineTo(px - M * .027, py); g.fill();
    for (let i = 0; i < 9; i++) { g.save(); g.translate(px, py - M * .06); g.rotate(-1.4 + i * .35 + Math.sin(waktuNyata * .6 + i) * .03); g.fillStyle = i % 2 ? '#1c2a1c' : '#243424'; g.beginPath(); g.ellipse(0, -M * .045, M * .012, M * .045, 0, 0, TAU); g.fill(); g.restore(); }
    g.strokeStyle = 'rgba(230,238,242,.35)'; g.lineWidth = 1.5; g.beginPath(); g.moveTo(px - M * .035, py - M * .06); g.lineTo(px + M * .035, py - M * .06); g.stroke();
    g.fillStyle = '#1c1411'; g.fillRect(win.x + win.w * .05, py - M * .025, M * .1, M * .025); g.fillStyle = '#3a2a22'; g.fillRect(win.x + win.w * .06, py - M * .045, M * .08, M * .02); }
  // her head, dark against the window
  for (let i = 0; i < 4; i++) burung(win.x + win.w * (.1 + i * .06) + t * win.w * .08, win.y + win.h * (.18 + (i % 2) * .03), M * .01, waktuNyata + i, .5, '#50585e');
  sinarDewa(win.x + win.w * .7, win.y, 6, Math.max(W, H) * .9, '#e8eef2', .05, waktuNyata, .05, PI * .62, .5);
  debu(waktuNyata, '#e8eef2', .4);
  g.fillStyle = '#1a1210'; g.beginPath(); g.moveTo(win.x + win.w + M * .01, win.y - M * .03); g.bezierCurveTo(win.x + win.w - M * .05 + Math.sin(waktuNyata * .8) * M * .01, win.y + win.h * .4, win.x + win.w + M * .02, win.y + win.h * .8, win.x + win.w - M * .01, win.y + win.h + M * .05); g.lineTo(W, win.y + win.h + M * .05); g.lineTo(W, win.y - M * .03); g.fill();
  TK.rim = '#e8eef2'; TK.rimSisi = 1;
  g.save(); g.translate(-t * W * .012, 0);
  saring('brightness(.25) blur(5px)', () => gadisBelakang(win.x - (P ? W * .02 : W * .02), H * (P ? 1.35 : 1.6), P ? H * .95 : H * 1.35, { angin: 0, bayangan: false }));
  g.restore();
  g.restore();
});
// 3 — close-up: she looks at you (11.5–16)
adeg(11.5, 16, t => {
  const P = potret(), M = Math.min(W, H), z = 1 + .06 * eio(t / 4.5);
  g.save(); dorong(z, W / 2, H * .4); g.translate(W / 2, H / 2); g.rotate(-.015 + .02 * eio(t / 4.5)); g.translate(-W / 2, -H / 2);
  const fokus = eio(u(t, 0, 1.1));
  saring(`blur(${lerp(2, 8, fokus)}px)`, () => dindingKamar(t));
  const s = P ? W * .34 : H * .3, x = W * .5, y = P ? H * .4 : H * .44;
  TK.rim = '#ffc07a'; TK.rimSisi = 1;
  const senyum = u(t, 2.4, 3.2), selip = eio(u(t, .5, 1.5)) * (1 - eio(u(t, 3.3, 4.4)));
  saring(`blur(${lerp(5, 0, fokus)}px)`, () => tokoh(() => gadisDada(x, y, s, { miring: -.05 - selip * .05, mata: 'sayu', bukaMata: lerp(.8, 1, senyum), mulut: senyum > .5 ? 'senyum' : 'datar', merah: .55 + senyum * .3, alis: -.02 * senyum, lirikX: -.3 * selip, tangan: selip > .01 ? { pose: 'rambut', k: selip } : null }),
    { sinar: [W, 0, M * 1.2, '#ffb266', .3], bayang: [x + s * .8, 0, x - s * 1.2, 0, '#3a1e2a', .35] }));
  g.restore(); debu(waktuNyata, '#ffd9a0', .4);
});
// 4 — through the car window: hood up, waving (16–21.5)
adeg(16, 21.5, t => {
  const P = potret(), M = Math.min(W, H), gx = Math.sin(waktuNyata * 7) * 1.2;
  g.save(); g.translate(gx, Math.sin(waktuNyata * 9) * 1);
  langit([[0, '#8fb3d6'], [.4, '#c3d6e6'], [1, '#e8ecef']]);
  gunung({ px: W * .72, py: H * (P ? .12 : .02), kiri: -W * .3, kanan: W * 1.4, alas: H * (P ? .52 : .6), c1: '#5f7894', c2: '#3a4f68', bayang: 'rgba(25,38,58,.45)', salju: '#eef3f8', saljuB: '#b9c9dc', garisSalju: H * (P ? .22 : .16), seed: 7, kasar: 1.4 });
  gunung({ px: W * .05, py: H * (P ? .3 : .22), kiri: -W * .4, kanan: W * .55, alas: H * (P ? .56 : .66), c1: '#6f84a0', c2: '#4a5f7a', bayang: 'rgba(30,40,60,.4)', salju: '#f2f5f8', saljuB: '#c3cfdd', garisSalju: H * (P ? .35 : .3), seed: 11, kasar: 1.2 });
  awan(W * .3 + t * M * .02, H * (P ? .2 : .12), M * .35, 14, '#ffffff', '#c9d4e2', .55); awan(W * .85 + t * M * .015, H * (P ? .3 : .25), M * .25, 15, '#ffffff', '#c9d4e2', .45);
  kabut(H * (P ? .54 : .62), H * .03, '#e6e2d8', .5, t, 6, 3);
  const pad = P ? H * .52 : H * .6;
  g.fillStyle = gradV(pad, H, [[0, '#c9a868'], [.4, '#d8b877'], [1, '#b8904e']]); g.fillRect(0, pad, W, H);
  { g.strokeStyle = '#6a5a44'; g.lineWidth = Math.max(1.5, M * .003); for (let i = 0; i < 26; i++) { const x = W * i / 25, y = pad + H * .015; g.beginPath(); g.moveTo(x, y); g.lineTo(x, y - M * .03); g.stroke(); }
    g.lineWidth = 1; g.strokeStyle = 'rgba(90,80,60,.7)'; for (const d of [.01, .022]) { g.beginPath(); g.moveTo(0, pad + H * .015 - M * d); g.lineTo(W, pad + H * .015 - M * d); g.stroke(); }
    g.fillStyle = 'rgba(40,40,40,.35)'; for (let i = 0; i < 3; i++) { const x = W * (.1 + i * .33), y = pad + H * .012; g.beginPath(); g.ellipse(x + Math.sin(i) * 20, y - M * .006, M * .012, M * .006, 0, 0, TAU); g.fill(); } }
  rumput(pad, H, 900, 'rgba(120,90,40,.55)', waktuNyata, M * .03, 4); rumput(pad + H * .05, H, 500, 'rgba(250,225,160,.6)', waktuNyata, M * .045, 6);
  // the girl
  TK.rim = '#fff4dc'; TK.rimSisi = -1;
  const s = P ? W * .2 : H * .17;
  { const gx0 = W * (P ? .52 : .5), gy0 = H * (P ? .6 : .52);
    tokoh(() => gadisDada(gx0, gy0, s, { tudung: true, lambai: eio(u(t, .3, 1.0)) * (1 - eio(u(t, 4.3, 5.2))), mata: t > 4.6 ? 'buka' : 'senyum', mulut: t > 4.6 ? 'senyum' : 'lebar', merah: .8, angin: .5, arahAngin: -1, miring: .06 }),
      { sinar: [0, 0, M * 1.4, '#fff6e0', .3], bayang: [gx0 - s, 0, gx0 + s * 1.5, 0, '#26304a', .3] }); }
  suar(W * .06, H * .06, .4, '#fff0d0');
  // car interior frame
  g.fillStyle = '#16181c'; g.beginPath(); g.rect(-20, -20, W + 40, H + 40);
  const wx0 = P ? W * .04 : W * .06, wy0 = P ? H * .12 : H * .08, wx1 = W * 1.02, wy1 = P ? H * .82 : H * .86;
  g.moveTo(wx0 + M * .06, wy0); g.lineTo(wx1, wy0 - M * .02); g.lineTo(wx1, wy1); g.lineTo(wx0, wy1); g.lineTo(wx0, wy0 + M * .12); g.quadraticCurveTo(wx0, wy0, wx0 + M * .06, wy0); g.fill('evenodd');
  g.fillStyle = '#23262c'; g.fillRect(0, wy1, W, M * .02); g.fillStyle = 'rgba(255,255,255,.08)'; g.fillRect(0, wy1, W, 2);
  g.fillStyle = '#2b2e34'; g.beginPath(); g.ellipse(wx0 + M * .14, wy1 - M * .02, M * .1, M * .06, 0, PI, TAU); g.fill();
  g.strokeStyle = '#c64a3a'; g.lineWidth = 3; g.beginPath(); g.arc(wx0 + M * .14, wy1 - M * .055, M * .018, 0, TAU); g.moveTo(wx0 + M * .128, wy1 - M * .067); g.lineTo(wx0 + M * .152, wy1 - M * .043); g.stroke();
  g.save(); g.globalCompositeOperation = 'lighter'; g.fillStyle = 'rgba(255,255,255,.06)'; g.beginPath(); g.moveTo(W * .1, wy0); g.lineTo(W * .35, wy0); g.lineTo(W * .1, wy1); g.lineTo(-W * .1, wy1); g.fill(); g.restore();
  g.restore();
});
// 5 — suspension bridge in the mist (21.5–26.5)
adeg(21.5, 26.5, t => {
  const P = potret(), M = Math.min(W, H), vp = [W * .5, H * (P ? .5 : .47)], dol = eio(t / 5);
  langit([[0, '#6e7c86'], [.5, '#a9b3b8'], [1, '#c6ccce']]);
  g.save(); dorong(1 + .05 * dol, vp[0], vp[1]);
  gunung({ px: W * .6, py: H * .08, kiri: -W * .2, kanan: W * 1.3, alas: H * .6, c1: '#56646a', c2: '#3c4a4c', bayang: 'rgba(20,30,32,.35)', seed: 3, kasar: 1.2 });
  kabut(H * .25, H * .1, '#c9d0d2', .6, t, 5, 2);
  punggung(H * .52, H * .06, 1.2, 4, '#3f4f48', t * 4); kabut(H * .5, H * .05, '#b9c2c2', .5, t, 9, 3);
  for (let i = 0; i < 30; i++) { const x = W * i / 29, y = H * (.5 + (i % 3) * .01); pinus(x, y, H * (.05 + (i % 4) * .012), '#2e3d36'); }
  // towers + cables + deck
  const tH = H * .2, tx = [vp[0] - M * .1, vp[0] + M * .1];
  g.fillStyle = '#4a4e4c'; for (const x of tx) { g.fillRect(x - M * .009, vp[1] - tH, M * .018, tH + H * .03); } g.fillRect(tx[0], vp[1] - tH, tx[1] - tx[0], M * .01); g.fillRect(tx[0], vp[1] - tH * .6, tx[1] - tx[0], M * .006);
  g.strokeStyle = '#3c403e'; g.lineWidth = 1.5; for (const s of [-1, 1]) { const x = s < 0 ? tx[0] : tx[1]; g.beginPath(); g.moveTo(x, vp[1] - tH); g.lineTo(vp[0] + s * W * .8, H * .92); g.stroke(); g.beginPath(); g.moveTo(x, vp[1] - tH); g.quadraticCurveTo(vp[0] + s * W * .02, vp[1] - H * .01, vp[0] + s * W * .01, vp[1] - H * .03); g.stroke(); }
  g.strokeStyle = '#3c403e'; g.lineWidth = 1; for (let k = 1; k < 12; k++) { const f = k / 12; for (const s of [-1, 1]) { const x = vp[0] + s * M * .1 * (1 - f * .6); g.beginPath(); g.moveTo(x, vp[1] + H * .015); g.lineTo(x, vp[1] - H * .05 * (1 - f)); g.stroke(); } }
  g.fillStyle = '#6b6258'; g.beginPath(); g.moveTo(vp[0] - W * .05, vp[1] + H * .02); g.lineTo(vp[0] + W * .05, vp[1] + H * .02); g.lineTo(vp[0] + W * .04, vp[1] + H * .01); g.lineTo(vp[0] - W * .04, vp[1] + H * .01); g.fill();
  for (let i = 0; i < 5; i++) burung(W * (.62 + i * .05) - t * W * .025, H * (.2 + (i % 2) * .025), M * .011, waktuNyata + i * 2, .55, '#3b4450');
  g.restore(); g.save(); dorong(1 + .12 * dol, vp[0], vp[1]);
  g.fillStyle = '#5a4a3a'; g.fillRect(vp[0] - W * .09, vp[1] + H * .0, M * .006, H * .035); g.fillStyle = '#7a6448'; g.fillRect(vp[0] - W * .11, vp[1] - H * .005, M * .05, M * .025); g.fillStyle = 'rgba(255,240,210,.5)'; g.fillRect(vp[0] - W * .105, vp[1] + H * .0, M * .035, M * .004);
  // rocky path
  g.fillStyle = gradV(vp[1], H, [[0, '#8b857a'], [1, '#6e675b']]); g.beginPath(); g.moveTo(vp[0] - W * .05, vp[1] + H * .02); g.lineTo(vp[0] + W * .05, vp[1] + H * .02); g.quadraticCurveTo(W * .7, H * .75, W * .95, H); g.lineTo(W * .05, H); g.quadraticCurveTo(W * .3, H * .75, vp[0] - W * .05, vp[1] + H * .02); g.fill();
  const r = rng(51); for (let i = 0; i < 45; i++) { const f = r(), y = lerp(vp[1] + H * .03, H, f * f), sp = lerp(W * .05, W * .45, f * f), x = vp[0] + (r() - .5) * 2 * sp, rr = M * (.004 + .02 * f * f) * (.5 + r());
    g.fillStyle = '#5b554b'; g.beginPath(); g.ellipse(x, y + rr * .2, rr * 1.2, rr * .7, 0, 0, TAU); g.fill(); g.fillStyle = r() < .5 ? '#a8a194' : '#958e81'; g.beginPath(); g.ellipse(x - rr * .1, y, rr, rr * .55, 0, 0, TAU); g.fill(); }
  // bushes both sides
  const d = lerp(1, .78, t / 5), gy = lerp(H * .9, H * .8, t / 5);
  TK.rim = '#eef2f2'; TK.rimSisi = 1;
  tokoh(() => gadisBelakang(vp[0] + W * .01, gy, (P ? H * .26 : H * .34) * d, { jalan: true, fase: waktuNyata * 5.2, ransel: true, angin: .15, arahAngin: 1, bayangan: .3 }), { tint: ['#aebcc4', .5], gelap: ['#c8d0d4', .35] });
  g.restore(); g.save(); dorong(1 + .25 * dol, vp[0], vp[1]);
  rimbun(W * -.05, H * .66, M * .35, '#3f5a3a', '#26382a', '#5f7d4e', 21, 22); rimbun(W * .08, H * .82, M * .25, '#46613e', '#2a3c2a', '#6c8a54', 22, 16);
  rimbun(W * 1.02, H * .7, M * .3, '#4a5e3e', '#2b3b2a', '#6f8a55', 23, 20);
  rumput(H * .75, H, 260, 'rgba(160,150,110,.7)', waktuNyata, M * .06, 8, 2);
  for (let i = 0; i < 6; i++) pakis(i % 2 ? W * (.62 + i * .06) : W * (.08 + i * .05), H * (.72 + i * .04), M * (.06 + i * .01), '#4a6a3e', waktuNyata, 90 + i);
  g.restore();
  saring('blur(9px)', () => { rimbun(-W * .02, -H * .02, M * .28, '#2f4430', '#1c2a1e', '#4a6444', 61, 16, .6); rimbun(W * 1.03, H * .05, M * .2, '#2f4430', '#1c2a1e', '#4a6444', 62, 12, .6); });
  kabut(H * .95, H * .06, '#c9d0d2', .25, t, 14, 7);
  g.fillStyle = 'rgba(160,172,176,.12)'; g.fillRect(0, 0, W, H);
});
// 6 — lantern street, looking up (26.5–31.5)
adeg(26.5, 31.5, t => {
  const P = potret(), M = Math.min(W, H), naik = eio(t / 5) * H * .05;
  g.save(); g.translate(W / 2, H / 2); g.rotate(-.03 + .04 * eio(t / 5)); g.translate(-W / 2, -H / 2 + naik);
  langit([[0, '#e9e4dc'], [1, '#d9d2c6']]);
  // tall concrete building in haze
  g.fillStyle = '#b7b1a6'; g.fillRect(W * .32, -H * .1, W * .36, H * .62); g.fillStyle = 'rgba(90,85,78,.35)'; for (let j = 0; j < 9; j++) g.fillRect(W * .32, -H * .1 + j * H * .07, W * .36, H * .012);
  for (let i = 0; i < 5; i++) g.fillRect(W * (.34 + i * .07), -H * .1, W * .012, H * .62);
  g.fillStyle = 'rgba(233,228,220,.55)'; g.fillRect(0, -H, W, H * 2);
  // buildings left + right with eaves and signs
  for (const s of [-1, 1]) {
    const x0 = s < 0 ? 0 : W, lebar = W * (P ? .33 : .28);
    g.fillStyle = '#3a2418'; g.beginPath(); g.moveTo(x0, -H * .1); g.lineTo(x0 - s * lebar * .8, H * .05); g.lineTo(x0 - s * lebar, H * 1.1); g.lineTo(x0, H * 1.1); g.fill();
    for (let k = 0; k < 4; k++) { const y = H * (.12 + k * .2), ex = x0 - s * lebar * (1.08 + k * .02);
      g.fillStyle = '#23140d'; g.beginPath(); g.moveTo(x0, y - H * .03); g.lineTo(ex, y); g.lineTo(ex, y + M * .018); g.lineTo(x0, y); g.fill();
      g.fillStyle = k % 2 ? '#b8322a' : '#e0b04a'; const sw2 = M * .07, sh = H * .1; g.fillRect(x0 - s * lebar * .75 - (s > 0 ? sw2 : 0), y + H * .03, sw2, sh);
      g.fillStyle = k % 2 ? '#f1d9a0' : '#5a1e14'; for (let c = 0; c < 3; c++) { const cy = y + H * .045 + c * sh * .3; g.fillRect(x0 - s * lebar * .75 - (s > 0 ? sw2 : 0) + sw2 * .3, cy, sw2 * .4, M * .006); g.fillRect(x0 - s * lebar * .75 - (s > 0 ? sw2 : 0) + sw2 * .47, cy - M * .01, M * .006, M * .03); }
      g.fillStyle = rgba('#ffcf8a', .7); g.fillRect(x0 - s * lebar * .45 - (s > 0 ? M * .08 : 0), y + H * .08, M * .08, H * .05); cahaya(x0 - s * lebar * .45, y + H * .1, M * .15, '#ffb46b', .25); }
  }
  g.strokeStyle = 'rgba(40,30,25,.55)'; g.lineWidth = 1; for (let k = 0; k < 4; k++) { g.beginPath(); g.moveTo(-10, H * (.08 + k * .05)); g.quadraticCurveTo(W * .5, H * (.14 + k * .05), W + 10, H * (.05 + k * .06)); g.stroke(); }
  // strings of lanterns converging to a point
  const pusat = [W * .5, H * .5];
  for (let k = 0; k < 7; k++) { const a0 = [k % 2 ? -W * .02 : W * 1.02, H * (.02 + k * .09)], sag = H * .03 + k * H * .006;
    g.strokeStyle = 'rgba(40,15,10,.7)'; g.lineWidth = 1.5; g.beginPath(); g.moveTo(...a0); g.quadraticCurveTo(lerp(a0[0], pusat[0], .5), lerp(a0[1], pusat[1] * .7, .5) + sag, ...pusat); g.stroke();
    for (let i = 1; i < 9; i++) { const f = i / 9, x = lerp(lerp(a0[0], lerp(a0[0], pusat[0], .5), f), lerp(lerp(a0[0], pusat[0], .5), pusat[0], f), f), y = lerp(lerp(a0[1], lerp(a0[1], pusat[1] * .7, .5) + sag, f), lerp(lerp(a0[1], pusat[1] * .7, .5) + sag, pusat[1], f), f);
      lampion(x, y + M * .03 * (1 - f * .6), M * .03 * (1.3 - f * .9), waktuNyata, i + k); } }
  g.restore();
  // the girl, head tilted up
  TK.rim = '#ffe2c0'; TK.rimSisi = -1;
  tokoh(() => gadisBelakang(W * .54, H * (P ? 1.55 : 2.05), P ? H * 1.05 : H * 1.7, { tengadah: 1, angin: .05, bayangan: false }), { sinar: [W * .1, H * .35, M * .8, '#ff7a4a', .35], bayang: [W, H * .4, W * .3, H, '#2a1418', .3] });
  saring('blur(5px)', () => { const r = rng(55); for (let i = 0; i < 9; i++) { const x = i < 5 ? W * (.02 + i * .07) : W * (.62 + (i - 5) * .1), h = H * (P ? .22 : .38) * (.8 + r() * .3); orangSiluet(x + Math.sin(waktuNyata * .5 + i) * 6, H * 1.02, h, mixC('#2a1810', '#4a2a1c', r()), 60 + i); } });
  saring('blur(12px)', () => { lampion(W * .92, H * .12 - naik * .5, M * .09, waktuNyata, 3); cahaya(W * .92, H * .12, M * .3, '#ff6a3a', .35); lampion(W * .04, H * .3, M * .07, waktuNyata, 5); });
  debu(waktuNyata, '#fff0d0', .3);
});
// 7 — snowy village from the lookout (31.5–36.5)
adeg(31.5, 36.5, t => {
  const P = potret(), M = Math.min(W, H), gx = -t * W * .012;
  langit([[0, '#c9d2dc'], [1, '#eef1f3']]);
  g.save(); g.translate(gx * .35, 0);
  gunung({ px: W * .5, py: H * .02, kiri: -W * .3, kanan: W * 1.4, alas: H * .38, c1: '#93a0ad', c2: '#6f7c88', bayang: 'rgba(40,50,62,.3)', salju: '#f4f6f8', saljuB: '#ccd5de', garisSalju: H * .25, seed: 19, kasar: 1.6 });
  kabut(H * .3, H * .06, '#e8ecef', .6, t, 5, 3);
  kabut(H * .2, H * .12, '#e8ecef', .5, t, 4, 8); for (let i = 0; i < 24; i++) { const x = W * 1.2 * i / 23 - W * .1, y = H * (.38 + (i % 3) * .015); pinus(x, y, M * (.16 + (i % 5) * .03), '#23302c'); }
  g.restore(); g.save(); g.translate(gx, 0);
  g.fillStyle = gradV(H * .38, H, [[0, '#e3e8ec'], [1, '#f6f7f8']]); g.fillRect(-W * .1, H * .38, W * 1.3, H);
  // gassho houses
  const R = rng(77), rumah = [];
  for (let i = 0; i < 11; i++) rumah.push([W * (-.05 + R() * 1.15), H * (.46 + R() * .38), M * (.07 + R() * .05)]);
  rumah.sort((a, b) => a[1] - b[1]);
  for (const [x, y, s0] of rumah) { const s = s0 * (.7 + (y / H - .4) * 1.2);
    g.fillStyle = 'rgba(80,90,110,.25)'; g.beginPath(); g.ellipse(x + s * .3, y + s * .08, s * 1.3, s * .18, 0, 0, TAU); g.fill();
    g.fillStyle = '#4a3525'; g.fillRect(x - s * .8, y - s * .5, s * 1.6, s * .5); g.fillStyle = '#6e5238'; g.fillRect(x - s * .8, y - s * .5, s * .7, s * .5);
    for (let k = 0; k < 3; k++) { g.fillStyle = rgba('#ffcf8a', .8); g.fillRect(x - s * .7 + k * s * .2, y - s * .35, s * .12, s * .12); }
    g.fillStyle = '#5c4630'; g.beginPath(); g.moveTo(x - s * 1.0, y - s * .45); g.lineTo(x - s * .1, y - s * 1.7); g.lineTo(x + s * 1.0, y - s * .45); g.closePath(); g.fill();
    g.fillStyle = '#f7f8fa'; g.beginPath(); g.moveTo(x - s * 1.05, y - s * .5); g.lineTo(x - s * .1, y - s * 1.78); g.lineTo(x + s * 1.05, y - s * .5); g.lineTo(x + s * .85, y - s * .6); g.lineTo(x - s * .1, y - s * 1.45); g.lineTo(x - s * .85, y - s * .6); g.closePath(); g.fill();
    g.fillStyle = '#e4e9f0'; g.beginPath(); g.moveTo(x - s * .1, y - s * 1.78); g.lineTo(x + s * 1.05, y - s * .5); g.lineTo(x + s * .6, y - s * .55); g.lineTo(x - s * .1, y - s * 1.5); g.fill();
    g.fillStyle = '#3a2a1c'; g.beginPath(); g.moveTo(x - s * .55, y - s * .65); g.lineTo(x - s * .1, y - s * 1.3); g.lineTo(x + s * .35, y - s * .65); g.closePath(); g.fill();
    g.strokeStyle = 'rgba(240,210,160,.6)'; g.lineWidth = 1; for (let k = 1; k < 4; k++) { g.beginPath(); g.moveTo(x - s * .55 + k * s * .1, y - s * .65 - k * s * .15); g.lineTo(x + s * .35 - k * s * .1, y - s * .65 - k * s * .15); g.stroke(); }
    g.fillStyle = rgba('#ffcf8a', .7); g.fillRect(x - s * .2, y - s * .9, s * .2, s * .12); cahaya(x - s * .1, y - s * .8, s * 1.2, '#ffb35a', .18);
    for (let k = 0; k < 5; k++) { const f = (waktuNyata * .25 + k / 5 + x * .01) % 1; g.fillStyle = `rgba(235,238,244,${.35 * Math.sin(f * PI)})`; bulat(x + s * .4 + Math.sin(f * 5 + x) * s * .15 + f * s * .5, y - s * 1.1 - f * s * 1.4, s * (.1 + f * .25)); }
  }
  g.strokeStyle = 'rgba(200,210,225,.8)'; g.lineWidth = M * .012; g.lineCap = 'round'; g.beginPath(); g.moveTo(W * .2, H * 1.02); g.bezierCurveTo(W * .35, H * .8, W * .3, H * .65, W * .5, H * .55); g.stroke();
  g.fillStyle = 'rgba(120,130,150,.35)'; for (let i = 0; i < 14; i++) { const f = i / 14, x = lerp(W * .21, W * .48, f) + Math.sin(f * 6) * W * .02, y = lerp(H, H * .56, f); bulat(x + (i % 2 ? 3 : -3), y, M * .004 * (1 - f * .5)); }
  g.strokeStyle = '#5a4636'; g.lineWidth = Math.max(1.5, M * .003); for (let i = 0; i < 12; i++) { const x = W * (.55 + i * .04), y = H * (.78 - i * .012); g.beginPath(); g.moveTo(x, y); g.lineTo(x, y - M * .03); g.stroke(); }
  g.lineWidth = 1.2; g.beginPath(); g.moveTo(W * .55, H * .78 - M * .022); g.lineTo(W * .99, H * (.78 - 11 * .012) - M * .022); g.stroke(); g.fillStyle = '#f4f6f8'; for (let i = 0; i < 12; i++) { const x = W * (.55 + i * .04), y = H * (.78 - i * .012); g.beginPath(); g.ellipse(x, y - M * .031, M * .006, M * .003, 0, 0, TAU); g.fill(); }
  // bare trees
  g.strokeStyle = '#3a342e'; g.lineCap = 'round'; for (const [x, y, h] of [[W * .55, H * .72, M * .2], [W * .18, H * .6, M * .12], [W * .85, H * .56, M * .1]]) { const cab = (x0, y0, a, L, w, n) => { if (n === 0 || L < 3) return; const x1 = x0 + Math.cos(a) * L, y1 = y0 + Math.sin(a) * L; g.lineWidth = w; g.beginPath(); g.moveTo(x0, y0); g.lineTo(x1, y1); g.stroke(); cab(x1, y1, a - .45, L * .72, w * .65, n - 1); cab(x1, y1, a + .4, L * .7, w * .65, n - 1); }; cab(x, y, -PI / 2, h * .4, h * .05, 6); }
  g.restore();
  salju(waktuNyata, .8, .8);
  // her shoulder + hair, out of focus in the foreground
  TK.rim = null;
  g.save(); g.translate(t * W * .02, 0);
  saring('blur(9px) brightness(.55)', () => gadisBelakang(W * (P ? 1.0 : .93), H * (P ? 1.9 : 2.6), P ? H * 1.25 : H * 2.1, { angin: .15, arahAngin: -1, syal: true, bayangan: false }));
  g.restore();
});
// 8 — harbour arch bridge at dusk (36.5–41.5)
adeg(36.5, 41.5, t => {
  const P = potret(), M = Math.min(W, H), hor = H * (P ? .42 : .5);
  langit([[0, '#8aa0c8'], [.5, '#e8b8b0'], [1, '#f7d6b8']]);
  const sun = [W * .12, hor - H * .05];
  g.save(); g.translate(t * W * .012, 0);
  cahaya(...sun, M * .8, '#ffb48a', .45); cahaya(...sun, M * .05, '#fff4e0', .9);
  awan(W * .2, H * .12, M * .5, 31, '#fbe0d4', '#c79ab0', .6);
  // skyline
  const R = rng(81); for (let i = 0; i < 48; i++) { const x = -W * .2 + R() * W * 1.4, w = M * (.02 + R() * .05), h = H * (.02 + R() * .08) * (x < W * .6 ? 1 : .6); g.fillStyle = mixC('#9a8c9a', '#c8b4b4', R()); g.fillRect(x, hor - h, w, h); jendelaGedung(x, hor - h, w, h, 3, 5, '#ffe6b0', .5); }
  // arch
  const L0 = W * (P ? -.15 : -.12), L1 = W * (P ? 1.15 : 1.08), dek = hor - H * .035, puncak = H * (P ? .2 : .12);
  const atas = f => dek - (dek - puncak) * Math.sin(f * PI), bawahA = f => dek - (dek - puncak - H * .035) * Math.sin(f * PI);
  g.strokeStyle = '#8a5a52'; g.lineWidth = M * .006; g.beginPath(); for (let i = 0; i <= 60; i++) { const f = i / 60, x = lerp(L0, L1, f); i ? g.lineTo(x, atas(f)) : g.moveTo(x, atas(f)); } g.stroke();
  g.beginPath(); for (let i = 0; i <= 60; i++) { const f = i / 60, x = lerp(L0, L1, f); i ? g.lineTo(x, bawahA(f)) : g.moveTo(x, bawahA(f)); } g.stroke();
  g.lineWidth = M * .0025; g.beginPath(); for (let i = 1; i < 40; i++) { const f = i / 40, f2 = (i + 1) / 40, x = lerp(L0, L1, f), x2 = lerp(L0, L1, f2); g.moveTo(x, atas(f)); g.lineTo(x, bawahA(f)); g.moveTo(x, atas(f)); g.lineTo(x2, bawahA(f2)); if (f > .12 && f < .88) { g.moveTo(x, bawahA(f)); g.lineTo(x, dek); } } g.stroke();
  g.fillStyle = '#6a4a44'; g.fillRect(L0, dek, L1 - L0, M * .008);
  for (const x of [lerp(L0, L1, .06), lerp(L0, L1, .94)]) { g.fillStyle = '#c8b09a'; g.fillRect(x - M * .02, dek - H * .06, M * .04, H * .065); }
  // water
  g.fillStyle = gradV(hor, H, [[0, '#9aa8c4'], [.3, '#6d82a8'], [1, '#3a4e76']]); g.fillRect(-W * .3, hor, W * 1.6, H);
  g.save(); g.globalCompositeOperation = 'lighter'; for (let i = 0; i < 140; i++) { const y = hor + Math.pow(R(), 1.5) * (H - hor), x = -W * .2 + R() * W * 1.4, w = M * (.01 + R() * .05) * (1 + (y - hor) / H * 3); g.fillStyle = rgba('#ffd6c0', (.05 + R() * .15) * (.6 + .4 * Math.sin(waktuNyata * 2 + i))); g.fillRect(x + Math.sin(waktuNyata + i) * 6, y, w, 1.5 + (y - hor) / H * 3); } g.restore();
  for (let i = 0; i < 3; i++) { const bx = W * (.2 + i * .22) + Math.sin(waktuNyata * .6 + i) * 4, by = hor + H * (.03 + i * .01), sz = M * (.03 - i * .005); g.fillStyle = '#f4efe6'; g.beginPath(); g.moveTo(bx, by - sz * 1.6); g.lineTo(bx + sz * .7, by - sz * .1); g.lineTo(bx, by - sz * .1); g.fill(); g.fillStyle = '#e8d8cc'; g.beginPath(); g.moveTo(bx - sz * .05, by - sz * 1.4); g.lineTo(bx - sz * .5, by - sz * .15); g.lineTo(bx - sz * .05, by - sz * .15); g.fill(); g.fillStyle = '#3a3a48'; g.fillRect(bx - sz * .6, by - sz * .1, sz * 1.4, sz * .18); }
  // ferry
  const fx = W * .72 - t * W * .015; g.fillStyle = '#efe6d2'; g.fillRect(fx, hor - M * .015, M * .08, M * .015); g.fillStyle = '#e0b03a'; g.fillRect(fx + M * .01, hor - M * .03, M * .055, M * .015); g.fillStyle = '#3a3a3a'; g.fillRect(fx, hor, M * .08, M * .005);
  g.restore();
  for (let i = 0; i < 3; i++) burung(W * (.25 + i * .09) + t * W * .03, H * (.22 + (i % 2) * .03), M * .014, waktuNyata * .8 + i, .8, '#f4eee8');
  // her, foreground
  TK.rim = '#ffd9c0'; TK.rimSisi = -1;
  const s = P ? W * .2 : H * .17, gx0 = W * (P ? .5 : .45) - t * W * .012, gy0 = H - s * (P ? 2.6 : 2.3), sel = eio(u(t, 1.2, 2.2)) * (1 - eio(u(t, 3.6, 4.6)));
  tokoh(() => gadisDada(gx0, gy0, s, { angin: .55, arahAngin: 1, lirikX: -.6, lirikY: .2, mulut: 'senyum', merah: .55, miring: .04 - sel * .04, tol: -.3, tangan: sel > .01 ? { pose: 'rambut', k: sel } : null }),
    { sinar: [sun[0], sun[1], M * 1.2, '#ffb48a', .35], bayang: [gx0 - s, 0, gx0 + s * 1.4, 0, '#3a2a4a', .35] });
  suar(sun[0] + t * W * .012, sun[1], .55, '#ffc49a');
  saring('blur(6px)', () => { g.fillStyle = '#2a2230'; g.fillRect(0, H * .9, W, H * .012); for (let x = -t * M * .06 % (M * .12); x < W; x += M * .12) g.fillRect(x, H * .9, M * .01, H * .12); g.fillRect(0, H * .95, W, H * .008); });
});
// 9 — the swing and the mountain (41.5–46.5)
adeg(41.5, 46.5, t => {
  const P = potret(), M = Math.min(W, H);
  const piv0 = [W * (P ? -.05 : .1), -H * .1], tali0 = P ? H * .78 : H * .8, a0 = -.55 + .32 * Math.sin(waktuNyata * 1.6), ikut = (piv0[0] + Math.sin(-a0) * tali0 - W * .45) * .12;
  langit([[0, '#1d2d58'], [.55, '#3b5a8e'], [1, '#6f8cb8']]);
  g.save(); g.translate(-ikut * .3, 0); bintangJatuh(t, W * .5, H * .08, 2.4);
  for (const [x, y, r, f] of BINTANG) { g.fillStyle = `rgba(255,255,255,${.15 + .35 * Math.abs(Math.sin(waktuNyata * .8 + f))})`; bulat(x * W, y * H * .6, r * .8); }
  // Fuji
  const pk = [W * .56, H * (P ? .5 : .36)], alas = H * (P ? .82 : .9), bw = P ? W * .95 : W * .62;
  const kerucut = jalur(p => { p.moveTo(pk[0] - bw, alas); p.quadraticCurveTo(pk[0] - bw * .35, alas - (alas - pk[1]) * .35, pk[0] - M * .05, pk[1]); p.lineTo(pk[0] + M * .05, pk[1]); p.quadraticCurveTo(pk[0] + bw * .35, alas - (alas - pk[1]) * .35, pk[0] + bw, alas); p.closePath(); });
  g.fillStyle = gradV(pk[1], alas, [[0, '#46557a'], [1, '#222c48']]); g.fill(kerucut);
  g.save(); g.clip(kerucut); g.fillStyle = 'rgba(15,20,40,.35)'; g.fillRect(pk[0], pk[1], W, H);
  g.fillStyle = gradV(pk[1], pk[1] + H * .15, [[0, '#f4f6fb'], [1, '#c9d2e6']]); g.beginPath(); g.moveTo(pk[0] - bw, pk[1] - 10);
  for (let i = 0; i <= 16; i++) { const f = i / 16, x = lerp(pk[0] - bw * .34, pk[0] + bw * .34, f), y = pk[1] + H * (.06 + (i % 2) * .05 + (1 - Math.abs(f - .5) * 2) * .03); g.lineTo(x, y); } g.lineTo(pk[0] + bw, pk[1] - 10); g.closePath(); g.fill();
  g.fillStyle = 'rgba(150,165,200,.55)'; g.beginPath(); g.moveTo(pk[0] + M * .05, pk[1]); g.lineTo(pk[0] + bw * .34, pk[1] + H * .12); g.lineTo(pk[0] + M * .02, pk[1] + H * .1); g.fill();
  g.strokeStyle = 'rgba(230,236,250,.5)'; g.lineWidth = 2; for (let i = 0; i < 18; i++) { const f = (i + .5) / 18, x = lerp(pk[0] - bw * .3, pk[0] + bw * .3, f); g.beginPath(); g.moveTo(x, pk[1] + H * .1); g.lineTo(x + (x - pk[0]) * .4, pk[1] + H * (.18 + (i % 3) * .03)); g.stroke(); }
  g.restore();
  kabut(alas - H * .01, H * .04, '#8aa2c8', .5, t, 6, 4);
  g.fillStyle = '#141a2c'; g.fillRect(-W, alas, W * 3, H);
  g.save(); g.beginPath(); g.rect(-W, alas + H * .02, W * 3, H * .1); g.clip(); g.fillStyle = gradV(alas, alas + H * .12, [[0, '#2a3a60'], [1, '#141a2c']]); g.fillRect(-W, alas, W * 3, H * .2);
  g.globalAlpha = .35; g.translate(0, (alas + H * .02) * 2); g.scale(1, -1); g.fillStyle = '#6a7aa6'; g.fill(kerucut); g.globalAlpha = 1; g.restore();
  g.strokeStyle = 'rgba(200,215,245,.3)'; g.lineWidth = 1; for (let i = 0; i < 18; i++) { const y = alas + H * (.03 + (i % 6) * .014), x = W * ((i * 37 % 100) / 100) + Math.sin(waktuNyata + i) * 8; g.beginPath(); g.moveTo(x, y); g.lineTo(x + M * .04, y); g.stroke(); }
  for (let i = 0; i < 22; i++) { const x = W * (.1 + (i * 41 % 80) / 100), y = alas + H * .01 + (i % 3) * 2; g.fillStyle = rgba('#ffd08a', .5 + .4 * Math.sin(waktuNyata * 2 + i)); g.fillRect(x, y, 2, 2); cahaya(x, y, M * .015, '#ffc070', .3); }
  g.restore(); g.save(); g.translate(-ikut, 0);
  // swing on a long chain from the top-left
  const piv = [W * (P ? -.05 : .1), -H * .1], tali = P ? H * .78 : H * .8, a = -.55 + .32 * Math.sin(waktuNyata * 1.6), va = Math.cos(waktuNyata * 1.6);
  const seat = [piv[0] + Math.sin(-a) * tali, piv[1] + Math.cos(a) * tali];
  g.strokeStyle = '#9aa3b4'; g.lineWidth = 2.5; g.setLineDash([5, 3]); g.beginPath(); g.moveTo(...piv); g.lineTo(seat[0], seat[1] - 4); g.stroke(); g.setLineDash([]);
  g.fillStyle = '#3a2a22'; g.save(); g.translate(...seat); g.rotate(a); g.fillRect(-M * .06, -3, M * .12, 8); g.restore();
  TK.rim = '#bcd0ff'; TK.rimSisi = 1;
  tokoh(() => gadisAyun(seat[0], seat[1] - 3, P ? H * .34 : H * .5, { kec: va, dir: 1, miring: a * .9 }), { gelap: ['#7f8fc0', .45], tint: ['#3a4a80', .4] });
  g.restore();
  rumput(H * .93, H * 1.02, 160, '#0c1020', waktuNyata, M * .07, 31, 2);
  g.save(); g.globalCompositeOperation = 'lighter'; for (let i = 0; i < 14; i++) { const x = W * ((i * 53 % 100) / 100) + Math.sin(waktuNyata * .7 + i) * M * .03, y = H * (.8 + (i * 29 % 20) / 100) + Math.cos(waktuNyata * .9 + i) * M * .02, a = Math.max(0, Math.sin(waktuNyata * 2 + i * 2)); cahaya(x, y, M * .02, '#e8ff9a', .6 * a); } g.restore();
});
// 10 — the smile (46.5–52)
adeg(46.5, 52, t => {
  const P = potret(), M = Math.min(W, H);
  langit([[0, '#c7d6e6'], [.5, '#e9d6c0'], [1, '#d8b48c']]);
  saring('blur(10px)', () => { g.strokeStyle = '#6a5a52'; g.lineCap = 'round'; const cab = (x0, y0, a, L, w, n) => { if (!n) return; const x1 = x0 + Math.cos(a) * L, y1 = y0 + Math.sin(a) * L; g.lineWidth = w; g.beginPath(); g.moveTo(x0, y0); g.lineTo(x1, y1); g.stroke(); cab(x1, y1, a - .5, L * .75, w * .7, n - 1); cab(x1, y1, a + .35, L * .7, w * .7, n - 1); }; cab(-W * .05, H * .6, -1.0, M * .35, M * .03, 7); cab(W * 1.05, H * .4, -2.2, M * .3, M * .025, 7); });
  saring('blur(3px)', () => bokeh(BOK_HANGAT, waktuNyata, 1.2));
  cahaya(W * .85, H * .15, M * 1.1, '#ffd9a0', .5);
  TK.rim = '#fff0cc'; TK.rimSisi = 1;
  const s = (P ? W * .33 : H * .29) * (1 + .06 * eio(t / 5.5)), tr = eio(u(t, .3, 1.3));
  daun(waktuNyata, 'rgba(230,160,90,.55)', .5, 3);
  tokoh(() => gadisDada(W * .5, P ? H * .42 : H * .46, s, { syal: true, mata: 'senyum', mulut: 'lebar', merah: .9, angin: .5, arahAngin: -1, miring: .07 + Math.sin(waktuNyata * .8) * .02, tol: .15, tangan: { pose: 'syal', k: tr } }),
    { sinar: [W * .85, H * .12, M * 1.2, '#ffd9a0', .4], bayang: [W * .7, H * .2, W * .2, H * .9, '#4a2a2a', .3] });
  suar(W * .85, H * .12, .8, '#ffe0b0');
  daun(waktuNyata + 3, 'rgba(210,130,70,.6)', .25, 7);
  debu(waktuNyata, '#fff0d0', .6);
});
// 11 — misty tea house with lanterns (52–56.5)
adeg(52, 56.5, t => {
  const P = potret(), M = Math.min(W, H), z = 1.05 + .04 * t / 4.5;
  langit([[0, '#a8a8a2'], [1, '#6e6a62']]);
  g.save(); dorong(z, W * .4, H * .5, 0, lerp(-H * .05, H * .03, eio(t / 4.5)));
  const bx = W * (P ? .05 : .2), bw = W * (P ? .9 : .62), lantai = 5;
  for (let k = 0; k < lantai; k++) { const y = H * (.12 + k * .15), h = H * .15;
    g.fillStyle = mixC('#3a1e14', '#5a2a1c', k / lantai); g.fillRect(bx, y, bw, h);
    g.fillStyle = '#26130c'; g.beginPath(); g.moveTo(bx - M * .06, y + M * .005); g.lineTo(bx + bw + M * .06, y + M * .005); g.lineTo(bx + bw + M * .02, y - M * .03); g.lineTo(bx - M * .02, y - M * .03); g.fill();
    g.fillStyle = '#6a8a5a'; g.fillRect(bx - M * .06, y + M * .005, bw + M * .12, M * .006);
    for (let i = 0; i < 7; i++) { const wx = bx + bw * (.05 + i * .135); g.fillStyle = rgba('#ffc47a', .55 + .2 * Math.sin(waktuNyata + i + k)); g.fillRect(wx, y + h * .3, bw * .09, h * .45); g.strokeStyle = '#26130c'; g.lineWidth = 1.5; g.strokeRect(wx, y + h * .3, bw * .09, h * .45); g.beginPath(); g.moveTo(wx + bw * .045, y + h * .3); g.lineTo(wx + bw * .045, y + h * .75); g.stroke(); }
    g.strokeStyle = '#1c0e08'; g.lineWidth = 2; g.beginPath(); g.moveTo(bx, y + h * .85); g.lineTo(bx + bw, y + h * .85); g.stroke();
    for (let i = 0; i < 6; i++) { const lx = bx + bw * (.1 + i * .16); lampion(lx, y + h * .15, M * .024, waktuNyata, i + k); cahaya(lx, y + h * .15, M * .1, '#ff6a3a', .3); }
    if (k === 2) { g.fillStyle = '#1c0e08'; g.fillRect(bx + bw * .35, y - M * .01, bw * .3, M * .06); g.fillStyle = '#e0b04a'; for (let c = 0; c < 4; c++) g.fillRect(bx + bw * (.38 + c * .07), y + M * .01, bw * .04, M * .025); }
  }
  g.strokeStyle = '#3f5a34'; g.lineWidth = 2; for (let i = 0; i < 6; i++) { const x = bx + bw * (i / 5); g.beginPath(); g.moveTo(x, H * .12); g.quadraticCurveTo(x + Math.sin(waktuNyata * .6 + i) * 6, H * .2, x + 4, H * (.22 + (i % 3) * .05)); g.stroke(); rimbun(x, H * .13, M * .03, '#4a6a3a', '#2c402a', null, 140 + i, 5); }
  // stone stairs + plants
  g.fillStyle = '#4a4540'; g.fillRect(0, H * .86, W, H); for (let k = 0; k < 6; k++) { g.fillStyle = k % 2 ? '#5a554e' : '#504b45'; g.fillRect(0, H * (.86 + k * .025), W, H * .012); }
  rimbun(W * .08, H * .84, M * .15, '#4a6a3a', '#2c402a', '#6f8f55', 41, 12); rimbun(W * .95, H * .83, M * .13, '#4a6a3a', '#2c402a', '#6f8f55', 42, 12);
  g.restore();
  // mist
  kabut(H * .3, H * .15, '#c9c6be', .42, t, 10, 6); kabut(H * .7, H * .12, '#bdb9b0', .3, t, 14, 8);
  g.fillStyle = 'rgba(190,186,176,.12)'; g.fillRect(0, 0, W, H);
  saring('blur(4px)', () => { const lx = W * (P ? .12 : .1), ly = H; g.fillStyle = '#5a564e'; g.fillRect(lx - M * .03, ly - M * .12, M * .06, M * .12); g.fillRect(lx - M * .06, ly - M * .16, M * .12, M * .04); g.fillStyle = '#4a463e'; g.beginPath(); g.moveTo(lx - M * .08, ly - M * .2); g.lineTo(lx, ly - M * .25); g.lineTo(lx + M * .08, ly - M * .2); g.fill(); g.fillStyle = '#ffcf8a'; g.fillRect(lx - M * .025, ly - M * .155, M * .05, M * .03); cahaya(lx, ly - M * .14, M * .12, '#ffb35a', .5); });
  TK.rim = '#ffc07a'; TK.rimSisi = -1;
  tokoh(() => gadisBelakang(W * (P ? .78 : .76), H * (P ? .98 : 1.02), P ? H * .36 : H * .5, { tengadah: .6, angin: .05, bayangan: .25 }), { sinar: [W * .4, H * .4, M, '#ff8a4a', .3], tint: ['#bdb9b0', .35] });
});
// 12 — rice terraces (56.5–61)
adeg(56.5, 61, t => {
  const P = potret(), M = Math.min(W, H), gx = -t * W * .012, turun = lerp(H * .12, 0, eio(u(t, 0, 3.2)));
  langit([[0, '#9cc0dc'], [.5, '#dfe6de'], [1, '#f2e6c6']]);
  g.save(); g.translate(gx, turun);
  awan(W * .7, H * .08, M * .6, 91, '#ffffff', '#d4dde4', .7);
  punggung(H * .2, H * .04, .7, 6, '#7d9a8c'); punggung(H * .25, H * .05, 1.1, 7, '#5f8466');
  for (let i = 0; i < 30; i++) rimbun(W * 1.2 * i / 29 - W * .1, H * (.26 + (i % 3) * .01), M * .05, '#4f7a46', '#355a36', '#78a060', 100 + i, 6);
  // terraces
  const bands = 14; for (let k = 0; k < bands; k++) { const y0 = H * (.28 + k * .045 + k * k * .0012), amp = H * (.015 + k * .002);
    const garis = x => y0 + Math.sin(x / W * 5 + k * .7) * amp + Math.sin(x / W * 11 + k) * amp * .3;
    g.fillStyle = k % 2 ? '#7fae4c' : '#6a9c40'; g.beginPath(); g.moveTo(-W * .1, H * 1.2); for (let x = -W * .1; x <= W * 1.3; x += 12) g.lineTo(x, garis(x)); g.lineTo(W * 1.3, H * 1.2); g.fill();
    g.strokeStyle = '#b8d27a'; g.lineWidth = 1.5 + k * .2; g.beginPath(); for (let x = -W * .1; x <= W * 1.3; x += 12) x > -W * .1 ? g.lineTo(x, garis(x)) : g.moveTo(x, garis(x)); g.stroke();
    g.strokeStyle = 'rgba(60,90,30,.35)'; g.lineWidth = 1; g.beginPath(); for (let x = -W * .1; x <= W * 1.3; x += 12) { const yy = garis(x) + amp * .6; x > -W * .1 ? g.lineTo(x, yy) : g.moveTo(x, yy); } g.stroke();
    if (k % 3 === 1) for (let i = 0; i < 3; i++) { const x = W * (.1 + ((i * 37 + k * 13) % 100) / 90); palem(x, garis(x), H * (.08 + k * .012), '#4d7a3e', '#2c4a26', waktuNyata, k * 3 + i); }
    if (k % 4 === 2) { g.save(); g.globalCompositeOperation = 'screen'; g.fillStyle = 'rgba(190,215,235,.35)'; g.beginPath(); for (let x = -W * .1; x <= W * 1.3; x += 12) x > -W * .1 ? g.lineTo(x, garis(x) + amp * .8) : g.moveTo(x, garis(x) + amp * .8); for (let x = W * 1.3; x >= -W * .1; x -= 12) g.lineTo(x, garis(x) + amp * 2.2); g.fill(); g.restore(); }
    if (k === 8) { const x = W * .2, y = garis(W * .2); g.fillStyle = '#6a4a30'; g.fillRect(x - M * .02, y - M * .03, M * .04, M * .03); g.fillStyle = '#b8a06a'; g.beginPath(); g.moveTo(x - M * .035, y - M * .028); g.lineTo(x, y - M * .06); g.lineTo(x + M * .035, y - M * .028); g.fill(); }
    if (k === 5) for (let i = 0; i < 4; i++) { const x = W * (.55 + i * .06); g.fillStyle = '#a4452e'; g.beginPath(); g.moveTo(x - M * .03, garis(x) - M * .01); g.lineTo(x, garis(x) - M * .035); g.lineTo(x + M * .03, garis(x) - M * .01); g.fill(); g.fillStyle = '#e6dcc8'; g.fillRect(x - M * .022, garis(x) - M * .012, M * .044, M * .02); }
  }
  g.restore();
  g.save(); g.translate(0, turun * 1.6);
  rimbun(-W * .05, H * .98, M * .4, '#3f6a34', '#27442a', '#6a9a4e', 55, 20);
  cahaya(W * .9, H * .05, M * 1.1, '#fff0c8', .35);
  sinarDewa(W * .95, -H * .05, 8, Math.max(W, H) * 1.2, '#fff4d0', .06, waktuNyata, .04, PI * .7, .7);
  TK.rim = '#fff0c8'; TK.rimSisi = 1;
  tokoh(() => gadisBelakang(W * (P ? .42 : .38), H * (P ? 1.12 : 1.25), P ? H * .5 : H * .8, { ransel: true, angin: .2, arahAngin: -1, bayangan: false }), { sinar: [W, 0, M * 1.4, '#fff0c8', .3], bayang: [W * .7, 0, W * .2, H, '#2a3a20', .3] });
  g.restore();
  saring('blur(8px)', () => rimbun(W * 1.02, -H * .03 + turun * 2.2, M * .26, '#3f6a34', '#22381e', '#5d8a48', 77, 16, .6));
});
// 13 — the beach (61–66)
adeg(61, 66, t => {
  const P = potret(), M = Math.min(W, H), hor = H * (P ? .4 : .42), pantai = H * (P ? .6 : .62);
  langit([[0, '#8ab0d6'], [.4, '#e9d6c0'], [1, '#ffe2b8']]);
  const sun = [W * .82, hor - H * .06]; cahaya(...sun, M * .9, '#ffc88a', .5); cahaya(...sun, M * .05, '#fffaf0', 1);
  awan(W * .3, H * .1, M * .5, 61, '#fff4e4', '#c9b8c4', .6, '#ffe8c0'); awan(W * .85, H * .2, M * .35, 62, '#ffefe0', '#c0aab8', .5, '#ffe8c0');
  // headland + town
  g.fillStyle = '#6a7a6a'; g.beginPath(); g.moveTo(-10, hor); g.lineTo(-10, hor - H * .05); g.quadraticCurveTo(W * .2, hor - H * .07, W * .45, hor - H * .03); g.lineTo(W * .58, hor - H * .02); g.lineTo(W * .6, hor); g.fill();
  const R = rng(91); for (let i = 0; i < 30; i++) { const x = R() * W * .5, h = M * (.008 + R() * .02); g.fillStyle = R() < .7 ? '#efe8dc' : '#d8a07a'; g.fillRect(x, hor - H * .045 + (x / W) * H * .03 - h, M * .015, h); }
  g.fillStyle = gradV(hor, pantai, [[0, '#5a86a8'], [1, '#8ab4c4']]); g.fillRect(0, hor, W, pantai - hor);
  g.save(); g.globalCompositeOperation = 'lighter';
  for (const [x, y, f, s] of GELITER) { const yy = hor + y * (pantai - hor), xx = x * W, a = Math.max(0, Math.sin(waktuNyata * 3 + f)); if (a > 0) { g.fillStyle = `rgba(255,236,200,${a * .5})`; g.fillRect(xx, yy, M * .02 * s + 2, 1.5); } }
  g.restore();
  for (let k = 0; k < 4; k++) { const f = ((waktuNyata * .12 + k / 4) % 1), y = lerp(hor + (pantai - hor) * .3, pantai + H * .05, f), a = Math.sin(f * PI);
    g.fillStyle = `rgba(255,252,245,${a * .8})`; g.beginPath(); g.moveTo(0, y); for (let x = 0; x <= W; x += 10) g.lineTo(x, y + Math.sin(x * .015 + k * 3 + waktuNyata) * 4); for (let x = W; x >= 0; x -= 10) g.lineTo(x, y + 4 + f * 8 + Math.sin(x * .02 + k) * 3); g.fill(); }
  { const r = rng(93); for (let i = 0; i < 6; i++) { const x = W * (.02 + r() * .2), y = hor + (pantai - hor) * (.4 + r() * .6), rr = M * (.02 + r() * .03); g.fillStyle = '#4a4a50'; g.beginPath(); g.ellipse(x, y, rr * 1.3, rr, 0, PI, TAU); g.fill(); g.fillStyle = 'rgba(255,230,200,.3)'; g.beginPath(); g.ellipse(x - rr * .3, y - rr * .6, rr * .5, rr * .2, 0, 0, TAU); g.fill(); g.fillStyle = 'rgba(255,255,255,.5)'; g.fillRect(x - rr * 1.4, y - 1, rr * 2.8, 2); } }
  const basah = pantai + H * .05 + Math.sin(waktuNyata * .9) * H * .015;
  g.fillStyle = gradV(pantai, H, [[0, '#c9a878'], [1, '#e6c898']]); g.fillRect(0, basah, W, H);
  g.fillStyle = 'rgba(120,150,170,.25)'; g.fillRect(0, basah, W, H * .04);
  g.fillStyle = 'rgba(255,250,240,.7)'; g.beginPath(); g.moveTo(0, basah); for (let x = 0; x <= W; x += 10) g.lineTo(x, basah + 4 + Math.sin(x * .03 + waktuNyata * 2) * 3); g.lineTo(W, basah - 2); g.closePath(); g.fill();
  { const r = rng(94); g.fillStyle = '#8a6a4a'; g.save(); g.translate(W * .18, H * .9); g.rotate(-.15); g.beginPath(); g.roundRect(-M * .12, -M * .012, M * .24, M * .024, M * .01); g.fill(); g.fillStyle = 'rgba(255,240,220,.3)'; g.fillRect(-M * .11, -M * .01, M * .2, M * .004); g.restore();
    for (let i = 0; i < 10; i++) { g.fillStyle = r() < .5 ? '#f4e8dc' : '#e8c8b0'; g.beginPath(); g.ellipse(W * r(), basah + H * .06 + r() * (H - basah) * .8, M * .006, M * .004, r() * 3, 0, TAU); g.fill(); } }
  // girl walking in the shallows
  const d = lerp(1, .8, t / 5), gx = lerp(W * .62, W * .66, t / 5), gy = lerp(basah + H * .04, basah + H * .01, t / 5);
  for (let i = 1; i < 9; i++) { g.fillStyle = 'rgba(120,90,60,.35)'; g.beginPath(); g.ellipse(gx - i * M * .012 + (i % 2 ? -1 : 1) * M * .012, gy + i * H * .025, M * .01, M * .004, 0, 0, TAU); g.fill(); }
  TK.rim = '#fff0d0'; TK.rimSisi = -1;
  tokoh(() => gadisBelakang(gx, gy, (P ? H * .2 : H * .3) * d, { jalan: true, fase: waktuNyata * 4.4, angin: .6, arahAngin: 1, mantel: '#efe7da', mantelB: '#cfc3b0', bayangan: .25 }), { sinar: [sun[0], sun[1], M * 1.2, '#ffc88a', .35], bayang: [W, 0, W * .3, 0, '#4a3a4a', .3] });
  g.fillStyle = 'rgba(255,255,255,.25)'; g.beginPath(); g.ellipse(gx, gy, M * .03 * d, M * .006, 0, 0, TAU); g.fill();
  for (let i = 0; i < 3; i++) { const f = (waktuNyata * 2.2 + i / 3) % 1; g.strokeStyle = `rgba(255,255,255,${.5 * (1 - f)})`; g.lineWidth = 1.5; g.beginPath(); g.ellipse(gx + (i - 1) * M * .012, gy, M * .02 * d * (.5 + f), M * .005 * (.5 + f), 0, PI, TAU); g.stroke(); }
  for (let i = 0; i < 3; i++) burung(W * (.2 + i * .07) + t * W * .025, H * (.16 + (i % 2) * .03), M * .013, waktuNyata * .9 + i, .7, '#ffffff');
  suar(sun[0], sun[1], .75, '#ffd9a0');
}, { goyang: 1.3 });
// 14 — the foggy trail (66–70)
adeg(66, 70, t => {
  const P = potret(), M = Math.min(W, H);
  langit([[0, '#5a6680'], [.6, '#8792a6'], [1, '#9aa2b0']]);
  kabut(H * .3, H * .2, '#aab2c2', .45, t, 10, 2);
  g.fillStyle = '#6a6458'; g.beginPath(); g.moveTo(-10, H * .45); g.quadraticCurveTo(W * .5, H * .4, W * 1.1, H * .25); g.lineTo(W * 1.1, H); g.lineTo(-10, H); g.fill();
  g.fillStyle = '#8a7a5e'; g.beginPath(); g.moveTo(-10, H * .52); g.quadraticCurveTo(W * .4, H * .5, W * 1.1, H * .4); g.lineTo(W * 1.1, H); g.lineTo(-10, H); g.fill();
  rumput(H * .45, H, 700, 'rgba(170,140,90,.55)', waktuNyata, M * .05, 12, 1.5); rumput(H * .6, H, 300, 'rgba(90,70,45,.6)', waktuNyata, M * .08, 13, 2);
  saring('blur(3px)', () => { for (let i = 0; i < 7; i++) { const x = W * (.05 + i * .15), tt = x / (W * 1.1), y = (1 - tt) * (1 - tt) * H * .45 + 2 * (1 - tt) * tt * H * .4 + tt * tt * H * .25 + 4; g.fillStyle = 'rgba(70,80,95,.45)'; g.fillRect(x - 2, y - M * .1, 4, M * .1); rimbun(x, y - M * .12, M * .05, 'rgba(70,80,95,.45)', 'rgba(60,70,85,.45)', null, 200 + i, 7); } });
  // path
  g.fillStyle = '#7a6a54'; g.beginPath(); g.moveTo(W * .3, H); g.bezierCurveTo(W * .45, H * .8, W * .5, H * .65, W * .62, H * .48); g.lineTo(W * .65, H * .47); g.bezierCurveTo(W * .56, H * .66, W * .58, H * .8, W * .62, H); g.fill();
  for (let i = 0; i < 8; i++) { const f = i / 8, x = lerp(W * .66, W * .7, f) + (1 - f) * W * .1, y = lerp(H * .98, H * .5, Math.pow(f, .7)), hh = M * .07 * (1 - f * .7); g.fillStyle = '#4a4238'; g.fillRect(x, y - hh, Math.max(2, hh * .1), hh); if (i) { g.strokeStyle = 'rgba(60,54,46,.8)'; g.lineWidth = 1; g.beginPath(); g.moveTo(x, y - hh * .7); const f2 = (i - 1) / 8, x2 = lerp(W * .66, W * .7, f2) + (1 - f2) * W * .1, y2 = lerp(H * .98, H * .5, Math.pow(f2, .7)), h2 = M * .07 * (1 - f2 * .7); g.lineTo(x2, y2 - h2 * .7); g.stroke(); } }
  { const sx = W * .4, sy = H * .86; g.fillStyle = '#4a3a2a'; g.fillRect(sx, sy - M * .12, M * .01, M * .12); g.save(); g.translate(sx + M * .005, sy - M * .1); g.rotate(-.08); g.fillStyle = '#6a5438'; g.beginPath(); g.moveTo(-M * .05, -M * .015); g.lineTo(M * .04, -M * .015); g.lineTo(M * .055, 0); g.lineTo(M * .04, M * .015); g.lineTo(-M * .05, M * .015); g.fill(); g.fillStyle = 'rgba(255,240,210,.5)'; g.fillRect(-M * .04, -M * .003, M * .06, M * .005); g.restore(); }
  rimbun(W * .9, H * .55, M * .12, '#5a5a48', '#3a3a30', null, 71, 12); rimbun(W * .1, H * .62, M * .1, '#5a5a48', '#3a3a30', null, 72, 10);
  const f = t / 4, gy = lerp(H * .7, H * .6, f), gx = lerp(W * .54, W * .57, f);
  TK.rim = '#c9d2e0'; TK.rimSisi = 1;
  tokoh(() => gadisBelakang(gx, gy, (P ? H * .15 : H * .22) * lerp(1, .85, f), { jalan: true, fase: waktuNyata * 4.8, ransel: true, angin: .3, arahAngin: -1, bayangan: .2 }), { tint: ['#9aa2b0', .6], gelap: ['#b4bccb', .4] });
  kabut(H * .45, H * .08, '#b8bfcc', .35, t, 16, 5); kabut(H * .85, H * .1, '#b0b7c4', .3, t, 20, 9);
  g.fillStyle = 'rgba(150,160,180,.08)'; g.fillRect(0, 0, W, H);
});
// 15 — back home with the laptop (70–76)
adeg(70, 76, t => {
  const P = potret(), M = Math.min(W, H), z = 1 + .04 * t / 6;
  g.save(); dorong(z, W / 2, H * .45);
  papan(0, 0, W, H, '#8a6446', '#a47a54', M * .09, 9);
  g.fillStyle = 'rgba(30,15,5,.25)'; g.fillRect(0, 0, W, H);
  // dark window/cabinet above
  const wy = P ? H * .12 : H * .08, ww = P ? W * .7 : W * .5, wh = P ? H * .14 : H * .22;
  g.fillStyle = '#1a120d'; g.fillRect(W / 2 - ww / 2 - M * .02, wy - M * .02, ww + M * .04, wh + M * .04); g.fillStyle = '#2b1d14'; g.fillRect(W / 2 - ww / 2, wy, ww, wh);
  g.fillStyle = 'rgba(255,220,170,.12)'; g.fillRect(W / 2 - ww / 2, wy + wh - 4, ww, 4);
  hiasanDinding(t, W * .04, W * .96, (P ? H * .12 : H * .08) + (P ? H * .14 : H * .22) + M * .06);
  rakBuku(P ? W * .04 : W * .05, P ? H * .55 : H * .62, P ? W * .26 : W * .2, t); rakBuku(P ? W * .7 : W * .75, P ? H * .55 : H * .62, P ? W * .26 : W * .2, t + 2);
  cahaya(W * .5, H * .1, M, '#ffc88a', .3);
  const lihat = eio(u(t, 1.6, 2.4)), s = P ? W * .25 : H * .2, gy0 = H - (P ? 3.1 : 3.2) * s;
  TK.rim = '#ffd9a0'; TK.rimSisi = 1;
  const kedip = .85 + .15 * Math.sin(waktuNyata * 9) * Math.sin(waktuNyata * 2.3);
  tokoh(() => gadisDada(W * .5, gy0, s, { lirikY: lerp(.9, 0, lihat), mata: 'sayu', bukaMata: lerp(.6, 1, lihat), mulut: lihat > .6 && t > 2.8 ? 'senyum' : 'datar', merah: .5 + .3 * lihat, miring: lerp(.1, -.04, lihat), tangan: { pose: 'dagu', k: 1 - eio(u(t, 1.2, 2.2)) } }),
    { sinar: [W * .5, H * .95, M * .9, '#a9d4ff', .3 * kedip], bayang: [0, gy0 - s, 0, gy0 + s * 3, '#2a1a20', .2] });
  // laptop lid, facing us
  const lw = P ? W * .5 : W * .3, lh = lw * .62, ly = H - lh * .92;
  cahaya(W * .5, ly, lw, '#bfe0ff', .25);
  g.fillStyle = gradV(ly, ly + lh, [[0, '#d9dce0'], [1, '#a9aeb4']]); g.beginPath(); g.roundRect(W / 2 - lw / 2, ly, lw, lh, M * .02); g.fill();
  g.fillStyle = 'rgba(255,255,255,.35)'; g.beginPath(); g.moveTo(W / 2 - lw / 2 + M * .02, ly + 2); g.lineTo(W / 2 - lw * .1, ly + 2); g.lineTo(W / 2 - lw * .35, ly + lh); g.lineTo(W / 2 - lw / 2, ly + lh); g.lineTo(W / 2 - lw / 2, ly + M * .02); g.fill();
  g.restore();
  // title
  const a = muncul(t, 3.4, 6.2, .8, .6);
  if (a > 0) { g.fillStyle = `rgba(10,6,4,${a * .72})`; g.fillRect(0, 0, W, H);
    g.save(); g.globalAlpha = a; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = '#fff4e2';
    g.font = `italic 500 ${P ? 76 : 84}px "Cormorant Garamond", Georgia, serif`; g.fillText('Out There', W / 2, H * .42);
    g.font = `500 ${P ? 18 : 18}px Inter, sans-serif`; g.globalAlpha = a * u(t, 4.0, 4.8) * .85; g.fillText('YOUR NEXT ADVENTURE IS WAITING', W / 2, H * .42 + (P ? 70 : 74)); g.restore(); }
});

// ---------- subtitles
const SUB = [
  [0.9, 5.9, 'Some days, these four walls feel a little too close.'],
  [7.0, 11.1, 'I don’t know what tomorrow looks like.'],
  [12.3, 15.7, 'Honestly? That’s the exciting part.'],
  [16.6, 21.1, 'So I packed light and said yes.'],
  [22.0, 26.2, 'Yes to trails I’d never heard of,'],
  [27.0, 31.2, 'to streets that smelled like rain and tea,'],
  [32.0, 36.2, 'to winters colder than my excuses,'],
  [37.0, 41.2, 'to cities that didn’t know my name,'],
  [42.0, 46.2, 'and mountains that made me feel weightless.'],
  [47.0, 51.7, 'Somewhere out there, I found parts of me I’d forgotten.'],
  [52.5, 56.3, 'Not every place was on the map.'],
  [57.0, 60.8, 'Not every road made sense.'],
  [61.5, 65.7, 'But every step taught me something,'],
  [66.3, 69.8, 'even the ones I took in the fog.'],
  [70.4, 73.2, 'So… where to next?'],
];

function subtitle(t) {
  const P = FORMAT === '916';
  for (const [a, b, s] of SUB) {
    const al = muncul(t, a, b, .45, .45); if (al <= 0) continue;
    L.save(); L.globalAlpha = al; L.font = `500 ${P ? 26 : 24}px Inter, sans-serif`; L.textAlign = 'center'; L.textBaseline = 'middle';
    const y = P ? VH * .8 : VH - 104;
    const kata = s.split(' '), baris = [[]]; let w = 0; const maks = P ? VW - 90 : VW - 300;
    for (const k of kata) { const lw = L.measureText(k + ' ').width; if (w + lw > maks && baris[baris.length - 1].length) { baris.push([]); w = 0; } baris[baris.length - 1].push(k); w += lw; }
    baris.forEach((bs, i) => { const tx = bs.join(' '), yy = y + (i - (baris.length - 1) / 2) * (P ? 36 : 32); L.lineWidth = 4; L.strokeStyle = 'rgba(0,0,0,.55)'; L.lineJoin = 'round'; L.strokeText(tx, VW / 2, yy); L.fillStyle = '#ffd84a'; L.fillText(tx, VW / 2, yy); });
    L.restore();
  }
}

// =====================================================================
//  SOUND: piano + pad + rain / wind / waves
// =====================================================================
let A = null, master = null, gema = null, bisingBuf = null, amb = {};
function siapAudio() {
  if (A) { A.resume(); return; }
  try {
    A = new (window.AudioContext || window.webkitAudioContext)();
    const k = A.createDynamicsCompressor(); k.threshold.value = -18; k.connect(A.destination);
    master = A.createGain(); master.gain.value = .85; master.connect(k);
    const pj = A.sampleRate * 4, ir = A.createBuffer(2, pj, A.sampleRate); for (let c = 0; c < 2; c++) { const d = ir.getChannelData(c); for (let i = 0; i < pj; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / pj, 2.6); }
    gema = A.createConvolver(); gema.buffer = ir; const gg = A.createGain(); gg.gain.value = .55; gema.connect(gg).connect(master);
    bisingBuf = A.createBuffer(1, A.sampleRate * 3, A.sampleRate); const d = bisingBuf.getChannelData(0); let last = 0; for (let i = 0; i < d.length; i++) { const w = Math.random() * 2 - 1; last = (last + .02 * w) / 1.02; d[i] = w * .5 + last * 3; }
    const bikin = (tipe, f, q) => { const s = A.createBufferSource(); s.buffer = bisingBuf; s.loop = true; const fl = A.createBiquadFilter(); fl.type = tipe; fl.frequency.value = f; fl.Q.value = q; const gn = A.createGain(); gn.gain.value = 0; s.connect(fl).connect(gn).connect(master); s.start(); return { gn, fl }; };
    amb.hujan = bikin('highpass', 1800, .5); amb.angin = bikin('bandpass', 420, .7); amb.ombak = bikin('lowpass', 700, .5);
  } catch (_) { A = null; }
}
const hz = m => 440 * Math.pow(2, (m - 69) / 12);
function keluar(node, pan, kirim = .35) { let n = node; if (A.createStereoPanner) { const p = A.createStereoPanner(); p.pan.value = pan; node.connect(p); n = p; } n.connect(master); const s = A.createGain(); s.gain.value = kirim; n.connect(s); s.connect(gema); }
function piano(m, t, v, d = 4) {
  const f0 = hz(m), lp = A.createBiquadFilter(), out = A.createGain();
  lp.type = 'lowpass'; lp.frequency.setValueAtTime(1600 + v * 14000, t); lp.frequency.exponentialRampToValueAtTime(480, t + d);
  for (const [k, ty, a] of [[1, 'triangle', 1], [2, 'sine', .4], [3, 'sine', .14], [4.02, 'sine', .05]]) { const o = A.createOscillator(), gg = A.createGain(); o.type = ty; o.frequency.value = f0 * k; o.detune.value = (Math.random() - .5) * 5; gg.gain.value = a; o.connect(gg); gg.connect(lp); o.start(t); o.stop(t + d + .1); }
  const n = A.createBufferSource(), nf = A.createBiquadFilter(), ng = A.createGain(); n.buffer = bisingBuf; nf.type = 'bandpass'; nf.frequency.value = Math.min(8000, f0 * 5); nf.Q.value = 1.5;
  ng.gain.setValueAtTime(v * .2, t); ng.gain.exponentialRampToValueAtTime(.0001, t + .04); n.connect(nf); nf.connect(ng); ng.connect(lp); n.start(t, Math.random()); n.stop(t + .05);
  out.gain.setValueAtTime(0, t); out.gain.linearRampToValueAtTime(v, t + .005); out.gain.exponentialRampToValueAtTime(v * .45, t + .3); out.gain.exponentialRampToValueAtTime(.0001, t + d);
  lp.connect(out); keluar(out, klem((m - 64) / 30, -.6, .6), .45);
}
function senar(ms, t, d, v) { // warm string pad
  for (const m of ms) for (const dt of [-7, 7]) { const o = A.createOscillator(), f = A.createBiquadFilter(), gn = A.createGain(); o.type = 'sawtooth'; o.frequency.value = hz(m); o.detune.value = dt + (Math.random() - .5) * 4;
    f.type = 'lowpass'; f.frequency.setValueAtTime(500, t); f.frequency.linearRampToValueAtTime(1400, t + d * .5); f.frequency.linearRampToValueAtTime(700, t + d); f.Q.value = .5;
    gn.gain.setValueAtTime(0, t); gn.gain.linearRampToValueAtTime(v, t + Math.min(1.6, d * .4)); gn.gain.setValueAtTime(v, t + d * .75); gn.gain.linearRampToValueAtTime(0, t + d + .6);
    o.connect(f); f.connect(gn); keluar(gn, dt > 0 ? .35 : -.35, .6); o.start(t); o.stop(t + d + .7); } }
function bas(m, t, d, v) { const o = A.createOscillator(), o2 = A.createOscillator(), f = A.createBiquadFilter(), gn = A.createGain(); o.type = 'sine'; o2.type = 'triangle'; o.frequency.value = o2.frequency.value = hz(m); f.type = 'lowpass'; f.frequency.value = 300;
  gn.gain.setValueAtTime(0, t); gn.gain.linearRampToValueAtTime(v, t + .05); gn.gain.exponentialRampToValueAtTime(v * .5, t + d * .6); gn.gain.exponentialRampToValueAtTime(.0001, t + d); o.connect(f); o2.connect(f); f.connect(gn); keluar(gn, 0, .1); o.start(t); o2.start(t); o.stop(t + d + .1); o2.stop(t + d + .1); }
function tendang(t, v) { const o = A.createOscillator(), gn = A.createGain(); o.frequency.setValueAtTime(120, t); o.frequency.exponentialRampToValueAtTime(42, t + .25); gn.gain.setValueAtTime(v, t); gn.gain.exponentialRampToValueAtTime(.0001, t + .4); o.connect(gn); keluar(gn, 0, .05); o.start(t); o.stop(t + .45); }
function kocok(t, v) { const n = A.createBufferSource(), f = A.createBiquadFilter(), gn = A.createGain(); n.buffer = bisingBuf; f.type = 'highpass'; f.frequency.value = 7000; gn.gain.setValueAtTime(0, t); gn.gain.linearRampToValueAtTime(v, t + .01); gn.gain.exponentialRampToValueAtTime(.0001, t + .07); n.connect(f); f.connect(gn); keluar(gn, .25, .2); n.start(t, Math.random() * 2); n.stop(t + .08); }
function lonceng(m, t, v) { const o = A.createOscillator(), o2 = A.createOscillator(), gn = A.createGain(), g2 = A.createGain(); o.type = o2.type = 'sine'; o.frequency.value = hz(m); o2.frequency.value = hz(m) * 2.76; g2.gain.value = .3;
  gn.gain.setValueAtTime(0, t); gn.gain.linearRampToValueAtTime(v, t + .003); gn.gain.exponentialRampToValueAtTime(.0001, t + 2.2); o.connect(gn); o2.connect(g2); g2.connect(gn); keluar(gn, .3, .8); o.start(t); o2.start(t); o.stop(t + 2.3); o2.stop(t + 2.3); }
function desir(t, v) { const n = A.createBufferSource(), f = A.createBiquadFilter(), gn = A.createGain(); n.buffer = bisingBuf; n.loop = true; f.type = 'bandpass'; f.Q.value = 2; f.frequency.setValueAtTime(300, t); f.frequency.exponentialRampToValueAtTime(3500, t + 1.1);
  gn.gain.setValueAtTime(0, t); gn.gain.linearRampToValueAtTime(v, t + .9); gn.gain.linearRampToValueAtTime(0, t + 1.4); n.connect(f); f.connect(gn); keluar(gn, 0, .6); n.start(t); n.stop(t + 1.5); }

const BPM = 72, E8 = 60 / BPM / 2, BAR = E8 * 8;
// D – A/C# – Bm – G – Em7 – D/F# – G – A
const PROG = [[38, [62, 66, 69]], [37, [61, 64, 69]], [35, [62, 66, 71]], [43, [62, 67, 71]], [40, [62, 64, 67, 71]], [42, [62, 66, 69]], [43, [62, 67, 71]], [45, [61, 64, 69]]];
const MELODI = [[[0, 78, 3], [3, 76, 1], [4, 74, 4]], [[0, 76, 2], [2, 73, 2], [4, 69, 4]], [[0, 74, 3], [3, 76, 1], [4, 78, 2], [6, 81, 2]], [[0, 79, 6], [6, 78, 1], [7, 76, 1]],
  [[0, 76, 3], [3, 74, 1], [4, 71, 4]], [[0, 74, 2], [2, 76, 2], [4, 78, 4]], [[0, 79, 3], [3, 81, 1], [4, 83, 2], [6, 81, 2]], [[0, 76, 4], [4, 78, 2], [6, 76, 2]]];
function bagian(b) { // arrangement per bar (1 bar = 3.33 s)
  if (b < 4) return { arp: 1, mel: 0, pad: 0, bas: 0, drum: 0, v: .5 };
  if (b < 5) return { arp: 2, mel: 1, pad: 0, bas: 0, drum: 0, v: .6 };
  if (b < 8) return { arp: 2, mel: 1, pad: 1, bas: 1, drum: 0, v: .75 };
  if (b < 16) return { arp: 3, mel: 1, pad: 1, bas: 1, drum: 1, v: 1, tinggi: b >= 12 };
  if (b < 20) return { arp: 2, mel: 2, pad: 1, bas: 1, drum: 0, v: .7 };
  return { arp: 1, mel: 0, pad: 1, bas: 0, drum: 0, v: .5 };
}
let jadwal = -1;
function langkah(i, at) {
  const b = Math.floor(i / 8), pos = i % 8;
  if (b >= 22) { if (b === 22 && pos === 0) { [50, 57, 62, 64, 66, 69, 74].forEach((m, k) => piano(m, at + k * .09, .1, 6)); senar([62, 66, 69, 76], at, 3, .012); bas(38, at, 5, .16); lonceng(86, at + .7, .03); } return; }
  const [ba, ak] = PROG[b % 8], S = bagian(b), v = S.v;
  if (pos === 0) { piano(ba, at, .14 * v + .04, 5); if (S.pad) senar(ak, at, BAR, .007 * v); if (S.bas) bas(ba, at, BAR * .95, .15 * v); }
  if (S.arp === 1 && pos % 2 === 0 && pos) piano(ak[(pos / 2) % ak.length] + (pos === 4 ? 12 : 0), at, .06 * v, 3.5);
  if (S.arp >= 2 && pos) { const pola = [0, ba + 7, ba + 12, ak[0], ba + 19, ak[1], ba + 12, ak[2]]; piano(pola[pos] + (S.tinggi && pos > 3 ? 12 : 0), at, (.05 + (pos % 2 ? 0 : .02)) * v, 3); }
  if (S.arp === 3 && (pos === 3 || pos === 7)) piano(ak[ak.length - 1] + 12, at, .03, 2.5);
  if (S.mel) for (const [p, m, l] of MELODI[b % 8]) if (p === pos) piano(m + (S.mel === 2 ? 12 : 0), at + (Math.random() - .5) * .012, (S.mel === 2 ? .06 : .1) * (.85 + .15 * v), l * E8 + 1.8);
  if (S.drum) { if (pos === 0 || pos === 4) tendang(at, .22); if (pos % 2 === 1) kocok(at, .018 + (pos === 3 || pos === 7 ? .01 : 0)); }
}
function musik() {
  if (!A || !main) return;
  if (jadwal < T - .1 || jadwal > T + 1) jadwal = Math.ceil(T / E8 - 1e-6) * E8;
  while (jadwal < T + .25) { const tb = jadwal, at = A.currentTime + Math.max(0, tb - T) + .03; if (tb < DUR - .3) langkah(Math.round(tb / E8), at); jadwal += E8; }
}
function ambiens(t) {
  if (!A) return; const now = A.currentTime;
  const dalam = (a, b) => t > a && t < b;
  const angin = (dalam(16, 26.5) ? .13 : 0) + (dalam(31.5, 36.5) ? .08 : 0) + (dalam(41.5, 52) ? .09 : 0) + (dalam(56.5, 61) ? .05 : 0) + (dalam(66, 70) ? .14 : 0);
  const ombak = dalam(61, 66.3) ? .22 * (.55 + .45 * Math.sin(t * .9)) : dalam(36.5, 41.5) ? .07 : 0;
  const hujan = t < 11.5 ? .03 : 0; // faint room tone
  const m = main && Suara ? 1 : 0;
  amb.hujan.gn.gain.setTargetAtTime(hujan * m, now, .3); amb.angin.gn.gain.setTargetAtTime(angin * m, now, .5); amb.ombak.gn.gain.setTargetAtTime(ombak * m, now, .3);
  amb.angin.fl.frequency.setTargetAtTime(380 + 160 * Math.sin(t * .5), now, .5);
}
let Suara = true;
const kicau = (n, f0) => () => { if (!A) return; const tt = A.currentTime; for (let k = 0; k < n; k++) { const o = A.createOscillator(), gn = A.createGain(); o.type = 'sine'; o.frequency.setValueAtTime(f0 + k * 250, tt + k * .12); o.frequency.exponentialRampToValueAtTime(f0 * 1.5, tt + k * .12 + .08); gn.gain.setValueAtTime(0, tt + k * .12); gn.gain.linearRampToValueAtTime(.022, tt + k * .12 + .01); gn.gain.exponentialRampToValueAtTime(.0001, tt + k * .12 + .12); o.connect(gn); gn.connect(gema); o.start(tt + k * .12); o.stop(tt + k * .12 + .15); } };
const ACARA = [
  ...[6.5, 11.5, 16, 21.5, 26.5, 31.5, 36.5, 41.5, 46.5, 52, 56.5, 61, 66, 70].map(b => [b - 1.0, () => { if (A) desir(A.currentTime, .025); }]),
  [16.1, () => { if (A) lonceng(90, A.currentTime, .025); }], [46.7, () => { if (A) { lonceng(86, A.currentTime, .025); lonceng(93, A.currentTime + .25, .02); } }],
  [22.4, kicau(3, 2800)], [24.6, kicau(4, 3000)], [57.2, kicau(3, 2900)], [59.4, kicau(4, 3100)],
];


// =====================================================================
//  RENDER
// =====================================================================
const butir = document.createElement('canvas'); butir.width = butir.height = 200;
(() => { const b = butir.getContext('2d'), d = b.createImageData(200, 200); for (let i = 0; i < d.data.length; i += 4) { const v = 128 + (Math.random() - .5) * 255; d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 255; } b.putImageData(d, 0, 0); })();
function lukisAdegan(ctx, sc, t) { g = ctx; const S = C.width / VW; g.setTransform(S, 0, 0, S, 0, 0); g.globalAlpha = 1; g.globalCompositeOperation = 'source-over'; g.filter = 'none'; W = VW; H = VH; const kk = sc.goyang ?? 1; g.translate(W / 2, H / 2); g.rotate(n1(t * .35, sc.a) * .005 * kk); g.scale(1.02, 1.02); g.translate(-W / 2 + n1(t * .5, sc.a + 1) * 3.5 * kk, -H / 2 + n1(t * .45, sc.a + 2) * 3.5 * kk); sc.f(t - sc.a); }
let lalu = performance.now(), tSebelum = T;
function bingkai(t0) {
  const dt = Math.min((t0 - lalu) / 1000, .05); lalu = t0;
  if (main) { T += dt; if (T >= DUR) { T = DUR; setMain(false); } for (const [w, f] of ACARA) if (tSebelum < w && w <= T) f(); musik(); }
  ambiens(T); tSebelum = T; waktuNyata = T; TK.t = T;
  let i = SCENES.findIndex(s => T >= s.a && T < s.b); if (i < 0) i = SCENES.length - 1;
  const sc = SCENES[i], nx = SCENES[i + 1], XF = 1.1;
  lukisAdegan(B, sc, T);
  L.setTransform(1, 0, 0, 1, 0, 0); L.globalAlpha = 1; L.globalCompositeOperation = 'source-over'; L.drawImage(buf, 0, 0);
  if (nx && T > sc.b - XF / 2) { const x = eio((T - (sc.b - XF / 2)) / XF); lukisAdegan(B2, nx, T); L.globalAlpha = x; L.filter = `blur(${((1 - x) * 5 * DPR).toFixed(1)}px)`; L.drawImage(buf2, 0, 0); L.filter = 'none'; L.globalAlpha = 1;
    const leak = Math.sin(x * PI) * .35; if (leak > .01 && true) { L.globalCompositeOperation = 'screen'; const gr = L.createRadialGradient(C.width * .85, C.height * .2, 0, C.width * .85, C.height * .2, C.width * .9); gr.addColorStop(0, `rgba(255,170,90,${leak})`); gr.addColorStop(1, 'rgba(255,120,60,0)'); L.fillStyle = gr; L.fillRect(0, 0, C.width, C.height); L.globalCompositeOperation = 'source-over'; } }
  if (i > 0) { const pv = SCENES[i - 1]; if (T < sc.a + XF / 2) { const x = eio((T - (pv.b - XF / 2)) / XF); lukisAdegan(B2, pv, T); L.globalAlpha = 1 - x; L.drawImage(buf2, 0, 0); L.globalAlpha = 1; } }
  // bloom
  K.setTransform(1, 0, 0, 1, 0, 0); K.globalCompositeOperation = 'source-over'; K.drawImage(C, 0, 0, kecil.width, kecil.height);
  L.globalCompositeOperation = 'screen'; L.globalAlpha = .28; L.filter = 'blur(6px)'; L.drawImage(kecil, 0, 0, C.width, C.height); L.filter = 'none'; L.globalAlpha = 1;
  // warm grade + vignette + grain
  L.globalCompositeOperation = 'soft-light'; L.fillStyle = 'rgba(255,190,130,.28)'; L.fillRect(0, 0, C.width, C.height);
  L.globalCompositeOperation = 'source-over';
  const vg = L.createRadialGradient(C.width / 2, C.height / 2, Math.min(C.width, C.height) * .35, C.width / 2, C.height / 2, Math.max(C.width, C.height) * .75); vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(0,0,0,.55)'); L.fillStyle = vg; L.fillRect(0, 0, C.width, C.height);
  L.globalAlpha = .07; L.globalCompositeOperation = 'overlay'; L.save(); L.translate(Math.random() * 200, Math.random() * 200); L.fillStyle = L.createPattern(butir, 'repeat'); L.fillRect(-200, -200, C.width + 400, C.height + 400); L.restore();
  L.globalAlpha = 1; L.globalCompositeOperation = 'source-over';
  L.setTransform(C.width / VW, 0, 0, C.width / VW, 0, 0);
  if (FORMAT === '169') { L.fillStyle = '#000'; L.fillRect(0, 0, VW, 62); L.fillRect(0, VH - 62, VW, 62); }
  subtitle(T);
  const fade = Math.min(u(T, 0, .8), 1 - u(T, DUR - .4, DUR)); if (fade < 1) { L.fillStyle = `rgba(0,0,0,${1 - fade})`; L.fillRect(0, 0, VW, VH); }
  isi.style.width = (T / DUR * 100) + '%'; waktuEl.textContent = `${T.toFixed(1)} / ${DUR.toFixed(1)}`;
  requestAnimationFrame(bingkai);
}
const bMain = document.getElementById('bMain'), mulaiEl = document.getElementById('mulai'), isi = document.getElementById('isi'), waktuEl = document.getElementById('waktu'), bar = document.getElementById('bar');
function setMain(v) { main = v; bMain.textContent = v ? '❚❚' : '▶'; bMain.setAttribute('aria-label', v ? 'Pause' : 'Play'); if (A) v ? A.resume() : A.suspend(); }
function putar(dariAwal) { siapAudio(); mulaiEl.hidden = true; if (dariAwal || T >= DUR - .01) { T = 0; tSebelum = 0; } setMain(true); }
document.getElementById('bMulai').onclick = () => putar(true);
bMain.onclick = () => main ? setMain(false) : putar(false);
document.getElementById('bUlang').onclick = () => putar(true);
bar.onclick = e => { const r = bar.getBoundingClientRect(); T = klem((e.clientX - r.left) / r.width) * DUR; tSebelum = T; if (!main) putar(false); };
bar.onkeydown = e => { if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { T = klem(T + (e.key === 'ArrowRight' ? 3 : -3), 0, DUR); tSebelum = T; } };
addEventListener('keydown', e => { if (e.key === ' ' && e.target.tagName !== 'BUTTON') { e.preventDefault(); main ? setMain(false) : putar(false); } });
function gantiFormat(f) { FORMAT = f; if (f === '916') { VW = 720; VH = 1280; } else { VW = 1280; VH = 720; } document.body.classList.toggle('v916', f === '916'); document.querySelectorAll('[data-format]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.format === f))); ukur(); }
document.querySelectorAll('[data-format]').forEach(b => b.onclick = () => gantiFormat(b.dataset.format));
gantiFormat(KONFIG_AWAL.format);
window.__video = { lompat: t => { T = t; tSebelum = t; }, format: gantiFormat };
requestAnimationFrame(bingkai);
})();
</script>

</html>
'''

html = HTML_ANIMATION.replace("const KONFIG_AWAL = { format: '916' };", f"const KONFIG_AWAL = {{ format: '{FORMAT}' }};")
components.html(html, height=1060 if FORMAT == "916" else 760, scrolling=False)
st.caption("Press ▶ Play with sound on, then screen-record for TikTok / YouTube.")