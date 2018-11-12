from flask import Flask, jsonify, request
import http

from aggregator_service.average_aggregator import AverageAggregator
from data_source.VolatileSource import VolatileSource
from extractor_service.spacy_extractor import SpacyExtractor
from models import ExtractorService, SentimentService, PreprocessorService, QueryParser, AggregatorService, \
    DataSourceService
from preprocessor_service.text_preprocessor import TextPreprocessor
from query_parser.simple_parser import SimpleParser
from sentiment_service.vader import Vader
from main import ABSA

app = Flask(__name__)

sentiment_service = Vader()
absa = ABSA(preprocessor=TextPreprocessor(),
            extractor=SpacyExtractor(sentiment_service),
            sentiment=sentiment_service,
            datasource=VolatileSource(),
            query_parser=SimpleParser(),
            aggregator=AverageAggregator())
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
    return {
        'attribute': entry.attribute,
        'expression': entry.expression,
        'sentiment': entry.sentiment
    }

def jsonify_entries(entries):
    return list(map(jsonify_entry, entries))

@app.route("/absa/load", methods=['POST'])
def load():
    document = request.files.get('file')
    if document is not None:
        absa.load_document(document)
        return ('', http.HTTPStatus.NO_CONTENT)
    return ('', http.HTTPStatus.BAD_REQUEST)


@app.route("/absa/query")
def query():
    query = request.args.get('query')
    score = -1
    relevant_entries = []
    if query is not None:
        (score, relevant_entries) = absa.process_query(query)
        return jsonify({'score': score, 'entries': jsonify_entries(relevant_entries)})
    return jsonify({'score': score, 'entries': relevant_entries})
