from collections import deque

import spacy

from extractor_service.coref import Coreferencer
from models import ExtractorService, Document, SentimentService, DocumentComponent
from sentiment_service.vader import Vader
import xml.etree.ElementTree as ET

''' Utilities '''

ENT_TYPE_BLACKLIST = {'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL'}
EXPR_END_BLACKLIST = {'adp'}


def stringify_subtree(subtree, ignore='\n'):
    return "".join([t.text_with_ws for t in subtree if ignore not in t.text_with_ws])


''''''


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

        if text not in ents and ent[0].ent_type_ not in ENT_TYPE_BLACKLIST:
            ents[text] = {'span': ent}

    return ents


def extract_entity_sentences(doc, entities):
    for sent in doc.sents:
        is_matching_entity = False
        entity = ""
        for token in sent:
            if token.ent_type_ in ENT_TYPE_BLACKLIST:
                continue

            # Beginning of entity: add token as
            if token.ent_iob_ == 'B':
                if is_matching_entity:
                    # If previously capturing entity, handle previous match first
                    entity = entity.strip()
                    if entity:
                        if 'sentences' in entities[entity]:
                            entities[entity]['sentences'].append(sent)
                        else:
                            entities[entity]['sentences'] = {sent}

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

    ent_to_delete = [ent for ent in entities if 'sentences' not in entities[ent]]
    for ent in ent_to_delete:
        del entities[ent]

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

    for ent in ents_to_sents:
        details = ents_to_sents[ent]
        sents = details['sentences']

        ent_exprs = []
        for sent in sents:
            exprs = retrieve_expression(ent, sent)

            for expr_dict in exprs:
                expr_str = stringify_subtree(expr_dict['expression'])
                sent = sentiment_service.compute_sentiment(expr_str)
                expr_dict['sentiment'] = sent

            ent_exprs += exprs

        details['expressions'] = ent_exprs
        ents_to_exprs[ent] = details

    return ents_to_exprs


def contains_entity(subtree):
    for token in subtree:
        if token.ent_iob_ != '':
            return True
    return False


def retrieve_expression(entity, sent):
    exprs = []
    offset = sent[0].i

    # Find the entity in the sentence
    tokens = [token for token in sent if token.text == entity]

    if not tokens:
        # This shouldn't happen - currently because of multi-word entities
        return exprs

    left_idx = 0
    end_idx = len(sent)
    for occurrence in tokens:
        right_idx = left_idx

        if right_idx == end_idx:
            break

        while right_idx < end_idx:
            token = sent[right_idx]

            not_ent = token.ent_iob_ == ''
            no_ent_type = not token.ent_type_
            same_ent = token == occurrence
            ignorable_ent = token.ent_type_ in ENT_TYPE_BLACKLIST

            if not (not_ent or no_ent_type or same_ent or ignorable_ent):
                break

            right_idx += 1

        if right_idx < end_idx:
            # print("Stopped " + sent[right_idx].text, sent[right_idx].ent_iob_, sent[right_idx].ent_type_)
            right_idx = sent[right_idx].left_edge.i - offset

        # Shrink window by restricting what an expression can "end" with
        while sent[right_idx - 1].pos_.lower() in EXPR_END_BLACKLIST:
            right_idx -= 1

        expr = sent[left_idx:right_idx]

        exprs.append({'expression': expr})
        left_idx = right_idx

    # for occurrence in tokens:
    #     # Find first verb
    #     first_verb = occurrence
    #     while first_verb.pos_ != 'VERB':
    #         first_verb = first_verb.head
    #
    #     root_verb = first_verb
    #     while root_verb.head != root_verb:
    #         root_verb = root_verb.head
    #
    #     print(root_verb)
    #
    #     # Expression defined as Span
    #     # Left index = left edge of entity
    #     # Right index = ...
    #
    #     left_idx = occurrence.left_edge.i
    #     right_idx = occurrence.right_edge.i
    #     print(left_idx, right_idx)
    #     for child in first_verb.children:
    #         left, right = child.left_edge.i, child.right_edge.i
    #         if left == left_idx:
    #             continue
    #
    #         print(left, right)
    #
    #         # Not contiguous
    #         if right_idx + 1 != left:
    #             break
    #
    #         print("Contiguous")
    #         # Does child subtree contain an entity?
    #         if contains_entity(child.subtree):
    #             break
    #
    #         print("No entity")
    #         right_idx = right
    #
    #     expr = sent[left_idx:(right_idx + 1)]
    #     exprs.append(expr)

    return exprs


