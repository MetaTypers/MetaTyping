def load_log():
    with open('../log/char_log.txt') as f:
        log_raw = f.readlines()
    return strip_log_ends([log.rstrip() for log in log_raw])
    
def load_words():
    with open('../data/10000words.txt') as f:
        data = f.readlines()
    return {d.strip():0 for d in data}

def strip_log_ends(log):
    start_index = 0
    while start_index < len(log) -1 and log[start_index][0] != ' ':
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

def valid_word(word):
    '''Checks it the base word in in the top 10,000 words'''
    return clean_word(word) in word_dic

def clean_word(word):
    '''converts words to lower with only alpha char'''
    return ''.join([char for char in word.lower() if 96 < ord(char) < 123])

def wpm(word_len, time):
    '''wpm formula for typing sites have 5 char = 1 word'''
    return (60/(float(time)/word_len))/5

def has_capitalization(word):
    return any([char.isupper() for char in word])

def has_symbols(word):
    return not all([96 < ord(char) < 123 for char in word.lower()])

def process_log(word, time, time_with_space, accuracy):
    '''only adds a clean word if it is in the 10,000 word dictionary'''
    return _process_log(word, time, time_with_space, accuracy) if valid_word(word) else None

def _process_log(word, time, time_with_space, accuracy):
    return {
        'word': clean_word(word),
        'raw word': word,
        'wpm without space': wpm(len(word), time),
        'wpm with space': wpm(len(word)+2, time_with_space),
        'accuracy': accuracy,
        'capitalization': has_capitalization(word),
        'symbols': has_symbols(word),
    }

def transform_log():
    log = load_log()
    word_dic = load_words()
    word, word_time, word_accuracy, word_log = '', 0, True, []
    for entry in log:
        char = entry[0]
        time, accuracy = entry[1:].split()
        print(char, time, accuracy)
        if char == ' ':
            if word:
                after_space = time
                time_with_space = float(before_space) + float(word_time) + float(after_space)
                processed_log = process_log(word, word_time, time_with_space, word_accuracy)
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