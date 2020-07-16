import curses
import sys
from application.typing_app import TypingApp
from application.settings_app import SettingsApp
from application.utilities import SelectionWindow


class App():

    def __init__(self, stdscr):
        self.stdscr = stdscr

    def start(self):
        start_menu_choice = self.get_start_menu_choice()
        self.start_menu_action(start_menu_choice)
        while start_menu_choice != 'Exit':
            start_menu_choice = self.get_start_menu_choice()
            self.start_menu_action(start_menu_choice)

    def get_start_menu_choice(self):
        start_menu = ['Typing', 'Settings', 'Exit']
        start_menu_window = SelectionWindow(self.stdscr, selection_list = start_menu)
        return start_menu_window.get_selected_response()

    def start_menu_action(self, response):
        if response == 'Typing':
            TypingApp(self.stdscr)
        elif response == 'Settings':
            SettingsApp(self.stdscr)
        elif response == 'Exit':
            sys.exit(0)
        else:
            pass
