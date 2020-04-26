#!/usr/bin/env/python
import sqlite3
import livepopulartimes as lpt
import json

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def get_all(conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM map_store')
    rows = cur.fetchall()
    return rows

def get_columns(conn, col):
    cur = conn.cursor()
    cur.execute("SELECT place_id FROM map_store")
    col = cur.fetchall()
    return col


def gen_days():
    days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    out = ""
    for d in days:
        for h in range(24):
            out = out + ", set {day}{hour} = {obrac}{day}{hour}{cbrac}".format(day=d, hour=h, obrac= "{", cbrac ="}")
    return out

def update_row(conn, data, rowID):

    sql_command = "UPDATE map_store, set name = {name}, set lat = {lat}, set lng = {lng}, set address = {address}, set live_busyness = {live_busyness}, set hours = {hours}"
    sql_command += gen_days()
    sql_command += " WHERE id = {rowID}"
    sql_command = sql_command.format(rowID = rowID, name = data['name'], lat = data['coordinates']['lat'], 
    lng = data['coordinates']['lng'], address = data['address'], live_busyness = data['current_popularity'],
    mon0 = data['populartimes'][0]['data'][0], mon1 = 
    data['populartimes'][0]['data'][1], mon2 = data['populartimes'][0]['data'][2], mon3 = 
    data['populartimes'][0]['data'][3], mon4 = data['populartimes'][0]['data'][4], mon5 = 
    data['populartimes'][0]['data'][5], mon6 = data['populartimes'][0]['data'][6], mon7 = 
    data['populartimes'][0]['data'][7], mon8 = data['populartimes'][0]['data'][8], mon9 = 
    data['populartimes'][0]['data'][9], mon10 = data['populartimes'][0]['data'][10], mon11 = 
    data['populartimes'][0]['data'][11], mon12 = data['populartimes'][0]['data'][12], mon13 = 
    data['populartimes'][0]['data'][13], mon14 = data['populartimes'][0]['data'][14], mon15 = 
    data['populartimes'][0]['data'][15], mon16 = data['populartimes'][0]['data'][16], mon17 = 
    data['populartimes'][0]['data'][17], mon18 = data['populartimes'][0]['data'][18], mon19 = 
    data['populartimes'][0]['data'][19], mon20 = data['populartimes'][0]['data'][20], mon21 = 
    data['populartimes'][0]['data'][21], mon22 = data['populartimes'][0]['data'][22], mon23 = 
    data['populartimes'][0]['data'][23], tue0 = data['populartimes'][1]['data'][0], tue1 = 
    data['populartimes'][1]['data'][1], tue2 = data['populartimes'][1]['data'][2], tue3 = 
    data['populartimes'][1]['data'][3], tue4 = data['populartimes'][1]['data'][4], tue5 = 
    data['populartimes'][1]['data'][5], tue6 = data['populartimes'][1]['data'][6], tue7 = 
    data['populartimes'][1]['data'][7], tue8 = data['populartimes'][1]['data'][8], tue9 = 
    data['populartimes'][1]['data'][9], tue10 = data['populartimes'][1]['data'][10], tue11 = 
    data['populartimes'][1]['data'][11], tue12 = data['populartimes'][1]['data'][12], tue13 = 
    data['populartimes'][1]['data'][13], tue14 = data['populartimes'][1]['data'][14], tue15 = 
    data['populartimes'][1]['data'][15], tue16 = data['populartimes'][1]['data'][16], tue17 = 
    data['populartimes'][1]['data'][17], tue18 = data['populartimes'][1]['data'][18], tue19 = 
    data['populartimes'][1]['data'][19], tue20 = data['populartimes'][1]['data'][20], tue21 = 
    data['populartimes'][1]['data'][21], tue22 = data['populartimes'][1]['data'][22], tue23 = 
    data['populartimes'][1]['data'][23], wed0 = data['populartimes'][2]['data'][0], wed1 = 
    data['populartimes'][2]['data'][1], wed2 = data['populartimes'][2]['data'][2], wed3 = 
    data['populartimes'][2]['data'][3], wed4 = data['populartimes'][2]['data'][4], wed5 = 
    data['populartimes'][2]['data'][5], wed6 = data['populartimes'][2]['data'][6], wed7 = 
    data['populartimes'][2]['data'][7], wed8 = data['populartimes'][2]['data'][8], wed9 = 
    data['populartimes'][2]['data'][9], wed10 = data['populartimes'][2]['data'][10], wed11 = 
    data['populartimes'][2]['data'][11], wed12 = data['populartimes'][2]['data'][12], wed13 = 
    data['populartimes'][2]['data'][13], wed14 = data['populartimes'][2]['data'][14], wed15 = 
    data['populartimes'][2]['data'][15], wed16 = data['populartimes'][2]['data'][16], wed17 = 
    data['populartimes'][2]['data'][17], wed18 = data['populartimes'][2]['data'][18], wed19 = 
    data['populartimes'][2]['data'][19], wed20 = data['populartimes'][2]['data'][20], wed21 = 
    data['populartimes'][2]['data'][21], wed22 = data['populartimes'][2]['data'][22], wed23 = 
    data['populartimes'][2]['data'][23], thu0 = data['populartimes'][3]['data'][0], thu1 = 
    data['populartimes'][3]['data'][1], thu2 = data['populartimes'][3]['data'][2], thu3 = 
    data['populartimes'][3]['data'][3], thu4 = data['populartimes'][3]['data'][4], thu5 = 
    data['populartimes'][3]['data'][5], thu6 = data['populartimes'][3]['data'][6], thu7 = 
    data['populartimes'][3]['data'][7], thu8 = data['populartimes'][3]['data'][8], thu9 = 
    data['populartimes'][3]['data'][9], thu10 = data['populartimes'][3]['data'][10], thu11 = 
    data['populartimes'][3]['data'][11], thu12 = data['populartimes'][3]['data'][12], thu13 = 
    data['populartimes'][3]['data'][13], thu14 = data['populartimes'][3]['data'][14], thu15 = 
    data['populartimes'][3]['data'][15], thu16 = data['populartimes'][3]['data'][16], thu17 = 
    data['populartimes'][3]['data'][17], thu18 = data['populartimes'][3]['data'][18], thu19 = 
    data['populartimes'][3]['data'][19], thu20 = data['populartimes'][3]['data'][20], thu21 = 
    data['populartimes'][3]['data'][21], thu22 = data['populartimes'][3]['data'][22], thu23 = 
    data['populartimes'][3]['data'][23], fri0 = data['populartimes'][4]['data'][0], fri1 = 
    data['populartimes'][4]['data'][1], fri2 = data['populartimes'][4]['data'][2], fri3 = 
    data['populartimes'][4]['data'][3], fri4 = data['populartimes'][4]['data'][4], fri5 = 
    data['populartimes'][4]['data'][5], fri6 = data['populartimes'][4]['data'][6], fri7 = 
    data['populartimes'][4]['data'][7], fri8 = data['populartimes'][4]['data'][8], fri9 = 
    data['populartimes'][4]['data'][9], fri10 = data['populartimes'][4]['data'][10], fri11 = 
    data['populartimes'][4]['data'][11], fri12 = data['populartimes'][4]['data'][12], fri13 = 
    data['populartimes'][4]['data'][13], fri14 = data['populartimes'][4]['data'][14], fri15 = 
    data['populartimes'][4]['data'][15], fri16 = data['populartimes'][4]['data'][16], fri17 = 
    data['populartimes'][4]['data'][17], fri18 = data['populartimes'][4]['data'][18], fri19 = 
    data['populartimes'][4]['data'][19], fri20 = data['populartimes'][4]['data'][20], fri21 = 
    data['populartimes'][4]['data'][21], fri22 = data['populartimes'][4]['data'][22], fri23 = 
    data['populartimes'][4]['data'][23], sat0 = data['populartimes'][5]['data'][0], sat1 = 
    data['populartimes'][5]['data'][1], sat2 = data['populartimes'][5]['data'][2], sat3 = 
    data['populartimes'][5]['data'][3], sat4 = data['populartimes'][5]['data'][4], sat5 = 
    data['populartimes'][5]['data'][5], sat6 = data['populartimes'][5]['data'][6], sat7 = 
    data['populartimes'][5]['data'][7], sat8 = data['populartimes'][5]['data'][8], sat9 = 
    data['populartimes'][5]['data'][9], sat10 = data['populartimes'][5]['data'][10], sat11 = 
    data['populartimes'][5]['data'][11], sat12 = data['populartimes'][5]['data'][12], sat13 = 
    data['populartimes'][5]['data'][13], sat14 = data['populartimes'][5]['data'][14], sat15 = 
    data['populartimes'][5]['data'][15], sat16 = data['populartimes'][5]['data'][16], sat17 = 
    data['populartimes'][5]['data'][17], sat18 = data['populartimes'][5]['data'][18], sat19 = 
    data['populartimes'][5]['data'][19], sat20 = data['populartimes'][5]['data'][20], sat21 = 
    data['populartimes'][5]['data'][21], sat22 = data['populartimes'][5]['data'][22], sat23 = 
    data['populartimes'][5]['data'][23], sun0 = data['populartimes'][6]['data'][0], sun1 = 
    data['populartimes'][6]['data'][1], sun2 = data['populartimes'][6]['data'][2], sun3 = 
    data['populartimes'][6]['data'][3], sun4 = data['populartimes'][6]['data'][4], sun5 = 
    data['populartimes'][6]['data'][5], sun6 = data['populartimes'][6]['data'][6], sun7 = 
    data['populartimes'][6]['data'][7], sun8 = data['populartimes'][6]['data'][8], sun9 = 
    data['populartimes'][6]['data'][9], sun10 = data['populartimes'][6]['data'][10], sun11 = 
    data['populartimes'][6]['data'][11], sun12 = data['populartimes'][6]['data'][12], sun13 = 
    data['populartimes'][6]['data'][13], sun14 = data['populartimes'][6]['data'][14], sun15 = 
    data['populartimes'][6]['data'][15], sun16 = data['populartimes'][6]['data'][16], sun17 = 
    data['populartimes'][6]['data'][17], sun18 = data['populartimes'][6]['data'][18], sun19 = 
    data['populartimes'][6]['data'][19], sun20 = data['populartimes'][6]['data'][20], sun21 = 
    data['populartimes'][6]['data'][21], sun22 = data['populartimes'][6]['data'][22], sun23 = 
    data['populartimes'][6]['data'][23] , mon0 = data['populartimes'][0]['data'][0], mon1 = 
    data['populartimes'][0]['data'][1], mon2 = data['populartimes'][0]['data'][2], mon3 = 
    data['populartimes'][0]['data'][3], mon4 = data['populartimes'][0]['data'][4], mon5 = 
    data['populartimes'][0]['data'][5], mon6 = data['populartimes'][0]['data'][6], mon7 = 
    data['populartimes'][0]['data'][7], mon8 = data['populartimes'][0]['data'][8], mon9 = 
    data['populartimes'][0]['data'][9], mon10 = data['populartimes'][0]['data'][10], mon11 = 
    data['populartimes'][0]['data'][11], mon12 = data['populartimes'][0]['data'][12], mon13 = 
    data['populartimes'][0]['data'][13], mon14 = data['populartimes'][0]['data'][14], mon15 = 
    data['populartimes'][0]['data'][15], mon16 = data['populartimes'][0]['data'][16], mon17 = 
    data['populartimes'][0]['data'][17], mon18 = data['populartimes'][0]['data'][18], mon19 = 
    data['populartimes'][0]['data'][19], mon20 = data['populartimes'][0]['data'][20], mon21 = 
    data['populartimes'][0]['data'][21], mon22 = data['populartimes'][0]['data'][22], mon23 = 
    data['populartimes'][0]['data'][23], tue0 = data['populartimes'][1]['data'][0], tue1 = 
    data['populartimes'][1]['data'][1], tue2 = data['populartimes'][1]['data'][2], tue3 = 
    data['populartimes'][1]['data'][3], tue4 = data['populartimes'][1]['data'][4], tue5 = 
    data['populartimes'][1]['data'][5], tue6 = data['populartimes'][1]['data'][6], tue7 = 
    data['populartimes'][1]['data'][7], tue8 = data['populartimes'][1]['data'][8], tue9 = 
    data['populartimes'][1]['data'][9], tue10 = data['populartimes'][1]['data'][10], tue11 = 
    data['populartimes'][1]['data'][11], tue12 = data['populartimes'][1]['data'][12], tue13 = 
    data['populartimes'][1]['data'][13], tue14 = data['populartimes'][1]['data'][14], tue15 = 
    data['populartimes'][1]['data'][15], tue16 = data['populartimes'][1]['data'][16], tue17 = 
    data['populartimes'][1]['data'][17], tue18 = data['populartimes'][1]['data'][18], tue19 = 
    data['populartimes'][1]['data'][19], tue20 = data['populartimes'][1]['data'][20], tue21 = 
    data['populartimes'][1]['data'][21], tue22 = data['populartimes'][1]['data'][22], tue23 = 
    data['populartimes'][1]['data'][23], wed0 = data['populartimes'][2]['data'][0], wed1 = 
    data['populartimes'][2]['data'][1], wed2 = data['populartimes'][2]['data'][2], wed3 = 
    data['populartimes'][2]['data'][3], wed4 = data['populartimes'][2]['data'][4], wed5 = 
    data['populartimes'][2]['data'][5], wed6 = data['populartimes'][2]['data'][6], wed7 = 
    data['populartimes'][2]['data'][7], wed8 = data['populartimes'][2]['data'][8], wed9 = 
    data['populartimes'][2]['data'][9], wed10 = data['populartimes'][2]['data'][10], wed11 = 
    data['populartimes'][2]['data'][11], wed12 = data['populartimes'][2]['data'][12], wed13 = 
    data['populartimes'][2]['data'][13], wed14 = data['populartimes'][2]['data'][14], wed15 = 
    data['populartimes'][2]['data'][15], wed16 = data['populartimes'][2]['data'][16], wed17 = 
    data['populartimes'][2]['data'][17], wed18 = data['populartimes'][2]['data'][18], wed19 = 
    data['populartimes'][2]['data'][19], wed20 = data['populartimes'][2]['data'][20], wed21 = 
    data['populartimes'][2]['data'][21], wed22 = data['populartimes'][2]['data'][22], wed23 = 
    data['populartimes'][2]['data'][23], thu0 = data['populartimes'][3]['data'][0], thu1 = 
    data['populartimes'][3]['data'][1], thu2 = data['populartimes'][3]['data'][2], thu3 = 
    data['populartimes'][3]['data'][3], thu4 = data['populartimes'][3]['data'][4], thu5 = 
    data['populartimes'][3]['data'][5], thu6 = data['populartimes'][3]['data'][6], thu7 = 
    data['populartimes'][3]['data'][7], thu8 = data['populartimes'][3]['data'][8], thu9 = 
    data['populartimes'][3]['data'][9], thu10 = data['populartimes'][3]['data'][10], thu11 = 
    data['populartimes'][3]['data'][11], thu12 = data['populartimes'][3]['data'][12], thu13 = 
    data['populartimes'][3]['data'][13], thu14 = data['populartimes'][3]['data'][14], thu15 = 
    data['populartimes'][3]['data'][15], thu16 = data['populartimes'][3]['data'][16], thu17 = 
    data['populartimes'][3]['data'][17], thu18 = data['populartimes'][3]['data'][18], thu19 = 
    data['populartimes'][3]['data'][19], thu20 = data['populartimes'][3]['data'][20], thu21 = 
    data['populartimes'][3]['data'][21], thu22 = data['populartimes'][3]['data'][22], thu23 = 
    data['populartimes'][3]['data'][23], fri0 = data['populartimes'][4]['data'][0], fri1 = 
    data['populartimes'][4]['data'][1], fri2 = data['populartimes'][4]['data'][2], fri3 = 
    data['populartimes'][4]['data'][3], fri4 = data['populartimes'][4]['data'][4], fri5 = 
    data['populartimes'][4]['data'][5], fri6 = data['populartimes'][4]['data'][6], fri7 = 
    data['populartimes'][4]['data'][7], fri8 = data['populartimes'][4]['data'][8], fri9 = 
    data['populartimes'][4]['data'][9], fri10 = data['populartimes'][4]['data'][10], fri11 = 
    data['populartimes'][4]['data'][11], fri12 = data['populartimes'][4]['data'][12], fri13 = 
    data['populartimes'][4]['data'][13], fri14 = data['populartimes'][4]['data'][14], fri15 = 
    data['populartimes'][4]['data'][15], fri16 = data['populartimes'][4]['data'][16], fri17 = 
    data['populartimes'][4]['data'][17], fri18 = data['populartimes'][4]['data'][18], fri19 = 
    data['populartimes'][4]['data'][19], fri20 = data['populartimes'][4]['data'][20], fri21 = 
    data['populartimes'][4]['data'][21], fri22 = data['populartimes'][4]['data'][22], fri23 = 
    data['populartimes'][4]['data'][23], sat0 = data['populartimes'][5]['data'][0], sat1 = 
    data['populartimes'][5]['data'][1], sat2 = data['populartimes'][5]['data'][2], sat3 = 
    data['populartimes'][5]['data'][3], sat4 = data['populartimes'][5]['data'][4], sat5 = 
    data['populartimes'][5]['data'][5], sat6 = data['populartimes'][5]['data'][6], sat7 = 
    data['populartimes'][5]['data'][7], sat8 = data['populartimes'][5]['data'][8], sat9 = 
    data['populartimes'][5]['data'][9], sat10 = data['populartimes'][5]['data'][10], sat11 = 
    data['populartimes'][5]['data'][11], sat12 = data['populartimes'][5]['data'][12], sat13 = 
    data['populartimes'][5]['data'][13], sat14 = data['populartimes'][5]['data'][14], sat15 = 
    data['populartimes'][5]['data'][15], sat16 = data['populartimes'][5]['data'][16], sat17 = 
    data['populartimes'][5]['data'][17], sat18 = data['populartimes'][5]['data'][18], sat19 = 
    data['populartimes'][5]['data'][19], sat20 = data['populartimes'][5]['data'][20], sat21 = 
    data['populartimes'][5]['data'][21], sat22 = data['populartimes'][5]['data'][22], sat23 = 
    data['populartimes'][5]['data'][23], sun0 = data['populartimes'][6]['data'][0], sun1 = 
    data['populartimes'][6]['data'][1], sun2 = data['populartimes'][6]['data'][2], sun3 = 
    data['populartimes'][6]['data'][3], sun4 = data['populartimes'][6]['data'][4], sun5 = 
    data['populartimes'][6]['data'][5], sun6 = data['populartimes'][6]['data'][6], sun7 = 
    data['populartimes'][6]['data'][7], sun8 = data['populartimes'][6]['data'][8], sun9 = 
    data['populartimes'][6]['data'][9], sun10 = data['populartimes'][6]['data'][10], sun11 = 
    data['populartimes'][6]['data'][11], sun12 = data['populartimes'][6]['data'][12], sun13 = 
    data['populartimes'][6]['data'][13], sun14 = data['populartimes'][6]['data'][14], sun15 = 
    data['populartimes'][6]['data'][15], sun16 = data['populartimes'][6]['data'][16], sun17 = 
    data['populartimes'][6]['data'][17], sun18 = data['populartimes'][6]['data'][18], sun19 = 
    data['populartimes'][6]['data'][19], sun20 = data['populartimes'][6]['data'][20], sun21 = 
    data['populartimes'][6]['data'][21], sun22 = data['populartimes'][6]['data'][22], sun23 = 
    data['populartimes'][6]['data'][23])
    
    cur = conn.cursor()
    cur.execute(sql_command)
    print("table updated")

conn = create_connection("/home/ihasdapie/Grocer_Check_Project/Org/GrocerCheck/grocercheck/db1.sqlite3")


API_KEY = open("/home/ihasdapie/keys/gmapkey.txt").readline()


place_id_list = get_columns(conn, "place_id")
place_id_list = [pid[0] for pid in place_id_list]


#place_data = lpt.get_populartimes_by_place_id(API_KEY, place_id_list[0])

place_data = json.load(open("/home/ihasdapie/Grocer_Check_Project/Org/LivePopularTimes/example_output(get_populartimes_by_PlaceID).json"))


print(update_row(conn, place_data, 1))




