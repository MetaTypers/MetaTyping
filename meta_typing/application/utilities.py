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
        self.stdscr = stdscr
        self.message = message
        self.termination_trigger = termination_trigger
        self.setup()
        self.output = self.prompt()

    def get_termination_trigger(self, char):
        if self.termination_trigger == 'enter' and self.enter(char):
            return True
        elif self.termination_trigger == 'f4' and self.f4(char):
            return True
        else:
            return False

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
            elif self.get_termination_trigger(char):
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

    def get_selected_response(self):
        return self.selection_list[self.selected_row]

class StaticWindow(Window):
    def __init__(self, stdscr, text):
        self.stdscr = stdscr
        self.text = text
        self.prompt()

    def prompt(self):
        self.stdscr.clear()
        max_line_height, max_line_width = self.stdscr.getmaxyx()
        screens = fit_words_on_screen(self.text, max_line_height, max_line_width)
        for screen in screens:
            x = 0
            y = 0
            self.stdscr.move(y, x)
            for lines in screen:
                self.stdscr.addstr(y, x, lines)
                y += 1
                x = 0
            key = self.stdscr.getch()
            while not self.enter(key):
                key = self.stdscr.getch()
            self.stdscr.clear()

def get_text_from_url(stdscr): # -> str
    # TODO checks for valid url outside to scrape
    # TODO add a trigger option for enter instead of F4 for this case
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
            text += header.get_text() + ' \h' + '\n'
            for elem in header.next_elements:
                if elem.name and elem.name.startswith('h'):
                    break
                if any([True for tag in wanted_tags if tag == elem.name]):
                    text += elem.get_text() + '\n'
    return text


def get_text_from_clipboard(stdscr): # -> str
    return TextWindow(stdscr, message = 'Paste Clipboard and F4 when done: ', termination_trigger = 'f4').get_output()


def format_text(raw_text, max_line_height, max_line_width):
    '''proccess the text and fits the text the app'''
    filtered_text = filter_text(raw_text) # str -> str
    paragraphs = fit_words_on_screen(filtered_text, max_line_height, max_line_width) # str -> List[List[str]]
    return paragraphs

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

def safe_split(sentence): # str -> List[word:str]
    '''used to retains multiple space values'''
    words = []
    word = ''
    for char in sentence:
        if char == ' ':
            if word:
                words.append(word)
                word = ''
            words.append(char)
        else:
            word += char
    if word:
        words.append(word)
    return words

def fit_words_on_screen(doc, max_line_height, max_line_width):
    '''Takes in a raw text and applies transforms so the text can be displayed
    - format text to screen
        - format width
        - format hight

    - output
        - List of screen each having a list of lines having a string
        - List[List[str]]
    '''
    def divide_text_by_width(doc, max_line_width):
        paragraphs = doc.split('\n')
        essay = []
        for paragraph in paragraphs:
            line = ''
            words = safe_split(paragraph)
            header = False
            if paragraph[-2:] == '\h':
                header = True
            for idx, word in enumerate(words):
                if len(line) + len(word) + 2 < max_line_width:
                    line += word + ''
                else:
                    if word == ' ':
                        line += word
                    if header:
                        line += "\h"
        
                    essay.append(line)
                    if word == ' ':
                        line = ''
                    else:
                        line = word + ''
                        
                if idx == len(words) - 1:
                    essay.append(line)
        return essay

    def divide_text_by_height(essay, max_line_height):
        screens = []
        screen = []
        for idx, line in enumerate(essay):

            if line[-2:] == '\h':
                if screen: # header starts at top
                    screens.append(screen)
                    screen = []
                screen.append(line)
            else:
                if len(screen) < max_line_height:
                    screen.append(line)
                else:
                    screens.append(screen)
                    screen = []
                    screen.append(line)
            if idx == len(essay) - 1:
                if screen:
                    screens.append(screen)
        return screens

    long_screen = divide_text_by_width(doc, max_line_width)
    screens = divide_text_by_height(long_screen, max_line_height)
    return screens

def analyze_word_time_log(stdscr, word_time_log): # List[Tuple[str, int, bool]] -> None
    '''collects stats from the word_time_log and displayed them'''
    word_stats_feedback, slowest_words = get_word_stats_feedback(word_time_log)
    StaticWindow(stdscr, text = word_stats_feedback)
    return slowest_words

def get_word_stats_feedback(word_time_log): # List[Tuple[str, int, bool]] -> str
    '''returns a stats page summarizing the typed words log'''
    
    def get_fastest_words():
        fastest_words = time_sorted[-WORDS_VIEWED:]
        fastest_words_string = ', '.join([str({ele[TYPED_WORD]: ele[TYPED_TIME]}) for ele in fastest_words[::-1]])
        return fastest_words_string
    
    def get_slowest_words():
        slowest_words = time_sorted[:WORDS_VIEWED]
        slowest_words_string = ', '.join([str({ele[TYPED_WORD]: ele[TYPED_TIME]}) for ele in slowest_words])
        slowest_word_stats = [ele[TYPED_WORD] for ele in slowest_words]
        return slowest_words_string, slowest_word_stats
    
    def get_slowest_correct_words():
        correct_words = [word for word in word_time_log if word[TYPED_CORRECTLY]]
        correct_words_sorted = sorted(correct_words, key = lambda x: int(x[TYPED_TIME]))
        slowest_correct_words = correct_words_sorted[:WORDS_VIEWED]
        slowest_correct_words_string = ', '.join([str({ele[TYPED_WORD]: ele[TYPED_TIME]}) for ele in slowest_correct_words])
        slowest_correct_words_stats = [ele[TYPED_WORD] for ele in slowest_correct_words]
        return slowest_correct_words_string, slowest_correct_words_stats
    
    def get_wpm():
        return str(sum([int(time) for word, time, accuracy in time_sorted])/len(time_sorted))
    
    def get_accuracy():
        return str(100 * sum([accuracy for word, time, accuracy in time_sorted])/len(time_sorted))
    
    def summarize():
        typed_words_summary = f'Words Typed Summary,\n'\
                              f'Average WPM: {wpm},\n'\
                              f'Typing Accuracy: {accuracy},\n'\
                              f'Fastest typed words: {fastest_words},\n'\
                              f'Slowest typed words: {slowest_words},\n'\
                              f'Slowest correctly typed words: {slowest_correct_words}'
        return typed_words_summary
    
    TYPED_WORD, TYPED_TIME, TYPED_CORRECTLY, WORDS_VIEWED = 0, 1, 2, 5
    time_sorted = sorted(word_time_log, key = lambda x: int(x[TYPED_TIME]))
    wpm = get_wpm()
    accuracy = get_accuracy()
    fastest_words = get_fastest_words()
    slowest_words, slowest_word_stats = get_slowest_words()
    slowest_correct_words, slowest_correct_words_stats = get_slowest_correct_words()
    typed_words_summary = summarize()
    slowest_words_set = list(set(slowest_word_stats + slowest_correct_words_stats))
    return typed_words_summary, slowest_words_set
   