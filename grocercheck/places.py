import json
import requests
import sqlite3
from sqlite3 import Error
import loadjson
import time

def makerequest(lat,lng,nextpage=''):
    global API_KEY
    if(nextpage!=''):
        nextpage = 'pagetoken='+nextpage

    print('request nextpage: '+nextpage)
    response = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?key='+API_KEY+'&location='+str(lat)+','+str(lng)+'&radius=3500&type=grocery_or_supermarket&'+nextpage)
    return response

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def create_store(conn, store):
    sql = ''' INSERT INTO map_store(id,name,busyness,lat,lng,address,hours,placeID)
              VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, store)
    return cur.lastrowid




API_KEY = 'AIzaSyBqwU_hVg2OJ3zB7FOORGzGIdsWnXdXT-w'


db = 'db1.sqlite3'
conn = create_connection(db)
counter = 1

added = set()







coords = open('coords.txt', encoding = 'utf-8')

for line in coords:
    spl = line.split(", ")
    clat = spl[0]
    clng = spl[1]

    nextpage = ''
    flag = True

    while flag:
        time.sleep(3)
        response = makerequest(clat,clng,nextpage)
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
                store = (counter,name[i],0,lat[i],lng[i],address[i],'',placeID[i])
                storeid = create_store(conn,store)
                counter+=1
        if('next_page_token' in data):
            nextpage = data['next_page_token']
        else:
            flag = False







coords.close()
print('finished '+str(len(added)))

