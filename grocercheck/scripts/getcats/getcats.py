#!/usr/bin/env/python
import sqlite3
import livepopulartimes as lpt
import json
import sys
import datetime
import time
import pytz
#--------GLOBAL VAR---------------#

BACKUP = open("/home/ihasdapie/GrocerCheck/grocercheck/scripts/logs/get_cats_raw_data.json", "a+")
LOG = open("/home/ihasdapie/GrocerCheck/grocercheck/scripts/logs/get_cats_log.txt", "a+")

def create_connection(db_file):
	conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def get_col_with_id(conn, col, i):
    cur = conn.cursor()
    cur.execute("SELECT {col} FROM map_store WHERE id = {i}".format(col=col, i=i))
    out = cur.fetchall()
    return out

def update_row(conn, data, row_id):
    log = []
    days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    cur = conn.cursor()
	keys = " ".join(data['categories'])

    try:
        if (data['current_popularity'] is None) == False:
            cur.execute("UPDATE map_store SET keywords=? WHERE id=?", (keys, row_id))
        else:
            cur.execute("UPDATE map_store SET keywords=NULL WHERE id=?", (row_id)) #if no live busyness, set to null (clean up!)
            log.append("CANNOT RETRIEVE CATEGORIES FOR STORE id"+str(row_id))
    except:
        log.append("CATEGORIES KEY ERROR FOR STORE id"+str(row_id))
    conn.commit()
    return(log)

def get_valid_ids(conn):
    #returns list of ids if the store has a name and address
    cur = conn.cursor()
    cur.execute("SELECT map_store.id FROM map_store WHERE address IS NOT NULL AND name IS NOT NULL")
    ids = cur.fetchall()
    return ids

def get_formatted_addresses(country, conn):
    ids = get_valid_ids(conn)
    formatted_address_list = []
    for i in open_ids:
		address = get_col_with_id(conn, "address", i)[0][0]
        name = get_col_with_id(conn, "name", i)[0][0]
        formatted_address_list.append("({name}) {address}, {country}".format(name=name, address=address, country = country))
    return (formatted_address_list, ids)

def get_categories(addr_and_id, doBackup, doLog, conn):
    formatted_address_list = addr_and_id[0]
    ids = addr_and_id[1]

    global BACKUP
    global LOG

    for ind in range(len(formatted_address_list)):
        place_data = lpt.get_populartimes_by_formatted_address(formatted_address_list[ind])
		print("STORE {id} COMPLETE".format(id=ids[ind]))
        log = update_row(conn, place_data, ids[ind]) #sql id starts at 1
		print("STORE {id} COMPLETE".format(id=ids[ind]))
       
		if doBackup == True:
            BACKUP.write(json.dumps(place_data, indent=4))
            BACKUP.write("\r\n")

        if doLog == True:
            for entry in log:
                LOG.write(entry)
                LOG.write("\r\n")
    cur = conn.cursor()
#clean up closed stores
    conn.commit()
    return

def get_cats(country, doBackup, doLog):
    global LOG
    conn = create_connection("/home/ihasdapie/GrocerCheck/grocercheck/db1.sqlite3")
    try:
        get_categories(get_formatted_addresses(country, conn), doBackup, doLog, conn)

    except:
        LOG.write("ERROR IN get_categories\r\n")



