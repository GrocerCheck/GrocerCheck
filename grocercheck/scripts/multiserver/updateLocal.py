import psycog2
import sqlite3

def create_pgsql_connection(dbname, user, password, host, port):
    conn = psycog2.connect(dbname=dbname, user=user, password=password, host=host, port=port)



