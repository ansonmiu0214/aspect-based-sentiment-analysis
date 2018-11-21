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

    :param doc:
    :return:
    '''

    ents = set()
    ents_text = set()
    for ent in doc.ents:
        text = ent.text.strip()
        if not text:
            continue

        if text not in ents_text:
            ents.add(ent)
            ents_text.add(text)

    return ents


def extract_entity_sentences(doc, entities):
    pass


def parse_expressions(ents_to_sents, sentiment_service):
    pass


def parse_attributes(ents_to_exprs):
    pass


def reformat_dict(ents_to_exprs):
    pass


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

        # Extract the sentences related to each entity
        ents_to_sents = extract_entity_sentences(doc, entities)

        # Parse the specific expressions from the sentences related to each entity
        ents_to_exprs = parse_expressions(ents_to_sents, self.sentiment_service)

        # Parse the attributes from the expressions related to each entity
        ents_to_exprs = parse_attributes(ents_to_exprs)

        # Reformat dictionary to index on entity/attribute rather than entity/expression
        ents_to_attrs = reformat_dict(ents_to_exprs)


if __name__ == '__main__':
    extractor = ExpressionExtractor(Vader())

    doc = Document()
    doc.add_component(DocumentComponent('content', '''
        Smartphone sales and cost savings helped BT beat market expectations for first-half earnings on 
        Thursday, with its departing chief executive saying his recovery plan was working
    '''))

    extractor.extract(doc)
