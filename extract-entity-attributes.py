# Given text, output a list of entity-attribute pairs.

import spacy


def add_to_dict(dict, key, value):
    if key in dict:
        dict[key].append(value)
    else:
        dict[key] = [value]


def main(text):
    VERBOSE = True
    SKIP_ENTITIES = ['LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']
    ADJ_JOIN_POS = ['ADJ', 'ADV', 'CCONJ', 'ADP']

    print('Loading model.')

    nlp = spacy.load('en_core_web_lg')

    print('Processing text.')

    doc = nlp(text)

    print('Extracting entity-attribute pairs.')

    dict = {}

    for entity in doc.ents:
        if entity.label_ in SKIP_ENTITIES:
            continue

        if VERBOSE:
            print('-- Found entity:', entity.text + '(' + entity.lemma_ + ')', entity.label_)

        sentences = entity.sent
        attr = None

        for i in range(len(sentences), 0, -1):
            token = sentences[i - 1]

            if attr is not None:
                if token.pos_ in ADJ_JOIN_POS:
                    attr = token.lemma_ + ' ' + attr
                else:
                    add_to_dict(dict, entity.lemma_, attr)
                    attr = None
            elif token.pos_ == 'ADJ':
                attr = token.lemma_

            if VERBOSE:
                print('- Found token:', token.text + '(' + token.lemma_ + ')', token.pos_,
                      token.dep_ + '(' + spacy.explain(token.tag_) + ')')

    return dict


text = '''Python packaging may or may not actually be very bad but at the same time also great today.''' \
       ''' Google's directions are not very much as terrible or bad as you think.'''
# Outputs {'python': ['also great', 'same', 'very bad'], 'google': ['not very much as terrible or bad']}
print(main(text))
