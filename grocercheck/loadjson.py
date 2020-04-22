import json
import requests

with open('grocercheckdata.txt') as json_file:
    data = json.load(json_file)
    print(json.dumps(data,indent=4))
