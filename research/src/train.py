from pathlib import Path

import json
import spacy
import random
import sys
from spacy.util import minibatch

'''
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

'''

'''
TRAIN_DATA = [
    ('The economy of Mexico is back on track', {
        'heads': [0, 3, 0, 3, 0, 0, 0, 0],  # index of token head
        'deps': ['-', 'ATTRIBUTE', '-', 'ENTITY', '-', '-', '-', '-']
    }),
    ('Argentina stocks closed at record high with interest rates at 19 month lows', {
        'heads': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'deps': ['ENTITY', 'ATTRIBUTE', '-', '-', '-', '-', '-', 'ATTRIBUTE', 'ATTRIBUTE', '-', '-', '-', '-']
    }),
    ('The company Chrysler is having record high profits over last year', {
        'heads': [0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0],
        'deps': ['-', '-', 'ENTITY', '-', '-', '-', '-', 'ATTRIBUTE', '-', '-', '-']
    }),
    ('Mexico has a bright future for their economy', {
        'heads': [1, 1, 1, 4, 7, 1, 1, 0],
        'deps': ['ENTITY', '-', '-', '-', '-', '-', '-', 'ATTRIBUTE']
    })
]

'''

'''

TRAIN_DATA = [
    ('Mexico has a bright future for their economy', {
        'heads': [1, 1, 1, 2, 3, 2, 0, 0],
        'deps': ['ENTITY', '-', '-', '-', '-', '-', '-', 'ATTRIBUTE']
    }),

    ('The company Chrysler is having record high profits over last year', {
        'heads': [1, 2, 4, 4, 4, 6, 7, 2, 4, 10, 4],
        'deps': ['-', '-', 'ENTITY', '-', '-', '-', '-', 'ATTRIBUTE', '-', '-', '-']
    }),


    ('Last year Chrysler had record high profits', {
        'heads': [1, 3, 3, 3, 5, 6, 2],
        'deps': ['-', '-', 'ENTITY', '-', '-', '-', 'ATTRIBUTE']
    }),

    ('When it was reported that the stocks of Argentina fell', {
        'heads': [3, 3, 3, 3, 9, 9, 8, 6, 5, 3],
        'deps': ['-', '-', '-', '-', '-', '-', 'ATTRIBUTE', '-', 'ENTITY','-']
    }),


    ('Apple is having issues with its iPhone sales which fell to a record low last year', {
        'heads': [2, 2, 2, 2, 3, 0, 0, 0, 9, 7, 9, 10, 13, 11,15,9],
        'deps': ['ENTITY', '-', '-', '-', '-', '-', 'ATTRIBUTE', 'ATTRIBUTE', '-', '-', '-','-','-','-','-','-']
    }),

    ('Argentina stocks closed at record high with interest rates at 19 month lows', {
        'heads': [2, 0, 2, 2, 5, 2, 5, 7, 6, 2, 11, 12, 2],
        'deps': ['ENTITY', 'ATTRIBUTE', '-', '-', '-', '-', '-', 'ATTRIBUTE', 'ATTRIBUTE', '-', '-', '-', '-']
    }),

    ('Mexico has a bright future for their economy', {
        'heads': [1, 1, 1, 2, 3, 4, 0, 0],
        'deps': ['ENTITY', '-', '-', '-', '-', '-', '-', 'ATTRIBUTE']
    }),


    ('Analysts report the company shares will decrease soon',{
        'heads': [1,1,6,2,3,6,1,6],
        'deps':  ['-','-','-','ENTITY','ATTRIBUTE', '-', '-','-']
    }),

    ('It was reported that Facebook profits dropped last month ', {
        'heads': [2,2,2,6,6,4,2,8,6],
        'deps':  ['-','-','-','-','ENTITY','ATTRIBUTE', '-','-','-']
    }),


    ('It was reported that Facebook prices dropped last month ', {
        'heads': [2,2,2,6,6,4,2,8,6],
        'deps':  ['-','-','-','-','ENTITY','ATTRIBUTE', '-','-','-']
    }),


    ('It was reported that Facebook shares dropped last month ', {
        'heads': [2,2,2,6,6,4,2,8,6],
        'deps':  ['-','-','-','-','ENTITY','ATTRIBUTE', '-','-','-']
    }),

    ('Studies show that Twitter stock prices have dropped', {
        'heads': [1,1,7,7,5,3,7,1],
        'deps': ['-','-','-','ENTITY', '-', 'ATTRIBUTE', '-', '-']
    }),


    ('Reports indicate that the shares of Google dropped last week', {
        'heads': [1,1,7,7,3,4,5,1,9,7],
        'deps': ['-','-','-','-', 'ATTRIBUTE', '-', 'ENTITY', '-','-','-']
    }),

    ('Analysts say that the stocks of Google dropped last week', {
        'heads': [1,1,7,7,3,4,5,1,9,7],
        'deps': ['-','-','-','-', 'ATTRIBUTE', '-', 'ENTITY', '-','-','-']
    }),


    ('Reports indicate that the shares of Facebook reached a record low', {
        'heads': [1,1,0,0,6,0,0,1,9,10,7],
        'deps': ['-','-','-','-', 'ATTRIBUTE', '-', 'ENTITY', '-','-','-','-']
    }),


    ('Australian stocks have faced losses after Apples worst day of trading sent shockwaves around the world', {
        'heads': [3,0,3,3,3,3,5,8,3,8,6,8,11,12,13,14],
        'deps': ['ENTITY','ATTRIBUTE', '-','-', '-', '-', 'ENTITY', '-','-','-','ATTRIBUTE','-','-','-','-','-']
    }),

    ('Facebook reported a big drop in stocks last week', {
        'heads': [1,1,1,4,1,1,0,1,1],
        'deps': ['ENTITY', '-', '-', '-', '-', '-', 'ATTRIBUTE', '-', '-']
    }),

    ('Google reported a big rise in prices last month', {
        'heads': [1,1,1,4,1,1,0,1,1],
        'deps': ['ENTITY', '-', '-', '-', '-', '-', 'ATTRIBUTE', '-', '-']
    }),


    ('Apple had a huge drop in shares last year', {
        'heads': [1,1,1,4,1,1,0,1,1],
        'deps': ['ENTITY', '-', '-', '-', '-', '-', 'ATTRIBUTE', '-', '-']
    }),


    ('Iphone users were surprised by its price', {
        'heads': [3,0,3,3,3,3,0],
        'deps': ['ENTITY','ATTRIBUTE', '-', '-', '-','-', 'ATTRIBUTE']
    }),

    ('Google reported their shares fell last year', {
        'heads': [1, 1, 0, 0, 1, 6, 4],
        'deps': ['ENTITY', '-', '-', 'ATTRIBUTE', '-', '-','-']
    }),

    ('Google indicated their prices fell last year', {
        'heads': [1, 1, 0, 0, 1, 6, 4],
        'deps': ['ENTITY', '-', '-', 'ATTRIBUTE', '-', '-', '-']
    }),

    ('Apple suggested their stocks fell last year', {
        'heads': [1, 1, 0, 0, 1, 6, 4],
        'deps': ['ENTITY', '-', '-', 'ATTRIBUTE', '-', '-', '-']
    }),

    ('Analysts reported that shares fell last year', {
        'heads': [1, 1, 0, 0, 1, 6, 4],
        'deps': ['ENTITY', '-', '-', 'ATTRIBUTE', '-', '-', '-']
    }),

    ('Apple indicated their prices fell last year', {
        'heads': [1, 1, 0, 0, 1, 6, 4],
        'deps': ['ENTITY', '-', '-', 'ATTRIBUTE', '-', '-', '-']
    }),

    ('Goolge denied their stocks fell last year', {
        'heads': [1, 1, 0, 0, 1, 6, 4],
        'deps': ['ENTITY', '-', '-', 'ATTRIBUTE', '-', '-', '-']
    }),

    ('Apple acknowledged that prices rose last month', {
        'heads': [1, 1, 0, 0, 1, 6, 4],
        'deps': ['ENTITY', '-', '-', 'ATTRIBUTE', '-', '-', '-']
    }),

]
'''

