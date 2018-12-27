from database_source import DatabaseSource
from models import *


def insert_test(db_source):
    doc = Document()
    doc.add_metadata('key1', 'value1')

    comp1 = DocumentComponent('Component 1 type', 'Component 1 text')
    comp2 = DocumentComponent('Component 2 type', 'Component 2 text')
    doc.add_component(comp1)
    doc.add_component(comp2)

    ent1 = EntityEntry('ent 1 name')
    attr1 = AttributeEntry('attr1', [ExpressionEntry('attr expr 1'), ExpressionEntry('attr expr 1.2')])
    attr1.add_metadata('key1', 'value1')
    attr1.add_metadata('key2', 'value2')
    ent1.add_attribute(attr1)
    ent1.add_attribute(AttributeEntry('attr2', [ExpressionEntry('attr expr 2', 0.5)]))
    ent2 = EntityEntry('ent 2 name')
    ent1.add_attribute(AttributeEntry('attr1', [ExpressionEntry('attr expr 3', 0.75)]))
    doc.add_entity(ent1)
    doc.add_entity(ent2)

    db_source.process_document(doc)


def select_test(db_source):
    ent = 'ent 1 name'
    attr = 'attr1'

    query = Query(ent, None, None)
    res = db_source.lookup(query)
    print('-----')
    print("Querying all related to ent 1 name")
    for row in res:
        print((row.text, row.expressions, row.metadata))
    print('-----')

    query = Query(ent, attr, None)
    res = db_source.lookup(query)
    print('-----')
    print("Querying all related to ent 1 name AND attr1")
    for row in res:
        print((row.text, row.expressions, row.metadata))
    print('-----')


def reset_database(db_source):
    db_source.reset()


db_source = DatabaseSource()
reset_database(db_source)
# insert_test(db_source)
# select_test(db_source)
