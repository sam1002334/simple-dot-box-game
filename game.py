import tkinter as tk
from tkinter import messagebox

class DotsAndBoxes:
    def __init__(self, root, size=9):
        self.root = root
        self.size = size
        self.h_lines = [[False] * size for _ in range(size + 1)]
        self.v_lines = [[False] * (size + 1) for _ in range(size)]
        self.boxes = [[None] * size for _ in range(size)]
        self.current_player = 1
        self.score1 = 0
        self.score2 = 0
        self.cell_size = 80  # Increased cell size for greater spacing between dots
        self.dot_radius = 7  # Increased radius for the dots
        self.line_width = 3  # Increased width for the lines
        self.offset = self.dot_radius + 10  # Offset adjusted to match the new dot size
        self.canvas = tk.Canvas(root, width=self.cell_size * (size + 1) + 2 * self.offset, 
                               height=self.cell_size * (size + 1) + 2 * self.offset, bg='white')
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_grid()

    def draw_grid(self):
        for i in range(self.size + 1):
            for j in range(self.size + 1):
                self.canvas.create_oval(
                    self.offset + j * self.cell_size - self.dot_radius,
                    self.offset + i * self.cell_size - self.dot_radius,
                    self.offset + j * self.cell_size + self.dot_radius,
                    self.offset + i * self.cell_size + self.dot_radius,
                    fill="black"
                )


    def on_click(self, event):
        x, y = event.x, event.y
        row = (y - self.offset) // self.cell_size
        col = (x - self.offset) // self.cell_size

        if row >= 0 and row < self.size + 1 and col >= 0 and col < self.size + 1:
            # Horizontal line click detection
            if abs(y - (self.offset + row * self.cell_size)) <= self.cell_size // 4:
                if col < self.size and not self.h_lines[row][col]:
                    self.h_lines[row][col] = True
                    self.canvas.create_line(self.offset + col * self.cell_size, self.offset + row * self.cell_size,
                                            self.offset + (col + 1) * self.cell_size, self.offset + row * self.cell_size,
                                            fill="blue" if self.current_player == 1 else "red", width=self.line_width)
                    if not self.check_boxes(row, col, 'h'):
                        self.current_player = 3 - self.current_player
            # Vertical line click detection
            elif abs(x - (self.offset + col * self.cell_size)) <= self.cell_size // 4:
                if row < self.size and not self.v_lines[row][col]:
                    self.v_lines[row][col] = True
                    self.canvas.create_line(self.offset + col * self.cell_size, self.offset + row * self.cell_size,
                                            self.offset + col * self.cell_size, self.offset + (row + 1) * self.cell_size,
                                            fill="blue" if self.current_player == 1 else "red", width=self.line_width)
                    if not self.check_boxes(row, col, 'v'):
                        self.current_player = 3 - self.current_player

        if self.game_over():
            self.show_winner()

    def check_boxes(self, row, col, orientation):
        scored = False
        if orientation == 'h':
            if row > 0 and all([self.h_lines[row-1][col], self.v_lines[row-1][col], self.v_lines[row-1][col+1]]):
                self.boxes[row-1][col] = self.current_player
                self.score1 += 1 if self.current_player == 1 else 0
                self.score2 += 1 if self.current_player == 2 else 0
                self.draw_box(row-1, col)
                scored = True
            if row < self.size and all([self.h_lines[row+1][col], self.v_lines[row][col], self.v_lines[row][col+1]]):
                self.boxes[row][col] = self.current_player
                self.score1 += 1 if self.current_player == 1 else 0
                self.score2 += 1 if self.current_player == 2 else 0
                self.draw_box(row, col)
                scored = True
        elif orientation == 'v':
            if col > 0 and all([self.v_lines[row][col-1], self.h_lines[row][col-1], self.h_lines[row+1][col-1]]):
                self.boxes[row][col-1] = self.current_player
                self.score1 += 1 if self.current_player == 1 else 0
                self.score2 += 1 if self.current_player == 2 else 0
                self.draw_box(row, col-1)
                scored = True
            if col < self.size and all([self.v_lines[row][col+1], self.h_lines[row][col], self.h_lines[row+1][col]]):
                self.boxes[row][col] = self.current_player
                self.score1 += 1 if self.current_player == 1 else 0
                self.score2 += 1 if self.current_player == 2 else 0
                self.draw_box(row, col)
                scored = True

        return scored

    def draw_box(self, row, col):
        x1 = self.offset + col * self.cell_size
        y1 = self.offset + row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, 
                                    outline="black",  # Add black border
                                    width=4,  # Set border width
                                    fill="blue" if self.current_player == 1 else "red")
        self.redraw_dots()
    def redraw_dots(self):
        for i in range(self.size + 1):
            for j in range(self.size + 1):
                self.canvas.create_oval(
                    self.offset + j * self.cell_size - self.dot_radius,
                    self.offset + i * self.cell_size - self.dot_radius,
                    self.offset + j * self.cell_size + self.dot_radius,
                    self.offset + i * self.cell_size + self.dot_radius,
                    fill="black"
                )


    def game_over(self):
        for row in self.h_lines:
            if not all(row):
                return False
        for row in self.v_lines:
            if not all(row):
                return False
        return True

    def show_winner(self):
        if self.score1 > self.score2:
            winner = "Player 1 wins!"
        elif self.score2 > self.score1:
            winner = "Player 2 wins!"
        else:
            winner = "It's a tie!"
        messagebox.showinfo("Game Over", f"Player 1: {self.score1}\nPlayer 2: {self.score2}\n{winner}")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Dots and Boxes")
    game = DotsAndBoxes(root)
    root.mainloop()
