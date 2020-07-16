from curses import wrapper
from application.app import App


def main(stdscr):
    app = App(stdscr)
    app.start()

if __name__ == "__main__":
    wrapper(main)
