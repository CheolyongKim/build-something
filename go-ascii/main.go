// go-ascii: convert an image (PNG/JPG) to ASCII art, stdlib only.
// Build: go build -o go-ascii.exe .   Run: ./go-ascii.exe <image> [width]
// demo mode writes a tiny PNG, decodes it, and checks the ASCII has content.
package main

import (
	"bytes"
	"fmt"
	"image"
	"image/color"
	"image/jpeg"
	"image/png"
	"io"
	"math"
	"os"
	"strings"
)

const ramp = " .:-=+*#%@"

func toGray(img image.Image) [][]float64 {
	b := img.Bounds()
	w, h := b.Dx(), b.Dy()
	g := make([][]float64, h)
	for y := 0; y < h; y++ {
		g[y] = make([]float64, w)
		for x := 0; x < w; x++ {
			r, gr, bl, _ := img.At(b.Min.X+x, b.Min.Y+y).RGBA()
			lum := (0.299*float64(r) + 0.587*float64(gr) + 0.114*float64(bl)) / 65535
			g[y][x] = lum
		}
	}
	return g
}

func ascii(g [][]float64, cols int) string {
	h := len(g)
	if h == 0 {
		return ""
	}
	w := len(g[0])
	rows := int(float64(h) * float64(cols) / float64(w) / 2) // char aspect
	if rows < 1 {
		rows = 1
	}
	var sb strings.Builder
	for ry := 0; ry < rows; ry++ {
		yy := int(float64(ry) / float64(rows) * float64(h))
		for rx := 0; rx < cols; rx++ {
			xx := int(float64(rx) / float64(cols) * float64(w))
			v := g[yy][xx]
			idx := int(math.Round(v * float64(len(ramp)-1)))
			sb.WriteByte(ramp[idx])
		}
		sb.WriteByte('\n')
	}
	return sb.String()
}

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--demo" {
		// build a 16x16 gradient PNG in memory, decode, ascii-fy
		img := image.NewRGBA(image.Rect(0, 0, 16, 16))
		for y := 0; y < 16; y++ {
			for x := 0; x < 16; x++ {
				v := uint8(255 * (x + y) / 30)
				img.Set(x, y, color.RGBA{v, v, v, 255})
			}
		}
		var buf bytes.Buffer
		png.Encode(&buf, img)
		dec, err := png.Decode(&buf)
		if err != nil {
			fmt.Println("FAIL decode:", err)
			os.Exit(1)
		}
		out := ascii(toGray(dec), 16)
		if !strings.ContainsAny(out, "*#%@") {
			fmt.Println("FAIL: no dark pixels in ascii")
			os.Exit(1)
		}
		fmt.Println("go-ascii_ok: gradient->ascii has shading")
		return
	}
	// --text: render an already-ASCII grid from stdin as-is (chain use)
	if len(os.Args) > 1 && os.Args[1] == "--text" {
		data, _ := os.ReadFile(os.Stdin.Name())
		if len(data) == 0 {
			b, _ := io.ReadAll(os.Stdin)
			data = b
		}
		fmt.Print(string(data))
		return
	}
	if len(os.Args) < 2 {
		fmt.Println("usage: go-ascii <image> [width]   (or --demo | --text)")
		return
	}
	f, err := os.Open(os.Args[1])
	if err != nil {
		fmt.Println("open:", err)
		return
	}
	defer f.Close()
	img, _, err := image.Decode(f)
	if err != nil {
		fmt.Println("decode:", err)
		return
	}
	cols := 80
	if len(os.Args) > 2 {
		fmt.Sscanf(os.Args[2], "%d", &cols)
	}
	fmt.Print(ascii(toGray(img), cols))
	_ = jpeg.Decode // keep jpeg registered
}