TRAIN_DATA = [
('Facebook reported a big drop in stocks last week', {
        'heads': [0,0,0,0,0,0,0,0,0],
        'deps': ['ENTITY', '-', '-', '-', '-', '-', 'ATTRIBUTE', '-', '-']
    }),

    ('Google reported a big rise in prices last month', {
        'heads': [0,0,0,0,0,0,0,0,0],
        'deps': ['ENTITY', '-', '-', '-', '-', '-', 'ATTRIBUTE', '-', '-']
    }),


    ('Apple had a huge drop in shares last year', {
        'heads': [0,0,0,0,0,0,0,0,0],
        'deps': ['ENTITY', '-', '-', '-', '-', '-', 'ATTRIBUTE', '-', '-']
    }),


    ('Iphone users were surprised by its price', {
        'heads': [0,0,0,0,0,0,0],
        'deps': ['ENTITY','ATTRIBUTE', '-', '-', '-','-', 'ATTRIBUTE']
    }),

    ('Google reported their shares fell last year', {
        'heads': [0, 0, 0, 0, 0, 0, 0],
        'deps': ['ENTITY', '-', '-', 'ATTRIBUTE', '-', '-','-']
    }),


    ('Apple reported their shares rose last year', {
        'heads': [0, 0, 0, 0, 0, 0, 0],
        'deps': ['ENTITY', '-', '-', 'ATTRIBUTE', '-', '-','-']
    }),

    ('Facebook reported their shares fell last year', {
        'heads': [0, 0, 0, 0, 0, 0, 0],
        'deps': ['ENTITY', '-', '-', 'ATTRIBUTE', '-', '-','-']
    }),

    ('Google indicated their prices fell last year', {
        'heads': [0, 0, 0, 0, 0, 0, 0],
        'deps': ['ENTITY', '-', '-', 'ATTRIBUTE', '-', '-', '-']
    }),

    ('Apple suggested their stocks fell last year', {
        'heads': [0, 0, 0, 0, 0, 0, 0],
        'deps': ['ENTITY', '-', '-', 'ATTRIBUTE', '-', '-', '-']
    }),

    ('Analysts reported that shares fell last year', {
        'heads': [0, 0, 0, 0, 0, 0, 0],
        'deps': ['ENTITY', '-', '-', 'ATTRIBUTE', '-', '-', '-']
    }),

    ('Apple indicated their prices fell last year', {
        'heads': [0, 0, 0, 0, 0, 0, 0],
        'deps': ['ENTITY', '-', '-', 'ATTRIBUTE', '-', '-', '-']
    }),

    ('Google denied their stocks fell last year', {
        'heads': [0, 0, 0, 0, 0, 0, 0],
        'deps': ['ENTITY', '-', '-', 'ATTRIBUTE', '-', '-', '-']
    }),

    ('Apple acknowledged that prices rose last month', {
        'heads': [0, 0, 0, 0, 0, 0, 0],
        'deps': ['ENTITY', '-', '-', 'ATTRIBUTE', '-', '-', '-']
    }),

    ('Apple suggested that profits rose last month', {
        'heads': [0, 0, 0, 0, 0, 0, 0],
        'deps': ['ENTITY', '-', '-', 'ATTRIBUTE', '-', '-', '-']
    }),

    ('Google denied their profits fell last year', {
        'heads': [0, 0, 0, 0, 0, 0, 0],
        'deps': ['ENTITY', '-', '-', 'ATTRIBUTE', '-', '-', '-']
    }),

    ('Facebook reported their profits increased last week', {
        'heads': [0, 0, 0, 0, 0, 0, 0],
        'deps': ['ENTITY', '-', '-', 'ATTRIBUTE', '-', '-', '-']
    }),


]

