# Press ⌃R to execute it or replace it with your code.
from typing import List


WORD_LENGTH = 5  # can be max of 9
MAX_WORDS_TO_SHOW = 15
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


def update_due_to_misplaced_char(words: List[str], position: str, misplaced_char: str):
    position = validate_position(position, prefix='?')
    if position == -1:
        return
    char = validate_is_letter(misplaced_char)
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


def update_due_to_found_char(words: List[str], position: str, found_char: str):
    position = validate_position(position, prefix='+')
    if position == -1:
        return

    char = validate_is_letter(found_char)
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


def print_help():
    print('Usage: enter one of these commands:')
    print('\tshow or nothing: show word suggestions')
    print('\thelp: show this help message')
    print('\treset: reset the words list')
    print('\tquit: quit the program')
    print('\t-{letter}: Remove all words with the given letter')
    print('\t?{position}{letter}: Remove all words with the letter in this position or not in the word at all.'
          ' E.g "?3q" tells us that the letter "q" is in the word, but not the 3rd letter')
    print('\t+{position}{letter}: Remove all words with the letter not in this position.'
          ' E.g "+3q" tells us that the letter "q" is in the word at the 3rd letter')


def helper(words: List[str]):
    inp = ''
    found_letters: List[str] = []

    while inp != 'quit':
        if len(words) == 1:
            print(f'\n\nThe word must be "{words[0]}"\n\n')

        inp = input('Enter your input (type help for syntax):').strip()
        if inp == 'show' or inp == '':
            show_suggestions(words)
        if inp == 'help':
            print_help()
        elif inp == 'quit':
            pass
        elif inp == 'reset':
            words = get_words(WORD_LENGTH)
            found_letters = []
            print(f'Reset game. {len(words)} words loaded')
        elif len(inp) == 2 and inp.startswith('-'):
            # e.g '-A'
            letter = inp[1:].upper()
            if letter in found_letters:
                print(f'Not removing "{letter}" because it was previously found')
            else:
                # Don't remove letters that were previously found
                remove_words_with_char(words, letter)
        elif len(inp) == 3 and inp.startswith('?'):
            # e.g '?3A'
            letter = inp[2:].upper()
            found_letters.append(letter)
            update_due_to_misplaced_char(words, inp[1], letter)
        elif len(inp) == 3 and inp.startswith('+'):
            # e.g '?3A'
            letter = inp[2:].upper()
            found_letters.append(letter)
            update_due_to_found_char(words, inp[1], letter)


if __name__ == '__main__':
    print_help()
    found_words = get_words(WORD_LENGTH)
    print(f'Found {len(found_words)} {WORD_LENGTH} character words')
    helper(found_words)