from pathlib import Path

import json
import spacy
import random
import sys
from spacy.util import minibatch


TRAIN_DATA = [
]

def create_training_data():
    file = open(sys.argv[1])
    json_text = json.load(file)

    train_data = []

    train_data.append((json_text["text"], {'heads': json_text["heads"], 'deps': json_text["deps"]}))
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

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'parser']
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
    # model = start_training()
    # doc = model(u'The food is bad but the service is good')
    # print([t.tag_ for t in doc])
    create_training_data()