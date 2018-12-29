import json

from models import *


def json_to_dict(entries):
    entities = {}

    for entry in entries:
        entity = entry['entity']
        attribute = entry['attribute']
        expression = entry['expression']
        sentiment = entry['sentiment']

        if entity not in entities:
            entities[entity] = {}

        if attribute not in entities[entity]:
            entities[entity][attribute] = []

        entities[entity][attribute].append(ExpressionEntry(expression, sentiment))

    return entities


def json_to_entities(json_string: str) -> List[EntityEntry]:
    entries = json.loads(json_string)
    entities = json_to_dict(entries)

    entity_entries = []
    for entity in entities:
        entity_entry = EntityEntry(entity)

        attributes = entities[entity]
        for attribute in attributes:
            expr_entries = attributes[attribute]
            attr_entry = AttributeEntry(attribute, expr_entries)
            entity_entry.add_attribute(attr_entry)
        entity_entries.append(entity_entry)
    return entity_entries


def update_tags_from_json(document: Document, json_string: str) -> Document:
    '''
    Given a Document object that has already been preprocessed with the DocumentComponents
    and a well-formatted JSON string of the ground truth tags, returns the annotated Document.
    '''

    entities = json_to_entities(json_string)
    for entity in entities:
        document.add_entity(entity)
    return document


# if __name__ == '__main__':
json_string = """[{"entity":"Mexico","attribute":"economy","expression":"Emerging evidence that Mexico 's economy was back on the recovery track sent Mexican markets into a buzz of excitement Tuesday , with stocks closing at record highs and interest rates at 19-month lows","sentiment":0.6}]
"""

entities = json_to_entities(json_string)
for entity in entities:
    print(entity)

    for attr in entity.attributes:
        print(attr)
        print(attr.expressions)
