import spacy
from spacy import displacy

if __name__ == '__main__':
    nlp = spacy.load('en_core_web_sm')
    text = input().strip()
    doc = nlp(text)
    displacy.serve(doc, style='dep')
