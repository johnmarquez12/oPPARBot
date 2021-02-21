import mysql.connector.pooling
import os
from dotenv import load_dotenv
load_dotenv()

db_config = {
    'host' : os.getenv('MYSQL_HOST'),
    'user' : os.getenv('MYSQL_USER'),
    'password' : os.getenv('MYSQL_PASS'),
    'database' : os.getenv('MYSQL_DB_NAME')
}


class MySqlPoolWrapper:

    def __init__(self, size):
        self.cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name='mypool',
        pool_size=size,
        **db_config)

        # self.connection = mysql.connector.connect(**db_config)
        # self.cnxpool = mysql.connector.connect(pool_name = "mypool", pool_size=5, **db_config)

    def get_connection(self):
        cnx = self.cnxpool.get_connection()
        # cnx.set_charset_collation(charset='utf8', collation='utf8')
        return cnx
    
    def get_cursor(self):
        pass

    def close_connection(self, cnx):
        cnx.close()



