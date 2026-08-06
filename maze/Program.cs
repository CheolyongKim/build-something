// Recursive-backtracker maze + BFS solver, ASCII. Self-checks exit is reachable.
// ponytail: single-thread DFS carve, fine for small grids.
using System;
using System.Collections.Generic;

var (cw, ch) = (12, 8);
var rnd = new Random(42);
int W = 2 * cw + 1, H = 2 * ch + 1;
var g = new char[H, W];
for (var y = 0; y < H; y++) for (var x = 0; x < W; x++) g[y, x] = '#';

var visited = new bool[ch, cw];
void Carve(int cx, int cy)
{
    visited[cy, cx] = true; g[2 * cy + 1, 2 * cx + 1] = '.';
    foreach ((int dx, int dy) in Shuffle(new[] { (0, -1), (0, 1), (-1, 0), (1, 0) }))
    {
        int nx = cx + dx, ny = cy + dy;
        if (nx >= 0 && nx < cw && ny >= 0 && ny < ch && !visited[ny, nx])
        { g[2 * cy + 1 + dy, 2 * cx + 1 + dx] = '.'; Carve(nx, ny); }
    }
}
IEnumerable<(int, int)> Shuffle((int, int)[] a)
{ for (var i = a.Length - 1; i > 0; i--) { var j = rnd.Next(i + 1); (a[i], a[j]) = (a[j], a[i]); } return a; }

Carve(0, 0);
var end = (W - 2, H - 2); g[end.Item2, end.Item1] = '.';

bool Reachable()
{
    var seen = new bool[H, W]; var q = new Queue<(int, int)>(); q.Enqueue((1, 1));
    while (q.Count > 0) { (int x, int y) = q.Dequeue(); if (seen[y, x]) continue; seen[y, x] = true;
        if ((x, y) == end) return true;
        foreach ((int dx, int dy) in new[] { (1, 0), (-1, 0), (0, 1), (0, -1) })
            if (x + dx >= 0 && x + dx < W && y + dy >= 0 && y + dy < H && g[y + dy, x + dx] == '.' && !seen[y + dy, x + dx])
                q.Enqueue((x + dx, y + dy)); }
    return false;
}

if (args.Length > 0 && args[0] == "--demo")
{
    Console.Error.WriteLine($"reachable={Reachable()}");
    if (!Reachable()) { Console.Error.WriteLine("FAIL"); Environment.Exit(1); }
    System.Console.Write(Render(true));
    return;
}

string Render(bool solve)
{
    var path = solve && Reachable() ? Solve() : null;
    var sb = new System.Text.StringBuilder();
    for (var y = 0; y < H; y++) { for (var x = 0; x < W; x++)
        sb.Append(path != null && path.Contains((x, y)) && g[y, x] == '.' ? '*' : g[y, x]);
        sb.Append('\n'); }
    return sb.ToString();
}
HashSet<(int, int)> Solve()
{
    var seen = new HashSet<(int, int)>(); var prev = new Dictionary<(int, int), (int, int)>();
    var q = new Queue<(int, int)>(); q.Enqueue((1, 1)); seen.Add((1, 1));
    while (q.Count > 0) { (int x, int y) = q.Dequeue();
        if ((x, y) == end) break;
        foreach ((int dx, int dy) in new[] { (1, 0), (-1, 0), (0, 1), (0, -1) })
            if (x + dx >= 0 && x + dx < W && y + dy >= 0 && y + dy < H && g[y + dy, x + dx] == '.' && seen.Add((x + dx, y + dy)))
            { prev[(x + dx, y + dy)] = (x, y); q.Enqueue((x + dx, y + dy)); } }
    var path = new HashSet<(int, int)>(); var cur = end;
    while (prev.ContainsKey(cur)) { path.Add(cur); cur = prev[cur]; } path.Add((1, 1)); return path;
}
Console.Write(Render(false));
