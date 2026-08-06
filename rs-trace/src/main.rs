// rs-trace: minimal ASCII raytracer — a shaded sphere, no deps (std only).
// Build: cargo build --release --target x86_64-pc-windows-gnu
// Run:   ./target/x86_64-pc-windows-gnu/release/rs-trace [frames]
// Renders `frames` ASCII frames of a rotating sphere (Lambert + rim).
const W: usize = 40;
const H: usize = 18;

fn frame(t: f64) -> String {
    let mut out = String::new();
    let light: [f64; 3] = [-0.5, 0.6, 0.8]; // direction toward light (in front of sphere)
    let lnorm = (light[0]*light[0] + light[1]*light[1] + light[2]*light[2]).sqrt();
    let l = [light[0]/lnorm, light[1]/lnorm, light[2]/lnorm];
    let ay = t * 0.6; // rotation angle about Y
    let (sy, cy) = ay.sin_cos();
    const CHARS: [char; 10] = ['.', ',', ':', ';', '+', '*', 'o', 'O', '#', '@'];
    for y in 0..H {
        let py = 1.0 - 2.0 * (y as f64 + 0.5) / H as f64; // -1..1
        for x in 0..W {
            let px = 2.0 * (x as f64 + 0.5) / W as f64 - 1.0; // -aspect..aspect
            let px = px * (W as f64 / H as f64);
            // ray from camera (0,0,3) toward (px,py,0)
            let ro = [0.0, 0.0, 3.0];
            let rd = [px - ro[0], py - ro[1], -3.0 - ro[2]];
            let rdn = (rd[0]*rd[0] + rd[1]*rd[1] + rd[2]*rd[2]).sqrt();
            let rd = [rd[0]/rdn, rd[1]/rdn, rd[2]/rdn];
            // intersect unit sphere at origin
            let b = ro[0]*rd[0] + ro[1]*rd[1] + ro[2]*rd[2];
            let c = ro[0]*ro[0] + ro[1]*ro[1] + ro[2]*ro[2] - 1.0;
            let disc = b*b - c;
            if disc < 0.0 { out.push(' '); continue; }
            let dist = -b - disc.sqrt();
            // hit point
            let hx = ro[0] + rd[0]*dist;
            let hy = ro[1] + rd[1]*dist;
            let hz = ro[2] + rd[2]*dist;
            // rotate normal about Y by -ay to get world normal (sphere fixed, light fixed)
            let nx = hx*cy + hz*sy;
            let nz = -hx*sy + hz*cy;
            let n = [nx, hy, nz];
            let nlen = (n[0]*n[0]+n[1]*n[1]+n[2]*n[2]).sqrt();
            let diff = (n[0]*l[0] + n[1]*l[1] + n[2]*l[2]) / nlen;
            let shade = if diff < 0.0 { 0.0 } else { diff };
            let rim = 1.0 - (hx*hx + hy*hy + hz*hz); // brighter near silhouette
            let v = (shade * 0.85 + rim.max(0.0) * 0.25).clamp(0.0, 0.999);
            out.push(CHARS[(v * (CHARS.len() as f64)) as usize]);
        }
        out.push('\n');
    }
    out
}

fn main() {
    let frames: usize = std::env::args().nth(1).and_then(|s| s.parse().ok()).unwrap_or(1);
    for i in 0..frames {
        let t = i as f64 * 0.25;
        print!("{}", frame(t));
        if i + 1 < frames { print!("\x1b[{}A", H); } // rewind cursor for animation
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn renders_full_frame() {
        let f = frame(0.0);
        assert_eq!(f.lines().count(), H);
        assert!(f.contains('@') || f.contains('#')); // lit pixels exist
    }
}
