import json

from data_source.database_source import DatabaseSource
from evaluator.metric import document_error
from extractor_service.rule_based_extractor import RuleBasedExtractor
from extractor_service.spacy_extractor import SpacyExtractor
from models import *
from preprocessor_service.text_preprocessor import TextPreprocessor
from sentiment_service.vader import Vader


def json_to_dict(entries):
    entities = {}

    for entry in entries:
        entity = entry['entity']
        attribute = entry['attribute']
        expression = entry['expression']
        sentiment = entry['sentiment']

        if entity not in entities:
            entities[entity] = {}

        if attribute not in entities[entity]:
            entities[entity][attribute] = []

        entities[entity][attribute].append(ExpressionEntry(expression, sentiment, is_header=False))

    return entities


def json_to_entities(json_string: str) -> List[EntityEntry]:
    entries = json.loads(json_string)
    entities = json_to_dict(entries)

    entity_entries = []
    for entity in entities:
        entity_entry = EntityEntry(entity.lower())

        attributes = entities[entity]
        for attribute in attributes:
            expr_entries = attributes[attribute]
            attr_entry = AttributeEntry(attribute.lower(), expr_entries)
            entity_entry.add_attribute(attr_entry)
        entity_entries.append(entity_entry)
    return entity_entries


def update_tags_from_json(document: Document, json_string: str) -> Document:
    '''
    Given a Document object that has already been preprocessed with the DocumentComponents
    and a well-formatted JSON string of the ground truth tags, returns the annotated Document.
    '''

    entities = json_to_entities(json_string)
    for entity in entities:
        document.add_entity(entity)
    return document


class Evaluator:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.sentiment_service = Vader()
        self.extractors = {
            'v1': {
                'label': 'v1.0',
                'extractor': SpacyExtractor(self.sentiment_service)
            },
            'v1.1': {
                'label': 'v1.1 (Coreference Resolution)',
                'extractor': SpacyExtractor(self.sentiment_service, use_coref=True)
            },
            'v1.2': {
                'label': 'v1.2 (Basic with Strict Sentiment)',
                'extractor': SpacyExtractor(self.sentiment_service, ignore_zero=True)
            },
            'v2': {
                'label': 'v2.0 (Generics Analysis)',
                'extractor': RuleBasedExtractor(self.sentiment_service)
            },
        }
        self.db = DatabaseSource(is_production=False)
        self.default = 'v2'

    def load_test_document(self, doc, ground_truth_json: str):
        '''
        Load document into test set database.

        :param doc: (str, str)
        :param ground_truth_json: str
        :return: int
        '''
        doc_string, ext = doc
        document = self.preprocessor.preprocess(doc_string, ext)

        # Adapt ground truth JSON tags to `EntityEntry' objects
        document = update_tags_from_json(document, ground_truth_json)

        return self.db.process_document(document)

    def get_all_documents(self):
        '''
        Returns the list of test documents in the test set.
        :return:
        '''
        return self.db.list_all_documents()

    def reset_all_test_documents(self):
        self.db.reset()

    def get_extractors(self):
        res = {}
        for extractor in self.extractors:
            res[extractor] = {'label': self.extractors[extractor]['label']}
        return res

    def run_evaluator(self, option=None):
        # Pick extractor
        extractor = self.extractors[self.default]['extractor']
        if option and option in self.extractors:
            extractor = self.extractors[option]['extractor']

        # Get all documents
        all_docs = self.db.list_all_documents()

        doc_count = len(all_docs)
        if doc_count == 0:
            return None

        total_score = 0
        total_entity_score = 0
        total_attribute_score = 0
        total_mse = 0
        id_to_score = []

        for id in all_docs:
            doc = self.db.retrieve_document(id)

            ground_truth = list(doc.entities)

            doc.entities = []
            doc = extractor.extract(doc)

            scores_dict = document_error(model_output=doc.entities, ground_truth=ground_truth)
            print(scores_dict['tp'])

            model_entities = list(map(lambda ent: ent.as_dict(), doc.entities))
            truth_entities = list(map(lambda ent: ent.as_dict(), ground_truth))

            scores_dict['id'] = id
            scores_dict['model'] = model_entities
            scores_dict['truth'] = truth_entities

            # id_to_score.append({'id': id,
            #                     'score': score,
            #                     'ent_f1': scores_dict['ent_f1'],
            #                     'attr_f1': scores_dict['attr_f1'],
            #                     'model': model_entities,
            #                     'truth': truth_entities
            #                     })
            id_to_score.append(scores_dict)
            total_score += scores_dict['score']
            total_entity_score += scores_dict['ent_f1']
            total_attribute_score += scores_dict['attr_f1']
            total_mse += scores_dict['mse']

        avg_score = total_score / doc_count
        avg_entity_f1 = total_entity_score / doc_count
        avg_attribute_f1 = total_attribute_score / doc_count
        avg_mse = total_mse / doc_count
        return avg_score, avg_entity_f1, avg_attribute_f1, avg_mse, id_to_score

    def get_document(self, document_id):
        document = self.db.retrieve_document(document_id)
        if document is None:
            return document

        return document.as_dict()
