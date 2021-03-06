from collections import deque

import spacy

from extractor_service.coref import Coreferencer
from models import ExtractorService, SentimentService, Document, EntityEntry, AttributeEntry, ExpressionEntry

MODEL = 'en_core_web_sm'

# Irrelevant NER categories from spaCy
ENT_WITH_ATTR_BLACKLIST = {'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL'}
ENT_TO_EXTRACT_BLACKLIST = {'PERSON', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL'}

# Irrelevant attributes from spaCy
ATTR_BLACKLIST = {'high', 'low', 'max', 'maximum', 'min', 'minimum', 'lot'}


class SpacyExtractor(ExtractorService):
    def __init__(self, sentiment_service, use_coref=False, ignore_zero=False):
        self.nlp = spacy.load(MODEL)
        self.sentiment_service = sentiment_service  # type: SentimentService
        self.coref = Coreferencer()

        # Flags
        self.use_coref = use_coref
        self.ignore_zero = ignore_zero

    def extract(self, input_doc: Document, verbose=False):
        '''
        Uses spaCy's NER to extract entities.
        Uses a rule-based system to extract attributes and match with an entity.
        Extracts the expression containing the attribute and computes the sentiment by
        delegating to the sentiment service.

        Stores all data extracted as [EntityEntry] in the Document.

        :param input_doc: Document
        :verbose: Bool
        :rtype: Document
        '''
        ents_to_extract = {}

        for component in input_doc.components:
            is_header = component.type == 'headline'
            paragraph = component.text.strip()

            if paragraph == '':
                continue

            if self.use_coref:
                paragraph = self.coref.process(paragraph)

            doc = self.nlp(paragraph)

            # Calculate polarity of paragraph.
            para_polar = sum(map(lambda sent: self.sentiment_service.compute_sentiment(sent.text), doc.sents))
            if self.ignore_zero and para_polar == 0:
                continue

            para_ents_with_attr = {}

            # Extract entities and add sentiments.
            for ent in filter(lambda x: x.label_ not in ENT_TO_EXTRACT_BLACKLIST and x.lemma_ != '', doc.ents):
                ents_to_extract[ent.lemma_] = {}

            # Map indices to entities.
            for ent in filter(lambda x: x.label_ not in ENT_WITH_ATTR_BLACKLIST and x.lemma_ != '', doc.ents):
                para_ents_with_attr[ent[0].i] = ent

            # Extract attributes and add sentiments.
            cur_entity = None
            cur_sent_polar = None
            for token in doc:
                # Reset current sentence polarity if new sentence.
                is_sent_start = token.sent.start == token.i
                if is_sent_start:
                    cur_sent_polar = None

                # Skip if current sentence has 0 polarity.
                if self.ignore_zero and cur_sent_polar == 0:
                    continue

                # Set current entity.
                if token.ent_iob_ == 'B' and token.i in para_ents_with_attr:
                    cur_entity = para_ents_with_attr[token.i]
                    if cur_entity.label_ in ENT_TO_EXTRACT_BLACKLIST:
                        cur_entity = None

                # Skip if no attached entity.
                if cur_entity is None:
                    continue

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

                if cur_sent_polar is None:
                    cur_sent_polar = self.sentiment_service.compute_sentiment(token.sent.text)

                # Skip if current sentence has 0 polarity.
                if self.ignore_zero and cur_sent_polar == 0:
                    continue

                ent_attributes = ents_to_extract[cur_entity.lemma_]
                if attribute in ent_attributes:
                    ent_attributes[attribute].append((token.sent.text, cur_sent_polar, is_header))
                else:
                    ent_attributes[attribute] = [(token.sent.text, cur_sent_polar, is_header)]

        input_doc = update_document(input_doc, ents_to_extract)
        return input_doc


def update_document(document, ents_to_extract):
    '''
    Translate `ents_to_extract` into EntityEntry components for the document.

    :param document: Document
    :param ents_to_extract: Dict<str, Dict<str, (str, float, bool)>>
    :rtype: Document
    '''

    for ent in ents_to_extract:
        attrs = ents_to_extract[ent]
        if len(attrs) == 0:
            continue

        entity_entry = EntityEntry(ent)
        for attr in set(attrs):
            expressions = []
            for expr, sentiment, is_header in attrs[attr]:
                expr_entry = ExpressionEntry(expression=expr, sentiment=sentiment, is_header=is_header)
                expressions.append(expr_entry)

            attr_entry = AttributeEntry(attribute=attr, expressions=expressions)
            entity_entry.add_attribute(attr_entry)

        document.add_entity(entity_entry)

    return document


def is_valid_attribute_token(token):
    '''
    Checks if the current token has valid properties of an attribute.

    :param token: Token
    :rtype: bool
    '''
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
    '''
    From an attribute Token, follows dependency arcs to collect the full compound attribute.

    :param token: Token
    :rtype: str
    '''
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
