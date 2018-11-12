from models import SentimentService
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class Vader(SentimentService):
    def compute_sentiment(self, text):
        analyzer = SentimentIntensityAnalyzer()
        return analyzer.polarity_scores(text)['compound']
