#!/usr/bin/env/python
import sqlite3
import livepopulartimes as lpt
import json
import sys


#--------GLOBAL VAR---------------#

BACKUP = open("/home/bitnami/apps/django/django_projects/GrocerCheck/grocercheck/scripts/logs/current_scraper_raw_data.json", "a+")
LOG = open("/home/bitnami/apps/django/django_projects/GrocerCheck/grocercheck/scripts/logs/current_scraper_log.txt", "a+")

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

    try:
        if (data['current_popularity'] is None) == False:
            cur.execute("UPDATE map_store SET live_busyness=? WHERE id=?", (data['current_popularity'], row_id))

        else:
            log.append("CANNOT RETRIEVE LIVE BUSYNESS FOR STORE id"+str(row_id))
    except:
        log.append("CURRENT POPULARITY KEY ERROR FOR STORE id"+str(row_id))
    conn.commit()
    return(log)

def get_valid_id(conn):
    #returns list of ids if the store has a name and address
    cur = conn.cursor()
    cur.execute("SELECT map_store.id FROM map_store WHERE address IS NOT NULL AND name IS NOT NULL AND fri00 IS NOT NULL")
    ids = cur.fetchall()
    return ids

def get_formatted_addresses(country, conn):
    ids = get_valid_id(conn)
    ids = [x[0] for x in ids]
    formatted_address_list = []
    for i in ids:
        address = get_col_with_id(conn, "address", i)[0][0]
        name = get_col_with_id(conn, "name", i)[0][0]
        formatted_address_list.append("({name}) {address}, {country}".format(name=name, address=address, country = country))
    return formatted_address_list

def update_current_popularity(formatted_address_list, doBackup, doLog, conn):
    global BACKUP
    global LOG
    for ind in range(len(formatted_address_list)):
        place_data = lpt.get_populartimes_by_formatted_address(formatted_address_list[ind])
        log = update_row(conn, place_data, (ind+1)) #sql id starts at 1

        if doBackup == True:
            BACKUP.write(json.dumps(place_data, indent=4))
            BACKUP.write("\r\n")

        if doLog == True:
            for entry in log:
                LOG.write(entry)
                LOG.write("\r\n")

def run_scraper(country, doBackup, doLog):
    global LOG
    conn = create_connection("/home/bitnami/apps/django/django_projects/GrocerCheck/grocercheck/db1.sqlite3")
    try:
        update_current_popularity(get_formatted_addresses(country, conn), doBackup, doLog, conn)
    except:
        LOG.write("ERROR IN update_current_popularity\r\n")
