import curses
from timeit import default_timer as timer
from application.utilities import get_text_from_url, get_text_from_clipboard
from application.utilities import format_text, SelectionWindow, analyze_word_time_log
from application.typing_drills import TypingDrills
from application.settings_app import apply_setting


class TypingApp:
    '''This class contains a pipline for running the Typing application
    using utilities, windows and typing drills.
    '''
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.setup()
        self.start_up()

    def setup(self):
        self.stdscr.clear()
        apply_setting()
        self.stdscr.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)
        self.stdscr.clear()
        self.stdscr.attron(curses.color_pair(1))
        curses.curs_set(2)

    def start_up(self):
        '''combines all the typing application components that execute on start'''
        text = self.get_text()
        formatted_text = self._format_text(text)
        char_time_log, word_time_log = self.type_text(formatted_text)
        slowest_words = analyze_word_time_log(self.stdscr, word_time_log)
        self.type_slowest_words(slowest_words)

    def get_text(self):
        '''user selects an input method that executes to get text from'''
        input_type = self.get_input_type()
        if input_type == 0: # 'drills':
            text = self._get_text_from_drills()
        elif input_type == 1: # 'url':
            text = self._get_text_from_url()
        elif input_type == 2: # 'clipboard':
            text = self._get_text_from_clipboard()
        else: # should there be a way to go back to menu?
            pass
        return text

    def get_input_type(self):
        '''creates a window for the user to select an input type'''
        input_text_types = ['Typing Drills', 'Type from URL', 'Type from Clipboard']
        input_text_types_window = SelectionWindow(self.stdscr, selection_list = input_text_types)
        selected_input_option = input_text_types_window.get_selected_row() # returns row value
        return selected_input_option

    def _get_text_from_drills(self):
        '''gets the requirements from the user to select a drill'''
        typing_drill = TypingDrills(self.stdscr)
        return typing_drill.get_word_drill()
        pass

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

    def type_text(self, screens):
        '''text is displayed for the user to type while recording input'''
        # TODO refactor, add ways to move up/down lines and left/right pages
        # TODO add a log file to store data over time
        self.setup()
        curses.curs_set(2)
        char_time_log = []
        word_time_log = []
        self.stdscr.attron(curses.color_pair(1))
        for screen in screens:
            self.stdscr.clear()
            y, x = 0, 0
            for lines in screen:
                if lines[-2:] == '\h':
                    lines_no_header = lines[:-2]
                    self.stdscr.attron(curses.color_pair(6))
                    self.stdscr.addstr(y, x,  lines_no_header + ' ')
                else:
                    self.stdscr.attron(curses.color_pair(1))
                    self.stdscr.addstr(y, x, lines)
                x = 0
                y += 2

            self.stdscr.move(0, 0)
            y, x = 0, 0

            for lines in screen: # this loop displayed the text on screen
                if lines[-2:] == '\h':
                    lines = lines[:-2]
                    self.stdscr.attron(curses.color_pair(6))
                    self.stdscr.addstr(y, x,  lines + ' ')
                else:
                    self.stdscr.attron(curses.color_pair(1))
                    self.stdscr.addstr(y, x, lines)

                self.stdscr.addstr(y, x, lines)
                self.stdscr.move(y, x)

                letters = ''
                good_accuracy_word = []
                for idx, letter in enumerate(lines): # loop where for typing
                    good_accuracy = True
                    char = self.stdscr.get_wch()
                    if idx == 0:
                        char_len = 1
                        start_word = timer()
                    start_time = timer()
                    while char != letter and char != '`':
                        char = self.stdscr.get_wch()
                        if char == '\x1b': # esc key
                            return char_time_log, word_time_log
                        good_accuracy = False
                    if char == '`': # an autoskip for not typable char
                        char = letter
                    end_time = timer()
                    delta = end_time - start_time
                    letters += letter
                    good_accuracy_word.append(good_accuracy)
                    char_time_log.append((char, delta, good_accuracy))
                    if char == ' ' or idx == len(lines) - 1:
                        end_word = timer()
                        delta_word = end_word - start_word
                        wpm = str(round((60 / (delta_word / char_len))/5))
                        if char_len > 2:
                            self.stdscr.addstr(y+1, x-char_len + 1, wpm, curses.color_pair(2))
                        char_len = 1
                        word_time_log.append((letters, wpm, all(good_accuracy_word)))
                        letters = ''
                        good_accuracy_word = []
                        start_word = timer()
                    else:
                        char_len += 1
                    if x + 1 < len(lines):  
                        x += 1

                    self.stdscr.move(y, x)
                x = 0
                y += 2
        return char_time_log, word_time_log

    def type_slowest_words(self, slowest_words):
        '''allows user the option to improve on there slowest words'''
        response = self.ask_to_type_slowest_words()
        if response:
            text = self.prepare_slowest_words_text(slowest_words)
            formatted_text = self._format_text(text)
            char_time_log, word_time_log = self.type_text(formatted_text)
            slowest_words = analyze_word_time_log(self.stdscr, word_time_log)

    def prepare_slowest_words_text(self, slowest_words):
        '''small drill to improve slowest words through repetition cycling'''
        slowest_words = [word.strip() for word in slowest_words]
        exercise_words = []
        word_q = []
        while slowest_words:
            word_p = slowest_words.pop(0)
            for j in range(2):
                for i in range(2):
                    for w in word_q:
                        exercise_words.append(w)
                for k in range(j + 1):
                    exercise_words.append(word_p)
            word_q.append(word_p)
        return ' '.join(exercise_words)

        
    def ask_to_type_slowest_words(self):
        '''optional improvement typing window prompts'''
        question = 'Would you like work on your slowest typed words?'
        options = ['No', 'Yes']
        boolean_window = SelectionWindow(self.stdscr, static_message = question, selection_list = options)
        response = boolean_window.get_selected_row()
        return response
