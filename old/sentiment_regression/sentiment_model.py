from abc import abstractmethod

from nltk.sentiment import SentimentIntensityAnalyzer


class SentimentModel:
    def __init__(self):
        pass

    def predict(self, data):
        analyser = SentimentIntensityAnalyzer()
        return analyser.polarity_scores(data)['compound']

    @abstractmethod
    def train_model(self, data_path):
        pass
