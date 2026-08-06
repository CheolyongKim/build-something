// clock: terminal clock that draws an ASCII analog face for the current time.
// Build: javac Clock.java   Run: java Clock   (java Clock --demo for self-check)
// ponytail: draws a 12x12 grid face; hands are rays from center at computed angles.
import java.time.LocalTime;

public class Clock {
    static final int R = 5;            // face radius in cells (half-height)
    static final int CX = R, CY = R;   // center

    // cell occupied by the hand at angle a (degrees, 0=12 o'clock, clockwise)
    static int[] handCell(double deg, int len) {
        double rad = Math.toRadians(deg - 90); // 0deg -> up
        int x = CX + (int) Math.round(Math.cos(rad) * len);
        int y = CY + (int) Math.round(Math.sin(rad) * len);
        return new int[]{x, y};
    }

    static char[][] face() {
        char[][] g = new char[2 * R + 1][2 * R + 1];
        for (int y = 0; y <= 2 * R; y++)
            for (int x = 0; x <= 2 * R; x++) g[y][x] = ' ';
        // rim ticks
        for (int h = 0; h < 12; h++) {
            int[] c = handCell(h * 30, R);
            g[c[1]][c[0]] = '.';
        }
        g[CY][CX] = 'O'; // center
        return g;
    }

    static void draw(char[][] g) {
        StringBuilder sb = new StringBuilder();
        for (char[] row : g) sb.append(new String(row)).append('\n');
        System.out.print(sb);
    }

    static double angle(int val, int max) { return (double) val / max * 360.0; }

    public static void main(String[] args) {
        boolean demo = args.length > 0 && args[0].equals("--demo");
        if (demo) {
            // verify hand geometry for 3:00 and 6:00
            int[] c = handCell(90, R);   // 3 o'clock -> right
            if (c[0] != 2 * R || c[1] != CY) { System.err.println("FAIL: 3oclock"); System.exit(1); }
            c = handCell(180, R);         // 6 o'clock -> bottom
            if (c[0] != CX || c[1] != 2 * R) { System.err.println("FAIL: 6oclock"); System.exit(1); }
            c = handCell(0, R);           // 12 o'clock -> top
            if (c[0] != CX || c[1] != 0) { System.err.println("FAIL: 12oclock"); System.exit(1); }
            System.err.println("clock_ok: hand angles 3/6/12 correct");
            return;
        }
        LocalTime t = LocalTime.now();
        int h = t.getHour() % 12, m = t.getMinute(), s = t.getSecond();
        char[][] g = face();
        int[][] hands = {
            handCell((int) angle(h * 60 + m, 720), R - 1), // hour
            handCell((int) angle(m, 60), R - 1),            // minute
            handCell((int) angle(s, 60), R)                 // second
        };
        char[] sym = {'H', 'M', 'S'};
        for (int i = 0; i < 3; i++) g[hands[i][1]][hands[i][0]] = sym[i];
        draw(g);
        System.out.printf("%02d:%02d:%02d%n", t.getHour(), m, s);
    }
}
