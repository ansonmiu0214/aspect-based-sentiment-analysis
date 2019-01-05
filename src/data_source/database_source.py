import json

from models import *
from data_source import aws_database


def insert(connection, document: Document):
    print(connection)
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
            sql = "INSERT INTO `entity` (name, metadata) VALUES (%s, %s)"

            cursor.execute(sql, (ent.text, json.dumps(ent.metadata)))
            sql = "SELECT LAST_INSERT_ID()"
            cursor.execute(sql, ())
            ent_id = cursor.fetchone()[0]

            for attr in ent.attributes:
                # Attribute.
                sql = "INSERT INTO `attribute` (entity_id, attribute, metadata) VALUES (%s, %s, %s)"
                cursor.execute(sql, (ent_id, attr.text, json.dumps(attr.metadata)))

                sql = "SELECT LAST_INSERT_ID()"
                cursor.execute(sql, ())
                attr_id = cursor.fetchone()[0]

                # Expressions.
                sql = "INSERT INTO `expression` (attribute_id, text, sentiment, document_id, is_header) VALUES (%s, %s, %s, %s, %s)"
                cursor.executemany(sql, list(map(lambda x: [attr_id, x.text, x.sentiment, doc_id, x.is_header],
                                                 attr.expressions)))

    connection.commit()
    return doc_id


def selectAttributes(connection, entity, attribute=None):
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

        return list(cursor.fetchall())


def selectExpressions(connection, attribute_id):
    with connection.cursor() as cursor:
        sql = "SELECT text, sentiment, document_id, is_header as doc_id " \
              "FROM expression " \
              "WHERE attribute_id = %s"
        cursor.execute(sql, (attribute_id))
        return list(cursor.fetchall())
        # return list(map(lambda x: x[0], cursor.fetchall()))


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

        doc_id = insert(self.connection, document)
        if not doc_id:
            print("Error: cannot get document ID from insertion")
            return

        for ent in document.entities:
            for attr in ent.attributes:
                for expr in attr.expressions:
                    expr.document_id = doc_id

    def lookup(self, query: Query):
        # Set up connection.
        if self.connection is None:
            self.connection = aws_database.get_connection()

        rows = selectAttributes(self.connection, query.entity, query.attribute)

        attrs = []

        for (id, name, metadata) in rows:
            expressions = selectExpressions(self.connection, id)
            exprs = [ExpressionEntry(text, sentiment, doc_id, is_header) for text, sentiment, doc_id, is_header in expressions]
            attr = AttributeEntry(name, exprs)
            attr.metadata = json.loads(metadata)
            attrs.append(attr)

        return attrs
