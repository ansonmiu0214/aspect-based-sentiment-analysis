# Given text, output a list of entity-attribute pairs.

import argparse
import spacy
from spacy.symbols import acomp, amod, advmod, dobj, nsubj, VERB, conj, attr, NOUN, PROPN, prep, poss, nmod, ADJ

compound = 7037928807040764755


# Get tokens at end of arcs from the current token.
def get_sources(token, arcs):
    return [child for child in token.children if child.dep in arcs]


# Extract entity-attribute pairs from a subject noun (before the verb)
# e.g. "Apple's iPhone has a good camera" -> [(Apple, iPhone)]
def extract_entity_attributes(noun):
    entity_attributes = list()

    entity_arcs = {poss, nmod, compound}
    # If current noun is a proper noun, it is assigned as an entity,
    # conjugated proper nouns are also found and assigned as entities.
    # We assume an entity does not have arcs to an attribute, only from.
    if noun.pos == PROPN:
        entity_attributes.append((noun.text, None))
        entity_sources = get_sources(noun, {conj})

        for source in entity_sources:
            entity_attributes.extend(extract_entity_attributes(source))
    # If current noun is a regular noun, it is assigned as an attribute,
    # its entity (if any) or conjugated attributes are also found.
    elif noun.pos == NOUN:
        entity_sources = get_sources(noun, entity_arcs)

        for source in entity_sources:
            entity_attributes.extend(extract_entity_attributes(source))
        entity_attributes = list(map(lambda e_a: (e_a[0], noun.text), entity_attributes))

        if not entity_attributes:
            entity_attributes.append((None, noun.text))

        attribute_sources = get_sources(noun, {conj})
        for source in attribute_sources:
            entity_attributes.extend(extract_entity_attributes(source))

    return entity_attributes


def extract_attribute_sentiments(token, entity_attributes):
    entity_attribute_sentiments = list()

    if token.pos == NOUN:
        sentiment_sources = get_sources(token, {amod})
        for source in sentiment_sources:
            entity_attribute_sentiments.extend(list(
                map(lambda e_a: (e_a[0], token.text, source.text),
                    filter(lambda e_a: not e_a[1], entity_attributes)
                    )
            ))

        further_sources = get_sources(token, {conj})
        for source in further_sources:
            entity_attribute_sentiments.extend(
                extract_attribute_sentiments(source, entity_attributes)
            )
    elif token.pos == ADJ:
        entity_attribute_sentiments.extend(list(
            map(lambda e_a: (e_a[0], e_a[1], token.text), entity_attributes)
        ))
        further_sources = get_sources(token, {conj})
        for source in further_sources:
            entity_attribute_sentiments.extend(
                extract_attribute_sentiments(source, entity_attributes)
            )

    return entity_attribute_sentiments


def extract_tuples(verb):
    entity_attribute_arcs = {nsubj}
    attribute_sentiment_arcs = {dobj, acomp, prep}

    entity_attribute_sources = get_sources(verb, entity_attribute_arcs)
    entity_attributes = list()
    for source in entity_attribute_sources:
        entity_attributes.extend(extract_entity_attributes(source))

    current = verb.head
    while not entity_attributes or not current:
        sources = get_sources(current, entity_attribute_arcs)
        for source in sources:
            entity_attributes.extend(extract_entity_attributes(source))

    entity_attribute_sentiments = list()
    attribute_sentiment_sources = get_sources(verb, attribute_sentiment_arcs)
    for source in attribute_sentiment_sources:
        entity_attribute_sentiments.extend(extract_attribute_sentiments(source, entity_attributes))

    return entity_attribute_sentiments


def main(text):
    print('Loading model.')
    nlp = spacy.load('en')

    print('Processing text.')
    doc = nlp(text)

    print('Extracting entity-attribute pairs.')

    entity_attribute_sentiments = list()

    for token in doc:
        if token.pos == VERB:
            entity_attribute_sentiments.extend(extract_tuples(token))
    print(entity_attribute_sentiments)


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
