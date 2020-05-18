import get_places
import gencoords
import add_place_detail
import os
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
#Bounds must be given as a list of list of tuples (lat, lng) in the format
    #[(bottom,left), (top, right)

seattle_bounds = [
# CENTRAL SEATTLE
        [
        (47.48290687, -122.39343805),
        (47.59601325, -122.27670831), #leschi
            ],
        [
        (47.59417591, -122.34250155), #chinatown to madison park corner
        (47.64242772, -122.27787883),
            ],
        [
        (47.59489101, -122.35767016),
        (47.64880977, -122.31767306), #downtown, no queen anne
            ],

        [
        (47.62118399, -122.37822272),
        (47.65334064, -122.34560706), #queen anne
            ],

        [
        (47.62956846, -122.41305438), # magnolia
        (47.66089822, -122.38710229),
            ],

        [
        (47.64785419, -122.39418722), #university & above, overlaps magnolia a bit
        (47.73281416, -122.27502302),
            ],
        [
        (47.52982143, -122.24156467),
        (47.59538492, -122.21409885), #mercer island
            ],
        [
        (47.57883392, -122.19693271), #bellevue to lower redmond
        (47.6626065, -122.10766879),
            ],

        [
        (47.61515644, -122.23785054), #clyde hill
        (47.64617081, -122.19317176),
            ],

        [
        (47.6555421, -122.20810629),
        (47.77150651, -122.07764364), #redmond to bothell
            ],

        [
        (47.58009247, -122.06147627), #sammamish
        (47.63771709, -122.0016913),
            ],
        #add everest and tacoma later

]

API_KEY = open("/home/ihasdapie/keys/gmapkey.txt").readline()

DATABASE_DIR = os.path.dirname(os.path.dirname(os.getcwd())) + "/db1.sqlite3"
KEYWORD = "department store"

#SCRAPE THREE TIMES W/ keywords: "department store", "grocery", "mall"
# consider implementing filter on index.html for grocery only (& costco for whatever godforsaken reason)

CITY = "seattle"

print("DATABASE DIR: ", DATABASE_DIR)
coord_list = gencoords.gen_coords(seattle_bounds, 1.4)

print("NUM COORDS: ", len(coord_list))
x, y= np.array(coord_list).T
plt.scatter(x,y)
#~ plt.show()

first_id = get_places.getplaces(API_KEY, coord_list, DATABASE_DIR, CITY) + 1

#add place detail will have to start on the index of the first added by getplaces: this is the lastid from getplaces + 1

add_place_detail.populate_populartimes(API_KEY, first_id, DATABASE_DIR)




