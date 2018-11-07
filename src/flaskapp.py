from flask import Flask, jsonify, request

app = Flask(__name__)

all_docs = [
    {
        "entity": "apple",
        "content": "real good apple stuff",
        "sentiment": 0.5
    },
    {
        "entity": "google",
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
