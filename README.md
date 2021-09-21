# Solitaire Solver

My CE301 Capstone project is to build a program that can solve the Microsoft Windows 10 Solitaire game.  
The way it does this is by parsing the screen and identifying cards.  
The program has access to the images of all of the cards and it will search the screen for each card.
Then mouse clicks are used to perform actions that will play the game.  
## Installation Requirements

- [Python version 3.7.9](https://www.python.org/downloads/release/python-379/)
- [PyAutoGUI version 0.9.50](https://pypi.org/project/PyAutoGUI/)
- [opencv-python version 4.2.0.34](https://pypi.org/project/opencv-python/)

## How to run the code
The files needed for the program are coded to work with my file management.  
There are lines of code that would need to be changed to work with your file system organisation.
Currently the code works only with a 1920x1080 monitor and with the Microsoft Windows solitaire game.  
The window has to maximised but not in fullscreen.
The code can be ran in a command window using the command "py SolitaireSolver.py" in the highest level in the git repository.

## Contents
If you want to go directly to a specific part of the repository, these links will take you there.
- [Challenge Week Files](../master/Challenge_week)
- [Code Files](../master/Code)
    - The techincal documentation can be found in this folder
    - [Screenshots of all the ace cards](../master/Code/ace_cards)
    - [Screenshots of all cards showing the full card](../master/Code/all_cards_faces)
    - [Screenshots of all the cards only showing the top left symbol](../master/Code/all_cards_symbols)
    - [Screenshots of the solitaire board where columns will be](../master/Code/column_images)
    - [Screenshots of the solataire board where the foundation positions are](../master/Code/foundation_images)
    - [Screenshots of all the king cards, both full face and symbol](../master/Code/king_cards)
    - [The readme file that contains the technical documentation about how my code works](../master/Code)
- [Interim Oral Presentation Files](../master/interim_oral_presentation)
- [Testing Files](../master/testing)
    - [Code testing files](../master/testing/code)
    - [Images used for testing](../master/testing/images)
