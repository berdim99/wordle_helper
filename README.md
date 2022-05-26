# wordle_helper

Help find words for the https://www.powerlanguage.co.uk/wordle/ game

To run the program, first install the dependant packages.
I'm using [pipenv](https://pipenv.pypa.io/en/latest/) so better install that first, and then run:

```shell
pipenv install
pipenv shell
```

And then run `python main.py` in a terminal. It was built with Python 3.8.9

To use the helper, play Wordle like you're used to, but after each guess, you can input your leanings to the helper,
and it will show you a list of words you can choose from.

To prevent removing words that should not be removed, start with the green (exact matches), then the partial matches,
and only then the words that are not found at all.

The list of words are scrapped from the Wordle game.

The list of words suggested are ordered by the popularity of letters in all the game words.
However, when there are only a few words left with the same letter popularity, the list will be randomized.

Usage:

- Type enter (or "show") to see a list of words (+ how many are left)
- If a letter is found, type "+{position}{letter}" to remove all words where that letter is not in that position
- If a letter is misplaced, type "?{position}{letter}" to remove all words without that letter, or if the letter is in that position.
- If a letter is not in the word, type "-{letters}" to remove all words with the given letters from the list
  (e.g "-ca" to remove the letters "c" and "a")
- Type "reset" to reset the game state and start over
- Type "define {word}" to open dictionary.com to define the word in the query. You can omit the word if there is only
  one word left.

Example run (spoiler for the 2/13/2022 game!)

```
Read 12972 5 character words
# I played "CARES"
Enter your input (type help for syntax):?2r
Removed 10003 words. Left: 2969
Enter your input (type help for syntax):?4n
Removed 2666 words. Left: 303
Enter your input (type help for syntax):-cae
Removed 238 words. Left: 65
Enter your input (type help for syntax):
Showing 30/65 words
NORIS
PORIN
MOURN
BOURN
ROBIN
BURIN
KORUN
NORKS
ROSIN
NORMS
PURIN
YOURN
MORON
NOIRS
BORON
NURDS
RONTS
GIRON
RUTIN
DOORN
NIRLS
NURLS
RUBIN
ROTON
RINDS
RUNDS
NURRS
MIRIN
RONIN
RUNTS
Enter your input (type help for syntax):+2o   # I played "NORIS"
Removed 44 words. Left: 21
Enter your input (type help for syntax):+4i
Removed 16 words. Left: 5
Enter your input (type help for syntax):?1n
Removed 1 words. Left: 4
Enter your input (type help for syntax):?3r
Removed 1 words. Left: 3
Enter your input (type help for syntax):-s
Removed 1 words. Left: 2
Enter your input (type help for syntax):
Showing 2/2 words in random order
ROBIN
RONIN
Enter your input (type help for syntax):^C     # I played the winning word
bye bye
```
