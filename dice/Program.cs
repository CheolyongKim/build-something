// Dice roller for tabletop/RPG. Usage:
//   dice roll 3d6          -> three six-sided dice
//   dice stat             -> 6 abilities, 4d6 drop lowest
//   dice adv d20          -> roll with advantage
//   dice dis d20          -> roll with disadvantage
// ponytail: stdlib RNG only.
using System;
using System.Linq;

var rnd = new Random();
int D(string spec) // "3d6" or "d20"
{
    var parts = spec.ToLower().Split('d');
    int n = parts[0] == "" ? 1 : int.Parse(parts[0]);
    int sides = int.Parse(parts[1]);
    return Enumerable.Range(0, n).Sum(_ => rnd.Next(1, sides + 1));
}
int Adv(string spec) => Math.Max(D(spec), D(spec));
int Dis(string spec) => Math.Min(D(spec), D(spec));

if (args.Contains("--demo"))
{
    foreach (var s in new[] { "d6", "d20", "3d6" })
    { var v = D(s); var (lo, hi) = (s.EndsWith("6") ? (1, 18) : s.EndsWith("20") ? (1, 20) : (1, 6)); if (v < lo || v > hi) { Console.Error.WriteLine("FAIL range"); Environment.Exit(1); } }
    Console.Error.WriteLine("range_ok=ok");
    return;
}

if (args.Length == 0) { Console.WriteLine("usage: dice roll 3d6 | stat | adv d20 | dis d20"); return; }
switch (args[0])
{
    case "roll": Console.WriteLine(D(args[1])); break;
    case "stat":
        for (var i = 0; i < 6; i++)
        {
            var rolls = Enumerable.Range(0, 4).Select(_ => rnd.Next(1, 7)).OrderBy(x => x).Skip(1).ToArray();
            Console.WriteLine($"{rolls.Sum()}  ({string.Join("+", rolls)} drop {rolls.Min()})");
        }
        break;
    case "adv": Console.WriteLine(Adv(args[1])); break;
    case "dis": Console.WriteLine(Dis(args[1])); break;
    default: Console.WriteLine("unknown command"); break;
}

if (args.Contains("--demo"))
{
    foreach (var s in new[] { "d6", "d20", "3d6" })
    { var v = D(s); var (lo, hi) = (s.EndsWith("6") ? (1, 18) : s.EndsWith("20") ? (1, 20) : (1, 6)); if (v < lo || v > hi) { Console.Error.WriteLine("FAIL range"); Environment.Exit(1); } }
    Console.Error.WriteLine("range_ok=ok");
}