TRAIN_DATA2 = [
    ('Last year it was reported that Apple prices rose dramatically', {
        'heads': [0,0,0,0,0,0,0,6,0,0],
        'deps':  ['-', '-', '-', '-', '-', '-', 'ENTITY', 'ATTRIBUTE', '-', '-']
    }),

    ('Last month it was reported that Apple stocks fell greatly', {
        'heads': [0,0,0,0,0,0,0,6,0,0],
        'deps':  ['-', '-', '-', '-', '-', '-', 'ENTITY', 'ATTRIBUTE', '-', '-']
    }),

    ('Last week it was suggested that Apple profits increased dramatically', {
        'heads': [0,0,0,0,0,0,0,6,0,0],
        'deps':  ['-', '-', '-', '-', '-', '-', 'ENTITY', 'ATTRIBUTE', '-', '-']
    }),
    ('Last year it was reported that Facebook prices rose dramtically', {
        'heads': [0,0,0,0,0,0,0,6,0,0],
        'deps':  ['-', '-', '-', '-', '-', '-', 'ENTITY', 'ATTRIBUTE', '-', '-']
    }),
    ('Last year it was reported that Twitter stocks fell quickly', {
        'heads': [0,0,0,0,0,0,0,6,0,0],
        'deps':  ['-', '-', '-', '-', '-', '-', 'ENTITY', 'ATTRIBUTE', '-', '-']
    }),

    ('Last year it was reported that Apple profits increased dramatically', {
        'heads': [0,0,0,0,0,0,0,6,0,0],
        'deps':  ['-', '-', '-', '-', '-', '-', 'ENTITY', 'ATTRIBUTE', '-', '-']
    }),
    ('Last week it was reported that Apple shares decreased spectacularly', {
        'heads': [0,0,0,0,0,0,0,6,0,0],
        'deps':  ['-', '-', '-', '-', '-', '-', 'ENTITY', 'ATTRIBUTE', '-', '-']
    }),
    ('Last month it was reported that Android prices fell extremely ', {
        'heads': [0,0,0,0,0,0,0,6,0,0],
        'deps':  ['-', '-', '-', '-', '-', '-', 'ENTITY', 'ATTRIBUTE', '-', '-']
    }),
    ('Last year it was reported that Apple prices rose dramtically', {
        'heads': [0,0,0,0,0,0,0,6,0,0],
        'deps':  ['-', '-', '-', '-', '-', '-', 'ENTITY', 'ATTRIBUTE', '-', '-']
    }),
]


def create_training_data():
    train_data = []

    _, *args = sys.argv
    for arg in args:
        file = open(arg)
        json_text = json.load(file)
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


def start_training(model=None, output=None, epoch=30):
    train_data = TRAIN_DATA2 + TRAIN_DATA
    # train_data = create_training_data()
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
        for _ in range(epoch):
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


def test_model(nlp, text):
    docs = nlp.pipe(text)
    for doc in docs:
        print(doc.text)


if __name__ == '__main__':
    model = start_training()#

    while True:
        print("Enter sentence: ", end="")
        doc = model(input().strip())
        print([(t.text, t.dep_, t.head.text) for t in doc if t.dep_ != '-'])
