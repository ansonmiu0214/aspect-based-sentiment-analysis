import thinc.extra.datasets

import pandas as pd
import spacy
import random
import csv

from collections import Counter

# Define function to cleanup text by removing personal pronouns, stopwords, and puncuation
from spacy.symbols import NOUN
from spacy.lang.en.stop_words import STOP_WORDS

stopwords = list(STOP_WORDS)


def find_n_most_frequent_word(docs, logging=True, word_count=10):
    nlp = spacy.load('en')
    texts = []
    counter = 1
    for doc in docs:
        if counter % 1000 == 0 and logging:
            print("Processed %d out of %d documents." % (counter, len(docs)))
        counter += 1
        doc = nlp(doc, disable=['parser', 'ner'])
        tokens = [tok.lemma_.lower().strip() for tok in doc if tok.pos == NOUN and not tok.is_stop]
        tokens = ' '.join(tokens)
        texts.append(tokens)
    text_cleaned = pd.Series(texts)
    text_cleaned = ' '.join(text_cleaned).split()
    text_cleaned = [word for word in text_cleaned if word != '\'s']
    text_counter = Counter(text_cleaned)
    return [word[0] for word in text_counter.most_common(word_count)]


if __name__ == '__main__':

    print("Loading data...")
    # train_data, _ = thinc.extra.datasets.imdb()
    # train_data = [i[0] for i in train_data]

    train_data = []
    with open('Amazon_Unlocked_Mobile.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            train_data.append(row[4])

    most_common = find_n_most_frequent_word(train_data)

    nlp = spacy.load("en_core_web_md")

    tokens = nlp(' '.join(most_common))
    for i in range(len(tokens)):
        for j in range(i + 1, len(tokens)):
            if tokens[i].similarity(tokens[j]) >= 0.7:
                most_common.pop(j)

    print(most_common)
