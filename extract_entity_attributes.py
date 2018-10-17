# Given text, output a list of entity-attribute pairs.

import argparse
import spacy
from spacy import displacy
from spacy.symbols import acomp, advmod, dobj, nsubj, VERB, conj, attr


def add_to_dict(dictionary, key, value):
    if key in dictionary:
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]


def get_phrase(token):
    subtree = token.subtree
    return " ".join(map(lambda x: x.text, subtree))


# Find the NSUBJ linked to the token.
# e.g. given "The battery life of the iPhone is..." and token="is", return the subject.
def extract_subjects(token):
    subjects = list()
    current = token
    while not subjects:
        for child in current.children:
            if child.dep == nsubj:
                subjects.append(get_phrase(child))
        current = current.head

    return subjects


def extract_attributes(token):
    attributes = list()
    ATTR_DEPENDENCIES = { acomp, dobj, advmod, attr }

    for child in token.children:
        dep = child.dep
        if dep in ATTR_DEPENDENCIES:
            # check if child has conjunction
            conjs = list(filter(lambda x: x.dep == conj, child.children))

            if len(conjs) > 0:
                attributes.append(child.text)
                attributes += list(map(get_phrase, conjs))
            else:
                attributes.append(get_phrase(child))
                # attributes.append(token.text + " " + get_phrase(child))

    return attributes


def main(text):
    print('Loading model.')
    nlp = spacy.load('en')

    print('Processing text.')
    doc = nlp(text)

    print('Extracting entity-attribute pairs.')

    dictionary = {}

    for token in doc:
        if token.pos == VERB:
            subjects = extract_subjects(token)
            attributes = extract_attributes(token)

            for subject in subjects:
                for attribute in attributes:
                    add_to_dict(dictionary, subject, attribute)

    print(dictionary)

    displacy.serve(doc, style="dep")


text = '''Python packaging may or may not actually be very bad but at the same time also great today.''' \
       '''Google's directions are not very much as terrible or bad as you think.'''
# Outputs {'python': ['also great', 'same', 'very bad'], 'google': ['not very much as terrible or bad']}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file")
    parser.add_argument("-t", "--text", default=text)
    args = parser.parse_args()

    data = ""
    if args.file:
        with open(args.file, 'r') as file:
            data = file.read().replace('\n', '')
    else:
        data = args.text

    # print(main(data))
    main(data)