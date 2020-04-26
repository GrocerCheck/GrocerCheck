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
    print(data['name'])
    cur = conn.cursor()
    cur.execute("UPDATE map_store SET name=? WHERE id=?", (data['name'], row_id))
    cur.execute("UPDATE map_store SET lat=? WHERE id=?", (data['coordinates']['lat'], row_id))
    cur.execute("UPDATE map_store SET lng=? WHERE id=?", (data['coordinates']['lng'], row_id))
    cur.execute("UPDATE map_store SET address=? WHERE id=?", (data['address'], row_id))
    cur.execute("UPDATE map_store SET live_busyness=? WHERE id=?", (data['current_popularity'], row_id))
    for day in range(7):
        for hour in range(24):
            if hour < 10:
                command = "UPDATE map_store SET {day}0{hour}=? WHERE id=?".format(day=days[day], hour=hour)
                print(command)
                cur.execute(command, (data['populartimes'][day]['data'][hour], row_id))
            else:
                cur.execute("UPDATE map_store SET {day}{hour}=? WHERE id=?".format(day=days[day], hour=hour), (data['populartimes'][day]['data'][hour], row_id))
    conn.commit()

    print("Data updated successfully")









conn = create_connection("/home/ihasdapie/Grocer_Check_Project/Org/GrocerCheck/grocercheck/test.sqlite3")


API_KEY = open("/home/ihasdapie/keys/gmapkey.txt").readline()


place_id_list = get_columns(conn, "place_id")
place_id_list = [pid[0] for pid in place_id_list]


#place_data = lpt.get_populartimes_by_place_id(API_KEY, place_id_list[0])

place_data = json.load(open("/home/ihasdapie/Grocer_Check_Project/Org/LivePopularTimes/example_output(get_populartimes_by_PlaceID).json"))

print(update_row(conn, place_data, 1))




