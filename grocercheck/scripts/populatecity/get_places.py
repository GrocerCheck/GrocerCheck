import json
import requests
import sqlite3
from sqlite3 import Error
import time

import sys

def readData(data):
    name = []
    lat = []
    lng = []
    address = []
    placeID = []
    types = []
    for store in data['results']:
        name.append(store['name'])
        lat.append(store['geometry']['location']['lat'])
        lng.append(store['geometry']['location']['lng'])
        address.append(store['vicinity'])
        placeID.append(store['place_id'])
        typestr =  " ".join(store['types'])
        types.append(typestr)
    output = [name,lat,lng,address,placeID,types]
    return output

def makerequest(API_KEY, lat,lng,radius, keyword, nextpage=''):
    if(nextpage!=''):
        nextpage = 'pagetoken='+nextpage

    print('request nextpage: '+nextpage)
    response = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?key='+API_KEY+'&location='+str(lat)+','+str(lng)+'&radius='+str(radius)+'&keyword='+keyword+'&'+nextpage) #change keyword depending on what is being scraped for
#-- to include things like costco, use "department store",
# scrape each city thrice - once with "grocery", "department", and "mall"

    return response

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def insert_store(conn, store):
    sql = ''' INSERT INTO map_store(id,name,lat,lng,place_id,keywords, city)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, store)
    return cur.lastrowid

def get_added(conn, city):
    cur = conn.cursor()
    sql = "SELECT place_id FROM map_store WHERE city=?"
    existing = cur.execute(sql, (city,)).fetchall()
    existing = [i[0] for i in existing]
    existing = set(existing)
    return existing


def getplaces(API_KEY, coords, database_dir, city, keyword):
    conn = create_connection(database_dir)
    added = get_added(conn, city)

    prev_last_id = conn.cursor().execute("SELECT MAX(id) FROM map_store").fetchall()[0][0]
    counter = prev_last_id+1

    for line in coords:
        clat = line[0]
        clng = line[1]
        r = 1200

        nextpage = ''
        flag = True

        while flag:
            time.sleep(3)
            response = makerequest(API_KEY, clat,clng,r, keyword, nextpage)
            data = response.json()
            #print(json.dumps(data,indent=4))

            output = readData(data)
            name = output[0]
            lat = output[1]
            lng = output[2]
            address = output[3]
            placeID = output[4]
            types=output[5]

            print("num-stores: ", len(name))

            for i in range(len(name)):
                with conn:
                    if(placeID[i] in added):
                        continue
                    added.add(placeID[i])
                    store = (counter, name[i],lat[i],lng[i],placeID[i],types[i], city)
                    storeid = insert_store(conn,store)
                    counter = counter + 1
                    print("appended store id ", storeid)
            if('next_page_token' in data):
                nextpage = data['next_page_token']
            else:
                flag = False

    print('finished, num_added: '+str(len(added)))
    return(prev_last_id)







