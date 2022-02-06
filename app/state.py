from typing import List, Dict

import constants
import popular_sort
from letter_count import LetterCount


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
        popular_letters_count = self.popular_letters()
        popular_letters = []
        for i in popular_letters_count:
            popular_letters.append(i.letter)
        words_with_popular_letters = []
        for word in self.words:
            for popular_letter in popular_letters:
                if popular_letter in word:
                    words_with_popular_letters.append(word)
                    break

        to_show = min(constants.MAX_WORDS_TO_SHOW, self.words_count())
        sorter = popular_sort.PopularSort(popular_letters_count)

        if len(words_with_popular_letters) > to_show:
            print(
                f"Showing {to_show}/{self.words_count()} words (words with popular letters)",
            )
            s = sorted(words_with_popular_letters, key=sorter.sort, reverse=True)
            for i in range(to_show):
                print(s[i])
        else:
            print(f"Showing {to_show}/{self.words_count()} words")
            s = sorted(self.words, key=sorter.sort, reverse=True)
            for i in range(to_show):
                print(s[i])

        formatted_letters = []
        for i in popular_letters_count:
            formatted_letters.append(f"{i.letter}: {i.count}")
        print(
            f"Most popular letters (minus found ones): {', '.join(formatted_letters)}",
        )

    def popular_letters(self) -> List[LetterCount]:
        """Return a list of up to the top 5 popular letters from the remaining words"""
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
        out: List[LetterCount] = []
        for key, value in sorted_map[:5]:
            out.append(LetterCount(key, value))
        return out
