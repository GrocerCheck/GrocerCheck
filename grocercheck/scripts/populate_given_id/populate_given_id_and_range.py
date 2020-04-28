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
    col = cur.fetchall()
    return col

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



#-------------------MAIN-----------------------------------#

conn = create_connection("/home/ihasdapie/Grocer_Check_Project/Org/GrocerCheck/grocercheck/db1.sqlite3")


API_KEY = open("/home/ihasdapie/keys/gmapkey.txt", "r").readline()
BACKUP = open("/home/ihasdapie/Grocer_Check_Project/Org/GrocerCheck/grocercheck/scripts/populate_given_id/db_backup.json", "a")
LOG = open("/home/ihasdapie/Grocer_Check_Project/Org/GrocerCheck/grocercheck/scripts/populate_given_id/populate_given_id_log.txt", "a+")

place_id_list = get_columns(conn, "place_id")
place_id_list = [pid[0] for pid in place_id_list]

log = []

args = sys.argv

if len(args) == 1:
    print("Please specify an option\nUse --help for help")
    sys.exit()

elif len(args) == 2:
    if args[1] == "--help":
        print("Options: \n--help: help\n--all: run for all entries in database\ni y (i == y == int) run for id i to id y in database, inclusive\nExampe usage: python3 populate_given_id_and_range.py 5 10\n")
        sys.exit()
    elif args[1] =="--all":
        r = range(1, (len(place_id_list)+1))
    else:
        print("Invalid entry\nUse --help for help")
        sys.exit()
elif len(args) == 3:
    try:
        i = int(args[1])
        y = int(args[2])+1
        r = range(i, y)
    except:
        print("Error! Double check your arguments!\nTry --help for help")
        sys.exit()
   
else:
    print("Too many arguments!\nUse --help for help")
    sys.exit()

        
for ind in r:
    place_data = lpt.get_populartimes_by_place_id(API_KEY, place_id_list[ind-1])
    log = update_row(conn, place_data, ind) #sql id starts at 1
    BACKUP.write(json.dumps(place_data, indent=4))
    BACKUP.write("\r\n")
    for entry in log:
        LOG.write(entry)
        LOG.write("\r\n")



