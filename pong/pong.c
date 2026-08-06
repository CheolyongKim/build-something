// pong: tiny terminal pong (C, MinGW, conio.h). Left paddle = W/S, right = arrows.
// Build: gcc -O2 -o pong.exe pong.c   Run: ./pong.exe   (./pong.exe --demo self-check)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <conio.h>
#include <windows.h>

#define W 60
#define H 20

static int ball_x, ball_y, vel_x, vel_y;
static int lp, rp;            // paddle centers (left, right)
static int lsc, rsc;

static unsigned s;
static int rnd(int n) { s = s * 1103515245u + 12345u; return (int)((s / 65536u) % n); }

static void reset(void) {
    ball_x = W / 2; ball_y = H / 2;
    vel_x = (rnd(2) ? 1 : -1);
    vel_y = (rnd(2) ? 1 : -1);
}

static void render(void) {
    printf("\x1b[2J\x1b[H");
    for (int y = 0; y < H; y++) {
        for (int x = 0; x < W; x++) {
            if (x == 0 || x == W - 1) { putchar('|'); continue; }
            if (y == 0 || y == H - 1) { putchar('-'); continue; }
            if (x == 2 && abs(y - lp) <= 2) { putchar('#'); continue; }
            if (x == W - 3 && abs(y - rp) <= 2) { putchar('#'); continue; }
            if (x == ball_x && y == ball_y) { putchar('@'); continue; }
            putchar(' ');
        }
        putchar('\n');
    }
    printf("L %d : %d R   (W/S left, arrows right)\n", lsc, rsc);
}

static void tick(int ldir, int rdir) {
    lp += ldir; rp += rdir;
    if (lp < 2) lp = 2; if (lp > H - 3) lp = H - 3;
    if (rp < 2) rp = 2; if (rp > H - 3) rp = H - 3;
    ball_x += vel_x; ball_y += vel_y;
    if (ball_y <= 1) { ball_y = 1; vel_y = -vel_y; }
    if (ball_y >= H - 2) { ball_y = H - 2; vel_y = -vel_y; }
    // paddle collisions
    if (ball_x == 3 && abs(ball_y - lp) <= 2) { vel_x = -vel_x; ball_x = 3; }
    if (ball_x == W - 4 && abs(ball_y - rp) <= 2) { vel_x = -vel_x; ball_x = W - 4; }
    if (ball_x <= 0) { rsc++; reset(); }
    if (ball_x >= W - 1) { lsc++; reset(); }
}

int main(int argc, char **argv) {
    if (argc > 1 && strcmp(argv[1], "--demo") == 0) {
        s = 1; reset();
        // simulate 2000 ticks with a centered paddle; ball must stay in bounds,
        // and a point should eventually be scored (one of the paddles misses).
        lp = rp = H / 2;
        int scored = 0;
        for (int t = 0; t < 2000; t++) {
            tick(0, 0);
            if (ball_x < 0 || ball_x > W - 1 || ball_y < 0 || ball_y > H - 1) {
                fprintf(stderr, "FAIL: ball out of bounds\n"); return 1;
            }
            if (lsc + rsc > 0) { scored = 1; break; }
        }
        if (!scored) { fprintf(stderr, "FAIL: no score in 2000 ticks\n"); return 1; }
        fprintf(stderr, "pong_ok: ball bounded, scored (L%d R%d)\n", lsc, rsc);
        return 0;
    }
    s = (unsigned)time(0);
    reset(); lp = rp = H / 2;
    while (lsc < 5 && rsc < 5) {
        int ldir = 0, rdir = 0;
        if (kbhit()) {
            int c = getch();
            if (c == 224 || c == 0) c = getch();
            if (c == 'w' || c == 'W') ldir = -1;
            else if (c == 's' || c == 'S') ldir = 1;
            else if (c == 'H') rdir = -1;
            else if (c == 'P') rdir = 1;
        }
        // crude right-paddle AI: track the ball
        if (ball_y < rp) rdir = -1; else if (ball_y > rp) rdir = 1;
        tick(ldir, rdir);
        render();
        Sleep(50);
    }
    printf("game over: L %d : %d R\n", lsc, rsc);
    return 0;
}
