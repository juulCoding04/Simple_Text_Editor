class Buffer:
    def __init__(self, lines):
        self.lines = lines
    
    def __len__(self):
        return len(self.lines)
    
    def __getitem__(self, index):
        return self.lines[index]
    
    def bottom(self):
        return len(self) - 1
    
    def insert(self, cursor, string):
        row, col = cursor.row, cursor.col
        try:
            current = self.lines.pop(row)
        except IndexError:
            current = ''
        new = current[:col] + string + current[col:]
        self.lines.insert(row, new)

    def delete(self, cursor):
        row, col = cursor.row, cursor.col
        if (row, col) < (self.bottom(), len(self[row])):
            current = self.lines.pop(row)
            new = current[:col] + current[col + 1:]
            self.lines.insert(row, new)