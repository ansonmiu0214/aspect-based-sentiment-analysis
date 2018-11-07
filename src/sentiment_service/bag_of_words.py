from src.models import SentimentService
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from pathlib import Path


class BagOfWords(SentimentService):
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.is_trained = False

    def compute_sentiment(self, text):
        if not self.is_trained:
            self.train()
            self.is_trained = True

        # Vectorise input text
        vector = self.vectorizer.transform([text])
        [score] = self.model.predict(vector)
        return score

    def train(self):
        # Parse training data
        pathlist = Path('sentiment_service/BoW_training').glob('*.txt')
        docs = []
        sentiments = []

        for path in pathlist:
            print(path)
            with open(str(path), 'r') as file:
                for line in file:
                    line = line.strip()

                    # Split into sentence and score
                    idx = len(line) - 1
                    sentence, score = line[:idx], line[idx:]
                    docs.append(sentence.lower())
                    sentiments.append(-1 if int(score) == 0 else 1)

        print("Training data parsed.")

        # Generate BoW matrix and sentiment vector
        matrix = self.vectorizer.fit_transform(docs)
        vector = np.array(sentiments)

        self.model = LinearRegression()
        self.model.fit(matrix, vector)
        print("Model fitted.")
