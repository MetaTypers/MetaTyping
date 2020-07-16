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
        self.char_time_log = []
        self.word_time_log = []
        self.x = 0
        self.y = 0
        self.start_up()

    def setup(self):
        self.stdscr.clear()
        apply_setting()
        self.stdscr.bkgd(' ', curses.color_pair(1))
        self.stdscr.clear()
        self.stdscr.attron(curses.color_pair(1))
        curses.curs_set(2)
        
    def start_up(self):
        '''combines all the typing application components that execute on start'''
        text = self.get_text()
        formatted_text = self._format_text(text)
        self.type_text(formatted_text)
        slowest_words = analyze_word_time_log(self.stdscr, self.word_time_log)
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

    def type_line(self, line):
        self.x = 0
        self.stdscr.addstr(self.y, self.x, line) 
        self.stdscr.move(self.y, self.x)
        letters = ''
        good_accuracy_word = [] # checks if every char was typed correctly
        for idx, letter in enumerate(line): # loop where for typing
            good_accuracy = True
            char = self.stdscr.get_wch()
            if idx == 0:
                char_len = 1
                start_word = timer()
            start_time = timer()
            while char != letter and char != '`':
                if char == curses.KEY_DOWN:
                    return 'next line'
                if char == curses.KEY_UP:
                    return 'prev line'
                if char == curses.KEY_RIGHT:
                    return 'next page'
                if char == curses.KEY_LEFT:
                    return 'prev page'
                if char == '\x1b':
                    return 'exit'
                char = self.stdscr.get_wch()
                good_accuracy = False
            if char == '`': # an autoskip for not typable char
                char = letter
            end_time = timer()
            delta = end_time - start_time
            letters += letter
            good_accuracy_word.append(good_accuracy)
            self.char_time_log.append((char, delta, good_accuracy))
            if char == ' ' or idx == len(line) - 1:
                end_word = timer()
                delta_word = end_word - start_word
                wpm = str(round((60 / (delta_word / char_len))/5))
                if char_len > 2:
                    self.stdscr.addstr(self.y+1, self.x-char_len + 1, wpm, curses.color_pair(2))
                char_len = 1
                self.word_time_log.append((letters, wpm, all(good_accuracy_word)))
                letters = ''
                good_accuracy_word = []
                start_word = timer()
            else:
                char_len += 1
            if self.x + 1 < len(line):
                self.x += 1

            self.stdscr.move(self.y, self.x)
        return 'next line'

    def type_screen(self, screen):
        self.y, self.x = 0, 0
        self.stdscr.move(self.y, self.x)
        line_index, line_amount = 0, len(screen)
        while line_index < line_amount:
            line = screen[line_index]
            navigation_code = self.type_line(line)
            if navigation_code == 'exit':
                return 'exit'
            elif navigation_code == 'next line':
                self.y += 2
                line_index+=1
            elif navigation_code == 'next page':
                return 'next page'
            elif navigation_code == 'prev page' or self.y == 0:
                return 'prev page'
            elif navigation_code == 'prev line':
                self.y -= 2
                line_index-=1
        return 'next page'

    def display_screen(self, screen):
        y, x = 0, 0
        self.stdscr.clear()
        for line in screen:
            self.stdscr.addstr(y, x, line)
            x = 0
            y += 2

    def type_text(self, screens):
        '''text is displayed for the user to type while recording input'''
        self.setup()
        screen_index, screen_amount = 0, len(screens)
        while screen_index < screen_amount:
            screen = screens[screen_index]
            self.x, self.y = 0, 0
            self.display_screen(screen)
            navigation_code = self.type_screen(screen)
            if navigation_code == 'next page':
                screen_index+=1
            elif navigation_code == 'prev page':
                if screen_index > 0:
                    screen_index-=1
            elif navigation_code == 'exit':
                return

    def type_slowest_words(self, slowest_words):
        '''allows user the option to improve on there slowest words'''
        if slowest_words:
            response = self.ask_to_type_slowest_words()
            if response:
                text = self.prepare_slowest_words_text(slowest_words)
                formatted_text = self._format_text(text)
                self.word_time_log = []
                self.type_text(formatted_text)
                slowest_words = analyze_word_time_log(self.stdscr, self.word_time_log)

    def prepare_slowest_words_text(self, slowest_words):
        '''small drill to improve slowest words through repetition cycling'''
        exercise = []
        boundary = 1
        while boundary < len(slowest_words):
            exercise.append(slowest_words[boundary-1])
            exercise.append(slowest_words[boundary-1])
            exercise.append(slowest_words[boundary-1])
            for i in range(boundary):
                exercise.append(slowest_words[i])
            for i in range(boundary):
                exercise.append(slowest_words[i])
            for i in range(boundary):
                exercise.append(slowest_words[i])
            boundary += 1
        return ''.join(exercise)
        
    def ask_to_type_slowest_words(self):
        '''optional improvement typing window prompts'''
        question = 'Would you like work on your slowest typed words?'
        options = ['No', 'Yes']
        boolean_window = SelectionWindow(self.stdscr, static_message = question, selection_list = options)
        response = boolean_window.get_selected_row()
        return response
