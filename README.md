# wordle_helper

Help find words for the https://www.powerlanguage.co.uk/wordle/ game

To run the program, run `python main.py` in a terminal. It was built with Python 3.8.9

To use the helper, play Wordle like you're used to, but after each guess, you can input your leanings to the helper,
and it will show you a list of words you can choose from.

To prevent removing words that should not be removed, start with the green (exact matches), then the partial matches, and only then the words
that are not found at all.

The list of words are taken from the default Mac/Linux words file (usually /usr/share/dict/words).
Note that not all words in that file are used by the game, and possibly, the game might use words not in this file.

Brief usage:
* Type "show" or enter to see a list of words (+ how many are left)
* If a letter is found, type "+{position}{letter}" to remove all words where that letter is not in that position
* If a letter is misplaced, type "?{position}{letter}" to remove all words without that letter, or if the letter is in that position.
* If a letter is not in the word, type "-{letters}" to remove all words with the given letters from the list 
  (e.g "-ca" to remove the letters "c" and "a")


Example run (spoiler for the 1/23/2022 game!)

```
// I played "AGILE"
Read 10230 5 character words
Enter your input (type help for syntax):+3i
Removed 9385 words. Left: 845
Enter your input (type help for syntax):-agle
Removed 631 words. Left: 214
Enter your input (type help for syntax):
Showing 25/214 words
BOIKO
BOIST
BRICK
BRINK
BRINY
BRISK
BRISS
BRITH
BRIZZ
BUIST
CHICK
CHICO
CHICO
CHIMU
CHINK
CHINK
CHINO
CHINT
CHIOT
CHIPS
CHIRK
CHIRM
CHIRO
CHIRP
CHIRR
// I played "BRICK"
Enter your input (type help for syntax):+2r
Removed 165 words. Left: 49
Enter your input (type help for syntax):?4c
Removed 43 words. Left: 6
Enter your input (type help for syntax):-bk
Removed 2 words. Left: 4
Enter your input (type help for syntax):
Showing 4/4 words
CRIMP
CRISP
CRISS
CRITH
Enter your input (type help for syntax):quit                                                                                                                 /1m-29.7s
```

Lastly, this project was made for fun, use it if you will, at your own risk.


