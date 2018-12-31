import http, json

from flask import Flask, jsonify, request

from aggregator_service.average_aggregator import AverageAggregator
from data_source.VolatileSource import VolatileSource
from data_source.database_source import DatabaseSource
from evaluator.evaluator import Evaluator
from extractor_service.spacy_extractor import SpacyExtractor
from main import ABSA
from preprocessor_service.text_preprocessor import TextPreprocessor
from query_parser.simple_parser import SimpleParser
from sentiment_service.vader import Vader

app = Flask(__name__)

sentiment_service = Vader()
absa = ABSA(preprocessor=TextPreprocessor(),
            extractor=SpacyExtractor(sentiment_service),
            sentiment=sentiment_service,
            # datasource=VolatileSource(),
            datasource=DatabaseSource(),
            query_parser=SimpleParser(),
            aggregator=AverageAggregator())

evaluator = Evaluator()

"""
all_docs = [
    {
        "id": 0,
        "entity": "Apple",
        "headline": "Apple does good things",
        "content": "real good apple stuff",
        "sentiment": 0.5
    },
    {
        "id": 1,
        "entity": "Google",
        "headline": "Google does inappropriate things",
        "content": "real bad google stuff",
        "sentiment": -0.5
    }
]

# replace with db calls?
def check_entity_name(doc_entity, search_entity):
    if not search_entity:
        return True
    return doc_entity.lower() == search_entity.lower()


# replace with db calls?
def check_document(requirements, doc):
    entity = requirements.get('entity')
    lower = float(requirements.get('lowerSentiment'))
    upper = float(requirements.get('upperSentiment'))
    return (check_entity_name(doc['entity'], entity)
        and doc['sentiment'] >= lower
        and doc['sentiment'] <= upper
    )


@app.route("/docs")
def docs():
    return jsonify(list(filter(lambda d: check_document(request.args, d), all_docs)))
"""


def jsonify_entry(entry):
    print(entry)
    return {
        'attribute': entry.text,
        'expression': ",\n\n ".join(map(str, entry.expressions)),
        'sentiment': sum([expr.sentiment if expr.sentiment else 0 for expr in entry.expressions])
                     / len(entry.expressions)
    }


def jsonify_entries(entries):
    return list(map(jsonify_entry, entries))


@app.route("/absa/load", methods=['POST'])
def load():
    document = request.files.get('file')
    if document is not None:
        absa.load_document(document)
        return '', http.HTTPStatus.NO_CONTENT
    return '', http.HTTPStatus.BAD_REQUEST


@app.route("/absa/query")
def query():
    entity = request.args.get('entity')
    attribute = None if request.args.get('attribute').strip() == '' else request.args.get('attribute')

    if entity is not None:
        # query = entity
        # if attribute is not None:
        #     query +=  " " + attribute
        (score, relevant_entries) = absa.process_query(entity, attribute)
        return jsonify({'score': score, 'entries': jsonify_entries(relevant_entries)})
    return '', http.HTTPStatus.NO_CONTENT


@app.route("/test/documents", methods=['GET'])
def get_test_documents():
    ids_to_metas = evaluator.get_all_documents()

    results = []
    for id in ids_to_metas:
        results.append({'id': id, 'metadata': ids_to_metas[id]})

    return jsonify(results)


@app.route("/test/document", methods=['POST'])
def upload_test_document():
    document = request.files.get('document')
    tags = request.files.get('tags')
    if not (document and tags):
        return '', http.HTTPStatus.BAD_REQUEST

    doc_id = evaluator.load_test_document(document.read().decode('utf-8'), tags.read().decode('utf-8'))
    return jsonify({'documentId': doc_id})


@app.route("/test/document", methods=['DELETE'])
def delete_test_document():
    document_id = request.args.get('id')
    if document_id is None:
        return '', http.HTTPStatus.NO_CONTENT

    status = evaluator.delete_test_document(document_id)
    return '', http.HTTPStatus.OK if status else http.HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/test/document", methods=['GET'])
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
def delete_all_test_documents():
    evaluator.reset_all_test_documents()
    return '', http.HTTPStatus.NO_CONTENT


@app.route("/test", methods=['GET'])
def run_evaluator():
    avg_score, idx_to_score = evaluator.run_evaluator()
    return jsonify({'result': avg_score, 'breakdown': idx_to_score})
