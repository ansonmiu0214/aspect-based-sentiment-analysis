from src.sentiment_service.sentiment_service import SentimentService
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class Vader(SentimentService):
    def compute_sentiment(self, text):
        analyzer = SentimentIntensityAnalyzer()
        return analyzer.polarity_scores(text)['compound']
