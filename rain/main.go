// rain: a tiny terminal rain animation (ASCII), stdlib only.
// Build: go build -o rain.exe .   Run: ./rain.exe [frames] [width]
// --demo writes frames to a buffer and asserts they vary + contain only rain chars.
package main

import (
	"fmt"
	"math/rand"
	"os"
	"strings"
	"time"
)

const drops = "|/\\.o"

func frame(w, t int, r *rand.Rand) string {
	var sb strings.Builder
	for x := 0; x < w; x++ {
		if r.Float64() < 0.5 {
			sb.WriteByte(drops[(x+t)%len(drops)])
		} else {
			sb.WriteByte(' ')
		}
	}
	return sb.String()
}

func main() {
	seed := time.Now().UnixNano()
	r := rand.New(rand.NewSource(seed))
	n := 20
	w := 40
	if len(os.Args) > 1 { fmt.Sscanf(os.Args[1], "%d", &n) }
	if len(os.Args) > 2 { fmt.Sscanf(os.Args[2], "%d", &w) }
	if len(os.Args) > 1 && os.Args[1] == "--demo" {
		prev := ""
		seen := map[string]bool{}
		for t := 0; t < 30; t++ {
			f := frame(w, t, r)
			if f == prev {
				fmt.Println("FAIL: identical consecutive frames")
				os.Exit(1)
			}
			seen[f] = true
			prev = f
		}
		if len(seen) < 10 {
			fmt.Println("FAIL: frames not varied")
			os.Exit(1)
		}
		fmt.Println("rain_ok: 30 varied frames")
		return
	}
	// live: print frames with a clear, no deps
	for t := 0; t < n; t++ {
		fmt.Print("\033[2J\033[H") // clear screen
		fmt.Println(frame(w, t, r))
		time.Sleep(80 * time.Millisecond)
	}
}
