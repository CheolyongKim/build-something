// morse: text -> Morse code converter (Go, stdlib). A-Z 0-9 + space.
// Build: go build -o morse.exe .   Run: ./morse.exe "HELLO WORLD"
//   ./morse.exe --demo   self-check: known letter mappings
package main

import (
	"fmt"
	"os"
	"strings"
)

var CODE = map[rune]string{
	'A': ".-", 'B': "-...", 'C': "-.-.", 'D': "-..", 'E': ".", 'F': "..-.",
	'G': "--.", 'H': "....", 'I': "..", 'J': ".---", 'K': "-.-", 'L': ".-..",
	'M': "--", 'N': "-.", 'O': "---", 'P': ".--.", 'Q': "--.-", 'R': ".-.",
	'S': "...", 'T': "-", 'U': "..-", 'V': "...-", 'W': ".--", 'X': "-..-",
	'Y': "-.--", 'Z': "--..", '0': "-----", '1': ".----", '2': "..---",
	'3': "...--", '4': "....-", '5': ".....", '6': "-....", '7': "--...",
	'8': "---..", '9': "----.",
}

func toMorse(s string) string {
	var out []string
	for _, r := range strings.ToUpper(s) {
		if r == ' ' {
			out = append(out, "/")
		} else if c, ok := CODE[r]; ok {
			out = append(out, c)
		}
	}
	return strings.Join(out, " ")
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--demo" {
		if toMorse("SOS") != "... --- ..." {
			fmt.Println("FAIL: SOS"); os.Exit(1)
		}
		if toMorse("A1") != ".- .----" {
			fmt.Println("FAIL: A1"); os.Exit(1)
		}
		if toMorse("HI THERE")[8] != '/' { // space between words -> '/'
			fmt.Println("FAIL: word gap"); os.Exit(1)
		}
		fmt.Println("morse_ok: SOS/A1/word-gap mappings correct")
		return
	}
	if len(os.Args) < 2 {
		fmt.Println("usage: morse.exe \"TEXT\"")
		return
	}
	fmt.Println(toMorse(os.Args[1]))
}
