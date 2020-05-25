import time

import get_places
import gencoords
import add_place_detail
import os
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
#Bounds must be given as a list of list of tuples (lat, lng) in the format
    #[(bottom,left), (top, right)

victoria_bounds = [
[
(48.41047131, -123.54010495), #langford
(48.46919384, -123.46151526),
    ],

    [
(48.41420075, -123.43426794), #viewroyal to victoria to oakbay to sannich
(48.50419563, -123.31444827),
    ],

[
(48.49803351, -123.38871523), #little vertical strip around royal oak burial park
(48.53263927, -123.36726535),
    ],

[
    (48.40794158, -123.32520833),
    (48.42659849, -123.29530412), #little protrusion by south oak bay
    ],

[
    (48.43556249, -123.32759598), #little protrusion by uplands park
    (48.45409697, -123.30010674),
    ],

[
(48.45067071, -123.31039082),
(48.47625147, -123.2678188), #protrusion by 10 mile point
    ],

[
(48.45974731, -123.32111184),
(48.4965039, -123.30514734), #ring road & university
    ],

]


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


toronto_bounds = [
        [
            (43.39401704, -80.5920202),
            (43.50305426, -80.42472839), #waterloo/kitchner
            ],
        [
            (43.16165444, -79.95749735),
            (43.60244289, -79.75412543), #hamilton , milton, left of oakville/missasage
            ],
        [
            (43.34441333, -79.76835765),
            (43.60488413, -79.49619642), #oakville, bottom missisauga
            ],
        [
            (43.5955699, -79.80081732),
            (43.91218304, -79.20705621), #toronto, richmond hill, markham,
            ],
        [
            (43.87129567, -79.47740725),
            (44.0791503, -79.41760664), #newmarket
            ],

        [
            (43.65936614, -79.31030273),
            (43.93098516, -79.14001456), #scarborough, pickering
            ],
        [
            (43.80405359, -79.14226184),
            (43.97626272, -78.61766467), #ajax, oshawa, bowmanville
            ],
        ]


API_KEY = open("/home/ihasdapie/keys/gmapkey.txt").readline()

DATABASE_DIR = os.path.dirname(os.path.dirname(os.getcwd())) + "/db1.sqlite3"
KEYWORD = "grocery"

#SCRAPE THREE TIMES W/ keywords: "department store", "grocery", "mall"
# consider implementing filter on index.html for grocery only (& costco for whatever godforsaken reason)

CITY = "toronto"

print("DATABASE DIR: ", DATABASE_DIR)
coord_list = gencoords.gen_coords(toronto_bounds, 1.68)


print("NUM COORDS: ", len(coord_list))
print("CITY ", CITY, " KEYWORd ", KEYWORD )



x, y= np.array(coord_list).T
plt.scatter(x,y)
plt.show()
time.sleep(5)

first_id = get_places.getplaces(API_KEY, coord_list, DATABASE_DIR, CITY, KEYWORD) + 1

#add place detail will have to start on the index of the first added by getplaces: this is the lastid from getplaces + 1

add_place_detail.populate_populartimes(API_KEY, first_id, DATABASE_DIR)




