import curses
from timeit import default_timer as timer
from bs4 import BeautifulSoup
import requests
import spacy


class MetaTypingDisplayer:
    def __init__(self, stdscr, input_type = None):
        '''
            Meta Typing take a input string of a url or clipboard.
            The text is then fit on screen and important words are colored
            The user then types the colored words and quickly reads the others

            Lines can be changed with up and down arrow
            Pages can be changed with left and right arrow
        '''
        self.stdscr = stdscr
        self.text = self.get_text(input_type)
        self.setup()
        self.draw()

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

    def get_text(self, input):
        if input == 'url':
            text = self.get_url()
        elif input == 'clipboard':
            text = self.get_clipboard()
        else:
            text = input
        return text            

    def get_clipboard(self):
        text = ''
        self.stdscr.clear()
        curses.curs_set(2)
        while True:
            self.stdscr.addstr(0, 0, 'Paste Text and enter F4 when done: ')
            char = self.stdscr.get_wch()
            if isinstance(char, str) and char.isprintable():
                text += char
            elif char == curses.KEY_ENTER or char == '\n':
                text += '\n'
            if char == curses.KEY_F4:
                break
        return text


    def get_url(self):

        self.stdscr.clear()
        url = ''
        curses.curs_set(2)
        while True:
            self.stdscr.addstr(0, 0, 'Enter a URL: ')
            self.stdscr.clrtoeol()
            self.stdscr.addstr(url)
            char = self.stdscr.get_wch()
            if char.isprintable():
                url += char
            elif char == curses.KEY_BACKSPACE or char == '\x7f':
                url = url[:-1]
            elif char == curses.KEY_ENTER or char == '\n':
                break
        self.stdscr.clear()
                
        text = ''
        headers = requests.utils.default_headers()
        headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
        #url = "https://towardsdatascience.com/build-your-first-open-source-python-project-53471c9942a7"
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        wanted_tags = ['p',  'li', 'ul']
        for header in soup.find_all(['h1','h2','h3']):
            text += header.get_text()+ '\h' + '\n'
            for elem in header.next_elements:
                if elem.name and elem.name.startswith('h'):
                    break
                if any([True for tag in wanted_tags if tag == elem.name]):
                    text += elem.get_text() + '\n'
        return text.split('\n')

    def Meta_type(self, doc):
        nlp = spacy.load('en_core_web_sm')
        max_line_pos, max_char_pos = self.stdscr.getmaxyx()
        char_pos = 0
        line_pos = 0
        self.stdscr.move(line_pos, char_pos)

        total_char_on_line = 0
        for paragraph in doc:
            header = False
            if paragraph[-2:] == '\h':
                header = True
                paragraph = paragraph[:-2]
            tokens = nlp(paragraph)
            if header:
                line_pos = 0
                x = self.stdscr.get_wch()
                self.stdscr.clear()
            elif line_pos + 2 < max_line_pos:
                line_pos += 2
            else:
                line_pos = 0
                x = self.stdscr.get_wch()
                self.stdscr.clear()
            char_pos = 0
            total_char_on_line = 0
            self.stdscr.move(line_pos, char_pos)

            
            for idx, token in enumerate(tokens):
                if total_char_on_line + len(str(token.text_with_ws)) < max_char_pos:
                    total_char_on_line += len(str(token.text_with_ws))
                else:
                    total_char_on_line = len(str(token.text_with_ws))
                    char_pos = 0
                    if line_pos + 2 < max_line_pos:
                        line_pos += 2
                    else:
                        line_pos = 0
                        x = self.stdscr.get_wch()
                        self.stdscr.clear()
                        # Typing goes here, will need to change to while loop so I can go backwards and type

                    self.stdscr.move(line_pos, char_pos)
                if header:
                    self.stdscr.attron(curses.color_pair(6))
                elif token.pos_ == 'NUM':
                    self.stdscr.attron(curses.color_pair(1))
                elif token.pos_ == 'PROPN':
                    self.stdscr.attron(curses.color_pair(1))
                elif token.pos_ == 'ADJ':
                    self.stdscr.attron(curses.color_pair(2))
                elif token.pos_ == 'NOUN':
                    self.stdscr.attron(curses.color_pair(3))
                elif token.pos_ == 'VERB' or token.pos_ == 'PART':
                    self.stdscr.attron(curses.color_pair(4))
                else:
                    self.stdscr.attron(curses.color_pair(5))
                
                self.stdscr.addstr(line_pos, char_pos, str(token.text_with_ws))
                char_pos += len(str(token.text_with_ws))


    def draw(self):
        words = self.text
        self.Meta_type(words)
