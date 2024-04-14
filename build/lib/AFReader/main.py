import os
import sys
import subprocess
import time
import argparse

try:
    import curses
except ImportError:
    if os.name == "ps":
        subprocess.run(["python3", "-m", "pip3", "install", "windows-curses"])


def typewriter_effect(stdscr, text, speed):
    curses.curs_set(0)
    stdscr.clear()

    row, col = 0, 0
    max_row, max_col = stdscr.getmaxyx()

    for line in text.split('\n'):
        for char in line:
            try:
                stdscr.addch(row, col, char)
            except curses.error:
                col = 0
                row = (row + 1) % max_row
                stdscr.addch(row, col, char)

            col += 1

            if col == curses.COLS - 1:
                col = 0
                row += 1

                if row == max_row - 1:
                    stdscr.refresh()
                    stdscr.getch()  # Wait for Enter key press
                    stdscr.clear()
                    row = 0

            stdscr.refresh()
            time.sleep(speed)

        # Move to the next line after processing a line
        col = 0
        row += 1

        # Check if the screen is full, and if so, scroll
        if row == max_row - 1:
            stdscr.refresh()
            stdscr.getch()  # Wait for Enter key press
            stdscr.clear()
            row = 0

    stdscr.getch()  # Wait for a key press before exiting


def color_cycling_effect(stdscr, text, speed):
    curses.curs_set(0)
    stdscr.clear()

    # Initialize color pairs
    curses.start_color()
    for i in range(1, curses.COLORS):
        curses.init_pair(i, i, curses.COLOR_BLACK)

    colors = list(range(1, curses.COLORS))

    max_row, max_col = stdscr.getmaxyx()

    col, row = 0, 0
    for char in text:
        if char == '\n':
            col = 0
            row += 1
        else:
            color_pair = curses.color_pair(colors[0])
            stdscr.addch(row, col, char, color_pair)
            col += 1

        if col == max_col - 1:
            col = 0
            row += 1

        if row == max_row - 1 and col == 0:  # Wait for key press only when the screen is full
            stdscr.refresh()
            stdscr.getch()  # wait for key press
            stdscr.clear()  # clear screen
            row = 0

        stdscr.refresh()
        time.sleep(speed)

        # Rotate colors to ensure continuous cycling
        colors.append(colors.pop(0))

    stdscr.getch()


def italic_in_effect(stdscr, text, speed):
    curses.curs_set(0)
    stdscr.clear()

    row, col = 0, 0
    max_row, max_col = stdscr.getmaxyx()

    for char in text:
        if char == '\n':
            col = 0
            row += 1
        else:
            # Use A_DIM for fading effect
            stdscr.addch(row, col, char, curses.A_ITALIC)
            col += 1

        if col == max_col - 1:
            col = 0
            row += 1

        if row == max_row - 1 and col == 0:
            stdscr.refresh()
            stdscr.getch()  # Wait for key press to continue
            stdscr.clear()
            row = 0

        time.sleep(speed)
        stdscr.refresh()

    stdscr.getch()  # Wait for a key press before exiting


def DIM_text_effect(stdscr, text, speed):
    curses.curs_set(0)
    stdscr.clear()

    row, col = 0, 0
    max_row, max_col = stdscr.getmaxyx()

    for char in text:
        if char == '\n':
            col = 0
            row += 1
        else:
            # Use A_DIM for fading effect
            stdscr.addch(row, col, char, curses.A_DIM)
            col += 1

        if col == max_col - 1:
            col = 0
            row += 1

        if row == max_row - 1 and col == 0:
            stdscr.refresh()
            stdscr.getch()  # Wait for key press to continue
            stdscr.clear()
            row = 0

        time.sleep(speed)
        stdscr.refresh()

    stdscr.getch()  # Wait for a key press before exiting


def read_text_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def interactive_menu(stdscr):
    curses.curs_set(0)
    stdscr.clear()

    options = ["Typewriter Effect", "Italic Text", "Color Cycling Effect",
               "Fade In Effect(DIM Text)"]

    selected_option = 0

    while True:
        stdscr.clear()

        for i, option in enumerate(options):
            stdscr.addstr(i + 1, 1, f"{i + 1}. {option}",
                          curses.A_BOLD if i == selected_option else curses.A_NORMAL)

        key = stdscr.getch()

        if key == curses.KEY_UP and selected_option > 0:
            selected_option -= 1
        elif key == curses.KEY_DOWN and selected_option < len(options) - 1:
            selected_option += 1
        elif key == 10:  # Enter key
            return selected_option


def funcmain(stdscr, cargs):
    input_file, speed = cargs

    if os.path.splitext(input_file)[1].lower().endswith("pdf"):
        _, ext = os.path.splitext(input_file)
        txt_file = _ + '.txt'
        subprocess.run(['fconverter', '5', input_file, txt_file])
        with open(txt_file, 'r') as file:
            text_content = file.read()

    elif os.path.splitext(input_file)[1].lower().endswith("docx"):
        _, ext = os.path.splitext(input_file)
        txt_file = _ + '.txt'
        subprocess.run(['fconverter', '4', input_file, txt_file])
        with open(txt_file, 'r') as file:
            text_content = file.read()

    elif os.path.splitext(input_file)[1].lower().endswith("txt"):
        with open(input_file, 'r') as file:
            text_content = file.read()
    else:
        try:
            with open(input_file, 'r') as file:
                text_content = file.read()
        except Exception:
            pass

    selected_option = interactive_menu(stdscr)

    if selected_option == 0:
        typewriter_effect(stdscr, text_content, speed)
    elif selected_option == 1:
        italic_in_effect(stdscr, text_content, speed)
    elif selected_option == 2:
        color_cycling_effect(stdscr, text_content, speed)
    elif selected_option == 3:
        DIM_text_effect(stdscr, text_content, speed)
    # Add more conditions for additional animation styles


def argsinit():
    # create argument parser
    parser = argparse.ArgumentParser(description='''Open documents in anymated mode''')
    parser.add_argument('-i', '--input_file', help='file to to open', required=True)
    parser.add_argument('-s', '--speed', default=0.001, type=float, help='Text display/animation speed')

    args = parser.parse_args()
    input_file = args.input_file
    speed = args.speed
    return input_file, speed


def main():
    try:
        curses.wrapper(funcmain, argsinit())
    except KeyboardInterrupt:
        print("\nQuit!")
        sys.exit()


if __name__ == '__main__':
    main()
