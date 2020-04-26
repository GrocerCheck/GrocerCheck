import json
import requests
import sqlite3
from sqlite3 import Error
import scripts
from scripts import loadjson
import time

import sys

def makerequest(lat,lng,radius,nextpage=''):
    global API_KEY
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


def create_store(conn, store):
    sql = ''' INSERT INTO map_store(id,name,lat,lng,place_id)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, store)
    return cur.lastrowid

def get_rows(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM map_store")
    rows = cur.fetchall()
    return rows


API_KEY = 'AIzaSyBqwU_hVg2OJ3zB7FOORGzGIdsWnXdXT-w'


db = 'db1.sqlite3'
conn = create_connection(db)
counter = int(input("number of existing stores: "))+1

added = set()

rows = get_rows(conn)

for row in rows:
    added.add(row[6])



coords = open(input("enter filename: "), encoding = 'utf-8')

for line in coords:
    spl = line.split(", ")
    clat = spl[0]
    clng = spl[1]
    r = 3000
    if(len(spl)>3):
        r = int(spl[3])


    nextpage = ''
    flag = True

    while flag:
        time.sleep(3)
        response = makerequest(clat,clng,r,nextpage)
        data = response.json()
        #print(json.dumps(data,indent=4)) 
        
        output = loadjson.readData(data)
        name = output[0]
        lat = output[1]
        lng = output[2]
        address = output[3]
        placeID = output[4]
        
        print(spl[2]+" "+str(len(name)))

        for i in range(len(name)):
            with conn:
                if(placeID[i] in added):
                    continue
                added.add(placeID[i])
                store = (counter,name[i],lat[i],lng[i],placeID[i])
                storeid = create_store(conn,store)
                counter+=1
        if('next_page_token' in data):
            nextpage = data['next_page_token']
        else:
            flag = False







coords.close()
print('finished '+str(len(added)))

