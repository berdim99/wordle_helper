from typing import Dict, List, Tuple


class PopularSort:
    popular_letters: Dict[str, int] = {}
    avg_count = 0

    def __init__(self, popular_letters: List[Tuple[str, int]]):
        max_count = 0
        for letter_count in popular_letters:
            max_count += letter_count[1]
            self.popular_letters[letter_count[0]] = letter_count[1]
        self.avg_count = int(max_count / len(popular_letters))

    def sort(self, word: str):
        """sorted key function that promotes words with the most popular letters in them, while reducing the
        weight of words where the same letter appear multiple times
        """
        count = 0
        found_letters = set()
        for letter in word:
            if letter in found_letters:
                count -= self.avg_count * 5
            else:
                found_letters.add(letter)

            if letter in self.popular_letters:
                count += self.popular_letters[letter]
        return count
