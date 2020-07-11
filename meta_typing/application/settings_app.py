import curses
from application.utilities import SelectionWindow


class SettingsApp:
    '''Themes are selected, using a theme function
    The themes.txt is then overwritten

    To add a new theme,
        - add theme under name under `get_themes_menu'
        - add a get_****_theme function with the text and background colors
        - add a the get_****_theme call to 'set_theme'
    '''
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.themes_menu = self.get_themes_menu()
        self.start_up()

    def get_themes_menu(self):
        '''The themes the user will see and select from'''
        themes_menu = ['Light', 'Dark']
        return themes_menu

    def start_up(self):
        '''executes the settings app for the user to change theme options'''
        selected_theme = self.get_theme()
        self.set_theme(selected_theme)

    def get_theme(self):
        '''creates a window for the user to select a theme option'''
        question = 'Select a theme'
        themes_window = SelectionWindow(self.stdscr, static_message = question, selection_list = self.themes_menu)
        selected_theme = themes_window.get_selected_response()
        return selected_theme

    def set_theme(self, selected_theme):
        '''links the user selected theme option and overwrites in the settings file'''
        if selected_theme == 'Light':
            self.set_light_theme()
        elif selected_theme == 'Dark':
            self.set_dark_theme()
            
    def set_light_theme(self):
        '''saves light theme settings to themes.txt'''
        light_theme = self.get_light_theme()
        self.write_theme(light_theme)

    def get_light_theme(self):
        return 'Light'

    def set_dark_theme(self):
        '''saves dark theme settings to themes.txt'''
        dark_theme = self.get_dark_theme()
        self.write_theme(dark_theme)

    def get_dark_theme(self):
        return 'Dark'

    def write_theme(self, theme):
        '''writes the theme properties to theme.txt'''
        path = f'../themes/themes.txt'
        with open(path, 'w') as f:
            f.write(theme)

def apply_setting():
    '''Reads the themes settings file and applies them'''
    theme_settings = get_theme_settings()
    apply_theme_settings(theme_settings)

def get_theme_settings():
    '''Opens a file and returns the contents'''
    path = f'../themes/themes.txt'
    with open(path, 'r') as f:
        theme_settings = f.readline().strip()
    return theme_settings

def apply_theme_settings(theme_settings):
    '''applies the theme color when called in other applications'''
    if theme_settings == 'Light':
        apply_light_theme()
    elif theme_settings == 'Dark':
        apply_dark_theme()
    else:
        pass

def apply_dark_theme():
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)

def apply_light_theme():
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_WHITE)
        