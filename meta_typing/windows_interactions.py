from curses import wrapper
from application.utilities import selection_menu


def main(stdscr):
    value = selection_menu(stdscr, 'instuctions', ['1 item', 'two t', 'exit'])
    stdscr.addstr(4, 20, str(value))
    stdscr.getch()

if __name__ == "__main__":
    wrapper(main)
