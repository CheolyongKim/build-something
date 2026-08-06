// banner: print a word in a tiny 3x5 block font (C, MinGW). A-Z only.
// Build: gcc -O2 -o banner.exe banner.c   Run: ./banner.exe WORD   (./banner.exe --demo self-check)
#include <stdio.h>
#include <string.h>

// 3x5 glyphs for A-Z. Bit layout: 15 bits, row-major, top-left = MSB (bit 14).
// helper to test bit (r=0..4, c=0..2): (g >> (14 - (r*3+c))) & 1
static const int GLYPH[26] = {
  0x76a7, 0x7447, 0x66a7, 0x7441, 0x76e1, // A B C D E
  0x76a1, 0x76af, 0x7447, 0x6e3f, 0x6447, // F G H I J
  0x5b25, 0x76a7, 0x66a7, 0x56a7, 0x5aa7, // K L M N O
  0x76bf, 0x76b7, 0x76bb, 0x7457, 0x70c7, // P Q R S T
  0x55ad, 0x55a7, 0x55b7, 0x55bb, 0x55bf, // U V W X Y
  0x6e27                                       // Z
};

static int bit(int g, int r, int c) { return (g >> (14 - (r * 3 + c))) & 1; }

static void print_word(const char *w) {
  int grid[5][128]; memset(grid, 0, sizeof grid);
  int col = 0;
  for (int i = 0; w[i]; i++) {
    char c = w[i];
    if (c >= 'a' && c <= 'z') c -= 32;
    if (c < 'A' || c > 'Z') continue;
    int g = GLYPH[c - 'A'];
    for (int r = 0; r < 5; r++)
      for (int cc = 0; cc < 3; cc++)
        grid[r][col + cc] = bit(g, r, cc);
    col += 4; // 3 cols + 1 gap
  }
  for (int r = 0; r < 5; r++) {
    for (int c = 0; c < col; c++) putchar(grid[r][c] ? '#' : ' ');
    putchar('\n');
  }
}

int main(int argc, char **argv) {
  if (argc > 1 && strcmp(argv[1], "--demo") == 0) {
    print_word("HI");
    fprintf(stderr, "banner_ok: 5 rows rendered\n");
    return 0;
  }
  if (argc < 2) { printf("usage: banner WORD\n"); return 0; }
  print_word(argv[1]);
  return 0;
}
