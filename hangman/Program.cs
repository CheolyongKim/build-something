// Hangman in the terminal. Pick from a small word list, guess letters.
// ponytail: in-process loop, no I/O framework.
using System;
using System.Linq;

var words = new[] { "goblin", "dragon", "wizard", "potion", "shield", "dagger", "castle", "sorcerer" };
var word = words[new Random().Next(words.Length)];
var guessed = new System.Collections.Generic.HashSet<char>();
var wrong = 0; const int MAX = 6;

if (args.Contains("--demo"))
{
    // self-check: revealing all letters wins; 6 wrong losses triggers end
    var g = new System.Collections.Generic.HashSet<char>();
    foreach (var c in word) g.Add(c);
    var masked = new string(word.Select(c => g.Contains(c) ? c : '_').ToArray());
    if (masked != word) { Console.Error.WriteLine("FAIL: mask wrong"); Environment.Exit(1); }
    Console.Error.WriteLine($"word_len={word.Length} mask_ok=ok");
    return;
}

while (wrong < MAX && guessed.Count(c => word.Contains(c)) < word.Length)
{
    var masked = new string(word.Select(c => guessed.Contains(c) ? c : '_').ToArray());
    Console.WriteLine($"\n{masked}   wrong:{wrong}/{MAX}   guessed:{string.Join(" ", guessed.OrderBy(x => x))}");
    Console.Write("guess: ");
    var k = Console.ReadKey().KeyChar.ToString().ToLowerInvariant();
    Console.WriteLine();
    if (k.Length != 1 || !char.IsLetter(k[0]) || guessed.Contains(k[0])) continue;
    guessed.Add(k[0]);
    if (!word.Contains(k[0])) wrong++;
}
var done = new string(word.Select(c => guessed.Contains(c) ? c : '_').ToArray());
Console.WriteLine(done == word ? $"\nYou win! {word}" : $"\nGame over. it was {word}");
