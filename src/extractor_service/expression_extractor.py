from collections import deque

import spacy

from extractor_service.coref import Coreferencer
from models import ExtractorService, Document, SentimentService, DocumentComponent
from sentiment_service.vader import Vader


def annotate_document(doc, annotations):
    '''
    Transfer the entity/attribute/expression/sentiment data in the :param annotations dict
    as AttributeEntry and EntityEntry in the :param doc.
    '''
    pass


def extract_entities(doc):
    '''
    Given a spaCy NLP document, return the set of valid named entities (as Span objects).
    Any filtering occurs here.

    Returns a dictionary mapping entity names (:str) to a dict() containing the entity Span object keyed with 'span'.
    '''

    ents = {}
    for ent in doc.ents:
        text = ent.text
        if not text.strip():
            continue

        if text not in ents:
            ents[text] = {'span': ent}

    return ents


def extract_entity_sentences(doc, entities):
    for sent in doc.sents:
        is_matching_entity = False
        entity = ""
        for token in sent:
            # Beginning of entity: add token as
            if token.ent_iob_ == 'B':
                if is_matching_entity:
                    # If previously capturing entity, handle previous match first
                    entity = entity.strip()
                    if entity:
                        if 'sentences' in entities[entity]:
                            entities[entity]['sentences'].append(sent)
                        else:
                            entities[entity]['sentences'] = [sent]

                        # Reset variables
                        entity = ""

                is_matching_entity = True
                entity += token.text_with_ws

            # Inside an entity
            elif token.ent_iob_ == 'I':
                entity += token.text_with_ws

            # Outside of an entity: add relevant sentence to entity_sentence dict
            elif token.ent_iob_ == 'O' and is_matching_entity:
                entity = entity.strip()
                if 'sentences' not in entities[entity]:
                    entities[entity]['sentences'] = {sent}
                elif sent not in entities[entity]['sentences']:
                    entities[entity]['sentences'].add(sent)

                # Reset flags/variables
                is_matching_entity = False
                entity = ""

    return entities


def parse_expressions(ents_to_sents, sentiment_service):
    '''
    Given a dictionary mapping entities to the set of sentences that refers to it,
    for each sentence, extracts the "expression" and computes the sentiment score for that expression.

    If the expression expresses no sentiment, it is not added to the list.

    Returns a new dictionary of the following structure:
        { entity:
            {
                'span': Span object of entity,
                'expressions': [ { 'expression': Span object of expression }]
            }
        }

    e.g. in the sentence 'Apple's profits are increasing but Google's business is getting worse' mapped
    to the entity 'Apple', extract the expression 'Apple's profits are increasing'.

    Postcondition: all expressions in the dictionary express some form of sentiment.
    '''
    ents_to_exprs = {}
    return ents_to_exprs


def extract_attributes(expr):
    '''
    Given an entity string and expression, extract the list of attributes from that expression.
    Returns a list of strings.
    '''
    ATTR_BLACKLIST = {'high', 'low', 'max', 'maximum', 'min', 'minimum', 'growth', 'trend', 'improvement'}
    attributes = []

    for token in expr:
        # Skip if compound (i.e. part of multi-word attribute)
        # Compound token will be gotten together with the base token.
        if token.dep_ == 'compound':
            continue

        # Skip if not valid attribute token.
        if not is_valid_attribute_token(token):
            continue

        # Retrieve attribute.
        attribute = retrieve_attribute(token)

        # Skip if in blacklist.
        if attribute in ATTR_BLACKLIST:
            continue

        attributes.append(attribute)

    return attributes


def is_valid_attribute_token(token):
    # if token.text == 'out':
    #     print(token, token.pos_, token.sent)

    # Skip if part of entity (e.g. 'pound' is MONEY).
    if token.ent_iob_ != 'O':
        return False

    # Skip if not noun.
    if token.pos_ != 'NOUN':
        return False

    # Skip nouns like 'who'.
    if token.tag_ == 'WP':
        return False

    # Skip quantifier modifier (e.g. 'times' in '5 times').
    if token.dep_ == 'quantmod':
        return False

    return True


