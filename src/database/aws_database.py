import pymysql
import time
import datetime
from eas import Eas

host = "myspicyanalysis.chywzz3l5nmu.us-east-1.rds.amazonaws.com"
port = 3306
dbname = "dbspicyanalysis"
user = "seoinchai"
password = "spicyanalysis"

try:
    connection = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)

except Exception as e:
    print(e)

c = connection.cursor()

c.execute("""DROP TABLE eas_pair""")

c.execute("""CREATE TABLE eas_pair(
                        entity VARCHAR(50),
                        attribute VARCHAR(50),
                        sentiment VARCHAR(50),
                        sentence VARCHAR(200),
                        document VARCHAR(1000),
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")


def insert_eas(eas):
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    with connection:
        c.execute("""INSERT INTO eas_pair VALUES ('%s', '%s', '%s', '%s', '%s', '%s')""" %
                  (eas.entity,
                   eas.attribute,
                   eas.sentiment,
                   eas.sentence,
                   eas.document,
                   timestamp))


def get_eas_by_entity(entity):
    c.execute("""SELECT * FROM eas_pair WHERE entity='%s'""" % entity)
    return c.fetchall()


eas1 = Eas("Iphone", "camera", "good", "Iphone has a good camera", "document1")
eas2 = Eas("Iphone", "screen", "bad", "Iphone has a bad screen", "document1")

insert_eas(eas1)
insert_eas(eas2)

print(get_eas_by_entity("Iphone"))

connection.close()
