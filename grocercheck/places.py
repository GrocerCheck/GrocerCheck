import json
import requests

API_KEY = 'AIzaSyBqwU_hVg2OJ3zB7FOORGzGIdsWnXdXT-w'

response = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?key='+API_KEY+'&inputtype=textquery&location=49.2399,-123.1251&radius=10000&type=grocery_or_supermarket')

output = response.json()


with open('grocercheckdata.txt','w') as outfile:
    json.dump(output,outfile)


print(output)
