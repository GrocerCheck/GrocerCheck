#!/usr/bin/env/python
import sqlite3
import time
import livepopulartimes as lpt
import json
import sys
import datetime
import time
import pytz
from multiprocessing.dummy import Pool #for compatability w/ celery


#--------GLOBAL VAR---------------#

BACKUP = open("/home/bitnami/apps/django/django_projects/GrocerCheck/grocercheck/scripts/logs/current_scraper_raw_data.json", "a+")
LOG = open("/home/bitnami/apps/django/django_projects/GrocerCheck/grocercheck/scripts/logs/current_scraper_log.txt", "a+")

#BACKUP = open("/home/ihasdapie/Grocer_Check_Project/Org/backup.json", "a+")
#LOG = open("/home/ihasdapie/Grocer_Check_Project/Org/LOG.txt", "a+")

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
    #print("called update_row",data['name'], row_id)
    log = []
    days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    cur = conn.cursor()
    try:
        if (data['current_popularity'] is None) == False:
            cur.execute("UPDATE map_store SET live_busyness=? WHERE id=?", (data['current_popularity'], row_id))
            conn.commit()
        else:
            cur.execute("UPDATE map_store SET live_busyness=NULL WHERE id=?", (row_id)) #if no live busyness, set to null (clean up!)
            log.append("CANNOT RETRIEVE LIVE BUSYNESS FOR STORE id"+str(row_id))
    except:
        log.append("CURRENT POPULARITY KEY ERROR FOR STORE id"+str(row_id))
    return(log)

def get_open_closed_ids(conn, city, timezone):
    local_timezone = pytz.timezone(timezone)
    local_time = datetime.datetime.now(local_timezone)
    localhour = local_time.hour
    localminute = local_time.minute
    weekday = local_time.weekday()
    days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    cur = conn.cursor()
    sql_query = "SELECT id, {day}hours FROM map_store where address IS NOT NULL AND name IS NOT NULL AND fri00 IS NOT NULL AND {day}hours IS NOT NULL AND city=?".format(day=days[weekday])
    cur.execute(sql_query, (city,))

    # cur.execute(sql_query, (city,))
    id_with_hours = cur.fetchall()
    open_ids= []
    closed_ids = []

    for pair in range(len(id_with_hours)):
        i = id_with_hours[pair][0]
        hours = id_with_hours[pair][1]
        if hours==None:
            continue
        else:
            hours = hours.split(": ")[1]
            if (' 24' in hours):
                open_ids.append(i) #open 24h
            elif ('–' not in hours):
                closed_ids.append(i)
            #en-dash! #only closed (24h already caught)
            else:
                hours = hours.split(" – ")
                oh, om = int(hours[0].split(':')[0]), int(hours[0].split(':')[1][:2]) #opening hour, opening minute
                ch, cm = int(hours[1].split(':')[0]), int(hours[1].split(':')[1][:2]) #closing hour, closing minute

                # print(oh, om, ch, cm, " | ", localhour, localminute)
                # convert to 24h format
                if ((hours[0][-2:] == "PM") and (oh != 12)):
                    oh += 12
                if ((hours[1][-2:] == "PM") and (ch !=12)): #12PM is noon, 12AM is midnight
                    # print(hours[1][-2])
                    ch += 12
                # print(oh, om, ch, cm, " | ", localhour, localminute)

                if ((hours[0][-2:] == "AM") and (oh == 12)):
                    oh = 0 #if it opens at midnight, set to 0 for comparison
                if ((hours[1][-2:] == "AM") and (ch == 12)):
                    ch = 24

                #everything in 24h format from this point on
                if ((hours[1][-2:] == "AM") and (ch < oh)) or ((hours[1][-2:] == "AM") and (ch == 24)): #check if the store closes after midnight or at midnight
                    if (ch == 24):
                        if ((localhour < ch) and (localhour > oh)):
                            open_ids.append(i)
                        else:
                            closed_ids.append(i)
                    else:
                        #if closing hour is after midnight and is not midnight,
                        # e.g. oh 7 ch 3, lt 2
                        # if the local time is lesser than the closing time, within the span of midnight - closing, the store is open
                        # e.g. oh 7 ch 3 lt 14
                        # if the local time is greater than the opening time in a situation where the closing time is in the AM and lesser than the opening time,
                        # the store is open
                        if (localhour >= oh):
                            open_ids.append(i)
                        if (localhour < ch):
                            open_ids.append(i)

                        elif (localhour == ch and localminute < cm):
                            open_ids.append(i)
                else:
                    if (localhour > oh and localhour < ch):
                        open_ids.append(i)
                    elif (localhour == oh and localminute >= om):
                        open_ids.append(i)
                    elif (localhour==ch and localminute <= cm):
                        open_ids.append(i)
                    else:
                        closed_ids.append(i)
