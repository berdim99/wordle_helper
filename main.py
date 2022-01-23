# Press ⌃R to execute it or replace it with your code.
from typing import List


WORD_LENGTH = 5
MAX_WORDS_TO_SHOW = 10
WORDS_SOURCE = '/usr/share/dict/words'


def get_words(word_length: int) -> List[str]:
    words: List[str] = []
    with open(WORDS_SOURCE) as f:
        lines = f.readlines()

    for word in lines:
        stripped_word = word.strip()
        if len(stripped_word) == word_length:
            words.append(stripped_word.upper())

    return words


def show_suggestions(words: List[str]):
    to_show = min(MAX_WORDS_TO_SHOW, len(words))
    print(f'Showing {to_show}/{len(words)} words')
    for i in range(to_show):
        print(words[i])


def validate_is_letter(char: str) -> str:
    if char < 'A' or char > 'Z':
        print(f'Invalid char {char}. Must be a-z or A-Z. Try again')
        return ''
    return char


def validate_position(char: str, prefix: str) -> int:
    if not char.isnumeric():
        print(f'Misplaced format is: "{prefix}pc" where p is a number between 1 and {WORD_LENGTH} and c is a character. '
              f'Try again')
        return -1
    position = int(char)
    if position < 1 or position > WORD_LENGTH:
        print(f'Misplaced format is: "{prefix}pc" where p is a number between 1 and {WORD_LENGTH} and c is a character. '
              f'Try again')
        return -1
    return position

def remove_words_with_char(words: List[str], char: str):
    if validate_is_letter(char) == '':
        return

    words_to_remove: List[str] = []
    for word in words:
        if word.find(char) > -1:
            words_to_remove.append(word)

    for word in words_to_remove:
        words.remove(word)

    print(f'Removed {len(words_to_remove)} words. Left: {len(words)}')


def update_due_to_misplaced_char(words: List[str], misplaced_char: str):
    position = validate_position(misplaced_char[0], prefix='?')
    if position == -1:
        return
    char = validate_is_letter(misplaced_char[1])
    if char == '':
        return

    words_to_remove: List[str] = []
    for word in words:
        # First, remove all the words without char
        if word.find(char.upper()) == -1:
            words_to_remove.append(word)
        # Then, remove all the words where char is in "position"
        if word[position-1] == char:
            words_to_remove.append(word)

    for word in words_to_remove:
        words.remove(word)

    print(f'Removed {len(words_to_remove)} words. Left: {len(words)}')


def update_due_to_found_char(words: List[str], found_char: str):
    position = validate_position(found_char[0], prefix='+')
    if position == -1:
        return

    char = validate_is_letter(found_char[1])
    if char == '':
        return

    words_to_remove: List[str] = []
    for word in words:
        # remove all the words where char is not in "position"
        if word[position-1] != char:
            words_to_remove.append(word)

    for word in words_to_remove:
        words.remove(word)

    print(f'Removed {len(words_to_remove)} words. Left: {len(words)}')


def print_usage():
    print('Usage: enter one of these commands:')
    print('\tshow or nothing: show word suggestions')
    print('\tusage: show this help message')
    print('\tquit: quit the program')
    print('\t-{letter}: Remove all words with the given letter')
    print('\t?{position}{letter}: Remove all words with the letter in this position or not in the word at all.'
          ' E.g "?3q" tells us that the letter "q" is in the word, but not the 3rd letter')
    print('\t+{position}{letter}: Remove all words with the letter not in this position.'
          ' E.g "+3q" tells us that the letter "q" is in the word at the 3rd letter')


def helper(words: List[str]):
    inp = ''

    while inp != 'quit':
        inp = input('Enter your input:').strip()
        if inp == 'show' or inp == '':
            show_suggestions(words)
        if inp == 'usage':
            print_usage()
        elif inp == 'quit':
            pass
        elif len(inp) == 2 and inp.startswith('-'):
            # e.g '-A'
            remove_words_with_char(words, inp[1:].upper())
        elif len(inp) == 3 and inp.startswith('?'):
            # e.g '?3A'
            update_due_to_misplaced_char(words, inp[1:].upper())
        elif len(inp) == 3 and inp.startswith('+'):
            # e.g '?3A'
            update_due_to_found_char(words, inp[1:].upper())


if __name__ == '__main__':
    print_usage()
    found_words = get_words(WORD_LENGTH)
    print(f'Found {len(found_words)} {WORD_LENGTH} character words')
    helper(found_words)
