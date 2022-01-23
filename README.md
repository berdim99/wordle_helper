# wordle_helper

Help find words for the https://www.powerlanguage.co.uk/wordle/ game

To run the program, run `python main.py` in a terminal. It was built with Python 3.8.9

To use the helper, play World like you're used to, but after each guess, you can input your leanings to the helper,
and it will show you a list of words you can choose from.

The list of words are taken from the default Mac/Linux words file (usually /usr/share/dict/words).
Note that not all words in that file are used by the game, and possibly, the game might use words not in this file.

Brief usage:
* Type "show" or enter to see a list of words (+ how many are left)
* If a letter is not in the word, type "-{letter}" to remove all words with it from the list (e.g "-c" to remove the letter "c")
* If a letter is misplaced, type "?{position}{letter}" to remove all words without that letter, or if the letter is in that position.
* If a letter is found, type "+{position}{letter}" to remove all words where that letter is not in that position


Lastly, this project was made for fun, use it if you will, at your own risk.
