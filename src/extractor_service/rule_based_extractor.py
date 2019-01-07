import spacy
from collections import deque

from extractor_service.coref import Coreferencer
from models import ExtractorService, SentimentService, Document, EntityEntry, AttributeEntry, ExpressionEntry, \
    DocumentComponent
from sentiment_service.vader import Vader

MODEL = 'en_core_web_sm'
ENT_WITH_ATTR_BLACKLIST = {'PERSON', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL',
                           'PRODUCT'}
ENT_TO_EXTRACT_BLACKLIST = {'PERSON', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL',
                            'PRODUCT'}
# ENT_TO_EXTRACT_BLACKLIST = {'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL'}
ATTR_BLACKLIST = {'high', 'low', 'max', 'maximum', 'min', 'minimum', 'lot'}


# ADDITIONS = {'focus','return','foreigner','buzz','point','mind','drop','strength','play','lack','move'}


def find_most_generic_entity(cur_entity):
    generic = cur_entity
    token = cur_entity

    while token.head != token:
        token = token.head
        if token.ent_iob_ == 'B' or token.ent_iob_ == 'I':
            generic = token

    return generic


def find_most_generic_attribute(cur_attr):
    generic = cur_attr
    token = cur_attr

    while token.head != token:
        if token.dep_ == 'conj':
            return generic

        token = token.head
        if is_valid_attribute_token(token):
            generic = token

    return generic


class RuleBasedExtractor(ExtractorService):
    def __init__(self, sentiment_service):
        self.nlp = spacy.load(MODEL)
        self.sentiment_service = sentiment_service  # type: SentimentService

    def extract(self, input_doc: Document, verbose=False):
        ents_to_extract = {}

        for component in input_doc.components:
            is_header = component.type == 'headline'
            paragraph = component.text.strip()

            if paragraph == '':
                continue

            doc = self.nlp(paragraph)

            # Map of token index to entity Span token
            para_ents_with_attr = {}

            # Extract entities and add sentiments.
            for ent in filter(lambda x: x.label_ not in ENT_TO_EXTRACT_BLACKLIST and x.lemma_ != '', doc.ents):
                print(ent, ent.label_)
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

                # Set current entity.
                if token.ent_iob_ == 'B' and token.i in para_ents_with_attr:
                    temp_entity = para_ents_with_attr[token.i]
                    if temp_entity.label_ in ENT_TO_EXTRACT_BLACKLIST:
                        temp_entity = None
                        cur_entity = temp_entity
                    else:
                        # Check if it is the most generic entity
                        generic_entity = find_most_generic_entity(token)
                        print("curr=%s generic=%s" % (token, generic_entity))

                        is_same = generic_entity == token
                        is_part_of_same_entity = generic_entity.text in temp_entity.text
                        if is_same or is_part_of_same_entity or generic_entity.i in para_ents_with_attr:
                            temp_entity = para_ents_with_attr[token.i]
                            cur_entity = temp_entity

                # Skip if compound (i.e. part of multi-word attribute)
                # Compound token will be gotten together with the base token.
                if token.dep_ == 'compound':
                    continue

                # Skip if not valid attribute token.
                if not is_valid_attribute_token(token):
                    continue

                # # Skip if no attached entity.
                # if cur_entity is None:
                #     ent_token = of_check(token)
                #     if ent_token is None:
                #         continue
                #
                #     temp_entity = para_ents_with_attr[ent_token.i]

                # Retrieve attribute.
                # token = find_most_generic_attribute(token)
                attribute = retrieve_attribute(token)

                # Skip if in blacklist.
                if attribute in ATTR_BLACKLIST:
                    continue

                if cur_sent_polar is None:
                    cur_sent_polar = self.sentiment_service.compute_sentiment(token.sent.text)

                # Skip if current sentence has 0 polarity.
                # if cur_sent_polar == 0:
                #     continue

                # TODO "of" check to override if required
                ent_token = of_check(token)

                entity_to_use = None

                print("attr=%s ent_token=%s" % (attribute, ent_token))

                if ent_token is not None and ent_token.i in para_ents_with_attr:
                    entity_to_use = para_ents_with_attr[ent_token.i]
                else:
                    # No entity in descendant
                    if cur_entity is not None:
                        entity_to_use = cur_entity
                    else:
                        # No live range
                        continue

                ent_attributes = ents_to_extract[entity_to_use.lemma_]
                if attribute in ent_attributes:
                    ent_attributes[attribute].append((token.sent.text, cur_sent_polar, is_header))
                else:
                    ent_attributes[attribute] = [(token.sent.text, cur_sent_polar, is_header)]

        input_doc = update_document(input_doc, ents_to_extract)

        return input_doc


def path_contains_another_valid_attr(entity, token):
    curr = entity.head
    while curr != token:
        if is_valid_attribute_token(curr):
            return True
        curr = curr.head
    return False


def of_check(token):
    all_descendants = [descendant for descendant in token.subtree]
    for desc in all_descendants:
        if desc.ent_iob_ == "B":
            # Check whether the path from ENT to TOKEN contains another valid attribute token
            if path_contains_another_valid_attr(entity=desc, token=token):
                return None

            return desc

    return None


def update_document(document, ents_to_extract):
    '''
    Translate `ents_to_extract` into EntityEntry components for the document.
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


if __name__ == '__main__':
    vader = Vader()
    extractor = RuleBasedExtractor(vader)

    doc = Document()
    doc.add_component(DocumentComponent(type="text", text=input().strip()))

    doc = extractor.extract(doc)
    for ent in doc.entities:
        print(ent.text, [attr.text for attr in ent.attributes])
