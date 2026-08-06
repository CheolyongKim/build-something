// Procedural ASCII dungeon generator. Seeded RNG so output is reproducible.
// ponytail: rooms-first + corridor carve, no room overlap check (ceiling: rare overlaps ok).
using System;
using System.Text;

var seed = args.Length > 0 && int.TryParse(args[0], out var s) ? s : 1337;
var rnd = new Random(seed);
const int W = 48, H = 24, Rooms = 7;

var grid = new char[H, W];
for (var y = 0; y < H; y++) for (var x = 0; x < W; x++) grid[y, x] = '#';

var rects = new (int x, int y, int w, int h)[Rooms];
for (var i = 0; i < Rooms; i++)
{
    var w = rnd.Next(4, 10); var h = rnd.Next(3, 7);
    var x = rnd.Next(1, W - w - 1); var y = rnd.Next(1, H - h - 1);
    rects[i] = (x, y, w, h);
    for (var yy = y; yy < y + h; yy++) for (var xx = x; xx < x + w; xx++) grid[yy, xx] = '.';
}

// carve L-shaped corridors between consecutive room centers
for (var i = 1; i < Rooms; i++)
{
    var (ax, ay) = Center(rects[i - 1]); var (bx, by) = Center(rects[i]);
    for (var x = Math.Min(ax, bx); x <= Math.Max(ax, bx); x++) grid[ay, x] = '.';
    for (var y = Math.Min(ay, by); y <= Math.Max(ay, by); y++) grid[y, bx] = '.';
}
(int, int) Center((int x, int y, int w, int h) r) => (r.x + r.w / 2, r.y + r.h / 2);

var sb = new StringBuilder();
for (var y = 0; y < H; y++) { for (var x = 0; x < W; x++) sb.Append(grid[y, x]); sb.Append('\n'); }

if (args.Contains("--demo"))
{
    var empty = 0; for (var y = 0; y < H; y++) for (var x = 0; x < W; x++) if (grid[y, x] == '.') empty++;
    Console.Error.WriteLine($"rooms={Rooms} floor_tiles={empty}");
    // self-check: every room center is reachable from room0 center (flood)
    var seen = new bool[H, W]; var q = new Queue<(int, int)>(); q.Enqueue(Center(rects[0]));
    while (q.Count > 0) { var (cx, cy) = q.Dequeue(); if (seen[cy, cx]) continue; seen[cy, cx] = true;
        foreach (var (dx, dy) in new[] { (1, 0), (-1, 0), (0, 1), (0, -1) })
            if (cx + dx >= 0 && cx + dx < W && cy + dy >= 0 && cy + dy < H && grid[cy + dy, cx + dx] == '.' && !seen[cy + dy, cx + dx])
                q.Enqueue((cx + dx, cy + dy)); }
    var roomsReached = rects.Count(r => seen[Center(r).Item2, Center(r).Item1]);
    Console.Error.WriteLine($"rooms_reachable={roomsReached}/{Rooms}");
    if (roomsReached != Rooms) { Console.Error.WriteLine("FAIL: disconnected dungeon"); Environment.Exit(1); }
}
Console.Write(sb);

// build: dotnet run --project dungeon -- --demo  (or pass a seed)
