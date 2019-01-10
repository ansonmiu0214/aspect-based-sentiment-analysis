from models import SentimentService
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class Vader(SentimentService):
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def compute_sentiment(self, text):
        '''
        Uses VADER to compute the sentiment for a given text.

        :param text: str
        :rtype: float
        '''
        return self.analyzer.polarity_scores(text)['compound']
