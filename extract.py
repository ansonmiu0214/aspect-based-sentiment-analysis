#!/bin/python3

import spacy
from spacy import displacy
from collections import deque

# TODO optimise imports to avoid undetected conflicts
from spacy.symbols import nsubj, dobj, amod, conj, acomp, poss, prep, pobj, advmod, advcl, neg

# Missing constants from spacy.symbols
compound = 7037928807040764755
case = 8110129090154140942

nlp = None

'''
Load NLP model into spaCy
'''
def load_model():
  global nlp
  nlp = spacy.load('en')


'''
Given a token, return the [Entity: String] associated with that token.
'''
def extract_entities(entity):
  entities = []

  entity_arcs = { compound, poss, case, amod }
  other_arcs = { conj }

  # Find OTHER entities
  for child in entity.children:
    if child.dep in other_arcs:
      entities += extract_entities(child)

  # Parse the CURRENT entity phrase
  curr_entity_components = extract_phrase(entity, entity_arcs)
  entity_text = " ".join(map(lambda x: x[1], curr_entity_components))

  entities.append(entity_text)
  return entities


'''
Given an entity token, return the [(index: Int, Entity: String)] associated with that token
'''
def extract_phrase(entity, arcs):
  # print("text={} subtree={}".format(entity.text, ", ".join(map(lambda x: "{} via {} enum {}".format(x.text, x.dep_, x.dep), entity.children))))
  entity_components = [(entity.i, entity.text)]
  for child in entity.children:
    if child.dep in arcs:
      entity_components += extract_phrase(child, arcs)
  
  entity_components.sort()
  return entity_components



'''
Given a spaCy document, returns [((Entity: String, Attribute: String), Polarity: String)]
'''
def extract_entity_attribute_pairs(root):
  entity_arcs = { nsubj }
  attribute_arcs = { dobj, acomp, prep }
  link_arcs = { conj, advcl }
  root_as_attr_arcs = { advmod }

  entity_sources = [child for child in root.children if child.dep in entity_arcs]
  attribute_sources = deque([child for child in root.children if child.dep in attribute_arcs])
  link_sources = [child for child in root.children if child.dep in link_arcs]
  root_as_attr_sources = [child for child in root.children if child.dep in root_as_attr_arcs]

  entities = []
  for entity in entity_sources:
    entities += extract_entities(entity)

  print("entities={}".format(entities))
  print("attributes={}".format(attribute_sources))

  attributes = []

  # "Edge case": this root node is part of the attribute
  if root_as_attr_sources:
    attr, rest = parse_attribute(root)
    attributes.append(attr)
    attribute_sources.extend(rest)

  while attribute_sources:
    attr_src = attribute_sources.popleft()
    attr, rest = parse_attribute(attr_src)

    attributes.append(attr)
    attribute_sources.extend(rest)

  pairs = [(entity, attribute) for attribute in attributes for entity in entities]

  # "Edge case": other attributes linked to THIS SAME ENTITY
  for link in link_sources:
    pairs += extract_entity_attribute_pairs(link)

  return pairs


'''
Given a token, return (Attribute: Text, [UnprocessedAttr])
'''
def parse_attribute(attr_src):
  # print("text={} subtree={}".format(attr_src.text, ", ".join(map(lambda x: "{} via {} enum {}".format(x.text, x.dep_, x.dep), attr_src.children))))
  attr = [(attr_src.i, attr_src.text)]

  attr_arcs = { amod, compound, pobj, advmod, neg }
  link_arcs = { conj } 

  rest = []
  for child in attr_src.children:
    if child.dep in attr_arcs:
      attr += extract_phrase(child, attr_arcs)
    elif child.dep in link_arcs:
      rest.append(child)
    
  attr.sort()
  attr = " ".join(map(lambda x: x[1], attr))

  return attr, rest


'''
Given a spaCy document, return the ROOT token
'''
def locate_root(token):
  parent = token
  while parent.head.i != parent.i:
    parent = parent.head
  return parent


if __name__ == "__main__":
  print("Loading model...")
  load_model()
  
  print("Enter text: ", end="")
  text = input().strip()

  if not text:
    text = "The iPhone has a great camera and long battery life."

  doc = nlp(text)
  for sentence in doc.sents:
    root = locate_root(sentence[0])
    print("root={}".format(root))

    pairs = extract_entity_attribute_pairs(root)
    print(pairs)
  
  displacy.serve(doc, style='dep')