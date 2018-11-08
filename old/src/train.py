from pathlib import Path

import json
import spacy
import random
import sys
from spacy.util import minibatch


TRAIN_DATA = [
    ('find a cafe with great wifi.', {
        'heads': [0, 2, 0, 5, 5, 2, 0],  # index of token head
        'deps': ['ROOT', '-', 'PLACE', '-', 'QUALITY', 'ATTRIBUTE', '-']
    }),
    ("find a hotel near the beach", {
        'heads': [0, 2, 0, 5, 5, 2],
        'deps': ['ROOT', '-', 'PLACE', 'QUALITY', '-', 'ATTRIBUTE']
    }),
    ("find me the closest gym that's open late", {
        'heads': [0, 0, 4, 4, 0, 6, 4, 6, 6],
        'deps': ['ROOT', '-', '-', 'QUALITY', 'PLACE', '-', '-', 'ATTRIBUTE', 'TIME']
    }),
    ("show me the cheapest store that sells flowers", {
        'heads': [0, 0, 4, 4, 0, 4, 4, 4],  # attach "flowers" to store!
        'deps': ['ROOT', '-', '-', 'QUALITY', 'PLACE', '-', '-', 'PRODUCT']
    }),
    ("find a nice restaurant in london", {
        'heads': [0, 3, 3, 0, 3, 3],
        'deps': ['ROOT', '-', 'QUALITY', 'PLACE', '-', 'LOCATION']
    }),
    ("show me the coolest hostel in berlin", {
        'heads': [0, 0, 4, 4, 0, 4, 4],
        'deps': ['ROOT', '-', '-', 'QUALITY', 'PLACE', '-', 'LOCATION']
    }),
    ("find a good italian restaurant near work", {
        'heads': [0, 4, 4, 4, 0, 4, 5],
        'deps': ['ROOT', '-', 'QUALITY', 'ATTRIBUTE', 'PLACE', 'ATTRIBUTE', 'LOCATION']
    })
]

def create_training_data():
    file = open(sys.argv[1])
    json_text = json.load(file)

    train_data = []
    train_data.append((json_text["text"], {'heads': json_text["heads"], 'deps': json_text["deps"]}))

    return train_data


def create_training_data_sentence():
    file = open(sys.argv[1])
    json_text = json.load(file)

    # Initialise variables
    current_sentence = ""
    last_word_count = 0
    current_word_count = 0
    current_heads = []
    current_deps = []
    train_data = []

    # Loop through text word by word and store in train_data sentence by sentence
    for word in json_text["text"].split():

        # If the word includes a full stop, break everything previous to the current word
        # and the current word into a sentence and append to train_data
        if word.find('.') != -1:
            current_sentence = current_sentence + word[:-1]

            # Set up heads and deps for the current sentence
            while current_word_count >= last_word_count:
                current_heads.append(json_text["heads"][last_word_count])
                current_deps.append(json_text["deps"][last_word_count])
                last_word_count = last_word_count + 1

            # Append the current sentence to train_data
            train_data.append((current_sentence, {'heads': current_heads, 'deps': current_deps}))

            # Clear variables for the next sentence
            current_sentence = ""
            current_heads = []
            current_deps = []
        else:
            # Append current word to the current sentence
            current_sentence = current_sentence + word + " "

        current_word_count = current_word_count + 1

    return train_data

def test_model(model):
    pass


def start_training(model=None, output=None, epoch=15):
    # train_data = create_training_data_sentence()
    train_data = create_training_data()
    print(train_data)

    # Loading or create an empty model.
    if model is not None:
        nlp = spacy.load(model)
        print("Loaded model '%s'." % model)
    else:
        nlp = spacy.blank('en')
        print("Created blank model to train.")

    # Create a fresh instance of parser.
    if 'parser' in nlp.pipe_names:
        nlp.remove_pipe('parser')
    parser = nlp.create_pipe('parser')
    nlp.add_pipe(parser, first=True)

    for text, tags in train_data:
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
    model = start_training()
    doc = model(u'The food is bad but the service is good')
    print([t.tag_ for t in doc])