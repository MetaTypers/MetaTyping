import curses
from application.utilities import SelectionWindow
import json


class SettingsApp:
    '''TODO'''
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.color_options = self.get_color_options()
        self.start_up()

    def get_color_options(self):
        '''The default colors the user will see and select'''
        return ['BLACK', 'BLUE', 'CYAN', 'GREEN','MAGENTA', 'RED', 'WHITE', 'YELLOW']

    def start_up(self):
        text_option = self.change_text_type()
        color_option = self.change_color()
        self.apply_color_change(text_option, color_option)

    def change_text_type(self):
        question = 'Change text color'
        text_types = ['Background', 'Main', 'Secondary']
        text_types_window = SelectionWindow(self.stdscr, static_message = question, selection_list = text_types)
        selected_type = text_types_window.get_selected_response()
        return selected_type

    def change_color(self):
        question = 'Change background color'
        color_window = SelectionWindow(self.stdscr, static_message = question, selection_list = self.color_options )
        selected_color = color_window.get_selected_response()
        return selected_color

    def apply_color_change(self, selected_type, selected_color):
        '''reads, updates, writes options back'''
        color_settings = read_color_settings()
        updated_colors = self.update_color_change(color_settings, selected_type, selected_color)
        write_color_settings(updated_colors)

    def update_color_change(self, color_settings, selected_type, selected_color):
        # for idx in range(len(color_settings)):
        #     color_type = str(*color_settings[idx].keys())
        # for color_type, color in color_settings.items():
        #     if color_type == selected_type:
        #         color_settings[color_type] = selected_color
        color_settings[0][selected_type] = selected_color
        return color_settings

def read_color_settings():
    path = f'../settings/colors.json'
    with open(path, 'r') as f:
        color_settings = json.load(f)
    return color_settings

def write_color_settings(data):
    path = f'../settings/colors.json'
    with open(path, 'w') as f:
        json.dump(data, f)

def apply_setting():
    color_settings = read_color_settings()
    apply_color_settings(color_settings)

def apply_color_settings(color_settings):
    background_color = f"COLOR_{color_settings[0]['Background']}"
    main_color = f"COLOR_{color_settings[0]['Main']}"
    secondary_color = f"COLOR_{color_settings[0]['Secondary']}"
    
    modpart = 'curses'
    module = __import__(modpart)
    curses.init_pair(1, getattr(module, main_color), getattr(module, background_color))
    curses.init_pair(2, getattr(module, secondary_color), getattr(module, background_color))
    curses.init_pair(3, curses.COLOR_WHITE, getattr(module, background_color))
