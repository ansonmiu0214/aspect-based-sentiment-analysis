from flask import Flask, jsonify, request

app = Flask(__name__)

all_docs = [
    {
        "id": 0,
        "entity": "apple",
        "headline": "Apple does good things",
        "content": "real good apple stuff",
        "sentiment": 0.5
    },
    {
        "id": 1,
        "entity": "google",
        "headline": "Google does inappropriate things",
        "content": "real bad google stuff",
        "sentiment": -0.5
    }
]

@app.route("/docs")
def docs():
    entity = request.args.get('entity')
    if not entity:
        return jsonify(all_docs)
    entity = entity.lower()
    return jsonify(list(filter(lambda d: d["entity"] == entity, all_docs)))
