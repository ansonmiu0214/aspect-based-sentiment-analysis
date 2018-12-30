import pymysql

host = "myspicyanalysis.chywzz3l5nmu.us-east-1.rds.amazonaws.com"
port = 3306
# dbname = "dbspicyanalysis"
dbname = "production"
user = "seoinchai"
password = "spicyanalysis"


def get_connection():
    try:
        connection = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
        return connection

    except Exception as e:
        print(e)


def close_connection(connection):
    connection.close()