def retrieve_expression_token(entity, sent):
    conjunctions = ['and', 'but']
    res = []
    idx = 0
    while idx < len(sent):
        token = sent[idx]
        print(token.text)
        if entity.lower() in token.text.lower():
            print('here %s' % {token.text})
            phrase = []
            while token.text not in conjunctions:
                if token.text[0] == '\'':
                    elem = phrase[-1]
                    del phrase[-1]
                    elem = ''.join([elem, token.text])
                    phrase.append(elem)
                else:
                    print('now %s' % {token.text})
                    phrase.append(token.text)
                idx += 1
                if idx < len(sent):
                    token = sent[idx]
                else:
                    break
            print(phrase)
            res.append(' '.join(phrase))
        else:
            idx += 1
    return res


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
        exprs = ents_to_exprs[ent]['expressions']
        for expr_dict in exprs:
            expr = expr_dict['expression']
            attributes = extract_attributes(expr)
            expr_dict['attributes'] = attributes
    return ents_to_exprs


def reformat_dict(ents_to_exprs):
    ents_to_attrs = {}

    for ent in ents_to_exprs:
        data = ents_to_exprs[ent]

        new_ent_dict = {'span': data['span'], 'attributes': {}}

        for expr_dict in data['expressions']:
            expr = expr_dict['expression']
            sent = expr_dict['sentiment']

            for attr in expr_dict['attributes']:
                if attr in new_ent_dict['attributes']:
                    new_ent_dict['attributes'][attr].append((stringify_subtree(expr), sent))
                else:
                    new_ent_dict['attributes'][attr] = [(stringify_subtree(expr), sent)]

        ents_to_attrs[ent] = new_ent_dict

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

        print(annotations)
        annotate_document(doc, annotations)

        return doc

    def update_annotations(self, annotations, paragraph):
        # Apply coreferencing
        paragraph = self.coref.process(paragraph)

        # spaCy NLP
        doc = self.nlp(paragraph)

        # Extract entities
        entities = extract_entities(doc)

        # Extract the sentences related to each entity
        ents_to_sents = extract_entity_sentences(doc, entities)

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
            if ent not in annotations:
                annotations[ent] = dict()

            attrs = ents_to_attrs[ent]['attributes']

            for attr in attrs:
                if attr not in annotations[ent]:
                    annotations[ent][attr] = []

                exprs_with_sentiments = attrs[attr]
                annotations[ent][attr] += exprs_with_sentiments


if __name__ == '__main__':
    extractor = ExpressionExtractor(Vader())

    xml_text = '''<data><p>Emerging evidence that Mexico's economy was back on the recovery track sent Mexican markets into a buzz of excitement Tuesday, with stocks closing at record highs and interest rates at 19-month lows.</p>
<p>&quot;Mexico has been trying to stage a recovery since the beginning of this year and it's always been getting ahead of itself in terms of fundamentals,&quot; said Matthew Hickman of Lehman Brothers in New York.</p>
<p>&quot;Now we're at the point where the fundamentals are with us. The history is now falling out of view.&quot;</p>
<p>That history is one etched into the minds of all investors in Mexico: an economy in crisis since December 1994, a free-falling peso and stubbornly high interest rates.</p>
<p>This week, however, second-quarter gross domestic product was reported up 7.2 percent, much stronger than most analysts had expected. Interest rates on governent Treasury bills, or Cetes, in the secondary market fell on Tuesday to 23.90 percent, their lowest level since Jan. 25, 1995.</p>
<p>The stock market's main price index rallied 77.12 points, or 2.32 percent, to a record 3,401.79 points, with volume at a frenzied 159.89 million shares.</p>
<p>Confounding all expectations has been the strength of the peso, which ended higher in its longer-term contracts on Tuesday despite the secondary Cetes drop and expectations of lower benchmark rates in Tuesday's weekly auction.</p>
<p>With U.S. long-term interest rates expected to remain steady after the Federal Reserve refrained from raising short-term rates on Tuesday, the attraction of Mexico, analysts say, is that it offers robust returns for foreigners and growing confidence that they will not fall victim to a crumbling peso.</p>
<p>&quot;The focus is back on Mexican fundamentals,&quot; said Lars Schonander, head of researcher at Santander in Mexico City. &quot;You have a continuing decline in inflation, a stronger-than-expected GDP growth figure and the lack of any upward move in U.S. rates.&quot;</p>
<p>Other factors were also at play, said Felix Boni, head o f research at James Capel in Mexico City, such as positive technicals and economic uncertainty in Argentina, which has put it and neighbouring Brazil's markets at risk.</p>
<p>&quot;There's a movement out of South American markets into Mexico,&quot; he said. But Boni was also wary of what he said could be &quot;a lot of hype.&quot;</p>
<p>The economic recovery was still export-led, and evidence was patchy that the domestic consumer was back with a vengeance. Also, corporate earnings need to grow strongly to justify the run-up in the stock market, he said.</p></data>
    '''

    text = ''

    root = ET.fromstring(xml_text)
    for p in root.findall('p'):
        text += p.text

    # text = '''Smartphone sales and cost savings helped BT beat market expectations for first-half earnings on Thursday, with its departing chief executive saying his recovery plan was working'''

    doc = Document()
    doc.add_component(DocumentComponent('content', text))

    extractor.extract(doc)
