# What is MetaTyping?
MetaTyping is a typing application that helps users improve their typing ability by using typing drills, typing techniques, and feedback metrics.

#### What do you type?
- Text is generated using built-in drills, clipboards and content on the web using a url link

#### What are typing drills?
- Most common words: top 100, 300, 600, 1000 most common words
- Most common ngraphs: 2-4 graphs that are the most frequent letter combinations
- Most common ngrams: 2 grams that are the most frequent word pairing
- Speed drills: repetitive series that slowly introduces new words

#### What are typing techniques?
- Unit typing: Users focus on typing a single word quickly with a break after each word
- Read ahead typing: n characters are hidden in front of cursor, forcing users to read ahead to type

#### What feedback metrics are shown?
- An approximate words per minute (wpm) is shown after each word typed
- Summary statistics like wpm, accuracy, slowest words and more after each session

### Installation Guide/ How to use

#### For Mac and Linux

```bash
git clone https://github.com/MetaTypers/MetaTyping
cd MetaTyping
python -m venv env
source env/bin/activate
pip install -r requirements.txt
cd meta_typing
python3 main.py
```
#### For Windows
```bash
git clone https://github.com/MetaTypers/MetaTyping
cd MetaTyping
py -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
cd meta_typing
py main.py
```
### How To Use

- start application with `python3 main.py` in `/MetaTyping/meta_typing` or `py main.py` if you are on Windows
- navigate with with arrow keys and select with enter
- Exit with `esc`
- Force close `ctrl c`
- Skip characters with `
- Navigate text:
    - Previous line with 'Up Arrow'
    - Next line with 'Down Arrow'
    - Previous screen with 'Left Arrow'
    - Next screen with 'Right Arrow'

