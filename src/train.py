import spacy
import random
from spacy.util import minibatch


def create_training_data():
    return


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
        for itn in epoch:
            random.shuffle(train_data)
            losses = {}
            batches = minibatch(train_data, size=4)
            for batch in batches:
                texts, labels = zip(*batch)
                nlp.update(texts, labels, sgd=optimizer, losses=losses)


def evalutation(model, data):
    # return all the E&A pairs and evidences
    pass
