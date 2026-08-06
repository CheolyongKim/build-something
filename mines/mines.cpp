// mines: tiny terminal Minesweeper (C++, g++).
// Build: g++ -O2 -o mines.exe mines.cpp   Run: ./mines.exe [w] [h] [mines] [seed]
//   ./mines.exe --demo   self-check: mine count + flood reveal correctness
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <vector>

struct Game {
    int w, h, m;
    std::vector<int> mine;   // 1 if mine
    std::vector<int> adj;    // adjacent mine count
    std::vector<int> rev;    // 1 if revealed
    unsigned seed;
    int rnd() { seed = seed * 1103515245u + 12345u; return (int)(seed / 65536u) % 32768; }

    Game(int w_, int h_, int m_, unsigned s) : w(w_), h(h_), m(m_),
        mine(w_*h_,0), adj(w_*h_,0), rev(w_*h_,0), seed(s) {}

    void place() {
        int placed = 0, cells = w*h;
        while (placed < m && placed < cells) {
            int i = rnd() % cells;
            if (!mine[i]) { mine[i] = 1; placed++; }
        }
        for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) {
            int c = 0;
            for (int dy=-1; dy<=1; dy++) for (int dx=-1; dx<=1; dx++) {
                int nx=x+dx, ny=y+dy;
                if (nx<0||ny<0||nx>=w||ny>=h) continue;
                if (dx==0&&dy==0) continue;
                if (mine[ny*w+nx]) c++;
            }
            adj[y*w+x] = c;
        }
    }

    void flood(int x, int y) {
        if (x<0||y<0||x>=w||y>=h) return;
        int i = y*w+x;
        if (rev[i] || mine[i]) return;
        rev[i] = 1;
        if (adj[i] == 0) {
            flood(x-1,y); flood(x+1,y); flood(x,y-1); flood(x,y+1);
        }
    }

    void render() {
        for (int y=0; y<h; y++) {
            for (int x=0; x<w; x++) {
                int i=y*w+x;
                if (rev[i]) putchar(mine[i] ? '*' : (adj[i] ? '0'+adj[i] : '.'));
                else putchar('#');
            }
            putchar('\n');
        }
    }
};

int main(int argc, char** argv) {
    bool demo = (argc>1 && strcmp(argv[1],"--demo")==0);
    if (demo) {
        Game g(10, 10, 12, 7);
        g.place();
        int mc = 0; for (int i=0;i<g.w*g.h;i++) mc += g.mine[i];
        if (mc != 12) { fprintf(stderr,"FAIL mine count %d\n", mc); return 1; }
        // find an empty, zero-adjacent cell and flood; expect a spill (>=2 revealed)
        int zi = -1;
        for (int i=0;i<g.w*g.h;i++) if (!g.mine[i] && g.adj[i]==0) { zi=i; break; }
        if (zi<0) { fprintf(stderr,"FAIL no zero cell\n"); return 1; }
        g.flood(zi%g.w, zi/g.w);
        int revealed = 0; for (int i=0;i<g.w*g.h;i++) revealed += g.rev[i];
        if (revealed < 2) { fprintf(stderr,"FAIL flood\n"); return 1; }
        fprintf(stderr,"mines_ok: count=%d flood_revealed=%d\n", mc, revealed);
        return 0;
    }
    int w = argc>1 ? atoi(argv[1]) : 10;
    int h = argc>2 ? atoi(argv[2]) : 10;
    int m = argc>3 ? atoi(argv[3]) : 12;
    unsigned s = argc>4 ? (unsigned)atoi(argv[4]) : (unsigned)time(0);
    Game g(w,h,m,s); g.place();
    int revealed = 0, safe = w*h - m;
    char line[32];
    while (revealed < safe) {
        g.render();
        printf("enter x y (or q): ");
        if (!fgets(line, sizeof(line), stdin)) break;
        if (line[0]=='q'||line[0]=='Q') break;
        int x,y; if (sscanf(line,"%d %d",&x,&y)!=2) continue;
        if (x<0||y<0||x>=w||y>=h) continue;
        int i = y*w+x;
        if (g.mine[i]) { g.rev[i]=1; g.render(); printf("BOOM. game over.\n"); return 0; }
        if (!g.rev[i]) { g.flood(x,y); }
        revealed = 0; for (int k=0;k<w*h;k++) revealed += g.rev[k];
    }
    g.render();
    printf("You cleared the board! mines=%d\n", m);
    return 0;
}
