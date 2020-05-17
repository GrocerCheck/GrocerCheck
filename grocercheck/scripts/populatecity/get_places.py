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

def makerequest(API_KEY, lat,lng,radius,nextpage=''):
    if(nextpage!=''):
        nextpage = 'pagetoken='+nextpage

    print('request nextpage: '+nextpage)
    response = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?key='+API_KEY+'&location='+str(lat)+','+str(lng)+'&radius='+str(radius)+'&keyword=grocery&'+nextpage)
    return response

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def insert_store(conn, store):
    sql = ''' INSERT INTO map_store(name,lat,lng,place_id,keywords)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, store)
    return cur.lastrowid

def getplaces(API_KEY, coords, database_dir):
    added = set()

    conn = create_connection(database_dir)

    if len(coords) < 1:
        first_id = "ERROR NO COORDS"

    else:
        first_id = conn.cursor().execute("SELECT MAX(id) FROM map_store").fetchall()[0][0] + 1

    for line in coords:
        clat = line[0]
        clng = line[1]
        r = 3000

        nextpage = ''
        flag = True

        while flag:
            time.sleep(3)
            response = makerequest(API_KEY, clat,clng,r,nextpage)
            data = response.json()
            #print(json.dumps(data,indent=4))

            output = readData(data)
            name = output[0]
            lat = output[1]
            lng = output[2]
            address = output[3]
            placeID = output[4]
            types=output[5]

            for i in range(len(name)):
                with conn:
                    if(placeID[i] in added):
                        continue
                    added.add(placeID[i])
                    store = (name[i],lat[i],lng[i],placeID[i],types[i])
                    storeid = insert_store(conn,store)
                    print("appended store id ", storeid)
            if('next_page_token' in data):
                nextpage = data['next_page_token']
            else:
                flag = False

    print('finished '+str(len(added)))
    return(first_id)







