import json

from data_source import aws_database
from models import *


def insert(connection, document: Document):
    doc_id = None
    with connection.cursor() as cursor:
        sql = "INSERT INTO `document` (metadata) VALUES (%s)"
        cursor.execute(sql, (json.dumps(document.metadata)))

        print("Inserted document.")
        sql = "SELECT LAST_INSERT_ID()"
        cursor.execute(sql, ())
        doc_id, *_ = cursor.fetchone()

        # Components.
        sql = "INSERT INTO `component` (document_id, type, text) VALUES (%s, %s, %s)"
        cursor.executemany(sql, list(map(lambda x: [doc_id, x.type, x.text], document.components)))

        print("Inserted document components.")
        for ent in document.entities:
            # Entity
            ent_id = None

            sql = "SELECT id FROM entity WHERE name = %s"
            cursor.execute(sql, ent.text)

            if cursor.rowcount > 0:
                ent_id = cursor.fetchone()[0]
            else:
                sql = "INSERT INTO `entity` (name, metadata) VALUES (%s, %s)"

                cursor.execute(sql, (ent.text, json.dumps(ent.metadata)))
                sql = "SELECT LAST_INSERT_ID()"
                cursor.execute(sql, ())
                ent_id = cursor.fetchone()[0]

            for attr in ent.attributes:
                # Attribute.
                attr_id = None

                sql = "SELECT id FROM attribute WHERE entity_id = %s AND attribute = %s"
                cursor.execute(sql, (ent_id, attr.text))

                if cursor.rowcount > 0:
                    attr_id = cursor.fetchone()[0]
                else:
                    sql = "INSERT INTO `attribute` (entity_id, attribute, metadata) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (ent_id, attr.text, json.dumps(attr.metadata)))

                    sql = "SELECT LAST_INSERT_ID()"
                    cursor.execute(sql, ())
                    attr_id = cursor.fetchone()[0]

                # Expressions.
                sql = "INSERT INTO `expression` (attribute_id, text, sentiment, document_id, is_header) " \
                      "VALUES (%s, %s, %s, %s, %s)"
                cursor.executemany(sql, list(map(lambda x: [attr_id, x.text, x.sentiment, doc_id, x.is_header],
                                                 attr.expressions)))

        connection.commit()
        return doc_id


def select_attributes(connection, entity, attribute=None):
    with connection.cursor() as cursor:
        if attribute is None:
            sql = "SELECT attribute.id as id, attribute, attribute.metadata " \
                  "FROM attribute JOIN entity ON entity.id = attribute.entity_id " \
                  "WHERE entity.name = %s"
            cursor.execute(sql, (entity))
        else:
            sql = "SELECT attribute.id as id, attribute, attribute.metadata " \
                  "FROM attribute JOIN entity ON entity.id = attribute.entity_id " \
                  "WHERE entity.name = %s AND attribute.attribute = %s"
            cursor.execute(sql, (entity, attribute))

        results = list(cursor.fetchall())
        return results


def select_expressions(connection, attribute_id):
    with connection.cursor() as cursor:
        sql = "SELECT text, sentiment, document_id, is_header as doc_id " \
              "FROM expression " \
              "WHERE attribute_id = %s"
        cursor.execute(sql, (attribute_id))
        results = list(cursor.fetchall())
        return results


def reset(connection):
    with connection.cursor() as cursor:
        sql = "DELETE FROM expression"
        cursor.execute(sql, ())
        sql = "DELETE FROM attribute"
        cursor.execute(sql, ())
        sql = "DELETE FROM entity"
        cursor.execute(sql, ())
        sql = "DELETE FROM component"
        cursor.execute(sql, ())
        sql = "DELETE FROM document"
        cursor.execute(sql, ())
        connection.commit()
        print("All deleted.")


def delete_document(connection, document_id):
    with connection.cursor() as cursor:
        sql = "SELECT attribute_id FROM expression WHERE document_id = %s"
        cursor.execute(sql, document_id)

        attr_ids = list(set(map(lambda x: x[0], cursor.fetchall())))

        formatters = ','.join(['%s'] * len(attr_ids))
        sql = "SELECT entity_id FROM attribute WHERE id IN (%s)" % formatters
        cursor.execute(sql, tuple(attr_ids))

        ent_ids = list(set(map(lambda x: x[0], cursor.fetchall())))

        # Delete expressions
        sql = "DELETE FROM expression WHERE document_id = %s"
        cursor.execute(sql, document_id)

        # For each attribute, check whether an expression still exists;
        # if not, delete the attribute

        attrs_to_delete = []
        for attr_id in attr_ids:
            sql = "SELECT id FROM expression WHERE attribute_id = %s"
            cursor.execute(sql, (attr_id))

            if cursor.rowcount == 0:
                attrs_to_delete.append(attr_id)

        if attrs_to_delete:
            formatters = ','.join(['%s'] * len(attrs_to_delete))
            sql = "DELETE FROM attribute WHERE id IN (%s)" % formatters
            cursor.execute(sql, tuple(attrs_to_delete))

        # For each entity, check whether an attribute still exists;
        # if not, delete the entity

        ents_to_delete = []
        for ent_id in ent_ids:
            sql = "SELECT id FROM attribute WHERE entity_id = %s"
            cursor.execute(sql, (ent_id))

            if cursor.rowcount == 0:
                ents_to_delete.append(ent_id)

        if ents_to_delete:
            formatters = ','.join(['%s'] * len(ents_to_delete))
            sql = "DELETE FROM entity WHERE id IN (%s)" % formatters
            cursor.execute(sql, tuple(ents_to_delete))

        # Delete document components
        sql = "DELETE FROM component WHERE document_id = %s"
        cursor.execute(sql, document_id)

        # Delete document
        sql = "DELETE FROM document WHERE id = %s"
        cursor.execute(sql, document_id)
        connection.commit()


