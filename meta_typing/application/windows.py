import curses
from curses import wrapper
import json
import types
import sys

class Window:
    '''
    Windows are the medium for communicating input and output to the application/user

    The Window describes how the user interacts with the window:
        Static Window - User views a page and navigates pages
        Text Window - User types text
        Selection Window - User sends selected highlighted row
    '''
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.setup()

    def setup(self):
        curses.curs_set(0)
        apply_setting()
        self.stdscr.clear()
    
    def cursor_on(self):
        curses.curs_set(2)
  
    def cursor_off(self):
        curses.curs_set(0)

    def move_up(self, key):
        return key == curses.KEY_UP

    def move_down(self, key):
        return key == curses.KEY_DOWN
        
    def move_left(self, key):
        return key == curses.KEY_LEFT

    def move_right(self, key):
        return key == curses.KEY_RIGHT
 
    def enter(self, key):
        return key == curses.KEY_ENTER or key in [10, 13] or key == '\n'

    def quit(self, key):
        return key == '\x1b'

    def f4(self, key):
        return key == curses.KEY_F4
                
class TextWindow(Window):
    '''
    text window is designed for getting user input
    
    Parameters
        static_message - text shown above where the user inputs text
            - ex. Enter a number: 

    input = user input
    designed_output = user_input

    use cases
        text - get url, clipboard
        numbers or letters - filters for drills
    '''
    def __init__(self, stdscr, message = '', termination_trigger = 'enter'):
        Window.__init__(self, stdscr)
        self.message = message
        self.termination_trigger = termination_trigger
        self.output = self.prompt()

    def get_termination_trigger(self, char):
        if self.termination_trigger == 'enter' and self.enter(char):
            return True
        elif self.termination_trigger == 'f4' and self.f4(char):
            return True
        else:
            return False

    def display_text(self, shown_output):
        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.addstr(0, 0, self.message)
        self.stdscr.attron(curses.color_pair(2))
        self.stdscr.addstr(shown_output)
        self.stdscr.clrtoeol()
        self.stdscr.refresh()

    def prompt(self):
        ''' Text will only show until screen fills'''
        self.cursor_on()
        shown_output, output = '', ''
        eol = False
        max_height, max_width = self.stdscr.getmaxyx()
        y, x = self.stdscr.getyx()
        while True:
            self.display_text(shown_output)
            if y + 2 > max_height:
                eol = True 
            char = (self.stdscr.get_wch())
            if char == curses.KEY_BACKSPACE or char == '\x7f':
                output = output[:-1]
                shown_output = shown_output[:-1]
            elif self.get_termination_trigger(char):
                    return output
            elif char == '\n':
                y += 1
                if y + 2 > max_height:
                    eol = True
                if not eol:
                    shown_output += (char)
                output += (char)
            elif self.quit(char):
                sys.exit()
            elif isinstance(char, str) and char.isprintable():
                y, x = self.stdscr.getyx()
                output += (char)
                if not eol:
                    shown_output += (char)
        self.stdscr.clear()


    def get_output(self):
        return self.output


class SelectionWindow(Window):
    '''
    Parameters
        static_message - text shown above where the user inputs text
        selection_functionality
            selection_names = keys - text to be displayed
            values - function or class to be called
        selected_row - int showing current position

    input = a dictionaries with names and a functional response
    output = the selected functional response

    use cases
        file menu
        typing drill selection
        boolean response for paramters
    '''
    def __init__(self, stdscr, static_message = None, selection_list = None):
        Window.__init__(self, stdscr)
        self.static_message = static_message
        self.selection_list = selection_list
        self.selected_row = 0
        self.display_screen()


    def update_selection_screen(self):
        '''Displays the selection keys with the highlights selected row'''
        def highlight_row(self):
            self.stdscr.attron(curses.color_pair(1))
            self.stdscr.addstr(y + row, 0, selection_name)
            self.stdscr.attron(curses.color_pair(3))

        if self.static_message:
            self.stdscr.addstr(0, 0, self.static_message, curses.color_pair(2))
            y = 1
        else:
            y = 0
        x = 0
        for row, selection_name in enumerate(self.selection_list):
            if row == self.selected_row:
                highlight_row(self)
            else:
                self.stdscr.addstr(y + row, 0, selection_name)
        self.stdscr.refresh()

    def move_up(self, key):
        return self.selected_row > 0 and key == curses.KEY_UP

    def move_down(self, key):
        return self.selected_row < len(self.selection_list) - 1 and key == curses.KEY_DOWN
 
    def enter(self, key):
        return key == curses.KEY_ENTER or key in [10, 13]

    def display_screen(self):
        self.update_selection_screen()
        while True:
            key = self.stdscr.getch()
            if self.move_up(key):
                self.selected_row -= 1
            elif self.move_down(key):
                self.selected_row += 1
            elif self.enter(key):
                return
            self.update_selection_screen()
    
    def get_selected_row(self):
        return self.selected_row

    def get_selected_response(self):
        return self.selection_list[self.selected_row]

class StaticWindow(Window):
    def __init__(self, stdscr, screens):
        Window.__init__(self, stdscr)
        self.screens = screens
        self.prompt()

    def prompt(self):
        self.stdscr.clear()
        for screen in self.screens:
            x, y = 0, 0
            self.stdscr.move(y, x)
            for lines in screen:
                self.stdscr.addstr(y, x, lines)
                y += 1
                x = 0
            key = self.stdscr.getch()
            while not self.enter(key):
                key = self.stdscr.getch()
            self.stdscr.clear()

def read_color_settings():
    path = f'../settings/colors.json'
    with open(path, 'r') as f:
        color_settings = json.load(f)
    return color_settings

def apply_setting():
    color_settings = read_color_settings()
    apply_color_settings(color_settings)

def apply_color_settings(color_settings):
    background_color = f"COLOR_{color_settings[0]['Background']}"
    main_color = f"COLOR_{color_settings[0]['Main']}"
    secondary_color = f"COLOR_{color_settings[0]['Secondary']}"
    
    modpart = 'curses'
    module = __import__(modpart)
    curses.init_pair(1, getattr(module, main_color), getattr(module, background_color))
    curses.init_pair(2, getattr(module, secondary_color), getattr(module, background_color))
    curses.init_pair(3, curses.COLOR_WHITE, getattr(module, background_color))