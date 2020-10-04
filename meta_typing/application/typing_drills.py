from collections import Counter
from application.windows import SelectionWindow, TextWindow
import os
import random

class TypingDrills:

    def __init__(self, stdscr, word_drill = None):
        self.stdscr = stdscr
        self.exercise_menu= self.get_exercise_menu()
        self.word_drill = word_drill

    def get_exercise_menu(self):
        '''Additional Exercises are named here with a below name_drill function'''
        menu = [
            'Ngraphs',
            'Word Bank',
            'Speed Drills'
        ]
        return menu

    def start_up(self):
        '''combines all the typing components to return a word drill list'''
        exercise_type = self.get_exercise_type()
        exercise_word_drill = self.get_exercise(exercise_type)
        customized_word_drill = self.ask_for_additional_paramters(exercise_word_drill)
        self.word_drill = customized_word_drill

    def get_exercise_type(self):
        '''selection window is created to get the exercise type from user'''
        exercise_types_window = SelectionWindow(self.stdscr, selection_list = self.exercise_menu)
        selected_exercise_response = exercise_types_window.get_selected_response() # should I get the row or the string value
        return selected_exercise_response

    def get_exercise(self, exercise_type):
        if exercise_type == 'Ngraphs':
            n_graph_response = self.n_graphs()
            words = self.get_n_graph(n_graph_response)
        elif exercise_type == 'Word Bank':
            word_bank_response = self.word_bank()
            words = self.get_word_bank(word_bank_response)
        elif exercise_type == 'Speed Drills':
            speed_drill_response = self.speed_drills()
            words = self.get_speed_drill(speed_drill_response)
        return words

    def n_graphs(self):
        n_graph_menu = ['Bigraphs', 'Trigraphs', 'Tetragraphs', 'Bigrams']
        n_graph_window = SelectionWindow(self.stdscr, selection_list = n_graph_menu)
        selected_n_graph_response = n_graph_window.get_selected_response()
        return selected_n_graph_response

    def get_n_graph(self, n_graph_response):
        if n_graph_response == 'Bigraphs':
            word_list = self.get_word_list('bigraphs')
        elif n_graph_response == 'Trigraphs':
            word_list = self.get_word_list('trigraphs')
        elif n_graph_response == 'Tetragraphs':
            word_list = self.get_word_list('tetragraphs')
        elif n_graph_response == 'Bigrams':
            word_list = self.get_word_list('2grams_top_1000')
        return word_list

    def word_bank(self):
        word_bank_menu = ['Top100', 'Top300', 'Top600', 'Top1000', 'TenFastFingers']
        word_bank_window = SelectionWindow(self.stdscr, selection_list = word_bank_menu)
        word_bank_response = word_bank_window.get_selected_response() # should I get the row or the string value
        return word_bank_response

    def get_word_bank(self, word_bank_response):
        if word_bank_response == 'Top100':
            word_list = self.get_word_list('top100')
        elif word_bank_response == 'Top300':
            word_list = self.get_word_list('top300')
        elif word_bank_response == 'Top600':
            word_list = self.get_word_list('top600')
        elif word_bank_response == 'Top1000':
            word_list = self.get_word_list('top1000')
        elif word_bank_response == 'TenFastFingers':
            word_list = self.get_word_list('tenfastfingers')
        return word_list

    def speed_drills(self):
        speed_drill_menu = ['Word Breakdown', 'Word Accumulator', 'Words By Length']
        speed_drill_window = SelectionWindow(self.stdscr, selection_list = speed_drill_menu)
        speed_drill_response = speed_drill_window.get_selected_response()
        return speed_drill_response

    def get_speed_drill(self, speed_drill_response):
        if speed_drill_response == 'Word Breakdown':
            word_list = self.word_breakdown()
        elif speed_drill_response == 'Word Accumulator':
            word_list = self.word_accumulator()
        elif speed_drill_response == 'Words By Length':
            word_list = self.word_by_length()
        return word_list

    def word_breakdown(self):
        '''prompts user for a word'''
        message = 'Enter the word you would like to practice on: '
        word = TextWindow(self.stdscr, message = message).get_output()
        while len(word) < 2 or len(word.split()) != 1:
            word = TextWindow(self.stdscr, message = message).get_output()

        message = 'Enter the amount of times you would like to repeat word parts: '
        amount = TextWindow(self.stdscr, message = message).get_output()
        while not str(amount).isdigit():
            amount = TextWindow(self.stdscr, message = message).get_output()
        return self.get_word_breakdown(word, int(amount))

    def get_word_breakdown(self, word, repeat_amount):
        word = word.strip()
        if len(word) < 2:
            return ''
        word_list = []
        for char_amount in range(2, len(word) + 1):
            i = 0
            while i + char_amount <= len(word):
                chunk = word[i:i+char_amount]
                chunks = [chunk] * repeat_amount
                word_list.extend(chunks)
                i += 1
        word_list.extend([word] * 3)
        return word_list

    def word_accumulator(self, word_list = None):
        if not word_list:
            word_list = self.get_word_list('top100')
        words = random.choices(word_list[:300], k=15)
        exercise_words = []
        word_q = []
        while words:
            word_p = words.pop(0)
            for j in range(1):
                for i in range(2):
                    for w in word_q:
                        exercise_words.append(w)
                for k in range(j + 1):
                    exercise_words.append(word_p)
            word_q.append(word_p)
        return exercise_words

    def word_by_length(self):
        message = 'Enter the length of words to type: '
        length = TextWindow(self.stdscr, message = message).get_output()
        while not str(length).isdigit() and 0 < length < 16:
            length = TextWindow(self.stdscr, message = message).get_output()
        return self.get_word_by_length(int(length))

    def get_word_by_length(self, length):
        words = self.get_word_list('training_words')
        return [word for word in words if len(word) == length]

    def get_word_list(self, file_name): # str -> list
        '''Opens a file and returns the contents'''
        path = f'../word_drills/{file_name}.txt'
        data = []
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                data.append(line.rstrip())
        return data

    def ask_for_additional_paramters(self, word_list):
        '''If the user wants to tailor his exercise, additional options will appear'''
        question = 'Would you like to customize the exercise?'
        options = ['No', 'Yes']
        boolean_window = SelectionWindow(self.stdscr, static_message = question, selection_list = options)
        response = boolean_window.get_selected_row()
        if response == 0: # selected no for additional parameters
            return word_list
        else:
            return self.get_additional_parameters(word_list)

    def get_additional_parameters(self, word_list):
        '''prompts user for additional paramters'''
        word_amount = self.get_word_amount() # an integer
        word_list = self.get_capitals(word_list)
        randomize = self.randomization() # 0/1
        if randomize == 1:
            word_list = self.randomize_word(word_list, word_amount)
        else:
            word_list = self.apply_word_amount(word_list, word_amount)
        return word_list

    def get_word_amount(self):
        '''prompts user for an integer for word amount'''
        message = 'Enter the amount of words you would like to type: '
        word_amount = TextWindow(self.stdscr, message = message).get_output()
        while not str(word_amount).isdigit():
            word_amount = TextWindow(self.stdscr, message = message).get_output()
        return word_amount

    def get_capitals(self, word_list):
        message = 'Do you want capitalization?'
        options = ['No', 'Yes']
        boolean_window = SelectionWindow(self.stdscr, static_message = message, selection_list = options)
        response = boolean_window.get_selected_row()
        if not response:
            word_list = [word for word in word_list if all(char.islower() for char in word)]
        return word_list

    def randomization(self):
        '''prompts user for if they want to randomize words'''
        question = 'Would you like to randomize the words for the exercise?'
        options = ['No', 'Yes']
        boolean_window = SelectionWindow(self.stdscr, static_message = question, selection_list = options)
        return boolean_window.get_selected_row()

    def randomize_word(self, word_list, word_amount):
        return random.choices(word_list, k=int(word_amount))

    def apply_word_amount(self, word_list, word_amount):
        if int(word_amount) < len(word_list):
            return word_list[:int(word_amount)]
        else:
            return word_list[:int(word_amount)] + random.choices(word_list, k=(int(word_amount) - len(word_list)))

    def get_word_drill(self):
        if self.word_drill[-1][-1] != ' ':
           self.word_drill[-1] += ' ' 
        return ' '.join(self.word_drill)