#    print("localtime" +  str(localhour) + " " + str(localminute))
#    print("-----------------------")
#    for i in open_ids:
#        print("open", i, (cur.execute("SELECT name, sunhours FROM map_store WHERE id=?", (i,)).fetchall()))
#        print("-----------------------")
#    for i in closed_ids:
#        print("closed", i, (cur.execute("SELECT name, sunhours FROM map_store WHERE id=?", (i,)).fetchall()))
#        print("------------------------")

    return (open_ids, closed_ids)


def get_valid_ids(conn):
    #returns list of ids if the store has a name and address
    cur = conn.cursor()
    cur.execute("SELECT map_store.id FROM map_store WHERE address IS NOT NULL AND name IS NOT NULL AND fri00 IS NOT NULL")
    ids = cur.fetchall()
    return ids

def get_formatted_addresses(country, city, conn, timezone):
    #returns formatted addresses in open ids
    #no point multi-processing this: memory concerns & it's fast enough anyways (for now)
    ids = get_open_closed_ids(conn, city, timezone)
    open_ids = ids[0]
    formatted_address_list = []
    if (country == ""):
        for i in open_ids:
            address = get_col_with_id(conn, "address", i)[0][0]
            name = get_col_with_id(conn, "name", i)[0][0]
            formatted_address_list.append("({name}) {address}".format(name=name, address=address))
    else:
        for i in open_ids:
            address = get_col_with_id(conn, "address", i)[0][0]
            name = get_col_with_id(conn, "name", i)[0][0]
            formatted_address_list.append("({name}) {address}, {country}".format(name=name, address=address, country = country))
    return (formatted_address_list, ids)

def update_current_popularity(addr_and_id, conn, doBackup, doLog, proxy, num_processes):
    formatted_address_list = addr_and_id[0] #formatted addresses of all open valid stores
    open_ids = addr_and_id[1][0]
    closed_ids = addr_and_id[1][1]
    print("LEN OPEN: ", len(open_ids), "LEN CLOSED: ", len(closed_ids))
    global BACKUP
    global LOG

    if ((num_processes is None) == True):
        print("without processes")
        #for ind in range(10):
        for ind in range(len(formatted_address_list)):
            place_data = lpt.get_populartimes_by_formatted_address(formatted_address_list[ind], proxy)
            log = update_row(conn, place_data, open_ids[ind])
            if doBackup == True:
                BACKUP.write(json.dumps(place_data, indent=4))
                BACKUP.write("\r\n")

            if doLog == True:
                for entry in log:
                    LOG.write(entry)
                    LOG.write("\r\n")

        cur = conn.cursor()
        #clean up closed stores
        cur.execute("UPDATE map_store SET live_busyness=NULL WHERE id IN {closed}".format(closed=tuple(closed_ids)))
        cur.commit()


    else:
        pool = Pool(num_processes)
        place_data = {}
        #for ind in range(len(formatted_address_list)):
        for ind in range(len(formatted_address_list)):
            place_data[ind] = pool.apply_async(lpt.get_populartimes_by_formatted_address, args=(formatted_address_list[ind], proxy,))

        pool.close()
        for ind in range(len(formatted_address_list)):
            try:
                place_data[ind] = place_data[ind].get()
            except:
                try:
                    place_data[ind] = place_data[ind].get()
                except:
                    continue #nest tries twice to catch bs

        for ind in range(len(formatted_address_list)):
            log = update_row(conn, place_data[ind], open_ids[ind])
            #print("updated store iD ", open_ids[ind])
            if doBackup == True:
                BACKUP.write(json.dumps(place_data, indent=4))
                BACKUP.write("\r\n")
            if doLog == True:
                for entry in log:
                    LOG.write(entry)
                    LOG.write("\r\n")

        #clean up closed stores
        cur = conn.cursor()
        cur.execute("UPDATE map_store SET live_busyness=NULL WHERE id IN {closed}".format(closed=tuple(closed_ids)))
        conn.commit()
        return

def run_scraper(country, city, timezone, doBackup = False, doLog = False, proxy = False, num_processes = None):
    """
    :param country: country to append to formatted address
    :param doBackup:  (optional) backup raw json data, default = False
    :param doLog: (optional) error/success log, default = False
    :param proxy: (optional) proxy ip, default = False
    :param num_processes (optional) number of threads to run, default = None
    """
    global LOG
    conn = create_connection("/home/bitnami/apps/django/django_projects/GrocerCheck/grocercheck/db1.sqlite3")
    #conn = create_connection("/home/ihasdapie/Grocer_Check_Project/Org/db1.sqlite3")

    try:
        update_current_popularity(get_formatted_addresses(country, city, conn, timezone), conn, doBackup, doLog, proxy, num_processes)
        conn.commit()
        print("COMPLETE UPDATE")
    except:
        print("error in update_current_popularity")
        LOG.write("ERROR IN update_current_popularity\r\n")











