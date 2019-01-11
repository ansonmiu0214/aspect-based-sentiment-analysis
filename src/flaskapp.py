import http

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from aggregator_service.average_aggregator import AverageAggregator
from data_source.database_source import DatabaseSource
from evaluator.evaluator import Evaluator
from extractor_service.rule_based_extractor import RuleBasedExtractor
from extractor_service.spacy_extractor import SpacyExtractor
from main import ABSA
from preprocessor_service.text_preprocessor import TextPreprocessor
from sentiment_service.vader import Vader

# Setup
app = Flask(__name__)
CORS(app, support_credentials=True)

vader = Vader()
database_source = DatabaseSource()
absa = ABSA(preprocessor=TextPreprocessor(),
            extractor=SpacyExtractor(vader),
            sentiment=vader,
            datasource=database_source,
            aggregator=AverageAggregator())


@app.route("/_health")
def health():
    return 'OK'


'''
ROUTING: PRODUCTION
'''


@app.route("/absa/documents", methods=['GET'])
@cross_origin(supports_credentials=True)
def get_all_documents():
    ids_to_metas = database_source.list_all_documents()
    results = []
    for id in ids_to_metas:
        results.append({'id': id, 'metadata': ids_to_metas[id]})
    return jsonify(results)


@app.route("/absa/documents", methods=['DELETE'])
@cross_origin(supports_credentials=True)
def delete_all_documents():
    database_source.reset()
    return '', http.HTTPStatus.NO_CONTENT


@app.route("/absa/document", methods=['GET'])
@cross_origin(supports_credentials=True)
def get_document():
    document_id = request.args.get('id')
    if document_id is None:
        return '', http.HTTPStatus.NO_CONTENT

    document = database_source.retrieve_document(document_id)
    if document is None:
        return '', http.HTTPStatus.BAD_REQUEST

    document = document.as_dict()
    document['id'] = document_id
    return jsonify(document)


@app.route("/absa/document", methods=['POST'])
@cross_origin(supports_credentials=True)
def upload_document():
    document = request.files.get('document')
    if not document:
        return '', http.HTTPStatus.BAD_REQUEST

    ext = document.filename.split('.')[-1]
    doc_string = document.read().decode('utf-8')

    doc_id = absa.load_document(doc_string, ext)
    return jsonify({'documentId': doc_id})


@app.route("/absa/query")
@cross_origin(supports_credentials=True)
def query():
    entity = request.args.get('entity')
    attribute = None if request.args.get('attribute').strip() == '' else request.args.get('attribute')

    if entity is not None:
        (score, relevant_entries) = absa.process_query(entity, attribute)
        return jsonify({'score': score, 'entries': jsonify_entries(relevant_entries)})
    return '', http.HTTPStatus.NO_CONTENT


'''
ROUTING: EVALUATOR
'''

preprocessor = TextPreprocessor()
extractors = {
    'v1': {
        'label': 'v1.0', 'extractor': SpacyExtractor(vader)
    },
    'v1.1': {
        'label': 'v1.1 (Coreference Resolution)', 'extractor': SpacyExtractor(vader, use_coref=True)
    },
    'v1.2': {
        'label': 'v1.2 (Basic with Strict Sentiment)', 'extractor': SpacyExtractor(vader, ignore_zero=True)
    },
    'v2': {
        'label': 'v2.0 (Generics Analysis)', 'extractor': RuleBasedExtractor(vader)
    },
}

test_db = DatabaseSource(is_production=False)
default = 'v2'

evaluator = Evaluator(preprocessor=preprocessor,
                      sentiment_service=vader,
                      extractors=extractors,
                      db=test_db,
                      default=default)


@app.route("/test/documents", methods=['GET'])
@cross_origin(supports_credentials=True)
def get_test_documents():
    ids_to_metas = evaluator.get_all_documents()

    results = []
    for id in ids_to_metas:
        results.append({'id': id, 'metadata': ids_to_metas[id]})

    return jsonify(results)


@app.route("/test/document", methods=['POST'])
@cross_origin(supports_credentials=True)
def upload_test_document():
    document = request.files.get('document')
    tags = request.files.get('tags')
    if not (document and tags):
        return '', http.HTTPStatus.BAD_REQUEST

    doc_string = document.read().decode('utf-8')
    ext = document.filename.split('.')[-1]
    tags_string = tags.read().decode('utf-8')
    doc_id = evaluator.load_test_document((doc_string, ext), tags_string)
    return jsonify({'documentId': doc_id})


@app.route("/test/document", methods=['GET'])
@cross_origin(supports_credentials=True)
def get_test_document():
    document_id = request.args.get('id')
    if document_id is None:
        return '', http.HTTPStatus.NO_CONTENT

    document = evaluator.get_document(document_id)
    if document is None:
        return '', http.HTTPStatus.BAD_REQUEST

    document['id'] = document_id
    return jsonify(document)


@app.route("/test/documents", methods=['DELETE'])
@cross_origin(supports_credentials=True)
def delete_all_test_documents():
    evaluator.reset_all_test_documents()
    return '', http.HTTPStatus.NO_CONTENT


@app.route("/test/extractors", methods=['GET'])
@cross_origin(supports_credentials=True)
def get_extractors():
    return jsonify(evaluator.get_extractors())


@app.route("/test", methods=['GET'])
@cross_origin(supports_credentials=True)
def run_evaluator():
    option = request.args.get('extractor')
    avg_score, avg_ent, avg_attr, avg_mse, idx_to_score = evaluator.run_evaluator(option=option)
    return jsonify(
        {'result': avg_score, 'ent_f1': avg_ent, 'attr_f1': avg_attr, 'mse': avg_mse, 'breakdown': idx_to_score})


'''
UTILITIES
'''


def jsonify_entry(entry):
    return {
        'attribute': entry.text,
        'entries': list(
            map(lambda e: {'expression': str(e.text), 'sentiment': e.sentiment, 'documentId': e.document_id},
                entry.expressions)),
        'score': sum(map(lambda e: e.sentiment, entry.expressions)) / len(entry.expressions)
    }


def jsonify_entries(entries):
    return list(map(jsonify_entry, entries))
