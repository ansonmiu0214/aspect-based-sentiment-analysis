# Given text, output a list of entity-attribute pairs.

import argparse
import spacy


def add_to_dict(dictionary, key, value):
    if key in dictionary:
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]


def main(text):
    VERBOSE = False
    SKIP_ENTITIES = ['LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']
    ADJ_JOIN_POS = ['ADJ', 'ADV', 'CCONJ', 'ADP']

    print('Loading model.')

    nlp = spacy.load('en_core_web_lg')

    print('Processing text.')

    doc = nlp(text)

    print('Extracting entity-attribute pairs.')

    dictionary = {}

    for entity in doc.ents:
        if entity.label_ in SKIP_ENTITIES:
            continue

        if VERBOSE:
            print('-- Found entity:', entity.text + '(' + entity.lemma_ + ')', entity.label_)

        attr = None

        for i in range(len(entity.sent), 0, -1):
            token = entity.sent[i - 1]

            if attr is not None:
                if token.pos_ in ADJ_JOIN_POS:
                    attr = token.lemma_ + ' ' + attr
                else:
                    add_to_dict(dictionary, entity.lemma_, attr)
                    attr = None
            elif token.pos_ == 'ADJ':
                attr = token.lemma_

            if VERBOSE:
                print('- Found token:', token.text + '(' + token.lemma_ + ')', token.pos_,
                      token.dep_ + '(' + spacy.explain(token.tag_) + ')')

    return dictionary


text = '''Python packaging may or may not actually be very bad but at the same time also great today.''' \
       ''' Google's directions are not very much as terrible or bad as you think.'''
# Outputs {'python': ['also great', 'same', 'very bad'], 'google': ['not very much as terrible or bad']}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file")
    parser.add_argument("-t", "--text", default=text)
    args = parser.parse_args()

    data = ""
    if args.file:
        with open('data.txt', 'r') as file:
            data = file.read().replace('\n', '')
    else:
        data = args.text

    print(main(data))
