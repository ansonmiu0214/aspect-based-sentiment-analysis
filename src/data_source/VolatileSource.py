from typing import List

from src.models import DataSourceService, Query, Document


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
        for doc in self.documents:
            for ent in doc.entities:
                if ent.name == entity:
                    relevant_attrs += ent.attributes

        # Further filter by the attribute if supplied in query
        if query.attribute:
            relevant_attrs = list(filter(lambda entry: entry.attribute == query.attribute, relevant_attrs))

        return relevant_attrs
