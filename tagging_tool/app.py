import spacy
import os
from flask import Flask, render_template, request, jsonify

TEMPLATE_DIR = os.path.abspath('static')
app = Flask(__name__, template_folder=TEMPLATE_DIR)
nlp = None
MODEL = 'en_core_web_sm'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tokenise', methods=['POST'])
def tokenise():
    if not request.json or 'text' not in request.json:
        return jsonify({'success': False, 'error': 'Text not found.'}), 400

    text = request.json['text']

    # Extract tokens from spaCy
    tokens = nlp.extract_tokens(text)
    return jsonify({'success': True, 'data': tokens})


@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)


class NLP:
    def __init__(self):
        self.nlp = spacy.load(MODEL)
        print("spaCy loaded.")

    def extract_tokens(self, text):
        doc = self.nlp(text)
        return list(map(lambda token: token.text, doc))


if __name__ == '__main__':
    nlp = NLP()
    app.run(debug=True)
