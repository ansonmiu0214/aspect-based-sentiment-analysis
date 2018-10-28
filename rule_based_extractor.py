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


def get_token_indices(token):
    if not token:
        return None
    return (token.idx, token.idx + len(token.text) - 1)


def get_phrase_indices(token, is_adjective=False):
    subtree = list(token.subtree)
    # Handles possible phrase duplication when adjective has a conjunction
    if is_adjective:
        prune_branches = map(lambda c: c.subtree, filter(lambda c: c.dep in {cc, conj}, token.children))
        subtree = [subtoken for subtoken in subtree if subtoken not in [
            branch_token for branch in prune_branches for branch_token in branch
        ]]
    indices = list(map(get_token_indices, subtree))
    if not indices:
        return None
    return (min(map(lambda i: i[0], indices)), max(map(lambda i: i[1], indices)))


# Returns the subtree of a token as a phrase.
def get_phrase(token, is_adjective=False):
    subtree = list(token.subtree)
    # Handles possible phrase duplication when adjective has a conjunction
    if is_adjective:
        prune_branches = map(lambda c: c.subtree, filter(lambda c: c.dep in {cc, conj}, token.children))
        subtree = [subtoken for subtoken in subtree if subtoken not in [
            branch_token for branch in prune_branches for branch_token in branch
        ]]
    phrase = " ".join(map(lambda x: x.text, subtree))
    return phrase


# Get tokens at end of arcs from the current token.
def get_sources(token, arcs):
    return filter(lambda c: c.dep in arcs, token.children)


# Extract entity-attribute pairs from a subject noun (before the verb)
# e.g. "Apple's iPhone has a good camera" -> [(Apple, iPhone)]
def extract_entity_attributes(noun):
    entity_attributes = list()

    if noun.pos == PROPN:
        # If current noun is a proper noun, it is assigned as an entity.
        entity_attributes.append((get_token_indices(noun), None))
    elif noun.pos == NOUN:
        # If current noun is a regular noun, it is assigned as an attribute.
        # Try to find the relevant entity.
        entity_sources = get_sources(noun, {poss, nmod, compound})
        entity_attributes += concatMap(extract_entity_attributes, entity_sources)
        token_indices = get_token_indices(noun)
        entity_attributes = list(map(lambda e_a: (e_a[0], token_indices), entity_attributes))

        if not entity_attributes:
            entity_attributes.append((None, token_indices))

    # Extract entity-attributes from further conjugated tokens.
    further_sources = get_sources(noun, {conj})
    entity_attributes += concatMap(extract_entity_attributes, further_sources)

    return entity_attributes


# Extract attribute-sentiment pairs and attach onto given entity-attribute pairs.
# e.g. "Apple has good cameras" -> [(Apple, cameras, good)]
def extract_attribute_sentiments(token, entity_attributes, negation=None):
    entity_attribute_sentiments = []

    # Add the negation prefix if it exists
    prefix = (get_phrase(negation) + " ") if negation else ""
    negation_indices = get_token_indices(negation)

    if token.pos == NOUN:
        # If token is a noun, attach attribute-sentiment pair to entity-attribute
        # pairs which do not currently have an attribute.
        sentiment_sources = get_sources(token, {amod})
        indices = get_token_indices(token)
        if negation_indices:
            indices = (min(indices[0], negation_indices[0], max(indices[1], negation_indices[1])))
        for source in sentiment_sources:
            entity_attribute_sentiments += list(
                map(lambda e_a: (e_a[0], indices, get_phrase_indices(source, True)),
                    filter(lambda e_a: not e_a[1], entity_attributes)
                    )
            )
    elif token.pos == ADJ:
        # If token is an adjective, attach sentiment to all entity-attribute pairs.
        print("token={} negation={}".format(token, prefix))
        indices = get_phrase_indices(token, True)
        if negation_indices:
            indices = (min(indices[0], negation_indices[0], max(indices[1], negation_indices[1])))
        entity_attribute_sentiments += list(
            map(lambda e_a: (e_a[0], e_a[1], indices), entity_attributes)
        )

    # Extract attribute-sentiment pairs from further conjugated tokens.
    further_sources = get_sources(token, {conj})
    entity_attribute_sentiments += concatMap(
            lambda s: extract_attribute_sentiments(s, entity_attributes),
            further_sources
    )

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

def extract_all_attribute_sentiments(sources, entity_attributes, negations):
    all_attribute_sentiments = []
    for source in sources:
        nearest_negation = extract_nearest_negation(source, negations)
        e_s = extract_attribute_sentiments(source, entity_attributes, nearest_negation)
        all_attribute_sentiments += e_s
    return all_attribute_sentiments

def extract_tuples(verb):
    entity_attribute_arcs = {nsubj}
    attribute_sentiment_arcs = {dobj, acomp, prep}

    # Collate the negations linked to the verb
    negations = filter(lambda x: x.dep == neg, verb.children)

    # Extracts entities and attributes from current verb, or from
    # nearest, previous verb if none found.
    current = verb
    entity_attributes = []
    while not entity_attributes and current:
        sources = get_sources(current, entity_attribute_arcs)
        entity_attributes = concatMap(extract_entity_attributes, sources)
        current = current.head

    # Attach attribute-sentiment pairs.
    entity_attribute_sources = get_sources(verb, attribute_sentiment_arcs)
    return extract_all_attribute_sentiments(entity_attribute_sources, entity_attributes, negations)


def extract_entity_attribute_sentiment(doc):
    return list(concatMap(extract_tuples, filter(lambda t: t.pos == VERB, doc)))


def position_to_JSON(i):
    if i is None:
        return json.dumps({'start': -1, 'end': -1})
    return json.dumps({'start': i[0], 'end': i[1]})


def tuple_to_JSON(t):
    return json.dumps({
        'entity': position_to_JSON(t[0]),
        'attribute': position_to_JSON(t[1]),
        'sentiment': position_to_JSON(t[2])
        })


def all_tuples_to_JSON(tuples):
    return list(map(tuple_to_JSON, tuples))


def indices_to_phrase(text, i):
    if not i:
        return None
    return text[i[0] : i[1] + 1]


def indices_to_phrases(text, t):
    return tuple(map(lambda i: indices_to_phrase(text, i), t))


def all_indices_to_phrases(text, tuples):
    return list(map(lambda t: indices_to_phrases(text, t), tuples))


def main(text):
    print('Loading model.')
    nlp = spacy.load('en')

    print('Processing text.')
    doc = nlp(text)

    print('Extracting entity-attribute pairs.')
    eas = extract_entity_attribute_sentiment(doc)
    print(eas)
    print(all_indices_to_phrases(text, eas))
    print(all_tuples_to_JSON(eas))


text = '''Python packaging may or may not actually be very bad but at the same time also great today.''' \
       '''Google's directions are not very much as terrible or bad as you think.'''

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
