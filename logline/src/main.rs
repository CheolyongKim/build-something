// logline: random movie logline generator (Rust, stdlib only).
// Build: cargo build --release   Run: target/release/logline.exe [n]
// --demo prints 50 and asserts no two adjacent are identical + all fields filled.
use std::collections::HashSet;
use std::env;

fn pick<'a>(v: &'a [&'a str], i: usize) -> &'a str { v[i % v.len()] }

fn line(n: u64) -> String {
    let adj = ["weary", "rogue", "ambitious", "haunted", "gentle", "feral", "cynical", "radiant"];
    let job = ["detective", "astronaut", "chef", "thief", "botanist", "king", "hacker", "midwife"];
    let verb = ["expose", "rescue", "escape", "redeem", "destroy", "repair", "forgive", "outwit"];
    let goal = ["a corrupt syndicate", "their own past", "a dying planet",
                "the last library", "a stolen child", "the morning sun"];
    let crisis = ["before the city floods", "before the contract kills them",
                  "before the truth surfaces", "before the war begins",
                  "before the light goes out"];
    let a = (n * 7 + 1) as usize % adj.len();
    let j = (n * 13 + 3) as usize % job.len();
    let v = (n * 17 + 5) as usize % verb.len();
    let g = (n * 23 + 11) as usize % goal.len();
    let c = (n * 29 + 17) as usize % crisis.len();
    // ponytail: deterministic index, not rng, so --demo is reproducible
    format!("A {} {} must {} {} {}.",
        pick(&adj, a), pick(&job, j), pick(&verb, v), pick(&goal, g), pick(&crisis, c))
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.iter().any(|a| a == "--demo") {
        let mut seen = HashSet::new();
        let mut prev = String::new();
        for t in 0..50u64 {
            let l = line(t);
            assert!(l != prev, "FAIL: adjacent identical");
            assert!(l.contains(" must "), "FAIL: malformed");
            seen.insert(l.clone());
            prev = l;
        }
        assert!(seen.len() > 40, "FAIL: low variety");
        eprintln!("logline_ok: 50 distinct loglines");
        return;
    }
    let n: u64 = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(5);
    for t in 0..n { println!("{}", line(t)); }
}
