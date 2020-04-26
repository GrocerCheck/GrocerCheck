import sqlite3
from sqlite3 import Error

def create_conn(db):
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    return conn

def write(conn, store):
    sql = ''' INSERT INTO map_store(id,name,lat,lng,place_id)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql,store)
    return cur.lastrowid


db = 'db1.sqlite3'
conn = create_conn(db)

with conn:
    store = (1,"hello",'123123','123123123','alskdjald')

    storeid = write(conn,store)
print(storeid)
