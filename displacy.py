import spacy
from spacy import displacy

if __name__ == '__main__':
    nlp = spacy.load('en')
    text = input().strip()
    doc = nlp(text)
    displacy.serve(doc, style='dep')
