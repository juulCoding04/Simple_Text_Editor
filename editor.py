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

def printHelp():
    print("-h or --help for help")
    print("-f <filename>.txt or --file <filename>.txt to open a file")

def get_args():
    n = len(sys.argv)
    txt_file = ""
    help_bit = 0

    for arg in range(1, n):
        if sys.argv[arg] == "-h" or sys.argv[arg] == "--help":
            help_bit = 1;
        if sys.argv[arg] == "-f" or sys.argv[arg] == "--file":
            txt_file = sys.argv[arg+1]

    return txt_file, help_bit

def main(stdscr):
    k = ''

    with open(txt_file, 'r') as f:
        lines = f.read().splitlines()
        buffer = Buffer(lines)

    window = Window(curses.LINES - 1, curses.COLS - 1)
    cursor = Cursor()

    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    while (True):
        # Initialization
        stdscr.erase()
        height, width = stdscr.getmaxyx()

        statusbarstr = "'CTRL-X' + 'y' to exit and save | 'CTRL-X' + 'n' to exit without saving | Pos: {}, {}".format(cursor.col, cursor.row)

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
        elif ord(k) == 24: # CRTL-X
            break
        else:
            buffer.insert(cursor, k)
            for i in k:
                right(window, cursor, buffer)
    
    while(True):
        k = stdscr.getkey()
        if k == 'n':
            break
        if k == 'y':
            buffer.lines = [line if line.endswith('\n') else line + '\n' for line in buffer.lines]
            with open(txt_file, 'w') as f:
                f.writelines(buffer.lines)
            break

if __name__ == "__main__":
    txt_file, help_bit = get_args()
    if help_bit:
        printHelp()
    elif os.path.exists(txt_file):
        curses.wrapper(main)
    else:
        print(f"File {txt_file} Not Found")