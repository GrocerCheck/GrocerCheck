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

def update_row(conn, data, row_id):
    days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    cur = conn.cursor()
    cur.execute("UPDATE map_store SET name=? WHERE id=?", (data['name'], row_id))
    cur.execute("UPDATE map_store SET lat=? WHERE id=?", (data['coordinates']['lat'], row_id))
    cur.execute("UPDATE map_store SET lng=? WHERE id=?", (data['coordinates']['lng'], row_id))
    cur.execute("UPDATE map_store SET address=? WHERE id=?", (data['address'], row_id))
    cur.execute("UPDATE map_store SET live_busyness=? WHERE id=?", (data['current_popularity'], row_id))
    for day in range(7):
        cur.execute("UPDATE map_store SET {day}hours=? WHERE id=?".format(day=days[day]), (data['hours']['weekday_text'][day], row_id))
        for hour in range(24):
            if hour < 10:
                cur.execute("UPDATE map_store SET {day}0{hour}=? WHERE id=?".format(day=days[day], hour=hour), (data['populartimes'][day]['data'][hour], row_id))
            else:
                cur.execute("UPDATE map_store SET {day}{hour}=? WHERE id=?".format(day=days[day], hour=hour), (data['populartimes'][day]['data'][hour], row_id))
    print(data['name'], " SUCCESS")
    conn.commit()



#-------------------MAIN-----------------------------------#

conn = create_connection("/home/ihasdapie/Grocer_Check_Project/Org/GrocerCheck/grocercheck/db1.sqlite3")


API_KEY = open("/home/ihasdapie/keys/gmapkey.txt", "r").readline()
BACKUP = open("/home/ihasdapie/Grocer_Check_Project/Org/GrocerCheck/grocercheck/scripts/Run_Once/db_backup.json", "w")


place_id_list = get_columns(conn, "place_id")
place_id_list = [pid[0] for pid in place_id_list]

backup = []


place_data=lpt.get_populartimes_by_PlaceID(API_KEY, place_id_list[0])
backup.append(place_data)
update_row(conn,place_data, 1)

backup_json = json.dumps(backup, indent=4)
BACKUP.write(backup_json)

"""
for ind in range(len(place_id_list)):
    place_data = lpt.get_populartimes_by_place_id(API_KEY, place_id_list[ind])
    update_row(conn, place_data, ind)
    backup.append(place_data)
"""



