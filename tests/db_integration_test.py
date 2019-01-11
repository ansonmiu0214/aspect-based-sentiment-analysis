import unittest

from data_source.database_source import DatabaseSource
from models import *


class DatabaseIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseSource()

    def test_crud_one(self):
        # Setup doc
        doc = Document()
        doc.add_metadata('key1', 'value1')

        comp1 = DocumentComponent('Component 1 type', 'Component 1 text')
        comp2 = DocumentComponent('Component 2 type', 'Component 2 text')
        doc.add_component(comp1)
        doc.add_component(comp2)

        ent1 = EntityEntry('ent 1 name')
        attr1 = AttributeEntry('attr1', [ExpressionEntry('attr expr 1', is_header=False),
                                         ExpressionEntry('attr expr 1.2', is_header=False)])
        attr1.add_metadata('key1', 'value1')
        attr1.add_metadata('key2', 'value2')
        ent1.add_attribute(attr1)
        ent1.add_attribute(AttributeEntry('attr2', [ExpressionEntry('attr expr 2', sentiment=0.5, is_header=True)]))
        ent2 = EntityEntry('ent 2 name')
        ent2.add_attribute(AttributeEntry('attr1', [ExpressionEntry('attr expr 3', sentiment=0.75, is_header=False)]))
        doc.add_entity(ent1)
        doc.add_entity(ent2)

        # Insertion
        id = self.db.process_document(doc)

        # Retrieval: not none
        db_doc = self.db.retrieve_document(id)
        self.assertIsNotNone(db_doc)

        # Retrieval: same metadata
        self.assertTrue('key1' in db_doc.metadata)
        self.assertEqual(db_doc.metadata['key1'], 'value1')

        # Retrieval: same entities
        self.assertEqual(len(db_doc.entities), 2)
        self.assertEqual({'ent 1 name', 'ent 2 name'}, set(map(lambda ent: ent.text, db_doc.entities)))

        # Delete document: assert should be None
        self.db.delete_document(id)
        id = self.db.retrieve_document(id)
        self.assertIsNone(id)

    def test_lookup_doc_aggregation(self):
        doc1 = Document()
        doc1.add_component(DocumentComponent('text', 'Hello'))

        ent1 = EntityEntry('mexico')
        ent1.add_attribute(AttributeEntry('economy', [ExpressionEntry('mexico economy 1', 0.5, is_header=False)]))

        ent2 = EntityEntry('mexico')
        ent2.add_attribute(AttributeEntry('economy', [ExpressionEntry('mexico economy 2', 0.5, is_header=False)]))

        doc1 = Document()
        doc1.add_component(DocumentComponent('text', 'Hello'))
        doc1.add_entity(ent1)

        doc2 = Document()
        doc2.add_component(DocumentComponent('text', 'Hello'))
        doc2.add_entity(ent2)

        id1 = self.db.process_document(doc1)
        id2 = self.db.process_document(doc2)

        entries = self.db.lookup(Query('mexico', 'economy'))

        # Assert only one E/A pair comes up (economy)
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry.text, 'economy')

        # Assert that entries come from 2 distinct documents
        self.assertEqual(len(entry.expressions), 2)
        self.assertEqual(len(set(map(lambda x: x.document_id, entry.expressions))), 2)

        self.db.delete_document(id1)
        self.db.delete_document(id2)
