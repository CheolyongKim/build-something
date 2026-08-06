// tictactoe: play vs a perfect minimax AI in the terminal (Go, stdlib only).
// Build: go build -o tictactoe.exe .   Run: ./tictactoe.exe        (./tictactoe.exe --demo)
// You are X, AI is O and moves second; AI never loses.
package main

import (
	"fmt"
	"math/rand"
	"os"
	"strconv"
)

// board: 9 cells, 0=empty,1=X,2=O.  AI is O (2).
func winner(b [9]int) int { // returns 1,2 or 0 (none yet), -1 (draw)
	lines := [8][3]int{{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6}}
	for _, l := range lines {
		if b[l[0]] != 0 && b[l[0]] == b[l[1]] && b[l[1]] == b[l[2]] {
			return b[l[0]]
		}
	}
	for _, c := range b {
		if c == 0 {
			return 0
		}
	}
	return -1
}

// minimax: AI=O(2) maximizes for 2. Returns score: +10-d (win), -10+d (loss), 0 draw.
func minimax(b [9]int, player, depth int) int {
	w := winner(b)
	switch {
	case w == 2:
		return 10 - depth
	case w == 1:
		return depth - 10
	case w == -1:
		return 0
	}
	best := -1000
	if player == 2 {
		best = -1000
		for i := 0; i < 9; i++ {
			if b[i] == 0 {
				b[i] = 2
				s := minimax(b, 1, depth+1)
				if s > best {
					best = s
				}
				b[i] = 0
			}
		}
		return best
	}
	best = 1000
	for i := 0; i < 9; i++ {
		if b[i] == 0 {
			b[i] = 1
			s := minimax(b, 2, depth+1)
			if s < best {
				best = s
			}
			b[i] = 0
		}
	}
	return best
}

func aiMove(b [9]int) int {
	best, mv := -1000, -1
	for i := 0; i < 9; i++ {
		if b[i] == 0 {
			b[i] = 2
			s := minimax(b, 1, 1)
			b[i] = 0
			if s > best {
				best, mv = s, i
			}
		}
	}
	return mv
}

func render(b [9]int) {
	g := map[int]string{0: ".", 1: "X", 2: "O"}
	for r := 0; r < 3; r++ {
		fmt.Printf(" %s %s %s\n", g[b[r*3]], g[b[r*3+1]], g[b[r*3+2]])
	}
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--demo" {
		// AI (as O, second) must never lose across many random player openings
		rng := rand.New(rand.NewSource(1))
		for g := 0; g < 200; g++ {
			var b [9]int
			turn := 1 // X first
			for {
				w := winner(b)
				if w != 0 {
					if w == 1 {
						fmt.Println("FAIL: AI lost")
						os.Exit(1)
					}
					break
				}
				if turn == 1 {
					// random legal X move
					var empties []int
					for i := 0; i < 9; i++ {
						if b[i] == 0 {
							empties = append(empties, i)
						}
					}
					if len(empties) == 0 {
						break
					}
					b[empties[rng.Intn(len(empties))]] = 1
					turn = 2
				} else {
					b[aiMove(b)] = 2
					turn = 1
				}
			}
		}
		fmt.Println("tictactoe_ok: AI never lost in 200 random games")
		return
	}

	var b [9]int
	turn := 1
	for {
		render(b)
		w := winner(b)
		if w != 0 {
			if w == 1 {
				fmt.Println("You win!")
			} else if w == 2 {
				fmt.Println("AI wins.")
			} else {
				fmt.Println("Draw.")
			}
			return
		}
		if turn == 1 {
			fmt.Print("your move (0-8): ")
			var s string
			fmt.Scanln(&s)
			i, err := strconv.Atoi(s)
			if err != nil || i < 0 || i > 8 || b[i] != 0 {
				fmt.Println("bad move")
				continue
			}
			b[i] = 1
			turn = 2
		} else {
			b[aiMove(b)] = 2
			turn = 1
		}
	}
}
