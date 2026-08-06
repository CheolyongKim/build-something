# build-something

A pile of small, runnable, dependency-light toys. Each folder is standalone.
Mode A = free builds; Mode B = chained pipelines reusing existing tools (see DIRECTIVE.md).

| folder | what | run |
|--------|------|-----|
| `DIRECTIVE.md` | 작업 지침 (free build ↔ chain build 번갈아) | — |
| `dungeon/` | seeded ASCII dungeon generator (C#) | `dotnet run --project dungeon -- --demo` |
| `life/` | Conway's Game of Life in terminal (py) | `python life/life.py --demo` |
| `serve/` | zero-dep static file server (node) | `node serve/server.js 8080 serve/site` |
| `maze/` | recursive-backtracker maze + BFS solver (C#) | `dotnet run --project maze -- --demo` |
| `mandel/` | Mandelbrot fractal as ASCII (py) | `python mandel/mandel.py --demo` |
| `freq/` | word frequency counter over stdin (py) | `python freq/freq.py --demo` |
| `dice/` | RPG dice roller (3d6, stat, adv/dis) (C#) | `dotnet run --project dice -- --demo` |
| `markov/` | Markov-chain text generator (py) | `cat corpus.txt \| python markov/markov.py --demo` |
| `jsonfmt/` | pretty-print + validate JSON (node) | `echo '{}' \| node jsonfmt/jsonfmt.js --demo` |
| `csv2md/` | CSV -> markdown table (py) | `printf 'a,b\n1,2\n' \| python csv2md/csv2md.py --demo` |
| `namegen/` | fantasy name generator, seeded (py) | `python namegen/namegen.py --demo` |
| `bf/` | Brainfuck interpreter (node) | `printf '...' \| node bf/bf.js --demo` |
| `rps/` | RPS vs adaptive bot (py) | `python rps/rps.py --demo` |
| `sloc/` | source-line counter (py) | `python sloc/sloc.py --demo` |
| `sudoku/` | sudoku generator + solver (C#) | `dotnet run --project sudoku -- --demo` |
| `lorem/` | lorem ipsum generator (py) | `python lorem/lorem.py --demo` |
| `metro/` | terminal metronome (py) | `python metro/metro.py --demo` |
| `passgen/` | diceware passphrase / password (node) | `node passgen/passgen.js --demo` |
| `dungeonmap/` | **chain**: maze -> namegen -> csv2md | `python dungeonmap/dungeonmap.py --demo` |
| `party/` | **chain**: passgen -> dungeonmap -> csv2md (lock codes) | `python party/party.py --demo` |
| `json2csv/` | JSON array -> CSV (node, zero-dep) | `echo '[...]' \| node json2csv/json2csv.js --demo` |
| `wordrank/` | **chain**: serve -> freq -> csv2md | `python wordrank/wordrank.py --demo` |
| `rpsmarkov/` | **chain**: markov -> rps(--auto) -> go-ascii(--text) 봇 대전 승률 ASCII | `python rpsmarkov/rpsmarkov.py --demo` |
| `summaries/` | 프로젝트 요약+유용성선별 HTML (인터랙티브) | `summaries/2026-08-06-projects-summary.html` |
| `mazegame/` | **web + deep** 브라우저 미로 크롤러 (보석+몬스터 추격/전투+승리/게임오버) | `node serve/server.js 8140 mazegame` → open index.html |
| `go-tone/` | **Go** 절차적 멜로디 → WAV 합성 (의존성 0) | `cd go-tone && go build -o go-tone.exe . && ./go-tone.exe 7` |
| `rain/` | **Go** 터미널 비 내리는 애니메이션 (ASCII, 의존성 0) | `cd rain && go build -o rain.exe . && ./rain.exe 30 40` |
| `loreforge/` | **chain**: lorem -> markov -> freq (산문 생성→리믹스→빈도분석) | `python loreforge/loreforge.py --demo` |

ponytail-made: shortest thing that runs, self-checks where logic is non-trivial.
