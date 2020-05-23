import time

import psycopg2
import psycopg2.extras
import sqlite3
import json
def create_pgsql_connection(dbname, user, password, host, port):
    conn = None
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    except Error as e:
        print(e)
    return conn

def create_sqlite3_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def updateLocal(remote_conn, local_conn):
    """
    :param remote_conn: a psycopg2 connection (all remote connections for this task will be postgreSQL)
    :param local_conn: a sqlite3 connection (all local connections for this task will be sqlite3)

    Updates local lpt from remote master
    """
    try:
        pg_cur = remote_conn.cursor()
        l3_cur = local_conn.cursor()

        pg_cur.execute("SELECT live_busyness, id FROM public.map_store")
        remote_data = pg_cur.fetchall() #[(live_busyness, id), ]

        for pair in remote_data:
            l3_cur.execute("UPDATE map_store SET live_busyness=? WHERE id=?", pair)

        local_conn.commit()
        print("updateLocal complete")
    except:
        print("ERROR in updateLocal")

def updateRemoteLoop(remote_conn, local_conn):
    """
    :param remote_conn: a psycopg2 connection (all remote connections for this task will be postgreSQL)
    :param local_conn: a sqlite3 connection (all local connections for this task will be sqlite3)

    updates live_busyness param via loop (slow bc multiple calls,  but no server-side caching of lpt)

    """
    try:
        pg_cur = remote_conn.cursor()
        l3_cur = local_conn.cursor()

        l3_cur.execute("SELECT live_busyness, id FROM map_store")
        local_data = l3_cur.fetchall() #[(live_busyness, id), ]

        for pair in local_data:
            print(pair)
            pg_cur.execute("UPDATE public.map_store SET live_busyness=%s WHERE id=%s", pair)
        remote_conn.commit()
        print("updateRemote Complete")

    except:
        print("ERROR in updateRemote")


def updateRemoteDump(remote_conn, local_conn):
    """
    :param remote_conn: a psycopg2 connection (all remote connections for this task will be postgreSQL)
    :param local_conn: a sqlite3 connection (all local connections for this task will be sqlite3)

    Creates json dump, updates in remote, runs SQL script to apply update
    """
    pg_cur = remote_conn.cursor()
    l3_cur = local_conn.cursor()

    l3_cur.execute("SELECT live_busyness, id FROM map_store")
    local_data = l3_cur.fetchall()
    local_data_dump = {}
    for pair in local_data:
        local_data_dump[int(pair[1])] = pair[0] #map live_busyness to id key
    local_data_dump = json.dumps(local_data_dump)
    pg_cur.execute("UPDATE public.lpt_buffer SET lpt_dump=%s WHERE public.lpt_buffer.id=1", (local_data_dump,))
    remote_conn.commit()
    updateFromDump(remote_conn)

def updateFromDump(remote_conn):
    """
    :param remote_conn: a psycopg2 connection (all remote connections for this task will be postgreSQL)
    :param local_conn: a sqlite3 connection (all local connections for this task will be sqlite3)

    Parses json dump in remote, applies json to live_busyness

    """
    pg_cur = remote_conn.cursor()
    cmd = """
            create or replace function unpackData(
                    n INTEGER DEFAULT 10
            )
            returns VOID as $$
            declare
                    rid RECORD;
                    lpt_value INTEGER;
                    lpt_dump JSON;
            begin
                    select public.lpt_buffer.lpt_dump into lpt_dump from public.lpt_buffer;
                    for rid in select public.map_store.id from public.map_store
                    loop
                            update public.map_store
                            set live_busyness=CAST(lpt_dump->>CAST(rid.id AS TEXT) AS INTEGER)
                            where public.map_store.id = rid.id;
                    end loop;
            end;

            $$ LANGUAGE plpgsql;
            select unpackData(0);
    """
    pg_cur.execute(cmd)
    remote_conn.commit()

def updateRow(remote_conn):
    pg_cur = remote_conn.cursor()




