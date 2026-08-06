// Pretty-print + validate JSON. node jsonfmt.js [--demo]  (reads stdin)
const fs = require("fs");
const input = fs.readFileSync(0, "utf8");

if (process.argv.includes("--demo")) {
  const ok = JSON.parse('{"a":1,"b":[2,3]}');
  if (ok.a !== 1 || ok.b.length !== 2) { console.error("FAIL"); process.exit(1); }
  // validate that invalid JSON throws
  let threw = false;
  try { JSON.parse("{bad"); } catch { threw = true; }
  if (!threw) { console.error("FAIL: invalid not rejected"); process.exit(1); }
  console.error("parse_ok=ok invalid_rejected=ok");
  process.exit(0);
}
const obj = JSON.parse(input); // throws on bad input -> nonzero exit
process.stdout.write(JSON.stringify(obj, null, 2) + "\n");
