import pandas as pd
import spacy
import random
from collections import Counter


# Define function to cleanup text by removing personal pronouns, stopwords, and puncuation
def cleanup_text(docs, logging=True):
    nlp = spacy.load('en')
    texts = []
    counter = 1
    for doc in docs:
        if counter % 1000 == 0 and logging:
            print("Processed %d out of %d documents." % (counter, len(docs)))
        counter += 1
        doc = nlp(doc, disable=['parser', 'ner'])
        tokens = [word for word in doc if not word.is_stop and not word.is_punct]
        tokens = [tok.lemma_.lower().strip() for tok in doc if tok.lemma_ != '-PRON-']
        tokens = ' '.join(tokens)
        texts.append(tokens)
    return pd.Series(texts)


def data_clean(path):
    file = open(path)
    data = file.readlines()
    print(cleanup_text(data))



if __name__ == '__main__':
    data_clean("train.ft.txt")
