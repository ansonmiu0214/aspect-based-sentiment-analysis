import random


class Loader:
    def __init__(self, limit=0, split=0.8, train_data=None):
        self.limit = limit
        self.split = split
        self.train_data = train_data

    def load_data(self):
        random.shuffle(self.train_data)
        train_data = self.train_data[-self.limit:]
        texts, labels = zip(*train_data)
        cats = [{'POSITIVE': bool(y)} for y in labels]
        split = int(len(train_data) * self.split)
        return (texts[:split], cats[:split]), (texts[split:], cats[split:])
