from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from argparse import ArgumentParser
from pathlib import Path

polynomial_degree = 2

sample_docs = [
  "The iPhone has a great camera.", 
  "The screen on the iPhone is not great.",
  "The iPhone provides great battery life for users.",
  "The iPhone's camera isn't great"
]

sample_sentiments = [
  0.9,
  -0.8,
  0.95
]

vectorizer = CountVectorizer()

'''
@param sample_docs := list of strings (documents)
@param sample_sentiments := list of sentiment scores
@returns (bag_of_word_matrix, sentiment_vector)
'''
def generate_matrix(vectorizer=vectorizer, docs=sample_docs, sentiments=sample_sentiments):
  matrix = vectorizer.fit_transform(docs)
  sentiments = np.array(sentiments)

  # print(vectorizer.vocabulary_)
  # print(matrix.shape)
  # print(matrix.toarray())

  return matrix, sentiments


def train_model(folder, extension='txt'):
  pathlist = Path(folder).glob('*.' + extension)
  docs = []
  sentiments = []
  for path in pathlist:
    print(path)
    with open(str(path), 'r') as f:
      for line in f:
        line = line.strip()
        
        split = len(line) - 1
        sentence, score = line[:split], line[split:]
        docs.append(sentence.lower())
        sentiments.append(-1 if int(score) == 0 else 1) 

  matrix, vector = generate_matrix(vectorizer, docs, sentiments)
  model = LinearRegression()
  
  print("Fitting model")
  model.fit(matrix, vector)
  return model

def predict(model, text):
  test_vector = vectorizer.transform([text])
  return model.predict(test_vector)


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument('folder', type=str)

  args = parser.parse_args()
  folder = args.folder

  model = train_model(folder)
  
  while True:
    print("Enter test text: ", end="")
    text = input().strip()
    if not text:
      break

    score = predict(model, text)
    print(score)