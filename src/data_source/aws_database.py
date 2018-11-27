import pymysql

host = "myspicyanalysis.chywzz3l5nmu.us-east-1.rds.amazonaws.com"
port = 3306
dbname = "dbspicyanalysis"
user = "seoinchai"
password = "spicyanalysis"


def get_connection():
    try:
        connection = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
        return connection

    except Exception as e:
        print(e)


def get_cursor(connection):
    return connection.cursor()


def drop_table(cursor, table_name):
    cursor.execute("DROP TABLE " + table_name)


# Takes in the table name and attributes dictionary
def create_table(cursor, table_name, attributes):
    attributes_format = ""
    for key in attributes.keys():
        attributes_format = attributes_format + key + " " + attributes[key] + ", "
    attributes_format = attributes_format[:-2]

    cursor.execute("CREATE TABLE " + table_name + "(" + attributes_format + ")")


def close_connection(connection):
    connection.close()
