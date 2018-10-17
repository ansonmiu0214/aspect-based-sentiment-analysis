from pathlib import Path

import spacy
import random
import sys
from spacy.util import minibatch

TAG_MAP = {
    'E': {'pos': 'NOUN'},
    'A': {'pos': 'NOUN'},
    'S': {'pos': 'ADJ'},
    '-': {'pos': 'NOUN'}
}

TRAIN_DATA = [
    ("I like green's eggs", {'tags': ['-', 'A', 'E', 'S', 'E']})
]

def create_training_data():
    file = open(sys.argv[1])
    data = file.readlines()
    sentences = []
    labels = []
    temp = []
    train_data = []

    is_sentence = True
    for d in data:
        elem = d.rstrip('\n')
        if elem == '/s':
            is_sentence = True
            continue
        elif elem == '/l':
            if is_sentence:
                is_sentence = False
                continue
            else:
                labels.append(temp.copy())
                temp.clear()
                #print(labels)

            continue
        else:
            if is_sentence:
                sentences.append(elem)
            else:
                #print(elem)
                temp.append(elem)
    print(sentences)
    print(labels)

    for pair in zip(sentences, labels):
        train_data.append((pair[0], {'tags': pair[1]}))

    return train_data




def test_model(model):
    pass


def start_training(model=None, output=None, epoch=10):
    train_data = create_training_data()
    print(train_data)
    # train_data = TRAIN_DATA

    # Loading or create an empty model.
    if model is not None:
        nlp = spacy.load(model)
        print("Loaded model '%s'." % model)
    else:
        nlp = spacy.blank('en')
        print("Create blank model to train.")

    # Create a fresh instance of tagger.
    if 'tagger' in nlp.pipe_names:
        nlp.remove_pipe('tagger')
    tagger = nlp.create_pipe('tagger')

    for text, label in TAG_MAP.items():
        tagger.add_label(text, label)
    nlp.add_pipe(tagger, first=True)

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'tagger']
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for _ in  range(epoch):
            random.shuffle(train_data)
            losses = {}
            batches = minibatch(train_data, size=4)
            for batch in batches:
                texts, labels = zip(*batch)
                nlp.update(texts, labels, sgd=optimizer, losses=losses)
            print('Losses', losses)

    # test the model with out-of-domain data
    #test_model(nlp)

    if output is not None:
        output = Path(output)
        if not output.exists():
            output.mkdir()
        nlp.to_disk(output)
        print("Saved model to directory %s." % output)

    def test_model(nlp,text):
        docs = nlp.pipe(text)
        for doc in docs:
            print(doc.text)
            #print data based on how labels are tagged

    # test the saved model to check it is correctly saved.
    #nlp_updated_model = spacy.load(output)
    #test_model(nlp_updated_model)


def evalutation(model, data):
    # return all the E&A pairs and evidences
    pass

if __name__ ==  '__main__':
    start_training()
    # print(create_training_data())
    # print(TRAIN_DATA)
