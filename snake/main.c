// snake: terminal snake game (C, MinGW gcc, ANSI escape codes).
// Build: gcc -O2 -o snake.exe main.c   Run: ./snake.exe   (./snake.exe --demo for self-check)
// Play: arrow keys or WASD. Eat '@', avoid walls and yourself.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <conio.h>
#include <windows.h>

#define W 24
#define H 12
#define MAX (W * H)

typedef struct { int x, y; } Pt;

static Pt snake[MAX];
static int len;
static Pt food;
static int over;
static unsigned seed;

static int rnd(int n) { seed = seed * 1103515245u + 12345u; return (int)((seed / 65536u) % n); }

static void place_food(void) {
    int i, tries = 0;
    for (;;) {
        food.x = rnd(W); food.y = rnd(H);
        int on = 0;
        for (i = 0; i < len; i++)
            if (snake[i].x == food.x && snake[i].y == food.y) { on = 1; break; }
        if (!on) return;
        if (++tries > W * H) return;  // board full: no food
    }
}

// dir: 0 up, 1 right, 2 down, 3 left
static int dx[4] = {0, 1, 0, -1}, dy[4] = {-1, 0, 1, 0};

// advance one tick in `dir`; returns 1 if food was eaten
static int step(int dir) {
    if (over) return 0;
    int hx = snake[0].x + dx[dir], hy = snake[0].y + dy[dir];
    if (hx < 0 || hx >= W || hy < 0 || hy >= H) { over = 1; return 0; }
    int i;
    for (i = 1; i < len; i++)
        if (snake[i].x == hx && snake[i].y == hy) { over = 1; return 0; }
    int ate = (hx == food.x && hy == food.y);
    for (i = len; i > 0; i--) snake[i] = snake[i - 1];
    snake[0].x = hx; snake[0].y = hy;
    if (ate) { len++; place_food(); }
    return ate;
}

static void render(void) {
    printf("\033[2J\033[H");
    for (int y = 0; y < H; y++) {
        for (int x = 0; x < W; x++) {
            int ish = 0, isf = (food.x == x && food.y == y);
            for (int k = 0; k < len; k++)
                if (snake[k].x == x && snake[k].y == y) { ish = 1; break; }
            putchar(isf ? '@' : ish ? '#' : ' ');
        }
        putchar('\n');
    }
    printf("len=%d\n", len);
}

int main(int argc, char **argv) {
    int demo = (argc > 1 && strcmp(argv[1], "--demo") == 0);
    seed = demo ? 1u : (unsigned)time(0);
    len = 3;
    for (int i = 0; i < len; i++) { snake[i].x = W / 2; snake[i].y = H / 2 + i; }
    place_food();

    if (demo) {
        int dir = 0, ate = 0;  // ponytail: headless auto-steer, asserts invariants
        for (int t = 0; t < 600; t++) {
            // greedily pick the safe step that reduces Manhattan distance to food
            int best = -1, bestd = 1 << 30;
            for (int d = 0; d < 4; d++) {
                int nx = snake[0].x + dx[d], ny = snake[0].y + dy[d];
                if (nx < 0 || nx >= W || ny < 0 || ny >= H) continue;
                int hit = 0;
                for (int j = 1; j < len; j++)
                    if (snake[j].x == nx && snake[j].y == ny) { hit = 1; break; }
                if (hit) continue;
                int dist = abs(nx - food.x) + abs(ny - food.y);
                if (dist < bestd) { bestd = dist; best = d; }
            }
            if (best < 0) break;  // boxed in; stop early
            dir = best;
            if (snake[0].x < 0 || snake[0].x >= W || snake[0].y < 0 || snake[0].y >= H) {
                fprintf(stderr, "FAIL: out of bounds\n"); return 1;
            }
            if (len < 1 || len > MAX) { fprintf(stderr, "FAIL: bad length\n"); return 1; }
            if (!over) ate += step(dir);
        }
        if (ate < 1) { fprintf(stderr, "FAIL: snake never grew\n"); return 1; }
        fprintf(stderr, "snake_ok: 600 ticks, ate=%d len=%d\n", ate, len);
        return 0;
    }

    int dir = 1;  // start moving right
    while (!over) {
        if (kbhit()) {
            int c = getch();
            if (c == 224 || c == 0) c = getch();  // arrow prefix
            if (c == 'H' || c == 'w' || c == 'W') dir = 0;
            else if (c == 'M' || c == 'd' || c == 'D') dir = 1;
            else if (c == 'P' || c == 's' || c == 'S') dir = 2;
            else if (c == 'K' || c == 'a' || c == 'A') dir = 3;
        }
        step(dir);
        render();
        Sleep(80);
    }
    printf("game over (len=%d)\n", len);
    return 0;
}
