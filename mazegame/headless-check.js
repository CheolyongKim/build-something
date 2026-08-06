// Headless harness: stub just enough DOM to run mazegame/index.html's <script>,
// then assert the maze is generated, solvable, and gems are placed.
const fs = require("fs");
const html = fs.readFileSync(__dirname + "/index.html", "utf8");
const script = html.split("<script>")[1].split("</script>")[0];

let errors = [];
const stubCtx = new Proxy({}, { get: () => () => {} }); // no-op canvas ops
const elements = {};
function el(id){ return elements[id] || (elements[id] = { style:{}, onclick:null,
  getContext: () => stubCtx, textContent:"", addEventListener(){}, width:480, height:480 }); }
global.document = {
  getElementById: el,
  addEventListener: () => {},
  documentElement: { },
};
global.getComputedStyle = () => ({ getPropertyValue: () => "#fff" });
global.window = global;

try {
  // expose internals by appending a probe to the script
  const probe = "\n;global.__t={genMaze,autoSolve,get g(){return g},get gems(){return gems},get got(){return got},newGame};";
  eval(script + probe);
  const T = global.__t;
  // run several mazes, each must be solvable end->start
  for (let i = 0; i < 20; i++) {
    T.newGame();
    const g = T.g, gems = T.gems;
    if (g[g.length-2][g[0].length-2] !== ".") errors.push("exit not open @"+i);
    if (gems.length !== 4) errors.push("gem count "+gems.length+" @"+i);
    // reachability via BFS
    const W = g[0].length, H = g.length;
    const seen = Array.from({length:H},()=>Array(W).fill(false));
    const q=[[1,1]]; seen[1][1]=true; let reached=false;
    while(q.length){const [x,y]=q.shift(); if(x===W-2&&y===H-2){reached=true;break;}
      for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1]]){const nx=x+dx,ny=y+dy;
        if(nx>=0&&nx<W&&ny>=0&&ny<H&&g[ny][nx]!=='#'&&!seen[ny][nx]){seen[ny][nx]=true;q.push([nx,ny]);}}}
    if(!reached) errors.push("exit unreachable @"+i);
  }
  T.autoSolve();
  if (!errors.length) console.log("mazegame_ok: 20 mazes generated, all solvable, 4 gems each, autoSolve ran");
  else { console.log("FAIL:", errors.slice(0,5)); process.exit(1); }
} catch (e) {
  console.log("FAIL exception:", e.message); process.exit(1);
}
