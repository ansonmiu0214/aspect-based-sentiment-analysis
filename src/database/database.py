import sqlite3
from eas import Eas

connection = sqlite3.connect(':memory:')
# connection = sqlite3.connect('eas.db')

c = connection.cursor()

c.execute("""CREATE TABLE eas_pair(
                        entity text,
                        attribute text,
                        sentiment text,
                        sentence text,
                        document text)""")


def insert_eas(eas):
    with connection:
        c.execute("""INSERT INTO eas_pair VALUES (:entity, :attribute, :sentiment, :sentence, :document)""",
                  {'entity': eas.entity,
                   'attribute': eas.attribute,
                   'sentiment': eas.sentiment,
                   'sentence': eas.sentence,
                   'document': eas.document})


def get_eas_by_entity(entity):
    c.execute("""SELECT * FROM eas_pair WHERE entity=:entity""", {'entity': entity})
    return c.fetchall()


eas1 = Eas("Iphone", "camera", "good", "Iphone has a good camera", "document1")
eas2 = Eas("Iphone", "screen", "bad", "Iphone has a bad screen", "document1")

insert_eas(eas1)
insert_eas(eas2)

print(get_eas_by_entity("Iphone"))

connection.close()
