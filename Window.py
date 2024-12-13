class Window:
    def __init__(self, n_rows, n_cols, row=0, col=0):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.row = row
        self.col = col

    def bottom(self):
        return self.row + self.n_rows - 1
    
    def down(self, buffer, cursor):
        if cursor.row == self.row + 1 and self.row < len(buffer) - 1:
            self.row += 1
    
    def up(self, cursor):
        if cursor.row == self.row - 1 and self.row > 0:
            self.row -= 1

    def translate(self, cursor):
        return cursor.row - self.row, cursor.col - self.col