from pathlib import Path

import spacy
import random
import sys
from spacy.util import minibatch


def create_training_data():
    file = open(sys.argv[1])
    data = file.readlines()
    sentences = []
    labels = []
    temp = []
    train_data = []

    s = True
    for d in data:
        if d == '/s':
            s = True
            continue
        elif d == '/l':
            if s:
                s = False
                continue
            else:
                labels.append(temp)
                temp.clear()

            continue
        else:
            if s:
                sentences.append(d)
            else:
                temp.append(d)

    for elem in zip(sentences,labels):
        train_data.append(elem[0],{'tags': elem[1]})

    return train_data




def test_model(model):
    pass


def start_training(model=None, output=None, epoch=10):
    train_data = create_training_data()

    # Loading or create a empty model.
    if model is not None:
        nlp = spacy.load(model)
        print("Loaded model '%s'." % model)
    else:
        nlp = spacy.blank('en')
        print("Create blank model to train.")

    # Create a fresh instance of parser.
    if 'parser' in nlp.pipe_names:
        nlp.remove_pipe('parser')
    parser = nlp.create_pipe('parser')
    nlp.add_pipe(nlp.create_pipe('parser'), first=True)

    for text, labels in train_data:
        for label in labels.get('deps', []):
            parser.add_label(label)

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'parser']
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for _ in epoch:
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
    nlp_updated_model = spacy.load(output)
    test_model(nlp_updated_model)


def evalutation(model, data):
    # return all the E&A pairs and evidences
    pass
