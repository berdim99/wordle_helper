import random
from typing import List, Dict

import constants
import popular_sort


def count_letters_frequency(words: List[str]) -> Dict[str, List[int]]:
    out: Dict[str, List[int]] = {}
    for word in words:
        pos = 0
        for letter in word:
            if letter not in out:
                out[letter] = [0, 0, 0, 0, 0]  # TODO use word length

            out[letter][pos] += 1
            pos += 1

    return out


def get_words(word_length: int) -> List[str]:
    """get the full list of 'word_length' words from the dictionary"""
    words: List[str] = []
    with open(constants.WORDS_SOURCE) as f:
        lines = f.readlines()

    for word in lines:
        stripped_word = word.strip()
        if len(stripped_word) == word_length:
            words.append(stripped_word.upper())

    return words


class State:
    found_letters: List[str] = []
    words: List[str]

    def __init__(self):
        self.words = get_words(constants.WORD_LENGTH)
        self.found_letters = []
        print(f"Read {len(self.words)} {constants.WORD_LENGTH} character words")

    def words_count(self) -> int:
        return len(self.words)

    def show_suggestions(self):
        """show a sample list of words left in the list"""
        letter_freq = count_letters_frequency(self.words)
        to_show = min(constants.MAX_WORDS_TO_SHOW, self.words_count())
        use_random_order = self.words_count() < 10
        if use_random_order:
            random.shuffle(self.words)
            s = self.words
        else:
            sorter = popular_sort.PopularSort(letter_freq, len(self.words))
            s = sorted(self.words, key=sorter.sort, reverse=True)

        print(
            f"Showing {to_show}/{self.words_count()} words {'in random order' if use_random_order else ''}",
        )
        for i in range(to_show):
            word = s[i]
            pos = 0
            freq_str = []
            total = 0
            for letter in word:
                freq = letter_freq[letter][pos]
                total += freq
                freq_str.append(f"{letter}: {freq}")
                pos += 1

            print(f"{word} | {', '.join(freq_str)} | total: {total}")
