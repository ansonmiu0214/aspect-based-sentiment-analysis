from models import SentimentService
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class Vader(SentimentService):
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def compute_sentiment(self, text):
        return self.analyzer.polarity_scores(text)['compound']
