from flask import Flask, jsonify, request

app = Flask(__name__)

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

def check_entity_name(doc_entity, search_entity):
    if not search_entity:
        return True
    return doc_entity.lower() == search_entity.lower()

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
