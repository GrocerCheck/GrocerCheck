#!/usr/bin/env/python
import sqlite3
import livepopulartimes as lpt
import json

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def get_all(conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM map_store')
    rows = cur.fetchall()
    return rows

def get_columns(conn, col):
    cur = conn.cursor()
    cur.execute("SELECT place_id FROM map_store")
    col = cur.fetchall()
    return col


def gen_days():
    days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    out = ""
    for d in days:
        for h in range(24):
            if h < 10:
                out = out + ", set {day}0{hour} = {obrac}{day}{hour}{cbrac}".format(day=d, hour=h, obrac= "{", cbrac ="}")
            else:
                out = out + ", set {day}{hour} = {obrac}{day}{hour}{cbrac}".format(day=d, hour=h, obrac= "{", cbrac ="}")
    return out

def update_row(conn, data, row_id):
    com1= "UPDATE map_store, SET name = {name}, SET lat = {lat}, SET lng = {lng}, SET address = {address}, SET live_busyness = {live_busyness}, WHERE id = {rowID}"
    com1 = com1.format(live_busyness = data['current_popularity'], name =data['name'], lat = data['coordinates']['lat'], lng = data['coordinates']['lng'], address = data['address'], rowID = row_id)
    print(com1)

    cur = conn.cursor()
    cur.execute(com1)

conn = create_connection("/home/ihasdapie/Grocer_Check_Project/Org/GrocerCheck/grocercheck/db1.sqlite3")


API_KEY = open("/home/ihasdapie/keys/gmapkey.txt").readline()


place_id_list = get_columns(conn, "place_id")
place_id_list = [pid[0] for pid in place_id_list]


#place_data = lpt.get_populartimes_by_place_id(API_KEY, place_id_list[0])

place_data = json.load(open("/home/ihasdapie/Grocer_Check_Project/Org/LivePopularTimes/example_output(get_populartimes_by_PlaceID).json"))

print(update_row(conn, place_data, 1))




