from abc import abstractmethod


class SentimentModel:
    def __init__(self):
        pass

    @abstractmethod
    def predict(self, data):
        pass

    @abstractmethod
    def train_model(self, data_path):
        pass
