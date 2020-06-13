#!/usr/bin/env/python
import sqlite3
import livepopulartimes as lpt
import json
import sys
import os
import time

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
    cur.execute("SELECT {col} FROM map_store".format(col=col))
    out = cur.fetchall()
    return out

def update_row(conn, data, row_id):
    log = []
    days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    cur = conn.cursor()
    try:
        if (data['name'] is None) == False:
            cur.execute("UPDATE map_store SET name=? WHERE id=?", (data['name'], row_id))
        else:
            log.append("CANNOT RETRIEVE NAME FOR STORE id"+str(row_id))
    except:
        log.append("NAME KEYERROR FOR STORE id "+str(row_id))

    try:
        if (data['categories'] is None) == False:
            types = cur.execute("SELECT keywords FROM map_store WHERE id=?", (row_id,)).fetchall()[0][0]
            keys= " ".join(data['categories'])
            keys = keys + " " + types
            cur.execute("UPDATE map_store SET keywords=? WHERE id=?", (keys, row_id))
        else:
            #cur.execute("UPDATE map_store SET keywords=NULL WHERE id=?", (row_id)) #if no live busyness, set to null (clean up!)
            log.append("CANNOT RETRIEVE CATEGORIES FOR STORE id"+str(row_id))
    except:
        log.append("CATEGORIES KEY ERROR FOR STORE id"+str(row_id))

    try:
        if (data['coordinates'] is None) == False:
            cur.execute("UPDATE map_store SET lat=? WHERE id=?", (data['coordinates']['lat'], row_id))
            cur.execute("UPDATE map_store SET lng=? WHERE id=?", (data['coordinates']['lng'], row_id))
        else:
            log.append("CANNOT RETRIEVE COORDS FOR STORE id"+str(row_id))
    except:
        log.append("COORDINATE KEYERROR FOR STORE id"+str(row_id))

    try:
        if (data['address'] is None) == False:
            cur.execute("UPDATE map_store SET address=? WHERE id=?", (data['address'], row_id))
        else:
            log.append("CANNOT RETRIEVE ADDRESS FOR STORE id"+str(row_id))
    except:
        log.append("ADDRESS KEY ERROR FOR STORE id"+str(row_id))

    try:
        if (data['current_popularity'] is None) == False:
            cur.execute("UPDATE map_store SET live_busyness=? WHERE id=?", (data['current_popularity'], row_id))
        else:
            log.append("CANNOT RETRIEVE LIVE BUSYNESS FOR STORE id"+str(row_id))
    except:
        log.append("CURRENT POPULARITY KEY ERROR FOR STORE id"+str(row_id))


    for day in range(7):
        try:
            if (data['hours']['weekday_text'][day] is None) == False:
                cur.execute("UPDATE map_store SET {day}hours=? WHERE id=?".format(day=days[day]), (data['hours']['weekday_text'][day], row_id))
            else:
                log.append("CANNOT RETRIEVE HOURS FOR STORE id"+str(row_id)+" ON DAY "+str(day))
        except:
            log.append("HOURS KEY ERROR FOR STORE id"+str(row_id))

        for hour in range(24):
            try:
                if (data['populartimes'][day]['data'][hour] is None) == False:
                    if hour < 10:
                        cur.execute("UPDATE map_store SET {day}0{hour}=? WHERE id=?".format(day=days[day], hour=hour), (data['populartimes'][day]['data'][hour], row_id))
                    else:
                        cur.execute("UPDATE map_store SET {day}{hour}=? WHERE id=?".format(day=days[day], hour=hour), (data['populartimes'][day]['data'][hour], row_id))
                else:
                    log.append("CANNOT RETRIEVE POPULARTIMES FOR STORE id"+str(row_id)+" ON DAY "+ str(day)+ "HOUR "+str(hour))
            except:
                log.append("POPULARTIMES KEYERROR FOR STORE id"+str(row_id))

    conn.commit()
    try:
        print(data['name']+" COMPLETE")
    except:
        print("STORE iD "+str(row_id)+" COMPLETE")

    return(log)



def get_last_id(conn):
    cur = conn.cursor()
    return cur.execute("SELECT MAX(id) FROM map_store").fetchall()[0][0]


#-------------------MAIN-----------------------------------#

def populate_populartimes(API_KEY, start_id, database_dir):
    log = []
    conn = create_connection(database_dir)
    last_id = get_last_id(conn)

    place_id_list = get_columns(conn, "place_id")
    place_id_list = [pid[0] for pid in place_id_list]

    CURRENT_DIRECTORY = os.getcwd()
    BACKUP = open(CURRENT_DIRECTORY+ "db_backup.json", "a+")
    LOG = open(CURRENT_DIRECTORY + "populate_given_id_log.txt", "a+")


    for ind in range(start_id, last_id+1):
        place_data = lpt.get_populartimes_by_place_id(API_KEY, place_id_list[ind-1])
        log = update_row(conn, place_data, ind)
        time.sleep(1)
        print("            add detail for id ", ind)
        BACKUP.write(json.dumps(place_data, indent=4))
        BACKUP.write("\r\n")
        for entry in log:
            LOG.write(entry)
            LOG.write("\r\n")


