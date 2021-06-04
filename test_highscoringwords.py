import unittest

from highscoringwords import HighScoringWords


class TestHighScoringWords(unittest.TestCase):

    def test_calculate_word_score(self):
        hsw = HighScoringWords()
        self.assertEqual(17, hsw.calculate_word_score('aardvarks'), 'should be 17')

    def test_word_match(self):
        word = "serendipity"
        hsw = HighScoringWords()
        valid_word_tokens = hsw.tokenize(word)

        # these are letters in the scrabble tiles
        t1 = "seren"
        t2 = "serenity"
        t3 = "ssdip"
        t4 = "dipitx"
        t5 = "sdipp"

        self.assertEqual(False, hsw.is_starting_letters_match(t1, valid_word_tokens))
        self.assertEqual(False, hsw.is_starting_letters_match(t2, valid_word_tokens))
        self.assertEqual(False, hsw.is_starting_letters_match(t3, valid_word_tokens))
        self.assertEqual(False, hsw.is_starting_letters_match(t4, valid_word_tokens))
        self.assertEqual(False, hsw.is_starting_letters_match(t5, valid_word_tokens))

    def test_word_match2(self):
        word1 = "bully"
        word2 = "adore"
        word3 = "road"
        word4 = "read"
        word5 = "rodeo"
        word6 = "roo"
        hsw = HighScoringWords()

        # these are words in my scrabble tiles
        tiles = "deora"

        self.assertEqual(False, hsw.is_starting_letters_match(tiles, hsw.tokenize(word1)))
        self.assertEqual(True, hsw.is_starting_letters_match(tiles, hsw.tokenize(word2)))
        self.assertEqual(True, hsw.is_starting_letters_match(tiles, hsw.tokenize(word3)))
        self.assertEqual(True, hsw.is_starting_letters_match(tiles, hsw.tokenize(word4)))
        self.assertEqual(False, hsw.is_starting_letters_match(tiles, hsw.tokenize(word5)))
        self.assertEqual(False, hsw.is_starting_letters_match(tiles, hsw.tokenize(word6)))
        self.assertEqual(False, hsw.is_starting_letters_match("bulxyy", hsw.tokenize("bull")))

    def test_leaderboard_for_word_list(self):
        hsw = HighScoringWords()
        sortedlist = hsw.build_leaderboard_for_word_list()
        self.assertEqual('razzamatazzes', sortedlist[0])
        self.assertEqual('cyclohexylamines', sortedlist[-1])

    def test_leaderboard_for_letters(self):
        hsw = HighScoringWords()
        self.assertEqual(37, len(hsw.build_leaderboard_for_letters('aardvarks')))


if __name__ == '__main__':
    unittest.main()
