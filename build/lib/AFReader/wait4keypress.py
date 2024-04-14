import curses


def kwait():
    global stdscr
    curses.initscr()
    curses.curs_set(0)

    stdscr.getch()


kwait()
