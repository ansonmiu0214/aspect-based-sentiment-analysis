import spacy
from spacy import displacy

nlp = spacy.load('en_core_web_sm')
doc = nlp('Blue is the colour of the sky')
displacy.serve(doc, style='dep')