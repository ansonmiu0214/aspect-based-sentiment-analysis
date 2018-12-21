import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding
import csv
from pprint import pprint
import ast

def main():
    data = list()
    with open('training.csv', newline='') as trainingdata:
        trainingdata.readline()
        reader = csv.reader(trainingdata)
        for row in reader:
            data.append((row[0], {'heads': ast.literal_eval(row[1]), 'deps': ast.literal_eval(row[2])}))

    nlp = spacy.blank('en')  # create blank Language class
    print("Created blank 'en' model")

    # We'll use the built-in dependency parser class, but we want to create a
    # fresh instance – just in case.
    if 'parser' in nlp.pipe_names:
        nlp.remove_pipe('parser')
    parser = nlp.create_pipe('parser')
    nlp.add_pipe(parser, first=True)

    for text, annotations in data:
        for dep in annotations.get('deps', []):
            parser.add_label(dep)

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'parser']
    with nlp.disable_pipes(*other_pipes):  # only train parser
        optimizer = nlp.begin_training()
        for itn in range(5):
            random.shuffle(data)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(data, size=compounding(4., 32., 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations, sgd=optimizer, losses=losses)
            print('Losses', losses)

    # test the trained model
    test_model(nlp)

    # save model to output directory
    output_dir = Path('trained_model/')
    if not output_dir.exists():
        output_dir.mkdir()
    nlp.to_disk(output_dir)
    print("Saved model to", output_dir)

    # test the saved model
    print("Loading from", output_dir)
    nlp2 = spacy.load(output_dir)
    test_model(nlp2)


def test_model(nlp):
    texts = ["Australian imports are suffering due to a lower than expected price.", "The BHP found support from troops all over Africa."]
    docs = nlp.pipe(texts)
    for doc in docs:
        print(doc.text)
        print([(t.text, t.dep_, t.head.text) for t in doc if t.dep_ != '-'])

if __name__ == '__main__':
    main()
