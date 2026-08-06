// go-tone: synthesize a short procedural melody to out.wav (no deps, stdlib only).
// Build: go build -o go-tone .   Run: ./go-tone [seed]  -> writes melody.wav
package main

import (
	"encoding/binary"
	"fmt"
	"math"
	"os"
	"strings"
	"time"
)

const (
	sampleRate = 44100
	bpm        = 120
	seconds    = 8
)

// pentatonic scale (A minor) semitone offsets from A2 (110 Hz)
var scale = []int{0, 3, 5, 7, 10, 12, 15}

func freq(semi int) float64 { return 110 * math.Pow(2, float64(semi)/12) }

func main() {
	notesFlag := false
	for _, a := range os.Args[1:] {
		if a == "--notes" {
			notesFlag = true
		}
	}
	seed := 7
	if len(os.Args) > 1 {
		fmt.Sscanf(os.Args[1], "%d", &seed)
	}
	// seed==0 => derive from current time for a fresh tune each run
	if seed == 0 {
		seed = int(time.Now().UnixNano() % 1_000_000)
	}
	rng := seed

	n := sampleRate * seconds
	buf := make([]float32, n)
	beat := sampleRate * 60 / bpm
	totalBeats := seconds * bpm / 60

	if notesFlag {
		// print the scale-index sequence instead of synthesizing audio
		idxs := make([]int, 0, totalBeats)
		r := rng
		for i := 0; i < totalBeats; i++ {
			r = r*1103515245 + 12345
			idxs = append(idxs, int(uint(r)/65536%uint(len(scale))))
		}
		fmt.Println(strings.TrimSpace(strings.Trim(fmt.Sprint(idxs), "[]")))
		return
	}

	for i := 0; i < totalBeats; i++ {
		// deterministic-ish pick from seed
		rng = rng*1103515245 + 12345
		idx := int(uint(rng) / 65536 % uint(len(scale)))
		semi := scale[idx]
		f := freq(semi)
		start := i * beat
		for j := 0; j < beat && start+int(j) < n; j++ {
			t := float64(j) / float64(sampleRate)
			// simple ADSR-ish envelope
			env := math.Exp(-3 * t)
			buf[start+int(j)] += float32(math.Sin(2*math.Pi*f*t) * env * 0.3)
		}
	}

	writeWav("melody.wav", buf)
	fmt.Printf("wrote melody.wav (%d beats, seed=%d)\n", totalBeats, seed)
}

func writeWav(path string, samples []float32) {
	f, err := os.Create(path)
	if err != nil {
		panic(err)
	}
	defer f.Close()
	dataBytes := len(samples) * 2
	hdr := make([]byte, 44)
	copy(hdr[0:4], "RIFF")
	binary.LittleEndian.PutUint32(hdr[4:8], uint32(36+dataBytes))
	copy(hdr[8:12], "WAVE")
	copy(hdr[12:16], "fmt ")
	binary.LittleEndian.PutUint32(hdr[16:20], 16)
	binary.LittleEndian.PutUint16(hdr[20:22], 1) // PCM
	binary.LittleEndian.PutUint16(hdr[22:24], 1) // mono
	binary.LittleEndian.PutUint32(hdr[24:28], sampleRate)
	binary.LittleEndian.PutUint32(hdr[28:32], sampleRate*2)
	binary.LittleEndian.PutUint16(hdr[32:34], 2)
	binary.LittleEndian.PutUint16(hdr[34:36], 16)
	copy(hdr[36:40], "data")
	binary.LittleEndian.PutUint32(hdr[40:44], uint32(dataBytes))
	f.Write(hdr)
	for _, s := range samples {
		v := int16(s * 32767)
		binary.Write(f, binary.LittleEndian, v)
	}
}
