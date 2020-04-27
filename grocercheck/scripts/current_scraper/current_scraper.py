#!/usr/bin/env/python
import sqlite3
import livepopulartimes as lpt
import json
import sys

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
    out = cur.fetchall()
    return out

def update_row(conn, data, row_id):
    log = []
    days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    cur = conn.cursor()
    
    try:
        if (data['current_popularity'] is None) == False:
            cur.execute("UPDATE map_store SET live_busyness=? WHERE id=?", (data['current_popularity'], row_id))
        else:
            log.append("CANNOT RETRIEVE LIVE BUSYNESS FOR STORE id"+str(row_id))
    except:
        log.append("CURRENT POPULARITY KEY ERROR FOR STORE id"+str(row_id))

    conn.commit()
    return(log)

def update_current_popularity(formatted_address_list):
    for ind in range(len(formatted_address_list)):
        place_data = lpt.get_populartimes_by_place_id(API_KEY, place_id_list[ind])
        log = update_row(conn, place_data, (ind+1)) #sql id starts at 1
        BACKUP.write(json.dumps(place_data, indent=4))
        BACKUP.write("\r\n")
        for entry in log:
            LOG.write(entry)
            LOG.write("\r\n")


#-------------------MAIN-----------------------------------#

conn = create_connection("/home/ihasdapie/Grocer_Check_Project/Org/GrocerCheck/grocercheck/db1.sqlite3")
BACKUP = open("/home/ihasdapie/Grocer_Check_Project/Org/GrocerCheck/grocercheck/scripts/current_scraper/raw_data.json", "a+")
LOG = open("/home/ihasdapie/Grocer_Check_Project/Org/GrocerCheck/grocercheck/scripts/current_scraper/current_scraper_log.txt", "a+")


address_list = get_columns(conn, "address")
address_list = [pid[0] for pid in address_list]

print(address_list)


