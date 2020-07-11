import curses
import sys
from application.menu import Menu
from application.typing_drills import TypingDrills
from application.speed_reading_displayer import SpeedReadingDisplayer
from application.typing_app import TypingApp
from application.meta_typing_app import MetaTypingApp
from application.settings_app import SettingsApp

'''This is the interface that connects the applications together'''
# TODO put speed reader in a displayer and apply themes to it

class Start(Menu):

    def __init__(self, stdscr):
        Menu.__init__(self, stdscr)
        self.package_functions()
        self.display_screen()

    def package_functions(self):
        
        def exit(self):
            sys.exit(0)

        func = {
            'Meta Typing': MetaTypingApp,
            'Typing': TypingApp,
            'Speed Reading': SpeedReading,
            'Settings': SettingsApp,
            'Exit': exit,
        }
        self.set_new_screen(Start)
        self.set_functionality(func)
        

class SpeedReading(Menu):
    
    def __init__(self, stdscr):
        Menu.__init__(self, stdscr)
        self.stdscr = stdscr
        self.package_functions()
        self.display_screen()

    def package_functions(self):

        def about(self):
            pass

        func = {
            'Enter URL': (SpeedReadingDisplayer, 'url'),
            'Paste Clipboard':  (SpeedReadingDisplayer, 'clipboard'),
            'Return To Menu': Start,
        }
        self.set_new_screen(Start)
        self.set_functionality(func)
