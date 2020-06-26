import curses
from curses import wrapper
from bs4 import BeautifulSoup
import requests

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
        curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_BLACK)        
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
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
        return key == curses.KEY_ENTER or key in [10, 13]

    def quit(self, key):
        return key == '\x1b'

    def termination(self, key):
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
    def __init__(self, stdscr, message = ''):
        Window.__init__(self, stdscr)
        self.stdscr = stdscr
        self.message = message
        self.setup()
        self.output = self.prompt()

    def prompt(self):
        ''' Text will only show until screen fills'''
        self.stdscr.clear()
        self.cursor_on()
        shown_output = ''
        output = ''
        eol = False
        max_height, max_width = self.stdscr.getmaxyx()
        y, x = self.stdscr.getyx()
        while True:
            # TODO submit bug to python curses that when an enter is used with
            # get_wch and addstr that the y position does not auto increment
            # if you call getyxp
            self.stdscr.attron(curses.color_pair(1))
            self.stdscr.addstr(0, 0, self.message)
            self.stdscr.attron(curses.color_pair(2))
            self.stdscr.addstr(shown_output)
            self.stdscr.clrtoeol()
            self.stdscr.refresh()
            if y + 2 > max_height:
                eol = True 
            char = (self.stdscr.get_wch())
            if char == curses.KEY_BACKSPACE or char == '\x7f':
                output = output[:-1]
                shown_output = shown_output[:-1]
            elif self.termination(char):
                    return output
            elif char == '\n' or repr(char) == '\n':
                y += 1 # these 2 commits show how if enter is typed many times, curses does not register change in y
                if y + 2 > max_height:
                    eol = True
                if not eol:
                    shown_output += (char)
                output += (char)
                #y, x = self.stdscr.getyx() # and will cause line error
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
        self.stdscr = stdscr
        self.static_message = static_message
        self.selection_list = selection_list
        self.selected_row = 0
        self.setup()
        self.display_screen()


    def update_selection_screen(self):
        '''Displays the selection keys with the highlights selected row'''
        def highlight_row(self):
            self.stdscr.attron(curses.color_pair(1))
            self.stdscr.addstr(y + row, 0, selection_name)
            self.stdscr.attron(curses.color_pair(9))

        if self.static_message:
            self.stdscr.addstr(0, 0, self.static_message)
            y, x = self.stdscr.getyx()
            y += 1
            x = 0
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
        return self.selected_row > 0 and (key == curses.KEY_UP or key == ord('k'))

    def move_down(self, key):
        return self.selected_row < len(self.selection_list) - 1 and (key == curses.KEY_DOWN or key == ord('y'))
 
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

def get_text_from_url(stdscr): # -> str
    # TODO checks for valid url outside to scrape
    url = TextWindow(stdscr, message = 'Enter a URL and F4 when done: ').get_output()
    text = scrape_url(url)
    return text

def scrape_url(url): # str -> str
    # TODO will need to recursively call to search for all nested list and paragraphs that may be in a span or div
    text = ''
    if url:
        headers = requests.utils.default_headers()
        headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        wanted_tags = ['p',  'li', 'ul']
        for header in soup.find_all(['h1','h2','h3']):
            # a \h is used to indicate header
            text += header.get_text() + '\h' + '\n'
            for elem in header.next_elements:
                if elem.name and elem.name.startswith('h'):
                    break
                if any([True for tag in wanted_tags if tag == elem.name]):
                    text += elem.get_text() + '\n'
    return text


def get_text_from_clipboard(stdscr): # -> str
    return TextWindow(stdscr, message = 'Paste Clipboard and F4 when done: ').get_output()


def format_text(raw_text, max_line_height, max_line_width):
    '''proccess the text and fits the text the app'''
    filtered_text = filter_text(raw_text) # string -> List[str]
    paragraphs = fit_words_on_screen(filtered_text, max_line_height, max_line_width) # str -> List[List[List[str]]]
    pass
    # ex. paragraphs = [[['paragraph 1 line 1'], ['paragraph 1 line 2']], [['paragraph 2 line 1'], ['paragraph 2 line 2']]]


def filter_text(text): # str -> str
    replace_symbols_mapping = {
        '’': "'",
        '“': '"',
        '”': '"',
        '—':'-',
    }

    # can do a perf test to see if one full iteration with multiple checks is better
    for symbol in replace_symbols_mapping.keys():
        if symbol in text:
            text = text.replace(symbol, replace_symbols_mapping[symbol])
    return text


def fit_words_on_screen(text, max_line_height, max_line_width):
    '''Takes in a raw text and applies transforms so the text can be displayed
    - format text to screen
        - format width
        - format hight

    - output
        - List of paragraphs each having a list of lines each having a string
        - List[List[List[str]]]
        ex. paragraphs = 
        [
            [['paragraph 1 line 1'], ['paragraph 1 line 2']],
            [['paragraph 2 line 1'], ['paragraph 2 line 2']],
        ]
    '''
    def divide_chunks_by_width(paragraph, max_line_width):
        line = ''
        words = paragraph.split()
        header = False
        if paragraph[-2:] == '\h':
            header = True
        for idx, word in enumerate(words):
            if len(line) + len(word) + 1 < max_line_width:
                line += word + ' '
            else:
                if header:
                    line += '\h'
                yield line
                line = word + ' '
            if idx == len(words) - 1:
                yield line

    def divide_chunks_by_height(paragraphs, max_line_height):
        if len(paragraphs) < max_line_height:
            yield paragraphs
        else:
            for idx in range(0, len(paragraphs), max_line_height):
                yield paragraphs[idx:idx + max_line_height]

    paragraphs = text.split('\n')
    paragraph_fitted_on_screen = []
    for paragraph in paragraphs:
        paragraph_by_width = [*divide_chunks_by_width(paragraph, max_line_width)]
        paragraph_fitted_on_screen.append([*divide_chunks_by_height(paragraph_by_width, (max_line_height))])
    return paragraph_fitted_on_screen
