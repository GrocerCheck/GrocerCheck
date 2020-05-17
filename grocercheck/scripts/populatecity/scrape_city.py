import get_places
import gencoords
import add_place_detail
import os

bounds = [
        ]



API_KEY = open("/home/ihasdapie/keys/gmapkey.txt").readline()


DATABASE_DIR = os.path.dirname(os.path.dirname(os.getcwd())) + "db1.sqlite3"

coord_list = gencoords.gen_coords(bounds)
first_id = get_places.getplaces(API_KEY, coord_list, DATABASE_DIR)
add_place_detail(API_KEY, first_id, DATABASE_DIR)




