# What is MetaTyping?
MetaTyping is a typing application that helps users improve their typing ability by using specialized drills, techniques, and feedback metrics.

#### What do you type?
- Text is generated using built-in drills, word lists, clipboards and word recommendations based on user-stats

#### What are typing drills?
- Most common words: top 100, 300, 600, 1000 most common words
- Most common ngraphs: 2-4 graphs that are the most frequent letter combinations
- Most common ngrams: 2 grams that are the most frequent word pairing
- Speed drills:
  - Word Breakdown: Breaks the word in sections to practice finger technique and to build up speed
  - Word Accumulator: A repetitive series that slowly introduces new words

#### What are typing techniques?
- Unit typing: Users focus on typing a single word quickly with a break after each word
  - Focuses on reducing the delay between letters
- Read ahead typing: n characters are hidden in front of cursor, forcing users to read ahead to type
  - Focuses on reducing space bar delay and improves typing consistency over time

#### What feedback metrics are shown?
- An approximate words per minute (wpm) is shown after each word typed
- Summary statistics like wpm, accuracy, slowest words and more after each session

#### How are words recommended?
- Each word typed gets stored into a database recording:
  -  word speed
  -  word speed with space (before and after)
  -  accuracy
  -  if it had a capitalization
  -  if it was surrounded by a symbol
  
- Words can be recommended based on worst:
  - wpm
  - wpm with space
  - accuracy
  - relative speed ordering that top typists have

### Installation Guide/ How to use

Must have python 3.7 +

#### For Mac and Linux using terminal

```bash
git clone https://github.com/MetaTypers/MetaTyping
cd MetaTyping
python -m venv env
source env/bin/activate
pip install -r requirements.txt
cd meta_typing
python3 main.py
```
#### For Windows using cmd
```bash
git clone https://github.com/MetaTypers/MetaTyping
cd MetaTyping
py -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
cd meta_typing
py main.py
```
### How To Use Typing App

- start application in `/MetaTyping/meta_typing` using `python3 main.py` or `py main.py` if you are on Windows
- navigate with with arrow keys and select with enter
- Exit with `esc`
- Force close `ctrl c`
- Skip characters with ` (the key left of 1)
- Navigate text:
    - Previous line with 'Up Arrow'
    - Next line with 'Down Arrow'
    - Previous screen with 'Left Arrow'
    - Next screen with 'Right Arrow'

### How To Use Dashboard

- start dashboard in `/MetaTyping/meta_typing` using `python3 dashboard.py` or `py dashboard.py` if you are on Windows
- you can filter the dashboard by:
  - grouping words by frequency to see wpm average over time
    - top 100, 300, 600, 1000, 3000, 10000, or all
  - type an individual word in a so see wpm over time
  - query the dashboard and see average of all time with bar plots
    - can navigate next page at the bottom
    - can sort words by using arrows near metrics(wpm, wpm_space, accuracy)
    - can type letters in the word filter to filter letter combinations (you may want to search in all words)
    - can use `< 80` under accuracy metric to filter words with accuracy less than 80%
- can exit by `ctrl c` in the terminal