import spacy

def load_model():
    # Load longer but more accurate.
    USE_LARGE_MODEL = True

    return spacy.load('en_core_web_lg' if USE_LARGE_MODEL else 'en_core_web_sm')


def extract(nlp, text):
    SKIP_ENTITY_LABELS = ['LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']
    WORD_POSS = {'NOUN': 'n', 'VERB': 'v', 'ADJ': 'a', 'ADV': 'r'}
    SKIP_WORD_LEMMAS = ['be', '-PRON-']

    doc = nlp(text)
    res = []

    for entity in doc.ents:
        if entity.label_ in SKIP_ENTITY_LABELS:
            continue

        negate = False
        attrs = []
        word_with_type = []

        for token in entity.sent:
            if token.pos_ == 'NOUN' and token.dep_ != 'attr':
                attrs.append(token.text)

            if token.dep_ == 'neg':
                negate = not negate

            if token.pos_ in WORD_POSS and token.lemma_ not in SKIP_WORD_LEMMAS:
                word_with_type.append((token.text, WORD_POSS[token.pos_]))

        res.append((entity.lemma_, attrs, negate, word_with_type))

    return res
