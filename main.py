from typing import List, Dict, Tuple

WORD_LENGTH = 5  # can be max of 9
MAX_WORDS_TO_SHOW = 30
# WORDS_SOURCE = "/usr/share/dict/words"
WORDS_SOURCE = "words.txt"


class State:
    found_letters: List[str] = []
    words: List[str]

    def __init__(self):
        self.words = get_words(WORD_LENGTH)
        self.found_letters = []
        print(f"Read {len(self.words)} {WORD_LENGTH} character words")

    def words_count(self) -> int:
        return len(self.words)

    def show_suggestions(self):
        """show a sample list of words left in the list"""
        to_show = min(MAX_WORDS_TO_SHOW, self.words_count())
        print(f"Showing {to_show}/{self.words_count()} words")
        for i in range(to_show):
            print(self.words[i])

        formatted_letters = []
        for letter_count in self.popular_letters():
            formatted_letters.append(f"{letter_count[0]}: {letter_count[1]}")
        print(
            f"Most popular letters (minus found ones): {', '.join(formatted_letters)}",
        )

    def popular_letters(self) -> List[Tuple[str, int]]:
        letter_to_count: Dict[str, int] = {}
        for word in self.words:
            for char in word:
                if char in letter_to_count:
                    letter_to_count[char] += 1
                else:
                    letter_to_count[char] = 1

        for letter in self.found_letters:
            if letter in letter_to_count:
                del letter_to_count[letter]
        sorted_map = sorted(letter_to_count.items(), key=lambda x: x[1], reverse=True)
        return sorted_map[:5]


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
            f"Try again",
        )
        return -1
    position = int(char)
    if position < 1 or position > WORD_LENGTH:
        print(
            f'Misplaced format is: "{prefix}pc" where p is a number between 1 and {WORD_LENGTH} and c is a character. '
            f"Try again",
        )
        return -1
    return position


def remove_words_with_chars(state: State, chars: List[str]):
    """remove all words that have the given char in them from the given words list"""
    removed = 0
    for char in chars:
        if validate_is_letter(char) == "":
            continue

        words_to_remove: List[str] = []
        for word in state.words:
            if word.find(char) > -1:
                words_to_remove.append(word)

        removed += len(words_to_remove)
        for word in words_to_remove:
            state.words.remove(word)

    print(f"Removed {removed} words. Left: {state.words_count()}")


def update_due_to_misplaced_char(state: State, position: str, misplaced_char: str):
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
    for word in state.words:
        # First, remove all the words without char
        if word.find(char.upper()) == -1:
            words_to_remove.append(word)
        # Then, remove all the words where char is in "position_int"
        if word[position_int - 1] == char:
            words_to_remove.append(word)

    for word in words_to_remove:
        state.words.remove(word)

    print(f"Removed {len(words_to_remove)} words. Left: {state.words_count()}")


def update_due_to_found_char(state: State, position: str, found_char: str):
    """remove all words where the found character is not in the given position"""
    position_int = validate_position(position, prefix="+")
    if position_int == -1:
        return

    char = validate_is_letter(found_char)
    if char == "":
        return

    words_to_remove: List[str] = []
    for word in state.words:
        # remove all the words where char is not in "position"
        if word[position_int - 1] != char:
            words_to_remove.append(word)

    for word in words_to_remove:
        state.words.remove(word)

    print(f"Removed {len(words_to_remove)} words. Left: {state.words_count()}")


def print_help():
    print("Usage: enter one of these commands:")
    print("\tshow or nothing: show word suggestions")
    print("\thelp: show this help message")
    print("\treset: reset the words list")
    print("\tquit or exit: quit the program")
    print(
        "\t+{position}{letter}: Remove all words with the letter not in this position."
        ' E.g "+3q" tells us that the letter "q" is in the word at the 3rd letter',
    )
    print(
        "\t?{position}{letter}: Remove all words with the letter in this position or not in the word at all."
        ' E.g "?3q" tells us that the letter "q" is in the word, but not the 3rd letter',
    )
    print(
        "\t-{letters}: Remove all words with the given letters (one or more letters to remove)",
    )


def helper(state: State):
    inp = ""

    while inp != "quit" and inp != "exit":
        if state.words_count() == 1:
            print(f'\n\nThe word must be "{state.words[0]}"\n\n')

        inp = input("Enter your input (type help for syntax):").strip()
        if inp == "show" or inp == "":
            state.show_suggestions()
        if inp == "help":
            print_help()
        elif inp == "quit" or inp == "exit":
            pass
        elif inp == "reset":
            print("Resetting helper")
            state = State()
        elif len(inp) >= 2 and inp.startswith("-"):
            # e.g '-A' or '-AB'
            letters = inp[1:].upper()
            to_remove_letters = []
            for letter in letters:
                if letter in state.found_letters:
                    print(f'Not removing "{letter}" because it was previously found')
                else:
                    to_remove_letters.append(letter)
            else:
                # Don't remove letters that were previously found
                remove_words_with_chars(state, to_remove_letters)
        elif len(inp) == 3 and inp.startswith("?"):
            # e.g '?3A'
            letter = inp[2:].upper()
            state.found_letters.append(letter)
            update_due_to_misplaced_char(state, inp[1], letter)
        elif len(inp) == 3 and inp.startswith("+"):
            # e.g '?3A'
            letter = inp[2:].upper()
            state.found_letters.append(letter)
            update_due_to_found_char(state, inp[1], letter)


if __name__ == "__main__":
    print_help()
    try:
        helper(State())
    except KeyboardInterrupt:
        print("\nbye bye")
