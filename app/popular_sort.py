from typing import Dict, List


class PopularSort:
    DOUBLE_LETTER_THRESHOLD = 50
    DOUBLE_LETTER_FACTOR = 0.5

    def __init__(self, letters_frequency: Dict[str, List[int]], word_count: int):
        self.letters_frequency = letters_frequency
        self.word_count = word_count
        self.sort_distribution: Dict[int, int] = {}
        self.word_to_count: Dict[str, int] = {}

    def sort(self, word: str):
        """sorted key function that promotes words with the most popular letters in them, while reducing the
        weight of words where the same letter appear multiple times
        """
        count = 0
        non_factored_count = 0
        found_letters = set()
        pos = 0
        for letter in word:
            factor = 1.0
            if letter in found_letters:
                # Don't consider duplicate letters when there are many words left
                factor = (
                    0.0
                    if self.word_count > self.DOUBLE_LETTER_THRESHOLD
                    else self.DOUBLE_LETTER_FACTOR
                )
            non_factored_count += self.letters_frequency[letter][pos]
            count += int(self.letters_frequency[letter][pos] * factor)

            if letter not in found_letters:
                found_letters.add(letter)
            pos += 1

        if non_factored_count not in self.sort_distribution:
            self.sort_distribution[non_factored_count] = 0
        self.sort_distribution[non_factored_count] += 1

        self.word_to_count[word] = count
        return count
