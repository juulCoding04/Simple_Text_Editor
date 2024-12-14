import curses
import sys, os
from Buffer import Buffer
from Cursor import Cursor
from Window import Window

def left(window, cursor, buffer):
    cursor.left(buffer)
    window.up(cursor)

def right(window, cursor, buffer):
    cursor.right(buffer)
    window.up(cursor)

def get_args():
    n = len(sys.argv)
    txt_file = ""
    help_bit = 0

    for arg in range(1, n):
        if sys.argv[arg] == "-h":
            print("You can search for help here")
            help_bit = 1;
        if sys.argv[arg] == "-f" or sys.argv[arg] == "--file":
            txt_file = sys.argv[arg+1]

    return txt_file, help_bit

def main(stdscr):
    txt_file, help_bit = get_args()
    k = ''

    if help_bit:
        return -1

    if os.path.exists(txt_file):
        print(f"File {txt_file} found")
        print("----------")
    else:
        print("File Not Found")
        return -1

    with open(txt_file) as f:
        lines = f.read().splitlines()
        buffer = Buffer(lines)

    window = Window(curses.LINES - 1, curses.COLS - 1)
    cursor = Cursor()

    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    while (k != '^'):
        # Initialization
        stdscr.erase()
        height, width = stdscr.getmaxyx()

        statusbarstr = "Press '^q' to exit | Press '^s' to save | Pos: {}, {}".format(cursor.col, cursor.row)

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        for row, line in enumerate(buffer[window.row:window.row + window.n_rows]):
            if row == cursor.row - window.row and window.col > 0:
                line = "<<" + line[window.col + 1:]
            if len(line) > window.n_cols:
                line = line[:window.n_cols - 1] + ">>"

            stdscr.addstr(row, 0, line)
        stdscr.move(*window.translate(cursor=cursor))

        # Wait for next input
        k = stdscr.getkey()

        if k == "KEY_LEFT":
            left(window=window, cursor=cursor, buffer=buffer)
        elif k == "KEY_RIGHT":
            right(window=window, cursor=cursor, buffer=buffer)
        elif k == "KEY_UP":
            cursor.up(buffer)
            window.up(cursor)
        elif k == "KEY_DOWN":
            cursor.down(buffer)
            window.down(buffer, cursor)
        elif k == "\n":
            buffer.split(cursor)
            right(window, cursor, buffer)
        elif k in ("KEY_BACKSPACE", "\x7f"):
            if (cursor.row, cursor.col) > (0, 0):
                left(window=window, cursor=cursor, buffer=buffer)
                buffer.delete(cursor)
        else:
            buffer.insert(cursor, k)
            for i in k:
                right(window, cursor, buffer)
    
    while(True):
        k = stdscr.getkey()
        if k == 'q':
            break

if __name__ == "__main__":
    curses.wrapper(main)