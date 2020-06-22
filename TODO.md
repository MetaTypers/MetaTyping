# TODO Goals

## Weekly Goals (6/21/20 - 28/28/20)

  ## Code
  ## Highest Priority
  - Restructure project using the windows, utilities and app organization
  - Implement MetaTyping
  ## Low Priority
  - add light and dark themes
  - add settings file and ways to change, store, and load settings
  - make it easier to add new drills

## Monthly Goals
  - annotations and docstrings on every class and function as needed
  - tests
  - linters
  - CI/CD tools (travis or azure?)
  - Docker setup
  - How to guides
    - Contribute to code (establish conventions)
    - How to add new drills
  - user database for storing typing stats, possibly notes
  
### and beyond Goals
  - alternative ways to display app
    - transform to an editor, local host, server

# Future layout

### Menu Layout
- meta typing
    - enter url
    - enter clipboard
- typing
    - typing drills
        - predefined exercise
        - custom exercise
    - enter url
    - enter clipboard
- reading
    - enter url
    - enter clipboard
- settings
    - colors
        - dark mode
        - light mode
    
# File Layout
- main.py
- Application
    - app.py
    - typing_app.py
    - reading_app.py
    - meta_typing_app.py
    - windows.py
    - utilities.py
    - typing_drills.py