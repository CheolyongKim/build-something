// quiz: tiny terminal arithmetic quiz (Rust, stdlib). Reads your answers from stdin.
// Build: cargo build --release   Run: target/release/quiz.exe [n]
//   target/release/quiz.exe --demo   self-check: answer key is correct
use std::env;
use std::io::{self, BufRead, Write};

fn answer(a: i32, b: i32, op: u8) -> i32 {
    match op { 0 => a + b, 1 => a - b, 2 => a * b, _ => a + b }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.iter().any(|a| a == "--demo") {
        assert_eq!(answer(6, 7, 0), 13);
        assert_eq!(answer(9, 4, 1), 5);
        assert_eq!(answer(3, 5, 2), 15);
        eprintln!("quiz_ok: answer key correct");
        return;
    }
    let n: usize = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(5);
    let mut correct = 0usize;
    let mut seed: u64 = 12345;
    let mut rng = || { seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1); (seed >> 33) as i32 };
    let stdin = io::stdin();
    for i in 1..=n {
        let a = (rng() % 12).abs() + 1;
        let b = (rng() % 12).abs() + 1;
        let op = (rng() % 3).abs() as u8;
        let sym = ['+', '-', '*'][op as usize];
        print!("Q{}: {} {} {} = ", i, a, sym, b);
        let _ = io::stdout().flush();
        let mut line = String::new();
        stdin.lock().read_line(&mut line).ok();
        let got: i32 = line.trim().parse().unwrap_or(i32::MIN);
        if got == answer(a, b, op) {
            correct += 1;
            println!("  correct!");
        } else {
            println!("  nope, it was {}", answer(a, b, op));
        }
    }
    println!("score: {}/{}", correct, n);
}
