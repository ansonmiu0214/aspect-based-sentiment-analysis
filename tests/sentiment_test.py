import unittest

from sentiment_service.vader import Vader


class SentimentTests(unittest.TestCase):
    def setUp(self):
        self.sentiment = Vader()

    def test_empty_string_returns_no_sentiment(self):
        score = self.sentiment.compute_sentiment("")
        self.assertEqual(score, 0)

    def test_trivial_positive_should_be_positive(self):
        score = self.sentiment.compute_sentiment("Today is a great day.")
        self.assertGreater(score, 0)

    def test_trivial_negative_should_be_negative(self):
        score = self.sentiment.compute_sentiment("Today was a terrible day.")
        self.assertLess(score, 0)


if __name__ == '__main__':
    unittest.main()
