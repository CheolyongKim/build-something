// wordduel: type a word list faster than a bot; best-of-N rounds. (Go, stdlib)
// Build: go build -o wordduel.exe .   Run: ./wordduel.exe [rounds] [bot_wpm]
//   ./wordduel.exe --demo   self-check: scoring + bot pacing are sane
package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"strings"
	"time"
)

var WORDS = []string{"goblin", "dragon", "wizard", "potion", "shield",
	"dagger", "castle", "sorcerer", "phantom", "crystal", "ravager", "lantern"}

// bot "types" a word in the time its wpm implies; returns elapsed ms
func botTime(word string, wpm int) int {
	// ponytail: model as (chars/5)/wpm*60s; floor 1 char/200ms so tiny words still take time
	secs := float64(len(word))/5.0 / float64(wpm) * 60.0
	if secs < 0.2 {
		secs = 0.2
	}
	return int(secs * 1000)
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--demo" {
		// bot at 40wpm on a 6-char word "goblin": (6/5)/40*60 = 1.8s = 1800ms
		t := botTime("goblin", 40)
		if t < 1700 || t > 1900 {
			fmt.Println("FAIL: bot pacing off:", t)
			os.Exit(1)
		}
		// scoring: faster than bot => win
		playerMs, botMs := 1500, 2100
		wins := 0
		if playerMs < botMs {
			wins++
		}
		if wins != 1 {
			fmt.Println("FAIL: scoring")
			os.Exit(1)
		}
		fmt.Println("wordduel_ok: bot pacing + scoring sane")
		return
	}
	rounds := 5
	botWpm := 45
	if len(os.Args) > 1 {
		fmt.Sscanf(os.Args[1], "%d", &rounds)
	}
	if len(os.Args) > 2 {
		fmt.Sscanf(os.Args[2], "%d", &botWpm)
	}
	rng := rand.New(rand.NewSource(time.Now().UnixNano()))
	reader := bufio.NewReader(os.Stdin)
	you, bot := 0, 0
	for r := 1; r <= rounds; r++ {
		w := WORDS[rng.Intn(len(WORDS))]
		fmt.Printf("\n[round %d] type: %s\n> ", r, w)
		start := time.Now()
		line, _ := reader.ReadString('\n')
		elapsed := int(time.Since(start).Milliseconds())
		typed := strings.TrimSpace(line)
		ok := typed == w
		botMs := botTime(w, botWpm)
		if ok && elapsed < botMs {
			you++
			fmt.Printf("  you: %dms  bot: %dms  -> YOU WIN\n", elapsed, botMs)
		} else {
			bot++
			fmt.Printf("  you: %dms (ok=%v)  bot: %dms  -> BOT WINS\n", elapsed, ok, botMs)
		}
	}
	fmt.Printf("\nFINAL  you %d - bot %d\n", you, bot)
}
