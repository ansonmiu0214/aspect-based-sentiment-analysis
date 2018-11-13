class Eas:
    def __init__(self, entity, attribute, sentiment, sentence, document):
        self.entity = entity
        self.attribute = attribute
        self.sentiment = sentiment
        self.sentence = sentence
        self.document = document

    def __repr__(self):
        return "Eas('{}', '{}', '{}', '{}', '{}')".format(self.entity, self.attribute, self.sentiment, self.sentence, self.document)