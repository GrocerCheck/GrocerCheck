import sqlite3

conn = sqlite3.connect('db1.sqlite3')

curr = conn.cursor()

with conn:
    curr.execute("UPDATE map_store SET city=?",("vancouver",))
    conn.commit()

