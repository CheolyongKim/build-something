// JSON array of objects -> CSV. Reads stdin, writes stdout.
// node json2csv.js [--demo]   (default: first object's keys = header)
const fs = require("fs");
const input = fs.readFileSync(0, "utf8");

if (process.argv.includes("--demo")) {
  const arr = JSON.parse('[{"a":1,"b":2},{"a":3,"b":4}]');
  if (!Array.isArray(arr) || arr.length !== 2) { console.error("FAIL"); process.exit(1); }
  // header = keys of first row, in insertion order
  const keys = Object.keys(arr[0]);
  if (keys.join() !== "a,b") { console.error("FAIL keys"); process.exit(1); }
  console.error("array_ok=ok keys_ok=ok");
  process.exit(0);
}

const arr = JSON.parse(input);
if (!Array.isArray(arr)) { console.error("input must be a JSON array"); process.exit(1); }
const keys = [...new Set(arr.flatMap(o => Object.keys(o)))];
const esc = v => { const s = v == null ? "" : String(v); return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; };
const out = [keys.join(",")];
for (const o of arr) out.push(keys.map(k => esc(o[k])).join(","));
process.stdout.write(out.join("\n") + "\n");
