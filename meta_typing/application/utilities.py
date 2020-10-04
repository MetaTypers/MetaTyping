import curses
from curses import wrapper
import types
import sys


def format_text(raw_text, max_line_height, max_line_width):
    '''proccess the text and fits the text the app'''
    filtered_text = filter_text(raw_text) # str -> str
    paragraphs = fit_words_on_screen(filtered_text, max_line_height, max_line_width) # str -> List[List[str]]
    return paragraphs

def filter_text(text): # str -> str
    replace_symbols_mapping = {
        '’': "'",
        '“': '"',
        '”': '"',
        '—': '-',
        '–': '-',
        '―': '-',
        '…': '...',
        '「': '(',
        '」': ')',
    }

    # can do a perf test to see if one full iteration with multiple checks is better
    for symbol in replace_symbols_mapping.keys():
        if symbol in text:
            text = text.replace(symbol, replace_symbols_mapping[symbol])
    return text

def safe_split(sentence): # str -> List[word:str]
    '''used to retains multiple space values'''
    words = []
    word = ''
    for char in sentence:
        if char == ' ':
            if word:
                words.append(word)
                word = ''
            words.append(char)
        else:
            word += char
    if word:
        words.append(word)
    return words

def fit_words_on_screen(doc, max_line_height, max_line_width):
    '''Takes in a raw text and applies transforms so the text can be displayed
    - format text to screen
        - format width
        - format hight

    - output
        - List of screen each having a list of lines having a string
        - List[List[str]]
    '''
    def divide_text_by_width(doc, max_line_width):
        paragraphs = doc.split('\n')
        essay = []
        for paragraph in paragraphs:
            line = ''
            words = safe_split(paragraph)

            for idx, word in enumerate(words):
                if len(line) + len(word) + 2 < max_line_width:
                    line += word + ''
                else:
                    if word == ' ':
                        line += word
 
        
                    essay.append(line)
                    if word == ' ':
                        line = ''
                    else:
                        line = word + ''
                        
                if idx == len(words) - 1:
                    essay.append(line)
        return essay

    def divide_text_by_height(essay, max_line_height):
        screens = []
        screen = []
        for idx, line in enumerate(essay):


            if len(screen) < max_line_height:
                screen.append(line)
            else:
                screens.append(screen)
                screen = []
                screen.append(line)
            if idx == len(essay) - 1:
                if screen:
                    screens.append(screen)
        return screens

    long_screen = divide_text_by_width(doc, max_line_width)
    screens = divide_text_by_height(long_screen, max_line_height)
    return screens

def analyze_word_time_log(stdscr, word_time_log): # List[Tuple[str, int, bool]] -> None
    '''collects stats from the word_time_log and displayed them'''
    if word_time_log:
        word_stats_feedback, slowest_words = get_word_stats_feedback(word_time_log)
        return word_stats_feedback, slowest_words
    else:
        return None

def get_word_stats_feedback(word_time_log): # List[Tuple[str, int, bool]] -> str
    '''returns a stats page summarizing the typed words log'''
    
    def get_fastest_words():
        fastest_words = time_sorted[-WORDS_VIEWED:]
        fastest_words_string = ', '.join([str({ele[TYPED_WORD]: ele[TYPED_TIME]}) for ele in fastest_words[::-1]])
        return fastest_words_string
    
    def get_slowest_words():
        slowest_words = time_sorted[:WORDS_VIEWED]
        slowest_words_string = ', '.join([str({ele[TYPED_WORD]: ele[TYPED_TIME]}) for ele in slowest_words])
        slowest_word_stats = [ele[TYPED_WORD] for ele in slowest_words]
        return slowest_words_string, slowest_word_stats
    
    def get_slowest_correct_words():
        correct_words = [word for word in word_time_log if word[TYPED_CORRECTLY]]
        correct_words_sorted = sorted(correct_words, key = lambda x: int(x[TYPED_TIME]))
        slowest_correct_words = correct_words_sorted[:WORDS_VIEWED]
        slowest_correct_words_string = ', '.join([str({ele[TYPED_WORD]: ele[TYPED_TIME]}) for ele in slowest_correct_words])
        slowest_correct_words_stats = [ele[TYPED_WORD] for ele in slowest_correct_words]
        return slowest_correct_words_string, slowest_correct_words_stats
    
    def get_wpm():
        return str(sum([int(time) for word, time, accuracy in time_sorted])/len(time_sorted))
    
    def get_accuracy():
        return str(100 * sum([accuracy for word, time, accuracy in time_sorted])/len(time_sorted))
    
    def summarize():
        typed_words_summary = f'Words Typed Summary,\n'\
                              f'Average WPM: {wpm},\n'\
                              f'Typing Accuracy: {accuracy},\n'\
                              f'Fastest typed words: {fastest_words},\n'\
                              f'Slowest typed words: {slowest_words},\n'\
                              f'Slowest correctly typed words: {slowest_correct_words}'
        return typed_words_summary
    
    TYPED_WORD, TYPED_TIME, TYPED_CORRECTLY, WORDS_VIEWED = 0, 1, 2, 5
    time_sorted = sorted(word_time_log, key = lambda x: int(x[TYPED_TIME]))
    wpm = get_wpm()
    accuracy = get_accuracy()
    fastest_words = get_fastest_words()
    slowest_words, slowest_word_stats = get_slowest_words()
    slowest_correct_words, slowest_correct_words_stats = get_slowest_correct_words()
    typed_words_summary = summarize()
    slowest_words_set = list(set(slowest_word_stats + slowest_correct_words_stats))
    return typed_words_summary, slowest_words_set
   