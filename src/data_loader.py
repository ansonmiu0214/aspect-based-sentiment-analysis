import random
import thinc.extra.datasets


class Loader:
    def __init__(self, limit=0, split=0.8):
        self.limit = limit
        self.split = split

    def load_data_default(self):
        train_data, _ = thinc.extra.datasets.imdb()
        random.shuffle(train_data)
        train_data = train_data[-self.limit:]
        print(train_data)
        texts, labels = zip(*train_data)
        cats = [{'POSITIVE': bool(y)} for y in labels]
        split = int(len(train_data) * self.split)
        return (texts[:split], cats[:split]), (texts[split:], cats[split:])

    def load_data_reviews(self):
        # Load file from yelp dataset
        filename = '../data/data_labelled.txt'
        file = open(filename)
        # create training data
        train_data = []
        # format data
        for line in file:
            tokens = line.split()
            text, label = " ".join(tokens[:-1]), int(tokens[-1])
            train_data.append((text, label))
        random.shuffle(train_data)
        train_data = train_data[-self.limit:]
        texts, labels = zip(*train_data)
        cats = [{'POSITIVE': bool(y)} for y in labels]
        split = int(len(train_data) * self.split)
        return (texts[:split], cats[:split]), (texts[split:], cats[split:])