import spacy


def load_model():
    return spacy.load('en_core_web_lg')


def extract(nlp, text):
    SKIP_ENTITY_LABELS = ['LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']
    WORD_POSS = ['NOUN', 'VERB', 'ADJ', 'ADV']
    SKIP_WORD_LEMMAS = ['be', '-PRON-']

    doc = nlp(text)
    res = []

    for entity in doc.ents:
        if entity.label_ in SKIP_ENTITY_LABELS:
            continue

        negate = False
        attrs = []
        words = []

        for token in entity.sent:
            if token.pos_ == 'NOUN' and token.dep_ != 'attr':
                attrs.append(token)

            if token.dep_ == 'neg':
                negate = not negate

            if token.pos_ in WORD_POSS and token.lemma_ not in SKIP_WORD_LEMMAS:
                words.append(token)

        res.append((entity.lemma_, attrs, negate, words))

    return res
