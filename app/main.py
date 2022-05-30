import sys
from typing import List
import webbrowser
import logger

from constants import WORD_LENGTH
from state import State

from rich.console import Console

console = Console()


def validate_is_letter(char: str) -> str:
    """verify that the given character is an alpha letter, return empty string otherwise"""
    if char < "A" or char > "Z":
        console.print(f"[red]Invalid char {char}. Must be a-z or A-Z. Try again[/red]")
        return ""
    return char


def validate_position(char: str, prefix: str) -> int:
    """validate that the given character is a number between 1 and WORD_LENGTH. return -1 otherwise"""
    if not char.isnumeric():
        console.print(
            f'[red]Misplaced format is: "{prefix}pc" where p is a number between 1 and {WORD_LENGTH} and c '
            f"is a character. Try again[/red]",
        )
        return -1
    position = int(char)
    if position < 1 or position > WORD_LENGTH:
        console.print(
            f'[red]Misplaced format is: "{prefix}pc" where p is a number between 1 and {WORD_LENGTH} and c '
            f"is a character. Try again[/red]",
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

    console.print(
        f"Removed [magenta]{removed}[/magenta] words. "
        f"Left: [magenta]{state.words_count()}[/magenta]",
    )


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

    console.print(
        f"Removed [magenta]{len(words_to_remove)}[/magenta] words. "
        f"Left: [magenta]{state.words_count()}[/magenta]",
    )


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

    console.print(
        f"Removed [magenta]{len(words_to_remove)}[/magenta] words. "
        f"Left: [magenta]{state.words_count()}[/magenta]",
    )


def print_help():
    console.print("")
    console.print("Usage: enter one of these commands:")
    console.print("\tshow or nothing: show word suggestions")
    console.print("\thelp: show this help message")
    console.print("\treset or r: reset the words list")
    console.print("\tquit or exit: quit the program")
    console.print(
        "\t+{position}{letter}: Remove all words with the letter not in this position."
        ' E.g "+3q" tells us that the letter "q" is in the word at the 3rd letter',
    )
    console.print(
        "\t?{position}{letter}: Remove all words with the letter in this position or not in the word at all."
        ' E.g "?3q" tells us that the letter "q" is in the word, but not the 3rd letter',
    )
    console.print(
        "\t-{letters}: Remove all words with the given letters (one or more letters to remove)",
    )
    console.print(
        "\tdefine [word]: (or d [word]) Open the dictionary to define a word. If only one word is left, "
        "you can omit the word argument from the command",
    )


def define(word: str) -> None:
    console.print(f"Defining word: {word}")
    webbrowser.open(f"https://www.dictionary.com/browse/{word}")


def helper(state: State):
    inp = ""

    while inp != "quit" and inp != "exit":
        if state.words_count() == 1:
            console.print(
                f'\n\n[magenta]The word must be "{state.words[0]}[/magenta]"\n\n',
            )

        inp = (
            console.input(
                "[magenta]Enter your input (type help for syntax):[/magenta] ",
            )
            .strip()
            .lower()
        )
        inp_parts = inp.split()
        if (
            inp == "show" or inp == ""
        ):  # This must be first. Other commands assume inp_parts is not empty
            state.show_suggestions()
        elif inp == "help":
            print_help()
        elif inp == "quit" or inp == "exit":
            pass
        elif inp == "reset" or inp == "r":
            console.print(f"[magenta]Resetting helper[/magenta]")
            state = State(state.logger)
        elif inp_parts[0] in ("define", "d"):
            if state.words_count() == 1:
                define(state.words[0])
            else:
                if len(inp_parts) == 2:
                    define(inp_parts[1])
                else:
                    console.print('Usage is: "define <word>"')
        elif len(inp) >= 2 and inp.startswith("-"):
            # e.g '-A' or '-AB'
            letters = inp[1:].upper()
            to_remove_letters = []
            for letter in letters:
                if letter in state.found_letters:
                    console.print(
                        f'[red]Not removing "{letter}" because it was previously found[/red]',
                    )
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
    is_debug = "-d" in sys.argv or "--debug" in sys.argv
    try:
        logger = logger.Logger(
            logger.LogLevel.DEBUG if is_debug else logger.LogLevel.INFO,
        )
        helper(State(logger))
    except KeyboardInterrupt:
        console.print("\nbye bye")
