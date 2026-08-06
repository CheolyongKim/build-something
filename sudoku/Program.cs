// Sudoku generator + backtracking solver. Self-check: solves a known puzzle.
// ponytail: naive solver, fine for 9x9.
using System;

var puzzle = new int[9, 9] {
  {5,3,0,0,7,0,0,0,0}, {6,0,0,1,9,5,0,0,0}, {0,9,8,0,0,0,0,6,0},
  {8,0,0,0,6,0,0,0,3}, {4,0,0,8,0,3,0,0,1}, {7,0,0,0,2,0,0,0,6},
  {0,6,0,0,0,0,2,8,0}, {0,0,0,4,1,9,0,0,5}, {0,0,0,0,8,0,0,7,9} };

bool Solve(int[,] g)
{
    for (var y = 0; y < 9; y++) for (var x = 0; x < 9; x++)
        if (g[y, x] == 0)
        {
            for (var v = 1; v <= 9; v++)
                if (Ok(g, x, y, v)) { g[y, x] = v; if (Solve(g)) return true; g[y, x] = 0; }
            return false; // no value fits this cell -> backtrack
        }
    return true; // no zeros left
}
bool Ok(int[,] g, int x, int y, int v)
{
    for (var i = 0; i < 9; i++) if (g[y, i] == v || g[i, x] == v) return false;
    var bx = x / 3 * 3; var by = y / 3 * 3;
    for (var dy = 0; dy < 3; dy++) for (var dx = 0; dx < 3; dx++) if (g[by + dy, bx + dx] == v) return false;
    return true;
}

if (args.Contains("--demo"))
{
    var cp = (int[,])puzzle.Clone();
    if (!Solve(cp)) { Console.Error.WriteLine("FAIL: unsolvable"); Environment.Exit(1); }
    // verify all rows/cols/boxes contain 1..9
    bool Valid()
    {
        bool UnitOk(Func<int, (int, int)> f)
        {
            var seen = new bool[10];
            for (var i = 0; i < 9; i++) { var (a, b) = f(i); var v = cp[a, b]; if (v < 1 || v > 9 || seen[v]) return false; seen[v] = true; }
            return true;
        }
        for (var i = 0; i < 9; i++)
            if (!UnitOk(r => (i, r)) || !UnitOk(c => (c, i))) return false; // row, col
        for (var by = 0; by < 9; by += 3) for (var bx = 0; bx < 9; bx += 3)
            if (!UnitOk(k => (by + k / 3, bx + k % 3))) return false; // box
        return true;
    }
    Console.Error.WriteLine($"solved=ok valid={Valid()}");
    return;
}

Solve(puzzle);
for (var y = 0; y < 9; y++) { for (var x = 0; x < 9; x++) Console.Write(puzzle[y, x] + " "); Console.WriteLine(); }
