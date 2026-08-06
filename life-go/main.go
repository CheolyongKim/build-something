// life: Conway's Game of Life in the terminal (Go, stdlib, ANSI).
// Build: go build -o life.exe .   Run: ./life.exe [gens] [w] [h]
//   ./life.exe --demo   self-check: a blinker oscillates with period 2
package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

func step(g [][]int) [][]int {
	h := len(g)
	w := len(g[0])
	ng := make([][]int, h)
	for y := range ng {
		ng[y] = make([]int, w)
	}
	for y := 0; y < h; y++ {
		for x := 0; x < w; x++ {
			n := 0
			for dy := -1; dy <= 1; dy++ {
				for dx := -1; dx <= 1; dx++ {
					if dx == 0 && dy == 0 {
						continue
					}
					ny, nx := y+dy, x+dx
					if ny < 0 || nx < 0 || ny >= h || nx >= w {
						continue
					}
					n += g[ny][nx]
				}
			}
			if g[y][x] == 1 && (n == 2 || n == 3) {
				ng[y][x] = 1
			} else if g[y][x] == 0 && n == 3 {
				ng[y][x] = 1
			}
		}
	}
	return ng
}

func same(a, b [][]int) bool {
	for y := range a {
		for x := range a[y] {
			if a[y][x] != b[y][x] {
				return false
			}
		}
	}
	return true
}

func blinker() [][]int {
	g := make([][]int, 5)
	for i := range g {
		g[i] = make([]int, 5)
	}
	g[2][1], g[2][2], g[2][3] = 1, 1, 1
	return g
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--demo" {
		g := blinker()
		g1 := step(g)
		g2 := step(g1)
		if same(g, g2) && !same(g, g1) {
			fmt.Println("life_ok: blinker has period 2")
		} else {
			fmt.Println("FAIL: blinker not period 2")
			os.Exit(1)
		}
		return
	}
	gens := 30
	w := 24
	h := 12
	if len(os.Args) > 1 {
		gens, _ = strconv.Atoi(os.Args[1])
	}
	if len(os.Args) > 2 {
		w, _ = strconv.Atoi(os.Args[2])
	}
	if len(os.Args) > 3 {
		h, _ = strconv.Atoi(os.Args[3])
	}
	// random seed
	g := make([][]int, h)
	for y := range g {
		g[y] = make([]int, w)
		for x := range g[y] {
			if (x*7+y*13)%5 == 0 {
				g[y][x] = 1
			}
		}
	}
	for i := 0; i < gens; i++ {
		fmt.Print("\x1b[2J\x1b[H")
		for y := 0; y < h; y++ {
			for x := 0; x < w; x++ {
				if g[y][x] == 1 {
					fmt.Print("#")
				} else {
					fmt.Print(" ")
				}
			}
			fmt.Println()
		}
		g = step(g)
		time.Sleep(100 * time.Millisecond)
	}
}