def select_documents(connection):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM document"
        cursor.execute(sql, ())
        results = list(cursor.fetchall())
        return results


def compose_document(connection, document_id: int) -> Document:
    document = Document(identifier=document_id)
    with connection.cursor() as cursor:
        # Select metadata
        sql = "SELECT metadata FROM document WHERE id = %s"
        cursor.execute(sql, (document_id))

        if cursor.rowcount == 0:
            return None

        metadata = cursor.fetchone()[0]
        document.metadata = json.loads(metadata)

        # Select document components
        sql = "SELECT type, text FROM component WHERE document_id = %s"
        cursor.execute(sql, (document_id))

        components = cursor.fetchall()

        all_text = []
        for type, text in components:
            document.add_component(DocumentComponent(type, text))
            all_text.append(text)

        document.text = " ".join(all_text)

        # Select expressions
        sql = "SELECT attribute_id, text, sentiment FROM expression WHERE document_id = %s"
        cursor.execute(sql, (document_id))

        expressions = cursor.fetchall()
        attributes = {}

        for attr_id, text, sentiment in expressions:
            if attr_id not in attributes:
                attributes[attr_id] = []
            attributes[attr_id].append(ExpressionEntry(text, sentiment))

        entities = {}
        for attr_id in attributes:
            sql = "SELECT entity_id, attribute FROM attribute WHERE id = %s"
            cursor.execute(sql, (attr_id))

            attrs = cursor.fetchall()
            for entity_id, attr_text in attrs:
                if entity_id not in entities:
                    entities[entity_id] = []

                entities[entity_id].append(AttributeEntry(attr_text, attributes[attr_id]))

        for ent_id in entities:
            sql = "SELECT name, metadata FROM entity WHERE id = %s"
            cursor.execute(sql, ent_id)

            entity_name, metadata = cursor.fetchone()

            entity_entry = EntityEntry(entity_name)
            entity_entry.metadata = json.loads(metadata)

            for attr_entry in entities[ent_id]:
                entity_entry.add_attribute(attr_entry)

            document.add_entity(entity_entry)

    return document


class DatabaseSource(DataSourceService):
    def __init__(self, is_production=True):
        self.connection = None
        self.is_production = is_production

    def reset(self):
        # Set up connection.
        self.setup_connection()
        reset(self.connection)

    def process_document(self, document: Document):
        # Set up connection.
        self.setup_connection()

        doc_id = insert(self.connection, document)
        if not doc_id:
            print("Error: cannot get document ID from insertion")
            return

        for ent in document.entities:
            for attr in ent.attributes:
                for expr in attr.expressions:
                    expr.document_id = doc_id

        return doc_id

    def lookup(self, query: Query):
        # Set up connection.
        self.setup_connection()

        rows = select_attributes(self.connection, query.entity, query.attribute)

        attrs = []

        for (id, name, metadata) in rows:
            expressions = select_expressions(self.connection, id)
            exprs = [ExpressionEntry(text, sentiment, doc_id, is_header)
                     for text, sentiment, doc_id, is_header in expressions]
            attr = AttributeEntry(name, exprs)
            attr.metadata = json.loads(metadata)
            attrs.append(attr)

        return attrs

    def list_all_documents(self):
        self.setup_connection()

        # Select documents
        rows = select_documents(self.connection)

        docs = {}
        for id, metadata in rows:
            docs[id] = json.loads(metadata)

        return docs

    def retrieve_document(self, document_id: int) -> Document:
        self.setup_connection()
        return compose_document(self.connection, document_id)

    def delete_document(self, document_id: int):
        self.setup_connection()
        return delete_document(self.connection, document_id)

    def setup_connection(self):
        self.connection = aws_database.get_connection(self.is_production)

    def destroy_connection(self):
        if self.connection:
            self.connection.close()
