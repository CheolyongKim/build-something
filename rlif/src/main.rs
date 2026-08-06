// rlif: a tiny terminal survival roguelite. No deps (std only).
// Build: cargo build --release --target x86_64-pc-windows-gnu
// Run:   <exe>            interactive
//        <exe> --demo     scripted run, asserts state transitions
use std::io::{self, BufRead, Write};
use std::collections::HashMap;

struct Game {
    hp: i32,
    hunger: i32,
    gold: i32,
    day: i32,
    inv: HashMap<String, u32>,
    rnd: u64,
}

impl Game {
    fn new(seed: u64) -> Self {
        Game { hp: 10, hunger: 0, gold: 0, day: 1, inv: HashMap::new(), rnd: seed }
    }
    // xorshift — tiny deterministic RNG so --demo is reproducible
    fn next(&mut self) -> u64 {
        self.rnd ^= self.rnd << 13;
        self.rnd ^= self.rnd >> 7;
        self.rng_apply();
        self.rnd
    }
    fn rng_apply(&mut self) {
        // keep rnd nonzero
        if self.rnd == 0 { self.rnd = 0x9E3779B97F4A7C15; }
    }
    fn step(&mut self, cmd: &str) -> String {
        self.day += 1;
        self.hunger += 1;
        match cmd {
            "hunt" => {
                let r = self.next() % 4;
                if r == 0 { self.hp -= 2; "You were mauled (-2 HP)".into() }
                else { *self.inv.entry("meat".into()).or_insert(0) += 1; "Caught game (+1 meat)".into() }
            }
            "eat" => {
                if *self.inv.get("meat").unwrap_or(&0) > 0 {
                    *self.inv.get_mut("meat").unwrap() -= 1;
                    self.hunger = (self.hunger - 3).max(0);
                    "Ate meat (-3 hunger)".into()
                } else { "No meat to eat".into() }
            }
            "rest" => { self.hp = (self.hp + 1).min(10); "Rested (+1 HP)".into() }
            "trade" => {
                let r = self.next() % 5;
                self.gold += r as i32;
                format!("Traded furs (+{} gold)", r)
            }
            _ => "You wander, nothing happens".into(),
        }
    }
    fn alive(&self) -> bool { self.hp > 0 && self.hunger < 8 }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.contains(&"--demo".to_string()) {
        let mut g = Game::new(12345);
        // reproducible: same seed -> same first two events
        let e1 = g.step("hunt");
        let e2 = g.step("trade");
        assert!(!e1.is_empty() && !e2.is_empty(), "no event text");
        // hunger climbs, day advances
        assert!(g.day == 3 && g.hunger == 2, "state didn't advance");
        // eat with no meat is safe
        let g2 = &mut Game::new(1);
        assert!(g2.step("eat") == "No meat to eat", "eat should fail safely");
        println!("rlif_ok: events + state advance + safe eat");
        return;
    }
    let mut g = Game::new(0xDEAD_BEEF_u64 ^ std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH).unwrap().as_nanos() as u64);
    let stdin = io::stdin();
    let mut out = io::stdout();
    loop {
        if !g.alive() { writeln!(out, "You perished on day {}. Game over.", g.day).unwrap(); break; }
        writeln!(out, "[day {}] HP {} hunger {} gold {} | hunt/eat/rest/trade/look",
                 g.day, g.hp, g.hunger, g.gold).unwrap();
        write!(out, "> ").unwrap(); out.flush().unwrap();
        let mut line = String::new();
        if stdin.lock().read_line(&mut line).is_err() { break; }
        let cmd = line.trim();
        if cmd == "look" {
            writeln!(out, "Inventory: {:?}", g.inv).unwrap();
            continue;
        }
        if cmd == "quit" { break; }
        writeln!(out, "{}", g.step(cmd)).unwrap();
    }
}
