import json
import requests
import sqlite3
from sqlite3 import Error
import loadjson

def makerequest(nextpage=''):
    global API_KEY
    if(nextpage!=''):
        nextpage = 'pagetoken='+nextpage

    print('request nextpage: '+nextpage)
    response = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?key='+API_KEY+'&inputtype=textquery&location=49.2399,-123.1251&radius=10000&type=grocery_or_supermarket&'+nextpage)
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


nextpage = ''
flag = True

db = 'db1.sqlite3'
conn = create_connection(db)
counter = 1
while flag:

    response = makerequest(nextpage)
    data = response.json()
    #print(json.dumps(data,indent=4)) 
    
    output = loadjson.readData(data)
    name = output[0]
    lat = output[1]
    lng = output[2]
    address = output[3]
    placeID = output[4]

    for i in range(len(name)):
        with conn:
            store = (counter,name[i],0,lat[i],lng[i],address[i],'',placeID[i])
            storeid = create_store(conn,store)
            print('added store '+str(storeid)+': '+str(store))
            counter+=1
    if('next_page_token' in data):
        print('found next')
        nextpage = data['next_page_token']
    else:
        print('didnt')
        flag = False




print('finished')

