# Given text, output a list of entity-attribute pairs.

import argparse
import json
import spacy
from spacy.symbols import acomp, amod, dobj, nsubj, VERB, conj, NOUN, PROPN, prep, poss, nmod, ADJ, neg, attr, cc

# Missing variables from spacy.symbols
compound = 7037928807040764755

def concatMap(f, ls):
    mapped = map(f, ls)
    res = []
    for m in mapped:
        res += m
    return res


# Returns the subtree of a token as a phrase.
def get_phrase(token, is_adjective=False):
    subtree = list(token.subtree)
    # Handles possible phrase duplication when adjective has a conjunction
    if is_adjective:
        prune_branches = [list(child.subtree) for child in token.children if child.dep in {cc, conj}]
        subtree = [subtoken for subtoken in subtree if subtoken not in [
            branch_token for branch in prune_branches for branch_token in branch
        ]]
    phrase = " ".join(map(lambda x: x.text, subtree))
    return phrase


# Get tokens at end of arcs from the current token.
def get_sources(token, arcs):
    return [child for child in token.children if child.dep in arcs]


# Extract entity-attribute pairs from a subject noun (before the verb)
# e.g. "Apple's iPhone has a good camera" -> [(Apple, iPhone)]
def extract_entity_attributes(noun):
    entity_attributes = list()

    # If current noun is a proper noun, it is assigned as an entity.
    if noun.pos == PROPN:
        entity_attributes.append((noun.text, None))

    # If current noun is a regular noun, it is assigned as an attribute.
    elif noun.pos == NOUN:
        # Try to find the relevant entity.
        entity_sources = get_sources(noun, {poss, nmod, compound})
        for source in entity_sources:
            entity_attributes.extend(extract_entity_attributes(source))
        entity_attributes = list(map(lambda e_a: (e_a[0], noun.text), entity_attributes))

        if not entity_attributes:
            entity_attributes.append((None, noun.text))

    # Extract entity-attributes from further conjugated tokens.
    further_sources = get_sources(noun, {conj})
    for source in further_sources:
        entity_attributes.extend(extract_entity_attributes(source))

    return entity_attributes


# Extract attribute-sentiment pairs and attach onto given entity-attribute pairs.
# e.g. "Apple has good cameras" -> [(Apple, cameras, good)]
def extract_attribute_sentiments(token, entity_attributes, negation=None):
    entity_attribute_sentiments = []

    # Add the negation prefix if it exists
    prefix = (get_phrase(negation) + " ") if negation else ""

    # If token is a noun, attach attribute-sentiment pair to entity-attribute
    # pairs which do not currently have an attribute.
    if token.pos == NOUN:
        sentiment_sources = get_sources(token, {amod})
        for source in sentiment_sources:
            entity_attribute_sentiments += list(
                map(lambda e_a: (e_a[0], prefix + token.text, get_phrase(source, True)),
                    filter(lambda e_a: not e_a[1], entity_attributes)
                    )
            )

    # If token is an adjective, attach sentiment to all entity-attribute pairs.
    elif token.pos == ADJ:
        print("token={} negation={}".format(token, prefix))
        entity_attribute_sentiments += list(
            map(lambda e_a: (e_a[0], e_a[1], prefix + get_phrase(token, True)), entity_attributes)
        )

    # Extract attribute-sentiment pairs from further conjugated tokens.
    further_sources = get_sources(token, {conj})
    for source in further_sources:
        entity_attribute_sentiments += extract_attribute_sentiments(source, entity_attributes)

    return entity_attribute_sentiments

def extract_nearest_negation(token, negations):
    # Compute distance from each negation to the source token
    # e.g. "not good but perfect", so "good" is 1 away and "perfect" is 3 away
    dist_from_neg = map(lambda x: (token.i - x.i, x), negations)

    # The relevant negations are where the source is AFTER the negation
    # so ignore entries with negative distances
    relevant_negations = list(filter(lambda x: x[0] > 0, dist_from_neg))

    negation = None
    if relevant_negations:
        # Relevant negation is the one that occurs first when searching
        # to the right of the token
        _, negation = min(relevant_negations)
    return negation


def extract_tuples(verb):
    entity_attribute_arcs = {nsubj}
    attribute_sentiment_arcs = {dobj, acomp, prep}

    # Collate the negations linked to the verb
    negations = filter(lambda x: x.dep == neg, verb.children)

    current = verb
    entity_attributes = []
    while not entity_attributes and current:
        sources = get_sources(current, entity_attribute_arcs)
        entity_attributes = concatMap(extract_entity_attributes, sources)
        current = current.head

    # Attach attribute-sentiment pairs.
    entity_attribute_sentiments = concatMap(
                lambda s:
                    extract_attribute_sentiments(s,
                                                 entity_attributes,
                                                 extract_nearest_negation(s, negations)
                                                ),
                get_sources(verb, attribute_sentiment_arcs)
            )
    return entity_attribute_sentiments


def extract_entity_attribute_sentiment(doc):
    entity_attribute_sentiments = []
    for token in doc:
        if token.pos == VERB:
            entity_attribute_sentiments += extract_tuples(token)
    return entity_attribute_sentiments;


def position_to_JSON(t):
    if t is None:
        return json.dumps({'start': -1, 'end': -1})
    return json.dumps({'start': t[0], 'end': t[1]})


def tuple_to_JSON(tuples):
    result = []
    for t in tuples:
        result += json.dumps(
                {
                    'entity': position_to_JSON(t[0]),
                    'attribute': position_to_JSON(t[1]),
                    'sentiment': position_to_JSON(t[2])
                }
            )


def main(text):
    print('Loading model.')
    nlp = spacy.load('en')

    print('Processing text.')
    doc = nlp(text)

    print('Extracting entity-attribute pairs.')
    print(extract_entity_attribute_sentiment(doc))


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

    main(data)
