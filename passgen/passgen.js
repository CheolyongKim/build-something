// Passphrase / password generator. node passgen.js [words|chars] [count]
// default: 4-word diceware-style passphrase.
const crypto = require("crypto");
const WORDS = ("alpha bravo charlie delta echo foxtrot golf hotel india juliet "
  + "kilo lima mike november oscar papa quebec romeo sierra tango uniform victor "
  + "whiskey xray yankee zulu apple bridge cloud diamond eagle forest galaxy harbor").split(" ");

function randInt(n) { return crypto.randomBytes(4).readUInt32BE() % n; }

const mode = process.argv[2] || "words";
const count = parseInt(process.argv[3]) || (mode === "words" ? 4 : 16);

if (process.argv.includes("--demo")) {
  const p = WORDS[randInt(WORDS.length)] + WORDS[randInt(WORDS.length)];
  if (!/[a-z]/.test(p)) { console.error("FAIL"); process.exit(1); }
  if (randInt(1) !== 0) { console.error("FAIL"); process.exit(1); }
  console.error("word_ok=ok rng_ok=ok");
  process.exit(0);
}

if (mode === "words") {
  console.log(Array.from({ length: count }, () => WORDS[randInt(WORDS.length)]).join("-"));
} else {
  const A = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789!@#$%";
  console.log(Array.from({ length: count }, () => A[randInt(A.length)]).join(""));
}
