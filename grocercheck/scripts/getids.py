import json
import sqlite3
import time
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def get_rows(conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM map_store')
    rows = cur.fetchall()

    return rows



conn = create_connection('db1.sqlite3')

rows = get_rows(conn)
ids = []
for row in rows:
    ids.append(row[7])


print(ids)
