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


#or

#[
#[(bottom, left), (bottom, right), (top, left), (top, right)],
#]


ottawa_bounds=[
        [
            (45.22002414, -75.98731306),
            (45.6041603, -75.38718489),
            ]
        ]



silconValley_bounds =[
[
        (37.56823139, -122.51447506), #san fran
        (37.81136208, -122.38210851),
        ],

[
        (37.49984665, -122.40351938), #san mateo
        (37.62728434, -122.25298799),
        ],
[
        (37.43194446, -122.32805082), #redwood city, menlo park, east palo alto
        (37.53576703, -122.09855523),
        ],

[
        (37.36584107, -122.26675207), #stanford, mountain view partially
        (37.45989559, -122.07758122),
        ],

[
        (37.33577026, -122.15061534), #little gap where foothill college is
        (37.43643022, -122.06269351),
        ],

[
        (37.19950721, -122.07371094), #san jose big block
        (37.44562387, -121.74586889),
        ],

[
        (37.43784277, -121.94056418), #little bit between san jose and fremont
        (37.48689519, -121.87876608),
        ],

[
        (37.47877153, -122.09618305),
        (37.60733322, -121.90660651), #up to union city
        ],

[
        (37.59934637, -122.17989142),
        (37.70249147, -122.01959096), #up to castro valley
        ],
[
        (37.69216859, -122.31391214),
        (37.90569205, -122.191065), #berkley, el cerrito
        ],
[
        (37.91135585, -122.40729593),
        (38.01996779, -122.27121523), #richmond & co
        ],
]



newYork_bounds = [
        [
            (40.50103108, -74.35654554), #staten island, woodbridge township
            (40.65183645, -74.05654387), #hudson county/new york/yorkbay x-section
            ],
        [
            (40.65240824, -74.27912621), #bottom left of elizabeth
            (40.95000005, -74.0436068),  #above paramus, directly in line with previous x-section on vertical axis
            ],
        [
            (40.54997004, -74.05041087),
            (40.94322173, -73.78171402), #big block across new york, brooklyn, manhatten, bronx, yonkers
            ],
        [
            (40.58815184, -73.80265667),
            (40.84053667, -73.73405457), #queens
            ]

        ]





lasVegas_bounds = [
        [
            (35.94807615, -115.34795587),
            (36.32517175, -115.0224859),
            ],
        [
            (35.96808527, -115.03347223),
            (36.0713858, -114.9304754)
            ],

        ]




longIsland_bounds = [
        [
            (40.57031532, -73.97644026),
            (41.15720738, -72.13822788),
            ]

        ]






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


montreal_bounds = [
        [
            (45.68078868, -73.57781145),
            (45.7938922, -73.28804704),
            ],
        [
            (45.35527313, -74.01639059),
            (45.69202982, -73.34897116),
            ],
        ]

#-------------variables----------
API_KEY = open("/home/ihasdapie/keys/gmapkey.txt").readline()

DATABASE_DIR = os.path.dirname(os.path.dirname(os.getcwd())) + "/db1.sqlite3"
KEYWORD = "grocery"

#SCRAPE THREE TIMES W/ keywords: "department store", "grocery", "mall", "costco"
# consider implementing filter on index.html for grocery only (& costco for whatever godforsaken reason)

RADIUS = 2000 #in meters
SPACING = ((2*RADIUS)/(2**(0.5)))/1000

#-------------------------------

print("radius, ", RADIUS,"spacing, ", SPACING)
CITY = "ottawa"

print("DATABASE DIR: ", DATABASE_DIR)
coord_list = gencoords.gen_coords(ottawa_bounds, SPACING)


print("NUM COORDS: ", len(coord_list))
print("CITY ", CITY, " KEYWORd ", KEYWORD )



x, y= np.array(coord_list).T
plt.scatter(x,y)
plt.show()


first_id = get_places.getplaces(API_KEY, coord_list, DATABASE_DIR, CITY, KEYWORD, RADIUS) + 1

#add place detail will have to start on the index of the first added by getplaces: this is the lastid from getplaces + 1

add_place_detail.populate_populartimes(API_KEY, first_id, DATABASE_DIR)




