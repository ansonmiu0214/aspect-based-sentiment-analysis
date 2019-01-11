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
            print("Entities in document: {}".format([ent.text for ent in doc.entities]))
            for ent in doc.entities:
                if ent.text == entity:
                    relevant_attrs += ent.attributes

        # Further filter by the attribute if supplied in query
        if query.attribute:
            relevant_attrs = [attr_entry for attr_entry in relevant_attrs if attr_entry.text == query.attribute]

        return relevant_attrs

    def retrieve_document(self, document_id):
        return self.documents[document_id]

    def list_all_documents(self):
        return self.documents
