import curses
from curses import wrapper
from bs4 import BeautifulSoup
import requests

from application.windows import TextWindow

def get_text_from_url(stdscr):
    url = TextWindow(stdscr, message = 'Enter a URL and F4 when done: ').get_output()
    text = scrape_url(url)
    return text

def scrape_url(url):
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


def get_text_from_clipboard(stdscr):
    return TextWindow(stdscr, message = 'Paste Clipboard and F4 when done: ').get_output()

def format_text(self):
    '''proccess the text and fits the text the app'''
    words = process_text()
    paragraphs = fit_words_on_screen()
    pass

def process_text(self):
    '''filters the text and breaks the text into words'''
    filtered_text = filter_text()
    split_words = split_text()
    pass


def filter_text(self):
    '''replaces slightly altered symbols to their equivalent form'''
    pass

def split_text(self):
    '''splits the words by space, newlines and headerlines'''
    pass

def fit_words_on_screen(self):
    '''divides the words into screen paragraphs'''
    pass


def fit_text(doc, max_line_height, max_char_width):
    '''Takes in a raw text and applies transforms so the text can be displayed
    - format text to screen
        - format width
        - format hight

    - output
        - screens of lines or words: screens[lines[words]]
    '''
    def divide_chunks_by_width(paragraph, max_char_width):
        line = ''
        words = paragraph.split()
        header = False
        if paragraph[-2:] == '\h':
            header = True
        for idx, word in enumerate(words):
            if len(line) + len(word) + 1 < max_char_width:
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

    paragraphs = doc.split('\n')
    paragraph_fitted_on_screen = []
    for paragraph in paragraphs:
        paragraph_by_width = [*divide_chunks_by_width(paragraph, max_char_width)]
        paragraph_fitted_on_screen.append([*divide_chunks_by_height(paragraph_by_width, (max_line_height))])
    return paragraph_fitted_on_screen

def analyze_text():
    pass
