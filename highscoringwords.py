__author__ = 'codesse'

import collections


class HighScoringWords:
    MAX_LEADERBOARD_LENGTH = 100  # the maximum number of items that can appear in the leaderboard
    MIN_WORD_LENGTH = 3  # words must be at least this many characters long
    letter_values = {}
    valid_words = []

    def __init__(self, validwords='wordlist.txt', lettervalues='letterValues.txt'):
        """
        Initialise the class with complete set of valid words and letter values by parsing text files containing the data
        :param validwords: a text file containing the complete set of valid words, one word per line
        :param lettervalues: a text file containing the score for each letter in the format letter:score one per line
        :return:
        """
        with open(validwords) as f:
            self.valid_words = f.read().splitlines()

        with open(lettervalues) as f:
            for line in f:
                (key, val) = line.split(':')
                self.letter_values[str(key).strip().lower()] = int(val)

        self.calculate_word_scores()

    def tokenize(self, word: str) -> dict:
        """
        Given a string, create a dict of characters and the number of times they occur in the string
        :param word: a string value representing a word
        :return: dict[str, int]
        """
        return dict(collections.Counter(word))

    def is_starting_letters_match(self, tiles: str, valid_word_tokens: dict) -> bool:
        """
        Given starting tiles and a valid word, return a boolean value indicated if the tiles can be used to create the valid word
        :param tiles: a string value representing the starting letters
        :param valid_word_tokens: dict[str, int] representing the number of times characters occur in a string
        :return: bool indicating if starting letters match a valid word
        """

        if len(tiles) < 5 or 15 < len(tiles):
            return False

        tile_tokens = self.tokenize(tiles)
        for ch, occur in valid_word_tokens.items():
            if ch not in tile_tokens:
                return False
            elif occur > tile_tokens[ch]:
                return False

        return True

    def calculate_word_score(self, word: str, score=0) -> int:
        """
        Given a word, calculate its word score
        :param score: word score
        :param word: string representing a word
        :return: int representing the word score
        """
        try:
            for ch in word:
                score += self.letter_values.get(ch)
        except KeyError:
            raise Exception("character is not present in lettervalues.txt")
        return score

    def calculate_word_scores(self):
        """
        Return a dict of words sorted in descending order based on word score and if the scores of words are equal then
        sorted in alphabetical order
        :return: a dict {word, (word score, dict[char, int])}, which has a word as key and a tuple value. The first tuple
        value is the word score and the second is a dict of the tokenized word
        """
        self.word_scores = {word: {'word_score': self.calculate_word_score(word), 'tokens': self.tokenize(word)} for word in self.valid_words if
                            len(word) >= self.MIN_WORD_LENGTH}

    def build_leaderboard_for_word_list(self):
        """
        Build a leaderboard of the top scoring MAX_LEADERBOAD_LENGTH words from the complete set of valid words.
        :return: The list of top words.
        """
        # returns top 100 words sorted by score
        return sorted(self.word_scores, key=lambda x: (-self.word_scores[x]['word_score'], x))[0:self.MAX_LEADERBOARD_LENGTH]

    def build_leaderboard_for_letters(self, starting_letters):
        """
        Build a leaderboard of the top scoring MAX_LEADERBOARD_LENGTH words that can be built using only the letters contained in the starting_letters String.
        The number of occurrences of a letter in the startingLetters String IS significant. If the starting letters are bulx, the word "bull" is NOT valid.
        There is only one l in the starting string but bull contains two l characters.
        Words are ordered in the leaderboard by their score (with the highest score first) and then alphabetically for words which have the same score.
        :param starting_letters: a random string of letters from which to build words that are valid against the contents of the wordlist.txt file
        :return: The list of top buildable words.
        """
        matches = {}
        for word in self.word_scores:
            if self.is_starting_letters_match(starting_letters, self.word_scores[word]['tokens']):
                matches[word] = self.word_scores[word]['word_score']
        # returns matching words sorted by score
        return sorted(matches, key=lambda x: (-matches[x], x))
