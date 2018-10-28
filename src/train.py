from pathlib import Path

import spacy
import random
import sys
from spacy.util import minibatch


TRAIN_DATA = [
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

            continue
        else:

            if is_sentence:
                sentences.append(elem)
            else:
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

    # Loading or create an empty model.
    if model is not None:
        nlp = spacy.load(model)
        print("Loaded model '%s'." % model)
    else:
        nlp = spacy.blank('en')
        print("Create blank model to train.")

    # Create a fresh instance of tagger.
    if 'parser' in nlp.pipe_names:
        nlp.remove_pipe('parser')
    parser = nlp.create_pipe('parser')
    nlp.add_pipe(parser, first=True)

    for text, tags in TRAIN_DATA:
        for dep in tags.get('deps', []):
            parser.add_label(dep)

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


    if output is not None:
        output = Path(output)
        if not output.exists():
            output.mkdir()
        nlp.to_disk(output)
        print("Saved model to directory %s." % output)

    return nlp

def test_model(nlp,text):
    docs = nlp.pipe(text)
    for doc in docs:
        print(doc.text)



if __name__ ==  '__main__':
    model = start_training()
    doc = model(u'The food is bad but the service is good')
    print([t.tag_ for t in doc])
