import spacy
from spacy import displacy

nlp = spacy.load('en')
text = input().strip()
doc = nlp(text)
displacy.serve(doc, style='dep')
