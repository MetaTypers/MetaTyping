import curses
from bs4 import BeautifulSoup
import requests


class SpeedReadingDisplayer:
    def __init__(self, stdscr, input_type = None):
        self.stdscr = stdscr
        self.text = self.get_text(input_type)
        self.speed = 300
        self.char_width = 9
        self.position = 0
        self.setup()
        self.draw()


    def setup(self):
        self.stdscr.clear()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.stdscr.attron(curses.color_pair(1))
        curses.curs_set(2)

    def get_text(self, input):
        if input == 'url':
            text = self.get_url()
        elif input == 'clipboard':
            text = self.get_clipboard()
        else:
            raise # error
        return text            

    def get_clipboard(self):
        text = ''
        self.stdscr.clear()
        curses.curs_set(0)
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
        curses.curs_set(0)
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
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        wanted_tags = ['p',  'li', 'ul']
        for header in soup.find_all(['h1','h2','h3']):
            text += header.get_text() + '\n'
            for elem in header.next_elements:
                if elem.name and elem.name.startswith('h'):
                    break
                if any([True for tag in wanted_tags if tag == elem.name]):
                    text += elem.get_text() + '\n'
        return text


    def speed_up(self, key):
        return key == curses.KEY_UP

    def speed_down(self, key):
        return self.speed > 0 and key == curses.KEY_DOWN

    def increase_char_width(self, key):
        return key == curses.KEY_RIGHT

    def decrease_char_width(self, key):
        return self.char_width > 0 and key == curses.KEY_LEFT

    def move_backward(self, key):
        return self.position - 10 > 0 and key == ord('b')

    def move_forward(self, key):
        return self.position + 10 < len(self.words) and key == ord('f')
 
    def space(self, key):
        return key == ord(' ')
    
    def display_words(self):
        max_y, max_x = self.stdscr.getmaxyx()
        self.stdscr.clear()
        curses.curs_set(0)
        self.stdscr.move(max_y//2, max_x//2 - (self.char_width//2))
        word = ''
        while True:
            if self.position + 1 >= len(self.words):
                self.stdscr.addstr(max_y//2, max_x//2 - self.char_width, word)
                break
            elif len(word) == 0 or len(word) + len(self.words[self.position]) <= self.char_width:
                word += self.words[self.position] + ' '
                self.position += 1
            else:
                self.stdscr.addstr(max_y//2, max_x//2 - (self.char_width//2), word)
                word = ''
                return

    def display_screen(self):
        self.stdscr.nodelay(1)
        self.stdscr.timeout(self.speed)
        
        while True:
            self.display_words()
            curses.delay_output(self.speed)
            key = self.stdscr.getch()
            if self.speed_up(key):
                self.speed -= 10
                self.stdscr.timeout(self.speed)
            elif self.speed_down(key):
                self.speed += 10
                self.stdscr.timeout(self.speed)
            elif self.increase_char_width(key):
                self.char_width += 1
            elif self.decrease_char_width(key):
                self.char_width -= 1
            elif self.move_backward(key):
                self.position -= 10
            elif self.move_forward(key):
                self.position += 10
            elif self.space(key):
                self.stdscr.nodelay(0)
                x = self.stdscr.getch()
                self.stdscr.nodelay(1)
                self.stdscr.timeout(self.speed)
            elif key == '\x1b':
                return

            if self.position + 1 == len(self.words):
                self.stdscr.clear()
                break

    def draw(self):
        self.words = self.text.split()
        self.display_screen()

