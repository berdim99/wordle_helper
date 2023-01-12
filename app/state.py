import random
from typing import List, Dict

import constants
import logger
import popular_sort


def count_letters_frequency(words: List[str]) -> Dict[str, List[int]]:
    out: Dict[str, List[int]] = {}
    for word in words:
        pos = 0
        for letter in word:
            if letter not in out:
                out[letter] = [0] * constants.WORD_LENGTH

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

    def __init__(self, logger: logger.Logger):
        self.logger = logger
        self.words = get_words(constants.WORD_LENGTH)
        self.found_letters = []
        print(f"Read {len(self.words)} {constants.WORD_LENGTH} character words")

    def words_count(self) -> int:
        return len(self.words)

    def show_suggestions(self):
        """show a sample list of words left in the list"""
        letter_freq = count_letters_frequency(self.words)
        to_show = min(constants.MAX_WORDS_TO_SHOW, self.words_count())

        sorter = popular_sort.PopularSort(letter_freq, len(self.words))
        s = sorted(self.words, key=sorter.sort, reverse=True)

        use_random_order = len(sorter.sort_distribution.keys()) == 1
        if use_random_order:
            random.shuffle(self.words)
            s = self.words

        self.logger.info(
            f"[magenta]Showing {to_show}/{self.words_count()} words "
            f"{f'in random order' if use_random_order else ''}[/magenta]",
        )
        max_count = max(sorter.word_to_count.values())
        width = len(f"{max_count}")
        for i in range(to_show):
            word = s[i]

            if self.logger.is_debug_enabled():
                pos = 0
                freq_str = []
                total = 0
                for letter in word:
                    freq = letter_freq[letter][pos]
                    total += freq
                    freq_str.append(f"{letter}: " + "{: >{}}".format(freq, width))
                    pos += 1

                self.logger.debug(
                    f"{word} | {', '.join(freq_str)} "
                    f"| total: {total} | sort_count: {sorter.word_to_count[word]}",
                )
            else:
                self.logger.info(word)
