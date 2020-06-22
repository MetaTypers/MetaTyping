from collections import Counter


class TypingDrills:

    def __init__(self, drill_type = 'words', file = '300words.txt', word_amount = 5, filter_letters = None):
        self.drill_type = drill_type
        self.file = file
        self.word_amount = word_amount
        self.filter_letters = filter_letters
        self.words = self.get_words()


    def get_words(self):
        word_list = self.get_word_list(self.file)
        drills = self.get_drill_type(word_list)
        filtered = self.get_filtered_words(drills)
        word_amount = self.get_word_amount(filtered)
        return word_amount


    def get_word_list(self, words):
        path = f'../data/{self.file}'
        with open(path) as f:
            lines = f.readlines()
            words = []
            for line in lines:
                words.append(line.rstrip())
        return words

    def get_drill_type(self, words):
        words_by_type = []
        if self.drill_type == 'words':
            words_by_type = words
        elif self.drill_type == 'bigrams':
            words_by_type = self.most_common_digraphs(words)
        elif self.drill_type == 'trigrams':
            words_by_type = self.most_common_trigraphs(words)
        return words_by_type

    def get_filtered_words(self, words):
        if self.filter_letters:
            return self.filter_by_starting_letter(words, self.filter_letters)
        else:
            return words


    def most_common_digraphs(self, words):
        alpha = [char for char in 'qwertasdfgzxcvbjuiophyklnm']
        two_combo = []
        for char1 in alpha:
            for char2 in alpha:
                two_combo.append(char1 + char2)

        two_char_counter = Counter()
        for word in words:
            for combo in two_combo:
                if combo in word:      
                    two_char_counter[combo] += 1
        return [digram[0] for digram in two_char_counter.most_common()]

    def most_common_trigraphs(self, words):
        alpha = [char for char in 'qwertasdfgzxcvbjuiophyklnm']
        three_combo = []
        for char1 in alpha:
            for char2 in alpha:
                for char3 in alpha:
                    three_combo.append(char1 + char2 + char3)

        three_char_counter = Counter()
        for word in words:
            for combo in three_combo:
                if combo in word:      
                    three_char_counter[combo] += 1
        return [trigram[0] for trigram in three_char_counter.most_common()]
        
    def get_word_amount(self, words):
        amount_words = self.word_amount
        if amount_words > len(words):
            return words
        else:
            return words[:amount_words]

    def training_exercise(self):
        word_q = []
        word_list = self.word_list.copy()
        word_list.sort(key = len)
        text = ''
        while word_list:
            word_p = word_list.pop(0)
            text += '\n'
            for j in range(2):
                for i in range(2):
                    for word in word_q:
                        text += word
                for k in range(j + 1):
                    text += word_p

            word_q.append(word_p)
        text += '\n'
        for j in range(2):
            for i in range(2):
                for word in word_q:
                    text += word

    def filter_by_starting_letter(self, words, letters):
        return [word for word in words if word[0] in letters]