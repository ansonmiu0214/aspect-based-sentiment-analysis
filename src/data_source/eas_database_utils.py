import time
import datetime

def insert_eas(cursor, eas):
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""INSERT INTO eas_pair VALUES ('%s', '%s', '%s', '%s', '%s', '%s')""" %
                   (eas.entity,
                    eas.attribute,
                    eas.sentiment,
                    eas.sentence,
                    eas.document,
                    timestamp))


def get_eas_by_entity(cursor, entity):
    cursor.execute("""SELECT * FROM eas_pair WHERE entity='%s'""" % entity)
    return cursor.fetchall()


def delete_eas(cursor, eas):
    pass