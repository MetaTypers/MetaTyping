import curses
from timeit import default_timer as timer
from bs4 import BeautifulSoup
import requests


class TypingDisplayer:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.setup()
        self.start_up()

    def setup(self):
        self.stdscr.clear()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.stdscr.attron(curses.color_pair(1))
        curses.curs_set(2)

    def start_up(self):
        '''combines all the typing application components that execute on start'''
        text = self.get_text()
        formatted_text = self.format_text(text) # a utilities function
        char_time_log, word_time_log = self.type_text(formatted_text)
        analyze_results()

    def get_text(self):
        '''user selects an input method that executes to get text from'''
        input_type = self.get_input_type()
        if input_type == 0: # 'drills':
            text = self.get_text_from_drills(input_type)
        elif input_type == 1: # 'url':
            text = self.get_text_from_url(input_type)
        elif input_type == 2: # 'clipboard':
            text = self.get_text_from_clipboard(input_type)
        else: # triggers exit
            pass
        return                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

    def get_input_type(self):
        '''creates a window for the user to select an input type'''
        input_text_types = ['Typing Drills', 'Type from URL', 'Type from Clipboard']
        input_text_types_window = SelectionWindow(input_text_types)
        selected_input_option = input_text_types_window.get_response() # returns row value
        return selected_input_option

    def get_text_from_drills(self):
        '''gets the requirements from the user to select a drill'''
        # Prompts the typing drills class
        pass

    def get_text_from_url(self):
        '''gets the url from the user to request the text'''
        # uses the get_text_from_url function in utilities
        pass

    def get_text_from_clipboard(self):
        '''gets the clipboard from the user as input text'''
        # uses the get_text_from_clipboard function in utilities 
        pass
    
    def format_text(self):
        '''proccess the text and fits the text to the screen'''
        # gets the format_text from utilities
        pass

    def type_text(self):
        '''text is displayed for the user to type while recording input'''
        pass

    def analyze_results(self):
        '''analyze and displays the stats'''
        word_stats = get_word_stats()
        formatted_word_stats = format_word_stats(word_stats)
        display_word_stats(formatted_word_stats)
        pass

    def get_word_stats(self):
        '''applies wpm stats for fastest, slowest, and slowest correct words'''
        pass

    def format_word_stats(self):
        '''formats the word stats to fit on screen'''
        words = process_stats()
        paragraphs = fit_words_on_screen() # utilities function
        pass

    def process_stats(self):
        ''''''
        pass

    def display_word_stats(self):
        '''user navigates stats in window and exits'''
        pass



    # def get_text(self, input):
    #     if input == 'url':
    #         text = self.get_url()
    #     elif input == 'clipboard':
    #         text = self.get_clipboard()
    #     else:
    #         text = input
    #     return text            

    # def get_clipboard(self):
    #     text = ''
    #     self.stdscr.clear()
    #     curses.curs_set(2)
    #     while True:
    #         self.stdscr.addstr(0, 0, 'Paste Text and enter F4 when done: ')
    #         char = self.stdscr.get_wch()
    #         if isinstance(char, str) and char.isprintable():
    #             text += char
    #         elif char == curses.KEY_ENTER or char == '\n':
    #             text += '\n'
    #         if char == curses.KEY_F4:
    #             break
    #     return text


    # def get_url(self):

    #     self.stdscr.clear()
    #     url = ''
    #     curses.curs_set(2)
    #     while True:
    #         self.stdscr.addstr(0, 0, 'Enter a URL: ')
    #         self.stdscr.clrtoeol()
    #         self.stdscr.addstr(url)
    #         char = self.stdscr.get_wch()
    #         if char.isprintable():
    #             url += char
    #         elif char == curses.KEY_BACKSPACE or char == '\x7f':
    #             url = url[:-1]
    #         elif char == curses.KEY_ENTER or char == '\n':
    #             break
    #     self.stdscr.clear()
                
    #     text = ''
    #     headers = requests.utils.default_headers()
    #     headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
    #     req = requests.get(url, headers)
    #     soup = BeautifulSoup(req.content, 'html.parser')
    #     wanted_tags = ['p',  'li', 'ul']
    #     for header in soup.find_all(['h1','h2','h3']):
    #         text += header.get_text() + '\n'
    #         for elem in header.next_elements:
    #             if elem.name and elem.name.startswith('h'):
    #                 break
    #             if any([True for tag in wanted_tags if tag == elem.name]):
    #                 text += elem.get_text() + '\n'
    #     return text

    # def fit_text_on_screen(self, words):
    #     ymax, xmax = self.stdscr.getmaxyx()
    #     paragraphs = []
    #     lines = []
    #     line_buffer = []
    #     total_char = 0
    #     for idx, word in enumerate(words):
    #         if word == '\n':
    #             lines.append(line_buffer)
    #             line_buffer = []
    #             total_char = 0
    #         elif total_char + len(word) + 1 < xmax:
    #             line_buffer.append(word)
    #             total_char += len(word) + 1
    #         else:
    #             line_buffer[-1] += ' '
    #             lines.append(line_buffer)
    #             line_buffer = []
    #             line_buffer.append(word)
    #             total_char = len(word) + 1

    #         if len(lines) * 2 >= ymax:
    #             paragraphs.append(lines)
    #             lines = []

    #         if idx == len(words) - 1:
    #             # last element
    #             lines.append(line_buffer)
    #             paragraphs.append(lines)
    #     return paragraphs

    # def type_paragraphs(self, paragraphs):
        
    #     char_time_log = []
    #     word_time_log = []
    #     for paragraph in paragraphs:
    #         self.stdscr.move(0, 0)
    #         self.stdscr.clear()
    #         x = 0
    #         y = 0

    #         for lines in paragraph:
    #             words = ' '.join(lines)
    #             self.stdscr.addstr(y, x, words)
    #             x = 0
    #             y += 2

    #         self.stdscr.move(0, 0)
    #         x = 0
    #         y = 0

    #         for lines in paragraph:
    #             words = ' '.join(lines)
    #             self.stdscr.addstr(y, x, words)
    #             self.stdscr.move(y, x)

    #             letters = ''
    #             good_accuracy_word = []
    #             # input starts here
    #             for idx, letter in enumerate(words):
    #                 good_accuracy = True
    #                 char = self.stdscr.get_wch()
    #                 if idx == 0:
    #                     char_len = 1
    #                     start_word = timer()
    #                 start_time = timer()
    #                 while char != letter:
    #                     char = self.stdscr.get_wch()
    #                     if char == '`':
    #                         # an autoskip for special characters that can not be entered
    #                         char = letter
    #                     if char == '\x1b':
    #                         return char_time_log, word_time_log
    #                     good_accuracy = False
    #                 end_time = timer()
    #                 delta = end_time - start_time
    #                 letters += letter
    #                 good_accuracy_word.append(good_accuracy)
    #                 char_time_log.append((char, delta, good_accuracy))
    #                 if char == ' ' or idx == len(words) - 1:
    #                     end_word = timer()
    #                     delta_word = end_word - start_word
    #                     wpm = str(round((60 / (delta_word / char_len))/5))
    #                     if char_len > 2:
    #                         self.stdscr.addstr(y+1, x-char_len + 1, wpm, curses.color_pair(2))
    #                     char_len = 1
    #                     word_time_log.append((letters, wpm, all(good_accuracy_word)))
    #                     letters = ''
    #                     good_accuracy_word = []
    #                     start_word = timer()
    #                 else:
    #                     char_len += 1
                        

    #                 if x + 1 < len(words):  
    #                     x += 1
    #                 else:
    #                     x = 0
    #                 self.stdscr.move(y, x)
    #             x = 0
    #             y += 2
    #     return char_time_log, word_time_log

    # def replace_symbols(self, doc):
    #     replace_symbols_mapping = {
    #         '’': "'",
    #         '“': '"',
    #         '”': '"',
    #         '—':'-',
    #     }

    #     for symbol in replace_symbols_mapping.keys():
    #         if symbol in doc:
    #             doc = doc.replace(symbol, replace_symbols_mapping[symbol])
    #     return doc

    # def split_words_on_space_and_newline(self, doc):
    #     words = self.replace_symbols(doc)
    #     word_list = []
    #     word = ''
    #     for char in words:
    #         if char == ' ':
    #             if word:
    #                 word_list.append(word)
    #                 word = ''
    #         elif char == '\n':
    #             if word:
    #                 word_list.append(word)
    #             word_list.append('\n')
    #             word = ''
    #         else:
    #             word += char
    #     word_list.append(word)
    #     return word_list

    # def display_word_stats(self, word_time_log):
    #     char = self.stdscr.get_wch()
    #     self.stdscr.clear()
    #     curses.curs_set(0)
    #     time_sorted = sorted(word_time_log, key = lambda x: int(x[1]))
    #     correct_words = [word for word in word_time_log if word[2]]
    #     correct_words_sorted = sorted(correct_words, key = lambda x: int(x[1]))
    #     fastest_words = time_sorted[-5:]
    #     slowest_words = time_sorted[:5]
    #     slowest_correct_words = correct_words_sorted[:5]
    #     average_wpm = sum([int(time) for word, time, accuracy in time_sorted])/len(time_sorted)
    #     average_accuracy = sum([accuracy for word, time, accuracy in time_sorted])/len(time_sorted)
    #     average_stats = f'Average wpm: {str(average_wpm)},  Accuracy: {str(average_accuracy)}'
    #     fastest_words_stats = f'Fastest Words: {str(fastest_words)}'
    #     slowest_words_stats = f'Slowest Words: {str(slowest_words)}'
    #     slowest_correct_words_stats = f'Slowest Correct Words: {str(slowest_correct_words)}'
    #     self.stdscr.move(0, 0)
    #     self.stdscr.addstr(0, 0, average_stats)
    #     self.stdscr.addstr(1, 0, fastest_words_stats)
    #     self.stdscr.addstr(2, 0, slowest_words_stats)
    #     self.stdscr.addstr(3, 0, slowest_correct_words_stats)
    #     char = self.stdscr.get_wch()
    #     self.stdscr.clear()

    # def draw(self):
    #     words = self.split_words_on_space_and_newline(self.text)
    #     paragraphs = self.fit_text_on_screen(words)
    #     char_time_log, word_time_log = self.type_paragraphs(paragraphs)
    #     self.display_word_stats(word_time_log)

