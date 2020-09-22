from application.windows import SelectionWindow, TextWindow
import os
import glob

class TypingLiterature:
    '''
    Actions
    -------
    TypingLiterature creates an interface so text or literature can be:
        - typed
            - user selects a file name
            - returns string the text body of the file name
        - added
            - user types a file name
            - user provides text body for file name
            - the txt file is stored at MetaTyping/saved_literature/
        - deleted
            - user selects a file name
            - the file is deleted
    '''
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def __call__(self):
        '''calls to perform actions until exit or type text is selected'''
        while True:
            action = self._literature_actions()
            text = self._perform_action(action)
            if action == 'Type Text' or action == 'Exit':
                break
        return text
       
    def _literature_actions(self):
        input_text_types = ['Type Text', 'Add New Text', 'Delete Text', 'Exit']
        input_text_types_window = SelectionWindow(self.stdscr, selection_list = input_text_types)
        selected_input_option = input_text_types_window.get_selected_response()
        return selected_input_option

    def _perform_action(self, action):
        text = None
        if action == 'Type Text':
            text = self._type_text()
        elif action == 'Add New Text':
            self._add_new_text()
        elif action == 'Delete Text':
            self._del_text()
        elif action == 'Exit':
            pass
        return text

    def _type_text(self):
        file_name = self._get_available_text()
        return self._get_literature(file_name) if file_name else None
        

    def _add_new_text(self):
        '''ask for a file name and a text body'''
        while True:
            title_message = 'First, Enter the Title of the Literature and F4 when done: '
            title_window = TextWindow(self.stdscr, message = title_message, termination_trigger = 'f4')
            file_name = title_window.get_output()
            if file_name:
                break
        
        while True:
            text_message = 'Now, Enter the Text for the Literature and F4 when done: '
            text_window = TextWindow(self.stdscr, message = text_message, termination_trigger = 'f4')
            content = text_window.get_output()
            if content:
                break
        self._write_literature(file_name, content)

    def _get_available_text(self):
        file_names = [file.replace('../saved_literature/', '').replace('.txt', '') 
            for file in glob.glob('../saved_literature/*.txt')]
        if not file_names:
            return None
        file_names_window = SelectionWindow(self.stdscr, selection_list = file_names)
        selected_file_name = file_names_window.get_selected_response()
        return selected_file_name

    def _del_text(self):
        file_name = self._get_available_text()
        if file_name:
            self._delete_literature(file_name)

    def _get_literature(self, file_name):
        with open(f'../saved_literature/{file_name}.txt', 'r') as f:        
            text = f.read()
        return text

    def _write_literature(self, file_name, content):
        with open(f'../saved_literature/{file_name}.txt', 'w') as f:
            f.write(content)

    def _delete_literature(self, file_name):
        if os.path.exists(f'../saved_literature/{file_name}.txt'):
            os.remove(f'../saved_literature/{file_name}.txt')
