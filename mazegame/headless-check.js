// Headless harness: stub just enough DOM to run mazegame/index.html's <script>,
// then assert the maze is generated, solvable, gems placed, and (Deep mode) the
// monster chases the player and reaches it on contact.
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

const probe = `
;global.__t={genMaze,autoSolve,
get g(){return g}, get gems(){return gems}, get got(){return got},
get px(){return px}, get py(){return py}, get monsters(){return monsters},
newGame, monsterStep, setMonsters(a){monsters=a;}, setPositions(a,b){px=a;py=b;}};`;

try {
  eval(script + probe);
  const T = global.__t;
  // run several mazes, each must be solvable end->start
  for (let i = 0; i < 100; i++) {
    T.newGame();
    const g = T.g, gems = T.gems;
    if (g[g.length-2][g[0].length-2] !== ".") errors.push("exit not open @"+i);
    if (gems.length !== 4) errors.push("gem count "+gems.length+" @"+i);
    const W = g[0].length, H = g.length;
    const seen = Array.from({length:H},()=>Array(W).fill(false));
    const q=[[1,1]]; seen[1][1]=true; let reached=false;
    while(q.length){const [x,y]=q.shift(); if(x===W-2&&y===H-2){reached=true;break;}
      for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1]]){const nx=x+dx,ny=y+dy;
        if(nx>=0&&nx<W&&ny>=0&&ny<H&&g[ny][nx]!=='#'&&!seen[ny][nx]){seen[ny][nx]=true;q.push([nx,ny]);}}}
    if(!reached) errors.push("exit unreachable @"+i);
  }
  // Deep mode: each monster steps closer (graph distance) and reaches player on contact
  T.newGame();
  const gD = T.g, WD = gD[0].length, HD = gD.length;
  const open = [];
  for (let y=1;y<HD-1;y++) for (let x=1;x<WD-1;x++) if (gD[y][x]==='.') open.push([x,y]);
  let p=null, m1=null, m2=null;
  // pick player + two far monsters
  for (const a of open) { p=a; break; }
  let best=[null,null], bestD=-1;
  for (const b of open) {
    const d = Math.abs(b[0]-p[0])+Math.abs(b[1]-p[1]);
    if (d > bestD) { bestD=d; best=[b, best[0]]; }
  }
  m1 = best[0]; m2 = best[1] || best[0];
  if (!p || !m1) { errors.push("no cells for monster test"); }
  else {
    function distField(px,py){
      const dist=Array.from({length:HD},()=>Array(WD).fill(-1));
      const q=[[px,py]]; dist[py][px]=0;
      while(q.length){const [x,y]=q.shift();
        for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1]]){const nx=x+dx,ny=y+dy;
          if(nx>=0&&nx<WD&&ny>=0&&ny<HD&&gD[ny][nx]!=='#'&&dist[ny][nx]<0){dist[ny][nx]=dist[y][x]+1;q.push([nx,ny]);}}}
      return dist;
    }
    T.setPositions(p[0], p[1]);
    T.setMonsters([{x:m1[0],y:m1[1]},{x:m2[0],y:m2[1]}]);
    const dist = distField(p[0], p[1]);
    for (const m of T.monsters) {
      const d0 = dist[m.y][m.x];
      const step = T.monsterStep(m.x, m.y);
      const d1 = dist[step[1]][step[0]];
      if (d1 !== d0 - 1) errors.push(`monster not on shortest path (d0=${d0} d1=${d1})`);
    }
    // contact: a monster on the player -> monsterStep returns player cell
    T.setMonsters([{x:p[0],y:p[1]}]);
    const hit = T.monsterStep(p[0], p[1]);
    if (!(hit[0]===p[0] && hit[1]===p[1])) errors.push("monster doesn't reach player on contact");
  }
  if (!errors.length) console.log("mazegame_ok: 100 mazes solvable, 4 gems, multi-monster chases + contacts");
  else { console.log("FAIL:", errors.slice(0,5)); process.exit(1); }
} catch (e) {
  console.log("FAIL exception:", e.message); process.exit(1);
}
