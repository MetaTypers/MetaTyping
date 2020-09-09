import curses
from application.windows import SelectionWindow, TextWindow, StaticWindow
from application.settings_app import apply_setting
from application.sql_queries import query_word_recommendation
from application.typing_app import TypingApp
from application.utilities import fit_words_on_screen
import pickle

class StatisticsApp:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.setup()
        self.start_up()

    def setup(self):
        self.stdscr.clear()
        apply_setting()
        self.stdscr.bkgd(' ', curses.color_pair(1))
        self.stdscr.clear()
        self.stdscr.attron(curses.color_pair(1))
        curses.curs_set(2)
        
    def start_up(self):
        selected_response = self.statistics_menu()
        if selected_response == 'Type Words':
            self.type_words_menu()
        elif selected_response == 'Visualize Statistics':
            self.prompt_visualize_statistics_text()
        elif selected_response == 'Exit':
            return

    def statistics_menu(self):
        menu = ['Type Words', 'Visualize Statistics', 'Exit']
        menu_window = SelectionWindow(self.stdscr, selection_list = menu)
        selected_response = menu_window.get_selected_response()
        return selected_response

    def type_words_menu(self):
        word_list_options = self.get_word_list_options()
        query = self.word_to_query_mapping(word_list_options)
        word_list = query_word_recommendation(query)
        word_list = self.apply_recommendation(query, word_list)
        TypingApp(self.stdscr, ' '.join(word_list))

    def get_word_list_options(self):
        word_list_type = self.list_type_menu()
        word_list_metric = self.get_word_metric()
        word_list_amount = self.get_word_amount()
        return [word_list_type, word_list_metric, word_list_amount]

    def word_to_query_mapping(self, word_list_options):
        list_type, metric, amount = query = word_list_options
        list_type_mappings = {'Top100':1, 'Top300':2, 'Top600':3, 'Top1000':4, 'Top3000':5}
        metric_mappings = {'Slowest Words no space':'wpm', 'Slowest Words with space':'wpm_space', 'Inaccurate Words':'accuracy', 'Relatively Slowest Words':'wpm_space'}
        return [list_type_mappings[list_type], metric_mappings[metric], amount]

    def list_type_menu(self):
        question = 'What group of words would would you like to search from?'
        word_list_menu = ['Top100', 'Top300', 'Top600', 'Top1000', 'Top3000']
        word_list_window = SelectionWindow(self.stdscr, static_message = question, selection_list = word_list_menu)
        word_list_response = word_list_window.get_selected_response()
        return word_list_response

    def get_word_amount(self):
        '''prompts user for an integer for word amount'''
        message = 'Enter the amount of words you would like to type: '
        word_amount = TextWindow(self.stdscr, message = message).get_output()
        while not str(word_amount).isdigit():
            word_amount = TextWindow(self.stdscr, message = message).get_output()
        return word_amount

    def get_word_metric(self):
        question = 'What metric would you like to apply?'
        word_list_menu = ['Slowest Words no space', 'Slowest Words with space', 'Inaccurate Words', 'Relatively Slowest Words']
        word_list_window = SelectionWindow(self.stdscr, static_message = question, selection_list = word_list_menu)
        word_list_response = word_list_window.get_selected_response()
        return word_list_response

    def apply_recommendation(self, query, word_list):
        list_type, metric, amount = query
        if metric == 'Relatively Slowest Words':
            sorted_word_list = self.open_file(word_list)
            word_list = relative_sort(word_list, sorted_word_list)
        return word_list
        
    def open_file(self, file_name):
        file_name = file_name.lower()
        with open(f'../word_tables/{file_name}_recommendation.p', 'rb') as fp:
            data = pickle.load(fp)
        return data

    def relative_sort(self, list_a, list_b):
        '''This sorts list_a to list_b by the difference in index value position'''
        list_b_no_missing = [b for b in list_b if b in list_a]
        indexes = [idx - list_b_no_missing.index(a) for idx, a in enumerate(list_a, start = 0)]
        list_a_sorted_by_index = [a for _, a in sorted(zip(indexes, list_a), reverse = True)]
        return list_a_sorted_by_index

    def prompt_visualize_statistics_text(self):
        text = 'To visualize your statistics, run "python3 dashboard.py" in /MetaTyping/meta_typing directory'
        max_line_height, max_line_width = self.stdscr.getmaxyx()
        screens = fit_words_on_screen(text, max_line_height, max_line_width)
        StaticWindow(self.stdscr, screens = screens)
