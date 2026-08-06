#!/usr/bin/env python3
"""Connect Four (terminal). 2 players, drop discs into a 7x6 grid.
Usage: connect4.py [cols] [rows]   (default 7 6)
  connect4.py --demo   self-check: drop gravity + 4-in-a-row detection
"""
import sys

def new_board(c, r):
    return [["." for _ in range(c)] for _ in range(r)]

def drop(board, col, who):
    r = len(board)
    for y in range(r - 1, -1, -1):
        if board[y][col] == ".":
            board[y][col] = who
            return y
    return -1  # column full

def win(board, who):
    h, w = len(board), len(board[0])
    for y in range(h):
        for x in range(w):
            if board[y][x] != who:
                continue
            # right / down / diag-down-right / diag-down-left
            for dx, dy in ((1, 0), (0, 1), (1, 1), (-1, 1)):
                if all(0 <= y + dy * k < h and 0 <= x + dx * k < w and
                       board[y + dy * k][x + dx * k] == who for k in range(4)):
                    return True
    return False

def render(board):
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (len(board[0]) * 2 + 1))
    print(" " + " ".join(str(i) for i in range(len(board[0]))))

def main():
    if "--demo" in sys.argv:
        b = new_board(7, 6)
        # vertical 4-in-a-row for X in column 3
        for _ in range(4):
            assert drop(b, 3, "X") >= 0
        assert win(b, "X"), "FAIL: vertical win not detected"
        # horizontal 4-in-a-row for O on row bottom
        b2 = new_board(7, 6)
        for c in range(4):
            drop(b2, c, "O")
        assert win(b2, "O"), "FAIL: horizontal win not detected"
        # gravity: dropping into a partially filled column lands on top
        b3 = new_board(7, 6)
        drop(b3, 0, "X")
        y2 = drop(b3, 0, "O")
        assert y2 == len(b3) - 2, "FAIL: gravity wrong"
        print("connect4_ok: gravity + vertical/horizontal win detected")
        return
    c = 7; r = 6
    if len(sys.argv) > 1 and sys.argv[1].isdigit(): c = int(sys.argv[1])
    if len(sys.argv) > 2 and sys.argv[2].isdigit(): r = int(sys.argv[2])
    board = new_board(c, r)
    turn = "X"
    moves = 0
    while moves < c * r:
        render(board)
        try:
            col = int(input(f"{turn}> ")) 
        except (EOFError, ValueError):
            return
        if not (0 <= col < c) or board[0][col] != ".":
            print("bad column"); continue
        drop(board, col, turn)
        if win(board, turn):
            render(board); print(f"{turn} wins!"); return
        turn = "O" if turn == "X" else "X"
        moves += 1
    render(board); print("draw")

if __name__ == "__main__":
    main()
