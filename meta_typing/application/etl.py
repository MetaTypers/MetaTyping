from datetime import datetime, timezone
from . import sql_queries
import pickle
import pandas as pd


def get_log():
    with open('../logs/char_log.txt') as f:
        log_raw = f.readlines()
    return log_raw
            
def load_all_words():
    with open('../word_tables/word_mappings.p', 'rb') as fp:
        data = pickle.load(fp)
    return data

def strip_log_ends(log):
    if not log:
        return ''

    start_index = 0
    while start_index < len(log) - 1 and log[start_index][0] != ' ':
        start_index +=1
    start_index
        
    end_index = len(log) - 1
    while end_index > 0 and log[end_index][0] != ' ':
        end_index -=1
    end_index
    
    if start_index >= end_index:
        return ''
    else:
        return log[start_index:end_index+1]


def valid_word(word, word_dictionary):
    '''Checks it the base word in in the top 10,000 words'''
    return clean_word(word) in word_dictionary

def clean_word(word):
    '''converts words to lower with only alpha char'''
    return ''.join([char for char in word.lower() if (96 < ord(char) < 123) or ord(char) == 39])

def tag(word, word_dictionary):
    return word_dictionary[clean_word(word)]

def wpm(word_len, space_amount, time):
    '''wpm formula for typing sites have 5 char = 1 word'''
    if time <= 0:
        return 0
    return round((60/(float(time)/(word_len + space_amount)))/5)

def has_capitalization(word):
    return any([char.isupper() for char in word])

def has_symbols(word):
    return not all([96 < ord(char) < 123 for char in word.lower()])

def date_format():
    d = datetime.now(timezone.utc)
    return f'{d.year}-{d.month}-{d.day}'

def process_log(word, time, time_with_space, space_amount, accuracy, word_dictionary):
    '''only adds a clean word if it is in the 10,000 word dictionary'''
    return _process_log(word, time, time_with_space, space_amount, accuracy, word_dictionary) if valid_word(word, word_dictionary) else None

def _process_log(word, time, time_with_space, space_amount, accuracy, word_dictionary):
    wpm_no_space =  wpm(len(word), 0, time)
    wpm_with_space = wpm(len(word), space_amount, time_with_space)
    if (0 < wpm_no_space < 1000 and 0 < wpm_with_space < 1000):
        return [clean_word(word), tag(word, word_dictionary), wpm_no_space, wpm_with_space, bool(accuracy), has_capitalization(word), has_symbols(word), date_format()]
    else:
        return None

def reset_variables():
    raw_word, word, word_time, word_accuracy, skip_first_char = '', '', 0, True, True
    return raw_word, word, word_time, word_accuracy, skip_first_char

def calibrate_unit_time(word, raw_word, word_time, time):
    word_time = word_time + (word_time/len(word)) # approximate first char typed
    word_time_with_space = float(word_time) + float(time)
    return word_time, word_time_with_space

def split_log_by_type(log):
    unit = []
    integration = []
    for entry in log:
        char = entry[0]
        time, accuracy, unit_type = entry[1:].split()
        if unit_type == 'True':
            unit.append([char, time, accuracy])
        elif unit_type == 'False':
            integration.append([char, time, accuracy])
    return unit, strip_log_ends(integration)

def combine_logs(log1, log2):
    combined_log = []
    for log in log1:
        combined_log.append(log)
    for log in log2:
        combined_log.append(log)
    return combined_log

def write_to_df(processed_log):
    df = pd.DataFrame(processed_log)
    df.columns = ['word', 'word_list', 'wpm', 'wpm_space', 'accuracy', 'capital', 'symbols', 'date']
    df.to_pickle('word_stats.pkl')

def clear_log():
    open('../logs/char_log.txt', 'w').close()

def process_integration_log(log):
    word_dictionary = load_all_words()
    word, word_time, word_accuracy, word_log = '', 0, True, []
    for entry in log:
        char, time, accuracy = entry
        if char == ' ':
            if word:
                after_space = time
                time_with_space = float(before_space) + float(word_time) + float(after_space)
                space_amount = 2
                processed_log = process_log(word, word_time, time_with_space, space_amount, word_accuracy, word_dictionary)
                if processed_log:
                    word_log.append(processed_log)
                word, word_time, word_accuracy = '', 0, True
            before_space = time
        else:
            word += char
            word_time += float(time)
        if accuracy == 'False':
            word_accuracy = False
    return word_log

def process_unit_log(log):
    raw_word, word, word_time, word_accuracy, skip_first_char = reset_variables()
    word_log = []
    word_dictionary = load_all_words()
    for entry in log:  
        char, time, accuracy = entry
        if char == ' ':
            if word:
                word_time, word_time_with_space = calibrate_unit_time(word, raw_word, word_time, time)
                space_amount = 1
                processed_log = process_log(raw_word, word_time, word_time_with_space, space_amount, word_accuracy, word_dictionary)
                if processed_log:
                    word_log.append(processed_log)
                raw_word, word, word_time, word_accuracy, skip_first_char = reset_variables()
            if len(raw_word) == 1:
                raw_word, word, word_time, word_accuracy, skip_first_char = reset_variables()
        else:
            if not skip_first_char:
                word += char
                word_time += float(time)
            skip_first_char = False
            raw_word += char
        if accuracy == 'False':
            word_accuracy = False

    return word_log

def extract_log():
    log_raw = get_log()
    cleaned_log = strip_log_ends([log.rstrip() for log in log_raw])
    return cleaned_log

def transform_log(log):
    '''splits the char log by unit/integration type, applies a transform on both,
    then combines logs together to store in a pandas data frame for loading
    '''
    # split log by type
    unit_log, integration_log = split_log_by_type(log)
    
    # process logs
    processed_unit_log = process_unit_log(unit_log)
    processed_integration_log = process_integration_log(integration_log)

    # combine processed logs together
    processed_log = combine_logs(processed_unit_log, processed_integration_log)

    # store to be loaded
    write_to_df(processed_log)

def load_log():
    '''Creates the db connection, loads the pandas dataframe word stats and performs bulk insertion'''
    sql_queries.bulk_insert_word_stats()

def clear_intermediate_files():
    clear_log()

def etl():
    log = extract_log()
    if not log:
        return
    processed_log = transform_log(log)
    load_log()

    clear_intermediate_files()

# if __name__ == "__main__":
#     etl()
