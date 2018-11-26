import json
from models import *
import aws_database


def insert(connection, document: Document):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `document` (metadata) VALUES (%s)"
        cursor.execute(sql, (json.dumps(document.metadata)))

        sql = "SELECT LAST_INSERT_ID()"
        cursor.execute(sql, ())
        doc_id = cursor.fetchone()[0]

        # Components.
        sql = "INSERT INTO `component` (document_id, type, text) VALUES (%s, %s, %s)"
        cursor.executemany(sql, list(map(lambda x: [doc_id, x.type, x.text], document.components)))

        for ent in document.entities:
            sql = "INSERT INTO `entity` (document_id, name, metadata) VALUES (%s, %s, %s)"
            cursor.execute(sql, (doc_id, ent.name, json.dumps(ent.metadata)))
            sql = "SELECT LAST_INSERT_ID()"
            cursor.execute(sql, ())
            ent_id = cursor.fetchone()[0]

            # Attributes.
            sql = "INSERT INTO `attribute` (entity_id, attribute, expression, sentiment, metadata) VALUES (%s, %s, %s, %s, %s)"
            cursor.executemany(sql, list(
                map(lambda x: [ent_id, x.attribute, x.expression, x.sentiment, json.dumps(x.metadata)],
                    ent.attributes)))

    connection.commit()


def select(connection, entity, attribute=None):
    with connection.cursor() as cursor:
        if attribute is None:
            sql = "SELECT attribute, expression, sentiment, attribute.metadata " \
                  "FROM attribute JOIN entity ON entity.id = attribute.entity_id " \
                  "WHERE entity.name = %s"
            cursor.execute(sql, (entity))
        else:
            sql = "SELECT attribute, expression, sentiment, attribute.metadata " \
                  "FROM attribute JOIN entity ON entity.id = attribute.entity_id " \
                  "WHERE entity.name = %s AND attribute.attribute = %s"
            cursor.execute(sql, (entity, attribute))

        return cursor.fetchall()


def reset(connection):
    with connection.cursor() as cursor:
        sql = "DELETE FROM attribute"
        cursor.execute(sql, ())
        sql = "DELETE FROM entity"
        cursor.execute(sql, ())
        sql = "DELETE FROM component"
        cursor.execute(sql, ())
        sql = "DELETE FROM document"
        cursor.execute(sql, ())


class DatabaseSource(DataSourceService):
    def __init__(self):
        self.connection = None

    def reset(self):
        # Set up connection.
        if self.connection is None:
            self.connection = aws_database.get_connection()

        reset(self.connection)

    def process_document(self, document: Document):
        # Set up connection.
        if self.connection is None:
            self.connection = aws_database.get_connection()

        insert(self.connection, document)

    def lookup(self, query: Query):
        # Set up connection.
        if self.connection is None:
            self.connection = aws_database.get_connection()

        rows = select(self.connection, query.entity, query.attribute)

        attrs = []

        for (name, expr, sentiment, metadata) in rows:
            attr = AttributeEntry(name, expr, sentiment)
            attr.metadata = json.loads(metadata)
            attrs.append(attr)

        return attrs
