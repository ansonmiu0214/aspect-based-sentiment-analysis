from typing import List

from models import DataSourceService, Query, Document


class VolatileSource(DataSourceService):
    '''
    Simple wrapper for data storage as a list of documents.
    Purely meant for testing purposes.
    '''

    def __init__(self):
        self.documents = []  # type: List[Document]

    def process_document(self, document: Document):
        self.documents.append(document)

    def lookup(self, query: Query):
        entity = query.entity
        relevant_attrs = []
        print("Entity to look up: {}".format(entity))
        for doc in self.documents:
            print("Entities in document: {}".format([ent.name for ent in doc.entities]))
            for ent in doc.entities:
                if ent.name == entity:
                    print("Found.")
                    relevant_attrs += ent.attributes

        # Further filter by the attribute if supplied in query
        if query.attribute:
            relevant_attrs = list(filter(lambda entry: entry.attribute == query.attribute, relevant_attrs))

        return relevant_attrs
