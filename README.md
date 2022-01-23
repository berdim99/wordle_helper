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


Example run (spoiler for the 1/23/2022 game!)

```
Found 10230 5 character words --- I played "AGILE"
Enter your input:-a
Removed 4932 words. Left: 5298
Enter your input:-g
Removed 667 words. Left: 4631
Enter your input:-l
Removed 1116 words. Left: 3515
Enter your input:-e
Removed 1846 words. Left: 1669
Enter your input:+3i
Removed 1455 words. Left: 214
Enter your input:
Showing 10/214 words
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
                                 --- I played "BRICK" (note, BOIKO and BOIST are not in the game dictionary)
Enter your input:-b 
Removed 12 words. Left: 202
Enter your input:-k
Removed 50 words. Left: 152
Enter your input:+2r
Removed 122 words. Left: 30
Enter your input:?4c
Removed 26 words. Left: 4
Enter your input:
Showing 4/4 words
CRIMP
CRISP
CRISS
CRITH
```

Lastly, this project was made for fun, use it if you will, at your own risk.


