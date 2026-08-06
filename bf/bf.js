// Brainfuck interpreter. Reads program from stdin, input via second arg or stdin-after.
// Usage: cat prog.bf | node bf.js [input_string]
const fs = require("fs");
const code = fs.readFileSync(0, "utf8");
const input = process.argv[2] || "";
const mem = new Uint8Array(30000);
let mp = 0, ip = 0, inp = 0, out = "";
const bracket = {};
const stack = [];
for (let i = 0; i < code.length; i++) {
  if (code[i] === "[") stack.push(i);
  else if (code[i] === "]") { const j = stack.pop(); bracket[j] = i; bracket[i] = j; }
}
while (ip < code.length) {
  switch (code[ip]) {
    case ">": mp = (mp + 1) % 30000; break;
    case "<": mp = (mp + 29999) % 30000; break;
    case "+": mem[mp] = (mem[mp] + 1) & 255; break;
    case "-": mem[mp] = (mem[mp] + 255) & 255; break;
    case ".": out += String.fromCharCode(mem[mp]); break;
    case ",": mem[mp] = inp < input.length ? input.charCodeAt(inp++) & 255 : 0; break;
    case "[": if (mem[mp] === 0) ip = bracket[ip]; break;
    case "]": if (mem[mp] !== 0) ip = bracket[ip]; break;
  }
  ip++;
}
if (process.argv.includes("--demo")) {
  // echo test: ",." should echo input char 'A' -> 'A'
  const echoOut = run(",.", "A");
  if (echoOut !== "A") { console.error("FAIL echo"); process.exit(1); }
  // multiply: +++++++++[>++++++++<-]> -> 9*8 = 72 = 'H'
  const mulOut = run("+++++++++[>++++++++<-]>.\n", "");
  if (mulOut !== "H") { console.error("FAIL mult: got " + JSON.stringify(mulOut)); process.exit(1); }
  console.error("echo_ok=ok multiply_ok=ok");
  process.exit(0);
}
process.stdout.write(out);

function run(src, inpStr) {
  const m = new Uint8Array(30000); let p = 0, i = 0, k = 0, o = "";
  const b = {}; const st = [];
  for (let x = 0; x < src.length; x++) { if (src[x] === "[") st.push(x); else if (src[x] === "]") { const j = st.pop(); b[j] = x; b[x] = j; } }
  while (i < src.length) {
    const c = src[i];
    if (c === ">") p = (p + 1) % 30000; else if (c === "<") p = (p + 29999) % 30000;
    else if (c === "+") m[p] = (m[p] + 1) & 255; else if (c === "-") m[p] = (m[p] + 255) & 255;
    else if (c === ".") o += String.fromCharCode(m[p]); else if (c === ",") m[p] = k < inpStr.length ? inpStr.charCodeAt(k++) & 255 : 0;
    else if (c === "[") { if (m[p] === 0) i = b[i]; } else if (c === "]") { if (m[p] !== 0) i = b[i]; }
    i++;
  }
  return o;
}
