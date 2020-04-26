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
    log = []
    days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    cur = conn.cursor()
    if data['name'] is None == False:
        cur.execute("UPDATE map_store SET name=? WHERE id=?", (data['name'], row_id))
    else:
        log.append("CANNOT RETRIEVE NAME FOR STORE id"+str(row_id))

    if data['coordinates'] is None == False:
        cur.execute("UPDATE map_store SET lat=? WHERE id=?", (data['coordinates']['lat'], row_id))
        cur.execute("UPDATE map_store SET lng=? WHERE id=?", (data['coordinates']['lng'], row_id))
    else:
        log.append("CANNOT RETRIEVE COORDS FOR STORE id"+str(row_id))

    if data['address'] is None == False:
        cur.execute("UPDATE map_store SET address=? WHERE id=?", (data['address'], row_id))
    else:
        log.append("CANNOT RETRIEVE ADDRESS FOR STORE id"+str(row_id))

    if data['current_popularity'] is None == False:
        cur.execute("UPDATE map_store SET live_busyness=? WHERE id=?", (data['current_popularity'], row_id))
    else:
        log.append("CANNOT RETRIEVE LIVE BUSYNESS FOR STORE id"+str(row_id))

    for day in range(7):
        if data['hours']['weekday_text']['day'] is None == False:
            cur.execute("UPDATE map_store SET {day}hours=? WHERE id=?".format(day=days[day]), (data['hours']['weekday_text'][day], row_id))
        else:
            log.append("CANNOT RETRIEVE HOURS FOR STORE id"+str(row_id)+"ON DAY "+str(day))
        for hour in range(24):
            if data['populartimes'][day]['data']['hour'] is None == False:
                if hour < 10:
                    cur.execute("UPDATE map_store SET {day}0{hour}=? WHERE id=?".format(day=days[day], hour=hour), (data['populartimes'][day]['data'][hour], row_id))
                else:
                    cur.execute("UPDATE map_store SET {day}{hour}=? WHERE id=?".format(day=days[day], hour=hour), (data['populartimes'][day]['data'][hour], row_id))
            else:
                log.append("CANNOT RETRIEVE POPULARTIMES FOR STORE id"+str(row_id)+" ON DAY "+ str(day)+ "HOUR "+str(hour))
    conn.commit()
    print(data['name']+"COMPLETE")
    return(log)



#-------------------MAIN-----------------------------------#

conn = create_connection("/home/ihasdapie/Grocer_Check_Project/Org/GrocerCheck/grocercheck/db1.sqlite3")


API_KEY = open("/home/ihasdapie/keys/gmapkey.txt", "r").readline()
BACKUP = open("/home/ihasdapie/Grocer_Check_Project/Org/GrocerCheck/grocercheck/scripts/Run_Once/db_backup.json", "a")
LOG = open("/home/ihasdapie/Grocer_Check_Project/Org/GrocerCheck/grocercheck/scripts/Run_Once/populate_given_id_log.txt", "a+")

place_id_list = get_columns(conn, "place_id")
place_id_list = [pid[0] for pid in place_id_list]

log = []

for ind in range(10):
    place_data = lpt.get_populartimes_by_place_id(API_KEY, place_id_list[ind])
    log = update_row(conn, place_data, (ind+1)) #sql id starts at 1
    BACKUP.write(json.dumps(place_data, indent=4))
    BACKUP.write("\r\n")
    for entry in log:
        LOG.write(entry)
        LOG.write("\r\n")



