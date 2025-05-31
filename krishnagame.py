import tkinter as tk
from tkinter import messagebox

ROWS = 6
COLS = 7
PLAYER_COLORS = ["red", "yellow"]

class Connect4:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect 4 Game")
        self.current_player = 0  # 0 = red, 1 = yellow
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]

        self.canvas = tk.Canvas(root, width=COLS*100, height=ROWS*100, bg="blue")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)

        self.draw_board()

    def draw_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                x0 = col * 100 + 5
                y0 = row * 100 + 5
                x1 = x0 + 90
                y1 = y0 + 90
                self.canvas.create_oval(x0, y0, x1, y1, fill="white", tags=f"{row}-{col}")

    def handle_click(self, event):
        col = event.x // 100
        row = self.find_row(col)
        if row is not None:
            self.board[row][col] = self.current_player
            color = PLAYER_COLORS[self.current_player]
            self.canvas.itemconfig(f"{row}-{col}", fill=color)

            if self.check_win(row, col):
                messagebox.showinfo("Game Over", f"Player {self.current_player + 1} ({color}) wins!")
                self.reset_game()
            elif all(self.board[0][c] is not None for c in range(COLS)):
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_game()
            else:
                self.current_player = 1 - self.current_player

    def find_row(self, col):
        for row in reversed(range(ROWS)):
            if self.board[row][col] is None:
                return row
        return None

    def check_win(self, row, col):
        def count(dir_x, dir_y):
            r, c = row + dir_y, col + dir_x
            count = 0
            while 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] == self.current_player:
                count += 1
                r += dir_y
                c += dir_x
            return count

        directions = [ (1, 0), (0, 1), (1, 1), (1, -1) ]
        for dx, dy in directions:
            total = 1 + count(dx, dy) + count(-dx, -dy)
            if total >= 4:
                return True
        return False

    def reset_game(self):
        self.canvas.delete("all")
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.draw_board()
        self.current_player = 0

if __name__ == "__main__":
    root = tk.Tk()
    game = Connect4(root)
    root.mainloop()
