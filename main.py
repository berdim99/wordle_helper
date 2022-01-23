# Press ⌃R to execute it or replace it with your code.
from typing import List


WORD_LENGTH = 5  # can be max of 9
MAX_WORDS_TO_SHOW = 30
WORDS_SOURCE = "/usr/share/dict/words"


def get_words(word_length: int) -> List[str]:
    """get the full list of 'word_length' words from the dictionary"""
    words: List[str] = []
    with open(WORDS_SOURCE) as f:
        lines = f.readlines()

    for word in lines:
        stripped_word = word.strip()
        if len(stripped_word) == word_length:
            words.append(stripped_word.upper())

    return words


def show_suggestions(words: List[str]):
    """show a sample list of words left in the list"""
    to_show = min(MAX_WORDS_TO_SHOW, len(words))
    print(f"Showing {to_show}/{len(words)} words")
    for i in range(to_show):
        print(words[i])


def validate_is_letter(char: str) -> str:
    """verify that the given character is an alpha letter, return empty string otherwise"""
    if char < "A" or char > "Z":
        print(f"Invalid char {char}. Must be a-z or A-Z. Try again")
        return ""
    return char


def validate_position(char: str, prefix: str) -> int:
    """validate that the given character is a number between 1 and WORD_LENGTH. return -1 otherwise"""
    if not char.isnumeric():
        print(
            f'Misplaced format is: "{prefix}pc" where p is a number between 1 and {WORD_LENGTH} and c is a character. '
            f"Try again"
        )
        return -1
    position = int(char)
    if position < 1 or position > WORD_LENGTH:
        print(
            f'Misplaced format is: "{prefix}pc" where p is a number between 1 and {WORD_LENGTH} and c is a character. '
            f"Try again"
        )
        return -1
    return position


def remove_words_with_chars(words: List[str], chars: List[str]):
    """remove all words that have the given char in them from the given words list"""
    removed = 0
    for char in chars:
        if validate_is_letter(char) == "":
            continue

        words_to_remove: List[str] = []
        for word in words:
            if word.find(char) > -1:
                words_to_remove.append(word)

        removed += len(words_to_remove)
        for word in words_to_remove:
            words.remove(word)

    print(f"Removed {removed} words. Left: {len(words)}")


def update_due_to_misplaced_char(words: List[str], position: str, misplaced_char: str):
    """remove all words where the misplaces char is at the given position, or words that don't
    have that char at all
    """
    position_int = validate_position(position, prefix="?")
    if position_int == -1:
        return
    char = validate_is_letter(misplaced_char)
    if char == "":
        return

    words_to_remove: List[str] = []
    for word in words:
        # First, remove all the words without char
        if word.find(char.upper()) == -1:
            words_to_remove.append(word)
        # Then, remove all the words where char is in "position_int"
        if word[position_int - 1] == char:
            words_to_remove.append(word)

    for word in words_to_remove:
        words.remove(word)

    print(f"Removed {len(words_to_remove)} words. Left: {len(words)}")


def update_due_to_found_char(words: List[str], position: str, found_char: str):
    """remove all words where the found character is not in the given position"""
    position_int = validate_position(position, prefix="+")
    if position_int == -1:
        return

    char = validate_is_letter(found_char)
    if char == "":
        return

    words_to_remove: List[str] = []
    for word in words:
        # remove all the words where char is not in "position"
        if word[position_int - 1] != char:
            words_to_remove.append(word)

    for word in words_to_remove:
        words.remove(word)

    print(f"Removed {len(words_to_remove)} words. Left: {len(words)}")


def print_help():
    print("Usage: enter one of these commands:")
    print("\tshow or nothing: show word suggestions")
    print("\thelp: show this help message")
    print("\treset: reset the words list")
    print("\tquit or exit: quit the program")
    print(
        "\t+{position}{letter}: Remove all words with the letter not in this position."
        ' E.g "+3q" tells us that the letter "q" is in the word at the 3rd letter'
    )
    print(
        "\t?{position}{letter}: Remove all words with the letter in this position or not in the word at all."
        ' E.g "?3q" tells us that the letter "q" is in the word, but not the 3rd letter'
    )
    print(
        "\t-{letters}: Remove all words with the given letters (one or more letters to remove)"
    )


def helper(words: List[str]):
    inp = ""
    found_letters: List[str] = []

    while inp != "quit" and inp != "exit":
        if len(words) == 1:
            print(f'\n\nThe word must be "{words[0]}"\n\n')

        inp = input("Enter your input (type help for syntax):").strip()
        if inp == "show" or inp == "":
            show_suggestions(words)
        if inp == "help":
            print_help()
        elif inp == "quit" or inp == "exit":
            pass
        elif inp == "reset":
            words = get_words(WORD_LENGTH)
            found_letters = []
            print(f"Reset game. {len(words)} words loaded")
        elif len(inp) >= 2 and inp.startswith("-"):
            # e.g '-A' or '-AB'
            letters = inp[1:].upper()
            to_remove_letters = []
            for letter in letters:
                if letter in found_letters:
                    print(f'Not removing "{letter}" because it was previously found')
                else:
                    to_remove_letters.append(letter)
            else:
                # Don't remove letters that were previously found
                remove_words_with_chars(words, to_remove_letters)
        elif len(inp) == 3 and inp.startswith("?"):
            # e.g '?3A'
            letter = inp[2:].upper()
            found_letters.append(letter)
            update_due_to_misplaced_char(words, inp[1], letter)
        elif len(inp) == 3 and inp.startswith("+"):
            # e.g '?3A'
            letter = inp[2:].upper()
            found_letters.append(letter)
            update_due_to_found_char(words, inp[1], letter)


if __name__ == "__main__":
    print_help()
    found_words = get_words(WORD_LENGTH)
    print(f"Read {len(found_words)} {WORD_LENGTH} character words")
    helper(found_words)
