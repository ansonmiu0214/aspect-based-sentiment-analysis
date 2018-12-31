import pymysql

host = "myspicyanalysis.chywzz3l5nmu.us-east-1.rds.amazonaws.com"
port = 3306
# dbname = "dbspicyanalysis"
PRODUCTION_DB = "production"
EVALUATION_DB = "evaluation"
user = "seoinchai"
password = "spicyanalysis"


def get_connection(is_production):
    dbname = PRODUCTION_DB if is_production else EVALUATION_DB
    try:
        connection = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
        return connection

    except Exception as e:
        print(e)


def close_connection(connection):
    connection.close()
