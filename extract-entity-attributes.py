# Given text, output a list of entity-attribute pairs.

import argparse
import spacy
from spacy.symbols import acomp, advmod, dobj, nsubj, VERB, conj, attr, NOUN, PROPN, prep, poss, nmod


compound = 7037928807040764755


def get_sources(token, arcs):
    return [child for child in token.children if child.dep in arcs]


def extract_entity_attributes(noun):
    entity_attributes = list()

    entity_arcs = {poss, nmod, compound}
    if noun.pos == PROPN:
        entity_attributes.append((noun.text, None))
        entity_sources = get_sources(noun, {conj})

        for source in entity_sources:
            entity_attributes.extend(extract_entity_attributes(source))
    elif noun.pos == NOUN:
        entity_sources = get_sources(noun, entity_arcs)

        for source in entity_sources:
            entity_attributes.extend(extract_entity_attributes(source))
        entity_attributes = list(map(lambda e_a: (e_a[0], noun.text), entity_attributes))

        if len(entity_attributes) == 0:
            entity_attributes.append((None, noun.text))

        attribute_sources = get_sources(noun, {conj})
        for source in attribute_sources:
            entity_attributes.extend(extract_entity_attributes(source))

    return entity_attributes


def extract_tuples(verb):
    entity_attribute_arcs = {nsubj}
    attribute_sentiment_arcs = {dobj, acomp, prep}

    entity_attribute_sources = [child for child in verb.children if child.dep in entity_attribute_arcs]
    foobar = list()
    for s in entity_attribute_sources:
        foobar.extend(extract_entity_attributes(s))
    return foobar


def main(text):
    print('Loading model.')
    nlp = spacy.load('en')

    print('Processing text.')
    doc = nlp(text)

    print('Extracting entity-attribute pairs.')

    foobar = list()

    for token in doc:
        if token.pos == VERB:
            foobar.extend(extract_tuples(token))
    print(foobar)


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
        with open('data.txt', 'r') as file:
            data = file.read().replace('\n', '')
    else:
        data = args.text

    # print(main(data))
    main(data)
