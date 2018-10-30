from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

sample_docs = [
  "The iPhone has a great camera.", 
  "The iPhone has a bad screen.",
  "The iPhone provides great battery life for users."
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


if __name__ == "__main__":
  matrix, vector = generate_matrix()
  print(matrix.toarray())
  print(vector)


