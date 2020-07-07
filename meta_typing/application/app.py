import curses
import sys
import os
from application.menu import Menu
from application.typing_drills import TypingDrills
from application.speed_reading_displayer import SpeedReadingDisplayer
from application.typing_app import TypingApp
from application.meta_typing_app import MetaTypingApp


'''
    This application contains all the interface menus since each 
    menu calls on a submenu and each submenu calls on another menu that
    also has a link to its parent
'''

class Start(Menu):

    def __init__(self, stdscr):
        Menu.__init__(self, stdscr)
        self.package_functions()
        self.display_screen()

    def package_functions(self):
        
        def exit(self):
            sys.exit(0)

        func = {
            'Meta Type v2': MetaTypingApp,
            'Typing': TypingApp,
            'Speed Reading': SpeedReading,
            'Settings': Settings,
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


class Settings(Menu):

    def __init__(self, stdscr):
        Menu.__init__(self, stdscr)
        self.package_functions()
        self.display_screen()

    def package_functions(self):
        
        def about(self):
            pass

        func = {
            'Change Key Configurations': about,
            'Restore Default Key Configurations': about,
            'Change Screen Colors': about,
            'Return To Menu': Start,
        }
        self.set_functionality(func)
