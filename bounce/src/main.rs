// bounce: a logo bounces around the terminal (Rust, stdlib, ANSI).
// Build: cargo build --release   Run: target/release/bounce.exe [frames] [w] [h]
//   target/release/bounce.exe --demo   self-check: position stays in bounds + flips at walls
use std::env;

struct Ball { x: i32, y: i32, dx: i32, dy: i32 }

fn step(b: &mut Ball, w: i32, h: i32) {
    b.x += b.dx; b.y += b.dy;
    if b.x <= 0 || b.x >= w - 1 { b.dx = -b.dx; b.x = b.x.clamp(0, w - 1); }
    if b.y <= 0 || b.y >= h - 1 { b.dy = -b.dy; b.y = b.y.clamp(0, h - 1); }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.iter().any(|a| a == "--demo") {
        let (w, h) = (20, 10);
        let mut b = Ball { x: 5, y: 5, dx: 1, dy: 1 };
        let mut flips = 0;
        for _ in 0..500 {
            step(&mut b, w, h);
            if b.x < 0 || b.x >= w || b.y < 0 || b.y >= h {
                eprintln!("FAIL: out of bounds"); std::process::exit(1);
            }
            if (b.x == 0 || b.x == w - 1) || (b.y == 0 || b.y == h - 1) { flips += 1; }
        }
        if flips < 2 { eprintln!("FAIL: never hit a wall"); std::process::exit(1); }
        eprintln!("bounce_ok: stayed in bounds, bounced {} times", flips);
        return;
    }
    let n: i32 = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(200);
    let w: i32 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(40);
    let h: i32 = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(12);
    let mut b = Ball { x: w / 2, y: h / 2, dx: 1, dy: 1 };
    for _ in 0..n {
        let mut grid = vec![vec![' '; w as usize]; h as usize];
        grid[b.y as usize][b.x as usize] = '@';
        print!("\x1b[2J\x1b[H");
        for row in &grid { println!("{}", row.iter().collect::<String>()); }
        step(&mut b, w, h);
        std::thread::sleep(std::time::Duration::from_millis(60));
    }
}
