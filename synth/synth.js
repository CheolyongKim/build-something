// synth.js: tiny chiptune WAV generator (square-wave arpeggio), zero deps.
// Usage: node synth.js [seed]            -> writes arp.wav
//        node synth.js --demo            -> validate WAV header bytes only
const fs = require("fs");

const SR = 44100, BPM = 120, SECONDS = 4;
const SCALE = [0, 3, 5, 7, 10, 12, 15]; // A-minor pentatonic semis from 110Hz
const freq = s => 110 * Math.pow(2, s / 12);

function genNotes(seed) {
  let r = seed || 7;
  const out = [];
  const beats = (SECONDS * BPM) / 60;
  for (let i = 0; i < beats; i++) {
    r = (r * 1103515245 + 12345) & 0x7fffffff;
    out.push(SCALE[(r / 65536) % SCALE.length | 0]);
  }
  return out;
}

function writeWav(path, samples) {
  const n = samples.length;
  const buf = Buffer.alloc(44 + n * 2);
  buf.write("RIFF", 0); buf.writeUInt32LE(36 + n * 2, 4); buf.write("WAVE", 8);
  buf.write("fmt ", 12); buf.writeUInt32LE(16, 16); buf.writeUInt16LE(1, 20);
  buf.writeUInt16LE(1, 22); buf.writeUInt32LE(SR, 24); buf.writeUInt32LE(SR * 2, 28);
  buf.writeUInt16LE(2, 32); buf.writeUInt16LE(16, 34);
  buf.write("data", 36); buf.writeUInt32LE(n * 2, 40);
  for (let i = 0; i < n; i++) buf.writeInt16LE(samples[i] * 32767, 44 + i * 2);
  fs.writeFileSync(path, buf);
}

function render(notes) {
  const beat = (SR * 60) / BPM;
  const total = SR * SECONDS;
  const out = new Float32Array(total);
  for (let i = 0; i < notes.length; i++) {
    const f = freq(notes[i]);
    const start = i * beat;
    for (let j = 0; j < beat && start + j < total; j++) {
      const t = j / SR;
      const env = Math.exp(-3 * t);
      // square wave
      out[start + j] += (Math.sin(2 * Math.PI * f * t) >= 0 ? 1 : -1) * env * 0.25;
    }
  }
  return out;
}

if (process.argv.includes("--demo")) {
  // reuse the same header-writing path on a tiny buffer and check RIFF/WAVE markers
  const tmp = Buffer.alloc(44 + 4);
  writeWav("__demo.wav", new Float32Array([0, 1]));
  const b = fs.readFileSync("__demo.wav");
  fs.unlinkSync("__demo.wav");
  if (b.toString("ascii", 0, 4) !== "RIFF") { console.error("FAIL: no RIFF"); process.exit(1); }
  if (b.toString("ascii", 8, 12) !== "WAVE") { console.error("FAIL: no WAVE"); process.exit(1); }
  if (b.readUInt16LE(22) !== 1) { console.error("FAIL: not PCM"); process.exit(1); }
  console.error("synth_ok: WAV header valid (RIFF/WAVE/PCM)");
  process.exit(0);
}

const seed = parseInt(process.argv[2] || "7", 10);
const notes = genNotes(seed);
writeWav("arp.wav", render(notes));
console.log("wrote arp.wav (" + notes.length + " notes, seed=" + seed + ")");
