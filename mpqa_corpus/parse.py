#!/bin/python3

from argparse import ArgumentParser
from functools import cmp_to_key
from collections import OrderedDict

def parse_sentence(document, startOffset, endOffset, token, typeName, attrs):
  sentence = Sentence(token, startOffset, endOffset)
  document.sentences.append(sentence)

def parse_targetSpeech(document, startOffset, endOffset, token, typeName, attrs):
  pass

def parse_split(document, startOffset, endOffset, token, typeName, attrs):
  pass

def parse_agent(document, startOffset, endOffset, token, typeName, attrs):
  pass

def parse_eTarget(document, startOffset, endOffset, token, typeName, attrs):
  entity = Entity(startOffset, endOffset)
  for sentence in document.sentences:
    if sentence.add_entity(entity):
       break

def parse_sTarget(document, startOffset, endOffset, token, typeName, attrs):
  id = attrs['id']
  annotation = Annotation(id, 'sTarget', token, attrs)
  document.annotations[id] = annotation

def parse_targetFrame(document, startOffset, endOffset, token, typeName, attrs):
  id = attrs['id']
  annotation = Annotation(id, 'targetFrame', token, attrs)
  document.annotations[id] = annotation

  sTargets = attrs['sTarget-link']
  if sTargets != 'none':
    sTargets = sTargets.split(',')
    for target in sTargets:
      print(document.annotations[target])

def parse_attitude(document, startOffset, endOffset, token, typeName, attrs):
  pass

def parse_objectiveSpeechEvent(document, startOffset, endOffset, token, typeName, attrs):
  pass

def parse_directSubjective(document, startOffset, endOffset, token, typeName, attrs):
  pass

def parse_expressiveSubjectivity(document, startOffset, endOffset, token, typeName, attrs):
  pass

# Parsing callbacks
annotation_parser = OrderedDict({
  'sentence': parse_sentence,
  'target-speech': parse_targetSpeech,
  'split': parse_split,
  'agent': parse_agent,
  'eTarget': parse_eTarget,
  'sTarget': parse_sTarget,
  'targetFrame': parse_targetFrame,
  'attitude': parse_attitude,
  'objective-speech-event': parse_objectiveSpeechEvent,
  'direct-subjective': parse_directSubjective,
  'expressive-subjectivity': parse_expressiveSubjectivity
})

ordered_types = list(annotation_parser.keys())
# ordered_types = ['sentence', 'target-speech', 'split', 'agent', 'eTarget', 'sTarget', 'targetFrame', 'attitude', 'objective-speech-event', 'direct-subjective', 'expressive-subjectivity']

def annotation_type_cmp(type1, type2):
  return ordered_types.index(type1) - ordered_types.index(type2)

class Sentence:
  def __init__(self, token, startOffset, endOffset):
    self.token = token
    self.startOffset = startOffset
    self.endOffset = endOffset
    self.entities = []
  
  def add_entity(self, entity):
    if entity.startOffset < self.startOffset or entity.endOffset > self.endOffset:
      return False

    newStartOffset = entity.startOffset - self.startOffset
    newEndOffset = entity.endOffset - self.startOffset

    self.entities.append((newStartOffset, newEndOffset))
    return True

  def __repr__(self):
    # entities = list(map(lambda x: (x[0], x[1], self.token[x[0]:x[1]]), self.entities))
    entities = self.entities
    return str((self.token, { 'entities': entities}))


class Entity:
  def __init__(self, startOffset, endOffset):
    self.startOffset = startOffset
    self.endOffset = endOffset


class Annotation:
  def __init__(self, id, typeName, token, attrs):
    self.id = id
    self.typeName = typeName
    self.token = token
    self.attrs = attrs
  
  def __repr__(self):
    return self.token
    # items = ["{}={}".format(key, self.attrs[key]) for key in self.attrs]
    # return "id={} type={} token={} {}".format(self.id, self.typeName, self.token, ",".join(items))


class Document:
  def __init__(self, original):
    self.original = original
    self.annotations = {}
    self.sentences = []
  
  def add_annotation(self, annotation):
    _, offsets, typeName, *rest = annotation

    # Only care about SENTENCE and ETARGET at the moment
    if typeName != 'sentence' and typeName != 'eTarget':
      return

    # Extract token from text
    startOffset, endOffset = list(map(int, offsets.split(',')))
    token = self.original[startOffset:endOffset]

    # Parse attributes into dictionary
    attrs = {}
    for entry in rest:
      key, val = entry.split('=')
      _, val, _ = val.split('"')
      attrs[key] = val

    annotation_parser[typeName](self, startOffset, endOffset, token, typeName, attrs)
  
  def getSentences(self):
    return list(filter(lambda x: x.entities != [], self.sentences))


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument('text', type=str)
  parser.add_argument('anns', type=str)

  args = parser.parse_args()
  file_text = args.text
  file_anns = args.anns

  with open(file_text, 'r') as f:
    original = "".join(f)
    document = Document(original)
  
  with open(file_anns, 'r') as f:
    annotations = [line.strip().split() for line in f if line[0] != '#']
    annotations.sort(key=cmp_to_key(lambda x, y: annotation_type_cmp(x[2], y[2])))
  
    for annotation in annotations:
      document.add_annotation(annotation)
    
    print(document.getSentences())