import curses
from timeit import default_timer as timer
from bs4 import BeautifulSoup
import requests
import spacy
from application.utilities import get_text_from_url, get_text_from_clipboard, safe_split
from application.utilities import format_text, SelectionWindow

class MetaTypingApp:
    def __init__(self, stdscr):
        ''''''
        self.stdscr = stdscr
        self.nlp = spacy.load('en_core_web_sm')
        self.setup()
        self.start_up()

    def setup(self):
        self.stdscr.clear()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        self.stdscr.attron(curses.color_pair(0))
        curses.curs_set(2)

    def start_up(self):
        '''combines all the typing application components that execute on start'''
        text = self.get_text()
        formatted_text = self._format_text(text)
        self.meta_type(formatted_text)

    def get_text(self):
        '''user selects an input method that executes to get text from'''
        input_type = self.get_input_type()
        if input_type == 0: # 'url':
            text = self._get_text_from_url()
        elif input_type == 1: # 'clipboard':
            text = self._get_text_from_clipboard()
        else: # should there be a way to go back to menu?
            pass
        return text

    def get_input_type(self):
        '''creates a window for the user to select an input type'''
        input_text_types = ['Type from URL', 'Type from Clipboard']
        input_text_types_window = SelectionWindow(self.stdscr, selection_list = input_text_types)
        selected_input_option = input_text_types_window.get_selected_row() # returns row value
        return selected_input_option

    def _get_text_from_url(self):
        '''gets the url from the user to request the text'''
        return get_text_from_url(self.stdscr)

    def _get_text_from_clipboard(self):
        '''gets the clipboard from the user as input text'''
        return get_text_from_clipboard(self.stdscr)

    def _format_text(self, raw_text):
        '''proccess the text and fits the text to the screen'''
        max_line_height, max_line_width = self.stdscr.getmaxyx()
        return format_text(raw_text, max_line_height // 2, max_line_width)

    def nlp_process(self, sentence): # str -> List[Tuple(token, tag)]
        '''returns the original text with a POS parts of speech tag'''
        tokenized_sentence = []
        for word in safe_split(sentence):
            tokens = self.nlp(word)
            for token in tokens:
                tokenized_sentence.append((token.text, token.pos_))
        return tokenized_sentence

    def meta_type(self, screens):
        '''text is displayed for the user to type while recording input'''
        # TODO refactor, add ways to move up/down lines and left/right pages
        self.stdscr.clear()
        curses.curs_set(2)
        char_time_log = []
        word_time_log = []
        tag_list = ['NUM','PROPN', 'ADJ', 'NOUN', 'VERB', 'PART', 'HEADER']

        self.stdscr.attron(curses.color_pair(1))
        for screen in screens:
            self.stdscr.clear()
            y, x = 0, 0
            y_max, x_max = self.stdscr.getmaxyx()
            tokenized_screen = []
            for lines in screen:
                header = False
                if lines[-2:] == '\h':
                    header = True
                tokenized_line = self.nlp_process(lines)
                tokenized_screen.append(tokenized_line)
                words = ''
                for idx, (word, tag) in enumerate(tokenized_line):
                    if tag == 'NUM':
                        self.stdscr.attron(curses.color_pair(1))
                    elif tag == 'PROPN':
                        self.stdscr.attron(curses.color_pair(1))
                    elif tag == 'ADJ':
                        self.stdscr.attron(curses.color_pair(2))
                    elif tag == 'NOUN':
                        self.stdscr.attron(curses.color_pair(3))
                    elif tag == 'VERB' or tag == 'PART':
                        self.stdscr.attron(curses.color_pair(4))
                    else:
                        self.stdscr.attron(curses.color_pair(5))

                    if header:
                        self.stdscr.attron(curses.color_pair(6))
                        if tag != 'SPACE':
                            tokenized_line[idx] = (word, 'HEADER')
                        if word[-2:] == '\h':
                            self.stdscr.addstr(y, x, str(word[:-2]))
                            tokenized_line[idx] = (word[:-2], 'HEADER')
                        else:
                            self.stdscr.addstr(y, x, str(word))
                    else:
                        self.stdscr.addstr(y, x, str(word))
                    x += len(word)
                self.stdscr.addstr(y, x, ' ')
                x = 0
                y += 2

            self.stdscr.move(0, 0)
            y, x = 0, 0

            for tokenized_line in tokenized_screen:
                for end, (word, tag) in enumerate(tokenized_line):
                    self.stdscr.move(y, x)
                    if tag in tag_list:
                        letters = ''
                        for idx, letter in enumerate(word):
                            char = self.stdscr.get_wch()
                            while char != letter:
                                char = self.stdscr.get_wch()
                                if char == '`': # an autoskip
                                    char = letter
                                if char == '\x1b': # esc key
                                    return
                                letters += letter
                            letters = ''

                            if x + 1 < x_max:  
                                x += 1
                            self.stdscr.move(y, x)
                            if idx == len(word) - 1:
                                space = self.stdscr.get_wch()
                                while space != ' ' and space != '`':
                                    space = self.stdscr.get_wch()
                            
                    else:
                        x += len(word)
                        self.stdscr.move(y, x)
                x = 0
                y += 2
