#! /usr/bin/python3

target_row_count = 40
target_col_count = 120

# resize terminal window to 40 rows and 120 columns
print("\x1b[8;" + str(target_row_count) + ";" + str(target_col_count) + "t")

import curses
import os

rows, columns = os.popen('stty size', 'r').read().split()

def setchar(stdscr, y, x, char):
    if len(char) != 1:
        raise ValueError("incorrect argument: char length")
    if y < 0 or y >= target_row_count:
        raise ValueError("incorrect argument: row")
    if x < 0 or x >= target_col_count:
        raise ValueError("incorrect argument: column")

    stdscr.addch(y, x, char, curses.color_pair(1))

def main(stdscr):

    # Change color
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # Clear screen
    stdscr.clear()

    setchar(stdscr, 1, 0, "=")

    stdscr.addstr(10, 10, rows)
    stdscr.addstr(11, 10, columns)

    stdscr.move(0, 0)

    stdscr.refresh()
    stdscr.getkey()

curses.wrapper(main)
