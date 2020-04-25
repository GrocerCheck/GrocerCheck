import json
import requests

def readData(data):
    name = []
    lat = []
    lng = []
    address = []
    placeID = []
    for store in data['results']:
        name.append(store['name'])
        lat.append(store['geometry']['location']['lat'])
        lng.append(store['geometry']['location']['lng'])
        address.append(store['vicinity'])
        placeID.append(store['place_id'])
    output = [name,lat,lng,address,placeID]
    return output


    
