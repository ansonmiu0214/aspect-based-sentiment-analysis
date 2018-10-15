import spacy


def create_training_data():
    pass


def start_training(model=None, output=None, epoch=10):
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
    nlp.add_pipe(nlp.create_pipe('parser'), first=True)


def evalutation(model, data):
    # return all the E&A pairs and evidences
    pass