def retrieve_attribute(token):
    s = deque([token.lemma_])
    cur = token

    while True:
        compound = next(filter(lambda x: x.dep_ == 'compound', cur.children), None)

        if compound is None or not is_valid_attribute_token(compound):
            break
        else:
            cur = compound
            s.appendleft(compound.lemma_)

    return " ".join(s)


def parse_attributes(ents_to_exprs):
    for ent in ents_to_exprs:
        for expr in ents_to_exprs[ent]['expressions']:
            attributes = extract_attributes(expr['expression'])
            expr['attributes'] = attributes
    return ents_to_exprs


def reformat_dict(ents_to_exprs):
    ents_to_attrs = {}
    return ents_to_attrs


class ExpressionExtractor(ExtractorService):
    def __init__(self, sentiment_service: SentimentService):
        self.nlp = spacy.load('en_core_web_sm')
        self.coref = Coreferencer()
        self.sentiment_service = sentiment_service

    def extract(self, doc: Document):
        annotations = {}

        for component in doc.components:
            paragraph = component.text.strip()
            self.update_annotations(annotations, paragraph)

        annotate_document(doc, annotations)

        return doc

    def update_annotations(self, annotations, paragraph):
        # Apply coreferencing
        paragraph = self.coref.process(paragraph)

        # spaCy NLP
        doc = self.nlp(paragraph)

        # Extract entities
        entities = extract_entities(doc)
        print(entities)

        # Extract the sentences related to each entity
        ents_to_sents = extract_entity_sentences(doc, entities)

        for ent in ents_to_sents:
            print()
            print("Entity: {}".format(ent))
            print(ents_to_sents[ent])
        return

        # Parse the specific expressions from the sentences related to each entity
        ents_to_exprs = parse_expressions(ents_to_sents, self.sentiment_service)

        # Parse the attributes from the expressions related to each entity
        ents_to_exprs = parse_attributes(ents_to_exprs)

        # Reformat dictionary to index on entity/attribute rather than entity/expression
        ents_to_attrs = reformat_dict(ents_to_exprs)

        '''
        ents_to_attrs has type
        { entity: Span -> { attr: Span -> [(expr: Span, score: float)] }
        '''

        # Update annotations
        for ent in ents_to_attrs:
            if ent.text not in annotations:
                annotations[ent.text] = dict()

            attrs = ents_to_attrs[ent]

            for attr in attrs:
                if attr.text not in annotations[ent.text]:
                    annotations[ent.text][attr.text] = []

                exprs_with_sentiments = attrs[attr]
                annotations[ent.text][attr.text] += exprs_with_sentiments


def retrieve_expression(entity,sentences):
    conjunctions = ['and', 'but']
    nlp = spacy.load('en_core_web_sm')
    res = []
    for s in sentences:

        doc = nlp(s)
        for d in doc:
            print(d.text)
        idx = 0
        while idx < len(doc):
            token = doc[idx]
            print(token.text)
            if entity.lower() in token.text.lower():
                print('here %s' % {token.text})
                phrase = []
                while ((not (token.text in conjunctions))):
                    if token.text[0] == '\'':
                        elem = phrase[-1]
                        del phrase[-1]
                        elem = ''.join([elem,token.text])
                        phrase.append(elem)
                    else:
                        print('now %s' % {token.text})
                        phrase.append(token.text)
                    idx += 1
                    if idx < len(doc):
                        token = doc[idx]
                    else:
                        break
                print(phrase)
                res.append(' '.join(phrase))
            else:
                idx += 1

    return res


if __name__ == '__main__':
    extractor = ExpressionExtractor(Vader())

    doc = Document()
    doc.add_component(DocumentComponent('content', '''
        Smartphone sales and cost savings helped BT beat market expectations for first-half earnings on 
        Thursday, with its departing chief executive saying his recovery plan was working
    '''))

    extractor.extract(doc)
