import curses
import sys
import glob
import os
from timeit import default_timer as timer
from itertools import zip_longest
from application.menu import Menu
from application.text_displayer import TextDisplayer
from application.typing_drills import TypingDrills
from application.speed_reading_displayer import SpeedReadingDisplayer
from application.meta_typing_displayer import MetaTypingDisplayer


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
            'Meta Typing(preview only)': MetaTyping,
            'Typing': Typing,
            'Speed Reading': SpeedReading,
            'Settings': Settings,
            'Exit': exit,
        }
        self.set_functionality(func)


class Typing(Menu):
    
    def __init__(self, stdscr):
        Menu.__init__(self, stdscr)
        self.package_functions()
        self.display_screen()

    def package_functions(self):
        
        def about(self):
            pass

        func = {
            'Drills': Drills,
            'Submit Text': SubmitText,
            'Return To Menu': Start,
        }
        self.set_functionality(func)


class Drills(Menu):
    
    def __init__(self, stdscr):
        Menu.__init__(self, stdscr)
        self.stdscr = stdscr
        self.package_functions()
        self.display_screen()

    def package_functions(self):

        def about(self):
            pass

        func = {
            'Bigrams': (DrillsWordList, 'bigrams'),
            'Trigrams': (DrillsWordList, 'trigrams'),
            'Words': (DrillsWordList, 'words'),
            'Return To Menu': Typing,
        }
        self.set_functionality(func)


class DrillsWordList(Menu):
    def __init__(self, stdscr, drill_type = 'words'):
        Menu.__init__(self, stdscr)
        self.stdscr = stdscr
        self.drill_type = drill_type
        self.package_functions()
        self.display_screen()

    def package_functions(self):

        def select_word_list(self):
            file_mappings = {}
            for file in os.listdir("../data/"):
                if file.endswith(".txt"):
                    file_mappings[file] = (DrillsWordAmount, (self.drill_type, file))

            file_mappings['Return To Menu'] = Drills
            return file_mappings
        
        func = select_word_list(self)
        self.set_functionality(func)


class DrillsWordAmount(Menu):
    def __init__(self, stdscr, drill_type = 'words'):
        Menu.__init__(self, stdscr)
        self.stdscr = stdscr
        self.drill_type = drill_type
        self.package_functions()
        self.display_screen()

    def __init__(self, stdscr, args):
        Menu.__init__(self, stdscr)
        self.stdscr = stdscr
        self.drill_type,  self.file = args
        self.package_functions()
        self.display_screen()

    def package_functions(self):

        def prompt_word_amount(self):
            amount = get_word_amount(self)
            return (DrillsWordFilter, (self.drill_type, self.file, amount))

        def get_word_amount(self):
            self.stdscr.clear()
            amount = ''
            curses.curs_set(2)
            while True:
                self.stdscr.addstr(0, 0, 'Enter The Amount Of Words To Type: ')
                self.stdscr.clrtoeol()
                self.stdscr.addstr(amount)
                char = self.stdscr.get_wch()
                if char.isprintable():
                    amount += char
                elif char == curses.KEY_BACKSPACE or char == '\x7f':
                    amount = amount[:-1]
                elif char == curses.KEY_ENTER or char == '\n':
                    try:
                        amount = int(amount)
                    except:
                        amount = ''
                    else:
                        break
            self.stdscr.clear()
            return int(amount)


        func = {
            'Words Amount': prompt_word_amount(self),
            'Return To Menu': Typing,
        }

        self.set_functionality(func)


class DrillsWordFilter(Menu):
    def __init__(self, stdscr, args):
        Menu.__init__(self, stdscr)
        self.stdscr = stdscr
        self.drill_type, self.file, self.word_amount = args
        self.package_functions()
        self.display_screen()

    def package_functions(self):

        def display_words(self):
            filtered_letters = get_filter_letters(self)
            displayed_words = TypingDrills(self.drill_type, self.file, self.word_amount, filtered_letters)
            return (TextDisplayer, ' '.join(displayed_words.words))

        def get_filter_letters(self):
            self.stdscr.clear()
            filter_letters = ''
            curses.curs_set(2)
            while True:
                self.stdscr.addstr(0, 0, 'Enter The Starting Letters To Use Or Enter Blank For All: ')
                self.stdscr.clrtoeol()
                self.stdscr.addstr(filter_letters)
                char = self.stdscr.get_wch()
                if char.isprintable():
                    filter_letters += char
                elif char == curses.KEY_BACKSPACE or char == '\x7f':
                    filter_letters = filter_letters[:-1]
                elif char == curses.KEY_ENTER or char == '\n':
                    break
            self.stdscr.clear()
            return filter_letters

        def about(self):
            pass

        func = {
            'Filtered Words': display_words(self),
            'Return To Menu': Typing,
        }
        self.set_new_screen(Start)
        self.set_functionality(func)


class SubmitText(Menu):
    
    def __init__(self, stdscr):
        Menu.__init__(self, stdscr)
        self.stdscr = stdscr
        self.package_functions()
        self.display_screen()

    def package_functions(self):

        def about(self):
            pass

        func = {
            'Enter URL': (TextDisplayer, 'url'),
            'Paste Clipboard':  (TextDisplayer, 'clipboard'),
            'Return To Typing': Typing,
        }
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

        
class MetaTyping(Menu):
    
    def __init__(self, stdscr):
        Menu.__init__(self, stdscr)
        self.stdscr = stdscr
        self.package_functions()
        self.display_screen()

    def package_functions(self):

        def about(self):
            pass

        func = {
            'Enter URL': (MetaTypingDisplayer, 'url'),
            'Return To Menu': Start,
        }
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
