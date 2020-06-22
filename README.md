# Meta Typer

Meta Typer is a productivity application used to speed read and type text from any URL, clipboard or builtin drill.  

To learn content faster, a combination of speed reading and typing can be used. There are many studies showing the benefits of reading and taking hand written notes. Hand writing notes is slow at 13-20 while typing is much faster at 40 wpm and can easily be improved to 75wpm+. Though typing is not the same as note taking, I would argue there are still overlapping benefits such as, an increase in ability to focus, comprehension, memory and many more.  

There is nothing stopping you from typing content in a notepad to take notes, but if you type incorrectly, take a micro break, or scroll pages then you will have to spend time finding your place. Additionally, Stats are collected to show what type of words you struggle.  

### Installation Guide

- clone it
- python -m venv env
- source env/bin/activate
- pip install -r requirements.txt
- python -m spacy download en_core_web_sm

### How To Use

- start application with `python3 main.py` in `/meta_typing/meta_typing`
- navigate with with arrow keys and select with enter
- for typing
    - if a weird symbol that you cannot type is found type `
    - to exit out early press `esc`
    - force close with `ctrl+c`
