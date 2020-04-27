import sqlite3
import requests
from scripts.Get_places import loadjson

def makerequest(lat,lng,radius,nextpage=''):
    global API_KEY
    if(nextpage!=''):
        nextpage = 'pagetoken='+nextpage
    response = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?key='+API_KEY+'&location='+str(lat)+','+str(lng)+'&radius='+str(radius)+'&keyword=costco+wholesale&'+nextpage)
    return response



conn = sqlite3.connect('db1.sqlite3')
index = int(input('How many stores are in the db: '))

API_KEY = 'AIzaSyBqwU_hVg2OJ3zB7FOORGzGIdsWnXdXT-w'


lat = input('lat: ')
lng = input('lng: ')

radius = 30000
response = makerequest(lat,lng,radius)

data = response.json()

output = loadjson.readData(data)
name = output[0]
lat = output[1]
lng = output[2]
address = output[3]
place_id = output[4]
sql = ''' INSERT INTO map_store(id,name,lat,lng,place_id)
        VALUES(?,?,?,?,?) '''

counter = 1
with conn:
    for x in range(len(name)):
        if 'Wholesale' in name[x]:
            cur = conn.cursor()
            store = (index+counter,name[x],lat[x],lng[x],place_id[x])
            cur.execute(sql, store)
            counter+=1
            print('added '+str(store))




    
