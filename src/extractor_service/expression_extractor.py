import spacy

from extractor_service.coref import Coreferencer
from models import ExtractorService, Document, SentimentService, DocumentComponent
from sentiment_service.vader import Vader


def annotate_document(doc, annotations):
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
            if token.ent_iob_ == 'B':
                if is_matching_entity:
                    # Handle previously matched entity first
                    entity = entity.strip()
                    if entity:
                        if 'sentences' in entities[entity]:
                            entities[entity]['sentences'].append(sent)
                        else:
                            entities[entity]['sentences'] = [sent]

                        # Reset flags/variables
                        entity = ""

                is_matching_entity = True
                entity += token.text_with_ws
            elif token.ent_iob_ == 'I':
                entity += token.text_with_ws
            elif token.ent_iob_ == 'O' and is_matching_entity:
                entity = entity.strip()
                if 'sentences' not in entities[entity]:
                    entities[entity]['sentences'] = set([sent])
                elif sent not in entities[entity]['sentences']:
                    entities[entity]['sentences'].add(sent)

                # Reset flags/variables
                is_matching_entity = False
                entity = ""

    return entities


def parse_expressions(ents_to_sents, sentiment_service):
    ents_to_exprs = {}
    return ents_to_exprs


def parse_attributes(ents_to_exprs):
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


if __name__ == '__main__':
    extractor = ExpressionExtractor(Vader())

    doc = Document()
    doc.add_component(DocumentComponent('content', '''
        Smartphone sales and cost savings helped BT beat market expectations for first-half earnings on 
        Thursday, with its departing chief executive saying his recovery plan was working
    '''))

    extractor.extract(doc)
