import curses
import types
import sys

class Menu:

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.menu = []
        self.functionality = {}
        self.selected_row = 0
        self.setup()
        self.new_screen = None

    def setup(self):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        self.stdscr.clear()

    def print_menu(self):
        for row, item in enumerate(self.menu):
            if row == self.selected_row:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(row, 0, item)
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(row, 0, item)
        self.stdscr.refresh()

    def prompt_response(self):
        response = self.functionality[self.menu[self.selected_row]]
        args = None
        if isinstance(response, tuple):
            response, args = response
            
        if isinstance(response, types.FunctionType):
            response(self)
        elif isinstance(response, type): # its a class.
            if args:
                response(self.stdscr, args)
            else:
                response(self.stdscr)
        else:
            pass

        if self.new_screen:
            self.new_screen(self.stdscr)
        else:
            sys.exit(0)

    def move_up(self, key):
        return self.selected_row > 0 and (key == curses.KEY_UP or key == ord('k'))

    def move_down(self, key):
        return self.selected_row < len(self.menu) - 1 and (key == curses.KEY_DOWN or key == ord('y'))
 
    def enter(self, key):
        return key == curses.KEY_ENTER or key in [10, 13]

    def display_screen(self):
        self.print_menu()
        while True:
            key = self.stdscr.getch()
            if self.move_up(key):
                self.selected_row -= 1
            elif self.move_down(key):
                self.selected_row += 1
            elif self.enter(key):
                self.prompt_response()
            self.print_menu()

    def set_functionality(self, functionalities):
        self.functionality = functionalities
        self.menu = list(self.functionality.keys())

    def set_new_screen(self, new_selection):
        self.new_screen = new_selection
