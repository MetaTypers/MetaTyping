from collections import Counter
from application.utilities import SelectionWindow, TextWindow
import os
import random

class TypingDrills:

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.exercise_menu= self.get_exercise_menu()
        self.word_drill = self.start_up()

    def get_exercise_menu(self):
        '''Additional Exercises are named here with a below name_drill function'''
        menu = [
            'Bigraphs',
            'Trigraphs',
            'Speed Drill',
            'Word Bank',
        ]
        return menu

    def start_up(self):
        '''combines all the typing components to return a word drill list'''
        exercise_type = self.get_exercise_type()
        additional_parameters = self.ask_for_additional_paramters()
        word_drill = self.get_exercise(exercise_type, additional_parameters)
        return word_drill

    def get_exercise_type(self):
        '''selection window is created to get the exercise type from user'''
        exercise_types_window = SelectionWindow(self.stdscr, selection_list = self.exercise_menu)
        selected_exercise_response = exercise_types_window.get_selected_response() # should I get the row or the string value
        return selected_exercise_response

    def ask_for_additional_paramters(self):
        '''If the user wants to tailor his exercise, additional options will appear'''
        question = 'Would you like to customize the exercise?'
        options = ['No', 'Yes']
        boolean_window = SelectionWindow(self.stdscr, static_message = question, selection_list = options)
        response = boolean_window.get_selected_row()
        if response == 0: # selected no for additional parameters
            return None
        else:
            return self.get_additional_parameters()

    def get_additional_parameters(self):
        '''prompts user for additional paramters'''
        file_name = self.get_word_list_file_name() # returns name_of_word_list.txt
        word_amount = self.get_word_amount() # an integer
        word_starting_letters = self.get_word_starting_letters() # string of starting letters
        additional_paramters = [file_name, word_amount, word_starting_letters]
        return additional_paramters

    def get_word_list_file_name(self):
        '''prompts user to select word list file name under the data source'''
        word_list_file_names = self.get_word_list_file_names()
        word_list_file_names_window = SelectionWindow(self.stdscr, selection_list = word_list_file_names)
        word_list_file_name = word_list_file_names_window.get_selected_response()
        return word_list_file_name

    def get_word_list_file_names(self):
        '''gets filenames where the word lists are stored'''
        return [file for file in os.listdir("../data/") if file.endswith(".txt")]

    def get_word_amount(self):
        '''prompts user for an integer for word amount'''
        message = 'Enter the amount of words you would like to type: '
        word_amount = TextWindow(self.stdscr, message = message).get_output()
        while not str(word_amount).isdigit():
            word_amount = TextWindow(self.stdscr, message = message).get_output()
        return word_amount

    def get_word_starting_letters(self):
        '''prompts user for starting letters to apply a filter'''
        message = 'Enter the starting letters for your words: '
        starting_letters = TextWindow(self.stdscr, message = message).get_output()
        while not str(starting_letters).isalpha() and None:
            starting_letters = TextWindow(self.stdscr, message = message).get_output()
        return starting_letters

    def get_exercise(self, exercise_type, exercise_parameters):
        '''applies the exercise types and parameters to created a word_drill'''
        if exercise_parameters == None:
            file_name, word_amount, starting_letters = '10000words.txt', 100, None
        else:
            file_name, word_amount, starting_letters = exercise_parameters

        words = self.get_word_list(file_name)
        words_filtered_1 = self.apply_word_drill(words, exercise_type)
        words_filtered_2 = self.apply_starting_letters(words_filtered_1, starting_letters)
        words_filtered_3 = self.apply_word_amount(words_filtered_2, word_amount)
        return words_filtered_3

    def get_word_list(self, file_name): # str -> list
        '''Opens a file and returns the contents'''
        path = f'../data/{file_name}'
        with open(path) as f:
            lines = f.readlines()
            words_list = []
            for line in lines:
                words_list.append(line.rstrip())
        return words_list

    def apply_word_drill(self, words_list, exercise_type):
        '''applies the word drill function'''
        if exercise_type == 'Bigraphs':
            word_drill = self.apply_bigraphs_drill(words_list)
        elif exercise_type == 'Trigraphs':
            word_drill = self.apply_trigraphs_drill(words_list)
        elif exercise_type == 'Speed Drill':
            word_drill = self.apply_speed_drill(words_list)
        elif exercise_type == 'Word Bank': # pass
            word_drill = words_list
        return word_drill

    def apply_bigraphs_drill(self, word_list):
        alpha = [char for char in 'qwertasdfgzxcvbjuiophyklnm']
        two_combo = []
        for char1 in alpha:
            for char2 in alpha:
                two_combo.append(char1 + char2)

        two_char_counter = Counter()
        for word in word_list:
            for combo in two_combo:
                if combo in word:      
                    two_char_counter[combo] += 1
        return [digram[0] for digram in two_char_counter.most_common()]

    def apply_trigraphs_drill(self, word_list):
        alpha = [char for char in 'qwertasdfgzxcvbjuiophyklnm']
        three_combo = []
        for char1 in alpha:
            for char2 in alpha:
                for char3 in alpha:
                    three_combo.append(char1 + char2 + char3)

        three_char_counter = Counter()
        for word in word_list:
            for combo in three_combo:
                if combo in word:      
                    three_char_counter[combo] += 1
        return [trigram[0] for trigram in three_char_counter.most_common()]

    def apply_speed_drill(self, word_list):
        words = random.choices(word_list[:300], k=14)
        exercise_words = []
        word_q = []
        while words:
            word_p = words.pop(0)
            for j in range(2):
                for i in range(2):
                    for w in word_q:
                        exercise_words.append(w)
                for k in range(j + 1):
                    exercise_words.append(word_p)
            word_q.append(word_p)
            exercise_words.append('\n')
        return exercise_words

    def apply_starting_letters(self, word_list, starting_letters):
        if starting_letters:
            return self.filter_by_starting_letter(word_list, starting_letters)
        else:
            return word_list

    def filter_by_starting_letter(self, word_list, starting_letters):
        return [word for word in word_list if word[0] in starting_letters]

    def apply_word_amount(self, word_list, word_amount):
        return word_list[:int(word_amount)]

    def get_word_drill(self):
        return ' '.join(self.word_drill)