def updateRemoteRowFromLocal(remote_conn, local_conn):
    """
    
    local(data) -> remote(data)
    
    :param remote_conn: a psycopg2 connection (all remote connections for this task will be postgreSQL)
    :param local_conn: a sqlite3 connection (all local connections for this task will be sqlite3)

    Checks if there are rows in local not found on remote. If so, add those rows to remote.

    """
    
    local_conn.row_factory = sqlite3.Row
    
    pg_cur = remote_conn.cursor()
    l3_cur = local_conn.cursor()

    pg_cur.execute("SELECT public.map_store.id FROM public.map_store ORDER BY public.map_store.id DESC LIMIT 1")
    l3_cur.execute("SELECT map_store.id FROM map_store ORDER BY map_store.id DESC LIMIT 1")
    
    remote_last_id = pg_cur.fetchall()[0][0]
    local_last_id = l3_cur.fetchall()[0][0]

    print(remote_last_id, local_last_id)
    
    if (remote_last_id < local_last_id):
        ids_to_update = "("+", ".join([str(i) for i in range(remote_last_id+1, local_last_id+1)])+")"  #do not update local last id, be inclusive of upper bound
        l3_cur.execute("SELECT * FROM map_store WHERE map_store.id IN {row_ids}".format(row_ids=ids_to_update,))
        local_rows = l3_cur.fetchall()
        sql = """INSERT INTO public.map_store (id, name, lat, lng, address, frihours, monhours, tuehours, wedhours, thuhours, sathours, sunhours, place_id, live_busyness, city, keywords, fri00, fri01, fri02, fri03, fri04, fri05, fri06, fri07, fri08, fri09, fri10, fri11, fri12, fri13, fri14, fri15, fri16, fri17, fri18, fri19, fri20, fri21, fri22, fri23, mon00, mon01, mon02, mon03, mon04, mon05, mon06, mon07, mon08, mon09, mon10, mon11, mon12, mon13, mon14, mon15, mon16, mon17, mon18, mon19, mon20, mon21, mon22, mon23, sat00, sat01, sat02, sat03, sat04, sat05, sat06, sat07, sat08, sat09, sat10, sat11, sat12, sat13, sat14, sat15, sat16, sat17, sat18, sat19, sat20, sat21, sat22, sat23, sun00, sun01, sun02, sun03, sun04, sun05, sun06, sun07, sun08, sun09, sun10, sun11, sun12, sun13, sun14, sun15, sun16, sun17, sun18, sun19, sun20, sun21, sun22, sun23, thu00, thu01, thu02, thu03, thu04, thu05, thu06, thu07, thu08, thu09, thu10, thu11, thu12, thu13, thu14, thu15, thu16, thu17, thu18, thu19, thu20, thu21, thu22, thu23, tue00, tue01, tue02, tue03, tue04, tue05, tue06, tue07, tue08, tue09, tue10, tue11, tue12, tue13, tue14, tue15, tue16, tue17, tue18, tue19, tue20, tue21, tue22, tue23, wed00, wed01, wed02, wed03, wed04, wed05, wed06, wed07, wed08, wed09, wed10, wed11, wed12, wed13, wed14, wed15, wed16, wed17, wed18, wed19, wed20, wed21, wed22, wed23) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        for fetched_row in local_rows:
            data = [fetched_row['id'], fetched_row['name'], fetched_row['lat'], fetched_row['lng'], fetched_row['address'], fetched_row['frihours'], fetched_row['monhours'], fetched_row['tuehours'], fetched_row['wedhours'], fetched_row['thuhours'], fetched_row['sathours'], fetched_row['sunhours'], fetched_row['place_id'], fetched_row['live_busyness'], fetched_row['city'], fetched_row['keywords'], fetched_row['fri00'], fetched_row['fri01'], fetched_row['fri02'], fetched_row['fri03'],
                    fetched_row['fri04'], fetched_row['fri05'], fetched_row['fri06'], fetched_row['fri07'], fetched_row['fri08'], fetched_row['fri09'], fetched_row['fri10'], fetched_row['fri11'], fetched_row['fri12'], fetched_row['fri13'], fetched_row['fri14'], fetched_row['fri15'], fetched_row['fri16'], fetched_row['fri17'], fetched_row['fri18'], fetched_row['fri19'], fetched_row['fri20'], fetched_row['fri21'], fetched_row['fri22'], fetched_row['fri23'], fetched_row['mon00'],
                    fetched_row['mon01'], fetched_row['mon02'], fetched_row['mon03'], fetched_row['mon04'], fetched_row['mon05'], fetched_row['mon06'], fetched_row['mon07'], fetched_row['mon08'], fetched_row['mon09'], fetched_row['mon10'], fetched_row['mon11'], fetched_row['mon12'], fetched_row['mon13'], fetched_row['mon14'], fetched_row['mon15'], fetched_row['mon16'], fetched_row['mon17'], fetched_row['mon18'], fetched_row['mon19'], fetched_row['mon20'], fetched_row['mon21'],
                    fetched_row['mon22'], fetched_row['mon23'], fetched_row['sat00'], fetched_row['sat01'], fetched_row['sat02'], fetched_row['sat03'], fetched_row['sat04'], fetched_row['sat05'], fetched_row['sat06'], fetched_row['sat07'], fetched_row['sat08'], fetched_row['sat09'], fetched_row['sat10'], fetched_row['sat11'], fetched_row['sat12'], fetched_row['sat13'], fetched_row['sat14'], fetched_row['sat15'], fetched_row['sat16'], fetched_row['sat17'], fetched_row['sat18'],
                    fetched_row['sat19'], fetched_row['sat20'], fetched_row['sat21'], fetched_row['sat22'], fetched_row['sat23'], fetched_row['sun00'], fetched_row['sun01'], fetched_row['sun02'], fetched_row['sun03'], fetched_row['sun04'], fetched_row['sun05'], fetched_row['sun06'], fetched_row['sun07'], fetched_row['sun08'], fetched_row['sun09'], fetched_row['sun10'], fetched_row['sun11'], fetched_row['sun12'], fetched_row['sun13'], fetched_row['sun14'], fetched_row['sun15'],
                    fetched_row['sun16'], fetched_row['sun17'], fetched_row['sun18'], fetched_row['sun19'], fetched_row['sun20'], fetched_row['sun21'], fetched_row['sun22'], fetched_row['sun23'], fetched_row['thu00'], fetched_row['thu01'], fetched_row['thu02'], fetched_row['thu03'], fetched_row['thu04'], fetched_row['thu05'], fetched_row['thu06'], fetched_row['thu07'], fetched_row['thu08'], fetched_row['thu09'], fetched_row['thu10'], fetched_row['thu11'], fetched_row['thu12'],
                    fetched_row['thu13'], fetched_row['thu14'], fetched_row['thu15'], fetched_row['thu16'], fetched_row['thu17'], fetched_row['thu18'], fetched_row['thu19'], fetched_row['thu20'], fetched_row['thu21'], fetched_row['thu22'], fetched_row['thu23'], fetched_row['tue00'], fetched_row['tue01'], fetched_row['tue02'], fetched_row['tue03'], fetched_row['tue04'], fetched_row['tue05'], fetched_row['tue06'], fetched_row['tue07'], fetched_row['tue08'], fetched_row['tue09'],
                    fetched_row['tue10'], fetched_row['tue11'], fetched_row['tue12'], fetched_row['tue13'], fetched_row['tue14'], fetched_row['tue15'], fetched_row['tue16'], fetched_row['tue17'], fetched_row['tue18'], fetched_row['tue19'], fetched_row['tue20'], fetched_row['tue21'], fetched_row['tue22'], fetched_row['tue23'], fetched_row['wed00'], fetched_row['wed01'], fetched_row['wed02'], fetched_row['wed03'], fetched_row['wed04'], fetched_row['wed05'], fetched_row['wed06'],
                    fetched_row['wed07'], fetched_row['wed08'], fetched_row['wed09'], fetched_row['wed10'], fetched_row['wed11'], fetched_row['wed12'], fetched_row['wed13'], fetched_row['wed14'], fetched_row['wed15'], fetched_row['wed16'], fetched_row['wed17'], fetched_row['wed18'], fetched_row['wed19'], fetched_row['wed20'], fetched_row['wed21'], fetched_row['wed22'], fetched_row['wed23']]
                    
            pg_cur.execute(sql, data)
        remote_conn.commit()
    
    if (remote_last_id > local_last_id):
        print("REMOTE IS AHEAD OF LOCAL; NO CHANGES")
        # CALL updateLocalFromRemote  from here?
        
    else:
        print("LOCAL IS EVEN WITH REMOTE")
        
        
        



def updateLocalRowFromRemote(remote_conn, local_conn):
    """
    
    remote(data) --> local(data)
    
    :param remote_conn: a psycopg2 connection (all remote connections for this task will be postgreSQL)
    :param local_conn: a sqlite3 connection (all local connections for this task will be sqlite3)

    Checks if there are rows in remote not found on local. If so, add those rows to local.

    """
    pg_dict_cur = remote_conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    pg_cur = remote_conn.cursor()
    l3_cur = local_conn.cursor()

    pg_cur.execute("SELECT public.map_store.id FROM public.map_store ORDER BY public.map_store.id DESC LIMIT 1")
    l3_cur.execute("SELECT map_store.id FROM map_store ORDER BY map_store.id DESC LIMIT 1")
    remote_last_id = pg_cur.fetchall()[0][0]
    local_last_id = l3_cur.fetchall()[0][0]

    print(remote_last_id, local_last_id)
    if (remote_last_id > local_last_id):
        ids_to_update = tuple([i for i in range(local_last_id+1, remote_last_id+1)])  #do not update local last id, be inclusive of upper bound
        pg_dict_cur.execute("SELECT * FROM public.map_store WHERE id in %s", (ids_to_update,))
        remote_rows = pg_dict_cur.fetchall()
        sql = """INSERT INTO map_store (id, name, lat, lng, address, frihours, monhours, tuehours, wedhours, thuhours, sathours, sunhours, place_id, live_busyness, city, keywords, fri00, fri01, fri02, fri03, fri04, fri05, fri06, fri07, fri08, fri09, fri10, fri11, fri12, fri13, fri14, fri15, fri16, fri17, fri18, fri19, fri20, fri21, fri22, fri23, mon00, mon01, mon02, mon03, mon04, mon05, mon06, mon07, mon08, mon09, mon10, mon11, mon12, mon13, mon14, mon15, mon16, mon17, mon18, mon19, mon20, mon21, mon22, mon23, sat00, sat01, sat02, sat03, sat04, sat05, sat06, sat07, sat08, sat09, sat10, sat11, sat12, sat13, sat14, sat15, sat16, sat17, sat18, sat19, sat20, sat21, sat22, sat23, sun00, sun01, sun02, sun03, sun04, sun05, sun06, sun07, sun08, sun09, sun10, sun11, sun12, sun13, sun14, sun15, sun16, sun17, sun18, sun19, sun20, sun21, sun22, sun23, thu00, thu01, thu02, thu03, thu04, thu05, thu06, thu07, thu08, thu09, thu10, thu11, thu12, thu13, thu14, thu15, thu16, thu17, thu18, thu19, thu20, thu21, thu22, thu23, tue00, tue01, tue02, tue03, tue04, tue05, tue06, tue07, tue08, tue09, tue10, tue11, tue12, tue13, tue14, tue15, tue16, tue17, tue18, tue19, tue20, tue21, tue22, tue23, wed00, wed01, wed02, wed03, wed04, wed05, wed06, wed07, wed08, wed09, wed10, wed11, wed12, wed13, wed14, wed15, wed16, wed17, wed18, wed19, wed20, wed21, wed22, wed23) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        for fetched_row in remote_rows:
            data = [fetched_row['id'], fetched_row['name'], fetched_row['lat'], fetched_row['lng'], fetched_row['address'], fetched_row['frihours'], fetched_row['monhours'], fetched_row['tuehours'], fetched_row['wedhours'], fetched_row['thuhours'], fetched_row['sathours'], fetched_row['sunhours'], fetched_row['place_id'], fetched_row['live_busyness'], fetched_row['city'], fetched_row['keywords'], fetched_row['fri00'], fetched_row['fri01'], fetched_row['fri02'], fetched_row['fri03'],
                    fetched_row['fri04'], fetched_row['fri05'], fetched_row['fri06'], fetched_row['fri07'], fetched_row['fri08'], fetched_row['fri09'], fetched_row['fri10'], fetched_row['fri11'], fetched_row['fri12'], fetched_row['fri13'], fetched_row['fri14'], fetched_row['fri15'], fetched_row['fri16'], fetched_row['fri17'], fetched_row['fri18'], fetched_row['fri19'], fetched_row['fri20'], fetched_row['fri21'], fetched_row['fri22'], fetched_row['fri23'], fetched_row['mon00'],
                    fetched_row['mon01'], fetched_row['mon02'], fetched_row['mon03'], fetched_row['mon04'], fetched_row['mon05'], fetched_row['mon06'], fetched_row['mon07'], fetched_row['mon08'], fetched_row['mon09'], fetched_row['mon10'], fetched_row['mon11'], fetched_row['mon12'], fetched_row['mon13'], fetched_row['mon14'], fetched_row['mon15'], fetched_row['mon16'], fetched_row['mon17'], fetched_row['mon18'], fetched_row['mon19'], fetched_row['mon20'], fetched_row['mon21'],
                    fetched_row['mon22'], fetched_row['mon23'], fetched_row['sat00'], fetched_row['sat01'], fetched_row['sat02'], fetched_row['sat03'], fetched_row['sat04'], fetched_row['sat05'], fetched_row['sat06'], fetched_row['sat07'], fetched_row['sat08'], fetched_row['sat09'], fetched_row['sat10'], fetched_row['sat11'], fetched_row['sat12'], fetched_row['sat13'], fetched_row['sat14'], fetched_row['sat15'], fetched_row['sat16'], fetched_row['sat17'], fetched_row['sat18'],
                    fetched_row['sat19'], fetched_row['sat20'], fetched_row['sat21'], fetched_row['sat22'], fetched_row['sat23'], fetched_row['sun00'], fetched_row['sun01'], fetched_row['sun02'], fetched_row['sun03'], fetched_row['sun04'], fetched_row['sun05'], fetched_row['sun06'], fetched_row['sun07'], fetched_row['sun08'], fetched_row['sun09'], fetched_row['sun10'], fetched_row['sun11'], fetched_row['sun12'], fetched_row['sun13'], fetched_row['sun14'], fetched_row['sun15'],
                    fetched_row['sun16'], fetched_row['sun17'], fetched_row['sun18'], fetched_row['sun19'], fetched_row['sun20'], fetched_row['sun21'], fetched_row['sun22'], fetched_row['sun23'], fetched_row['thu00'], fetched_row['thu01'], fetched_row['thu02'], fetched_row['thu03'], fetched_row['thu04'], fetched_row['thu05'], fetched_row['thu06'], fetched_row['thu07'], fetched_row['thu08'], fetched_row['thu09'], fetched_row['thu10'], fetched_row['thu11'], fetched_row['thu12'],
                    fetched_row['thu13'], fetched_row['thu14'], fetched_row['thu15'], fetched_row['thu16'], fetched_row['thu17'], fetched_row['thu18'], fetched_row['thu19'], fetched_row['thu20'], fetched_row['thu21'], fetched_row['thu22'], fetched_row['thu23'], fetched_row['tue00'], fetched_row['tue01'], fetched_row['tue02'], fetched_row['tue03'], fetched_row['tue04'], fetched_row['tue05'], fetched_row['tue06'], fetched_row['tue07'], fetched_row['tue08'], fetched_row['tue09'],
                    fetched_row['tue10'], fetched_row['tue11'], fetched_row['tue12'], fetched_row['tue13'], fetched_row['tue14'], fetched_row['tue15'], fetched_row['tue16'], fetched_row['tue17'], fetched_row['tue18'], fetched_row['tue19'], fetched_row['tue20'], fetched_row['tue21'], fetched_row['tue22'], fetched_row['tue23'], fetched_row['wed00'], fetched_row['wed01'], fetched_row['wed02'], fetched_row['wed03'], fetched_row['wed04'], fetched_row['wed05'], fetched_row['wed06'],
                    fetched_row['wed07'], fetched_row['wed08'], fetched_row['wed09'], fetched_row['wed10'], fetched_row['wed11'], fetched_row['wed12'], fetched_row['wed13'], fetched_row['wed14'], fetched_row['wed15'], fetched_row['wed16'], fetched_row['wed17'], fetched_row['wed18'], fetched_row['wed19'], fetched_row['wed20'], fetched_row['wed21'], fetched_row['wed22'], fetched_row['wed23']]
            l3_cur.execute(sql, data)
        local_conn.commit()
    
    if (remote_last_id < local_last_id):
        print("REMOTE IS BEHIND LOCAL; NO CHANGES")
        # CALL updateRemoteRowFromLocal bc from here?
        
    else:
        print("LOCAL IS EVEN WITH REMOTE")
        
        
        
        
#----------variables------------
pg_creds = json.load(open('/home/ihasdapie/keys/postgreDB.json'))
l3_dir = "db1.sqlite3" #obviously this is just for now

pg_conn = create_pgsql_connection(pg_creds['dbname'], pg_creds['user'], pg_creds['password'], pg_creds['host'], pg_creds['port'])

l3_conn = create_sqlite3_connection(l3_dir)

#----------main----------------


updateRemoteRowFromLocal(pg_conn, l3_conn)
