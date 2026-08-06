// Typing speed test in the terminal. Timed entry of a sample line -> WPM + accuracy.
// ponytail: uses Stopwatch; single sample, no file of texts needed.
using System;
using System.Diagnostics;
using System.Linq;

var sample = "the quick brown fox jumps over the lazy dog";
if (args.Contains("--demo"))
{
    var a = sample.Length; var b = sample.Split(' ').Length;
    if (a != 43 || b != 9) { Console.Error.WriteLine("FAIL: sample changed"); Environment.Exit(1); }
    Console.Error.WriteLine($"sample_len={a} words={b} ok");
    return;
}

Console.WriteLine(sample);
Console.Write("type it: ");
var sw = Stopwatch.StartNew();
var input = Console.ReadLine() ?? "";
sw.Stop();
var secs = sw.Elapsed.TotalSeconds;
var wpm = (input.Split(' ').Length / secs) * 60;
var correct = input.Where((c, i) => i < sample.Length && c == sample[i]).Count();
var acc = input.Length == 0 ? 0 : 100.0 * correct / Math.Max(input.Length, sample.Length);
Console.WriteLine($"\n{secs:F1}s  {wpm:F0} wpm  {acc:F0}% accuracy");
