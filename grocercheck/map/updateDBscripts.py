import time
import psycopg2
import psycopg2.extras
import sqlite3
import json
import datetime

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
    remote_conn = create_pgsql_connection(remote_conn[0], remote_conn[1], remote_conn[2], remote_conn[3], remote_conn[4])
    local_conn = create_sqlite3_connection(local_conn)
    try:
        pg_cur = remote_conn.cursor()
        l3_cur = local_conn.cursor()
        pg_cur.execute("SELECT live_busyness, id FROM public.map_store")
        remote_data = pg_cur.fetchall() #[(live_busyness, id), ]
        for pair in remote_data:
            l3_cur.execute("UPDATE map_store SET live_busyness=? WHERE id=?", pair)
        local_conn.commit()
        pg_cur.close()
        print("updateLocal LPT complete")

    except:
        print("ERROR in updateLocal LPT")

    remote_conn.close()




def updateRemoteLoop(remote_conn, local_conn):
    """
    :param remote_conn: a psycopg2 connection (all remote connections for this task will be postgreSQL)
    :param local_conn: a sqlite3 connection (all local connections for this task will be sqlite3)

    updates live_busyness param via loop (slow bc multiple calls,  but no server-side caching of lpt)
    ***deprecated***
    """
    remote_conn = create_pgsql_connection(remote_conn[0], remote_conn[1], remote_conn[2], remote_conn[3], remote_conn[4])
    local_conn = create_sqlite3_connection(local_conn)
    try:
        pg_cur = remote_conn.cursor()
        l3_cur = local_conn.cursor()

        l3_cur.execute("SELECT live_busyness, id FROM map_store")
        local_data = l3_cur.fetchall() #[(live_busyness, id), ]

        for pair in local_data:
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
    remote_creds = remote_conn
    local_creds = local_conn
    remote_conn = create_pgsql_connection(remote_conn[0], remote_conn[1], remote_conn[2], remote_conn[3], remote_conn[4])
    local_conn = create_sqlite3_connection(local_conn)
    try:
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

        remote_conn.close()
        pg_cur.close()
        print("Dumped Local LPT to remote, calling updateFromDump")
        updateFromDump(remote_creds)

    except:
        print("ERRUR IN updateRemoteDump")

def updateFromDump(remote_conn):
    """
    :param remote_conn: a psycopg2 connection (all remote connections for this task will be postgreSQL)
    :param local_conn: a sqlite3 connection (all local connections for this task will be sqlite3)

    Parses json dump in remote, applies json to live_busyness

    """
    # Make sure this is updated to the current dev version w/ new procedure
    remote_conn = create_pgsql_connection(remote_conn[0], remote_conn[1], remote_conn[2], remote_conn[3], remote_conn[4])
    try:
        pg_cur = remote_conn.cursor()
        # cmd = """
        #         create or replace function unpackData(
        #                 n INTEGER DEFAULT 10
        #         )
        #         returns VOID as $$
        #         declare
        #                 rid RECORD;
        #                 lpt_value INTEGER;
        #                 lpt_dump JSON;
        #         begin
        #                 select public.lpt_buffer.lpt_dump into lpt_dump from public.lpt_buffer;
        #                 for rid in select public.map_store.id from public.map_store
        #                 loop
        #                         update public.map_store
        #                         set live_busyness=CAST(lpt_dump->>CAST(rid.id AS TEXT) AS INTEGER)
        #                         where public.map_store.id = rid.id;
        #                 end loop;
        #         end;

        #         $$ LANGUAGE plpgsql;
        #         select unpackData(0);
        # """

        procedure = """
        CREATE OR REPLACE PROCEDURE public.unpack()
            LANGUAGE 'plpgsql'
        AS $BODY$declare
            rid RECORD;
            lpt_dump JSON;
        begin
            select public.lpt_buffer.lpt_dump into lpt_dump from public.lpt_buffer;
            for rid in select public.map_store.id from public.map_store
            loop
                update public.map_store
                set live_busyness=CAST(lpt_dump->>CAST(rid.id as TEXT) AS INTEGER)
                where public.map_store.id=rid.id;
            end loop;
        end;$BODY$;
        """

        call_procedure = "call unpack();"


        pg_cur.execute(call_procedure)
        remote_conn.commit()

        pg_cur.close()
        remote_conn.close()
        print("updateFromDump complete -- data unpacked successfully")
    except:
        print("ERROR IN UPDATEFROMDUMP")

def updateMapStore(remote_conn, local_conn):
    """

    local(data) -> remote(data)

    :param remote_conn: a psycopg2 connection (all remote connections for this task will be postgreSQL)
    :param local_conn: a sqlite3 connection (all local connections for this task will be sqlite3)

    Checks if there are rows in local not found on remote. If so, add those rows to remote.

    """
    remote_creds = remote_conn
    local_creds = local_conn
    remote_conn = create_pgsql_connection(remote_conn[0], remote_conn[1], remote_conn[2], remote_conn[3], remote_conn[4])
    local_conn = create_sqlite3_connection(local_conn)

    local_conn.row_factory = sqlite3.Row

    pg_cur = remote_conn.cursor()
    l3_cur = local_conn.cursor()

    pg_cur.execute("SELECT public.map_store.id FROM public.map_store ORDER BY public.map_store.id DESC LIMIT 1")
    l3_cur.execute("SELECT map_store.id FROM map_store ORDER BY map_store.id DESC LIMIT 1")

    remote_last_id = pg_cur.fetchall()[0][0]
    local_last_id = l3_cur.fetchall()[0][0]

    print("REMOTE LAST", remote_last_id, "LOCAL LAST", local_last_id)

    if (remote_last_id < local_last_id):
        ids_to_update = "("+", ".join([str(i) for i in range(remote_last_id+1, local_last_id+1)])+")"  #do not update local last id, be inclusive of upper bound
        l3_cur.execute("SELECT * FROM map_store WHERE map_store.id IN {row_ids}".format(row_ids=ids_to_update,))
        local_rows = l3_cur.fetchall()
        sql = """INSERT INTO public.map_store (id, name, lat, lng, address, frihours, monhours, tuehours, wedhours, thuhours, sathours, sunhours, place_id, live_busyness, city, keywords, fri00, fri01, fri02, fri03, fri04, fri05, fri06, fri07, fri08, fri09, fri10, fri11, fri12, fri13, fri14, fri15, fri16, fri17, fri18, fri19, fri20, fri21, fri22, fri23, mon00, mon01, mon02, mon03, mon04, mon05, mon06, mon07, mon08, mon09, mon10, mon11, mon12, mon13, mon14, mon15, mon16, mon17, mon18, mon19,
        mon20, mon21, mon22, mon23, sat00, sat01, sat02, sat03, sat04, sat05, sat06, sat07, sat08, sat09, sat10, sat11, sat12, sat13, sat14, sat15, sat16, sat17, sat18, sat19, sat20, sat21, sat22, sat23, sun00, sun01, sun02, sun03, sun04, sun05, sun06, sun07, sun08, sun09, sun10, sun11, sun12, sun13, sun14, sun15, sun16, sun17, sun18, sun19, sun20, sun21, sun22, sun23, thu00, thu01, thu02, thu03, thu04, thu05, thu06, thu07, thu08, thu09, thu10, thu11, thu12, thu13, thu14, thu15, thu16, thu17,
        thu18, thu19, thu20, thu21, thu22, thu23, tue00, tue01, tue02, tue03, tue04, tue05, tue06, tue07, tue08, tue09, tue10, tue11, tue12, tue13, tue14, tue15, tue16, tue17, tue18, tue19, tue20, tue21, tue22, tue23, wed00, wed01, wed02, wed03, wed04, wed05, wed06, wed07, wed08, wed09, wed10, wed11, wed12, wed13, wed14, wed15, wed16, wed17, wed18, wed19, wed20, wed21, wed22, wed23) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

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
        pg_cur.close()
        remote_conn.close()
        print("UPDATE REMOTE MAP DATABASE FROM LOCAL COMPLETE")

    elif (remote_last_id > local_last_id):
            print("REMOTE IS AHEAD OF LOCAL; UPDATELOCALFROMREMOTE")
            updateLocalRowFromRemoteMap(remote_creds, local_creds)

    else:
        print("LOCAL IS EVEN WITH REMOTE FOR updateMapRow")


def updateLocalRowFromRemoteMap(remote_conn, local_conn):

    print("CALLED updateLocalRowFromRemoteMap")
    remote_conn = create_pgsql_connection(remote_conn[0], remote_conn[1], remote_conn[2], remote_conn[3], remote_conn[4])
    local_conn = create_sqlite3_connection(local_conn)

    pg_dict_cur = remote_conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    pg_cur = remote_conn.cursor()
    l3_cur = local_conn.cursor()

    pg_cur.execute("SELECT public.map_store.id FROM public.map_store ORDER BY public.map_store.id DESC LIMIT 1")
    l3_cur.execute("SELECT map_store.id FROM map_store ORDER BY map_store.id DESC LIMIT 1")
    remote_last_id = pg_cur.fetchall()[0][0]
    local_last_id = l3_cur.fetchall()[0][0]

    if (remote_last_id > local_last_id):
        ids_to_update = tuple([i for i in range(local_last_id+1, remote_last_id+1)])  #do not update local last id, be inclusive of upper bound
        pg_dict_cur.execute("SELECT * FROM public.map_store WHERE id in %s", (ids_to_update,))
        remote_rows = pg_dict_cur.fetchall()
        sql = """INSERT INTO map_store (id, name, lat, lng, address, frihours, monhours, tuehours, wedhours, thuhours, sathours, sunhours, place_id, live_busyness, city, keywords, fri00, fri01, fri02, fri03, fri04, fri05, fri06, fri07, fri08, fri09, fri10, fri11, fri12, fri13, fri14, fri15, fri16, fri17, fri18, fri19, fri20, fri21, fri22, fri23, mon00, mon01, mon02, mon03, mon04, mon05, mon06, mon07, mon08, mon09, mon10, mon11, mon12, mon13, mon14, mon15, mon16, mon17, mon18, mon19, mon20,
        mon21, mon22, mon23, sat00, sat01, sat02, sat03, sat04, sat05, sat06, sat07, sat08, sat09, sat10, sat11, sat12, sat13, sat14, sat15, sat16, sat17, sat18, sat19, sat20, sat21, sat22, sat23, sun00, sun01, sun02, sun03, sun04, sun05, sun06, sun07, sun08, sun09, sun10, sun11, sun12, sun13, sun14, sun15, sun16, sun17, sun18, sun19, sun20, sun21, sun22, sun23, thu00, thu01, thu02, thu03, thu04, thu05, thu06, thu07, thu08, thu09, thu10, thu11, thu12, thu13, thu14, thu15, thu16, thu17, thu18,
        thu19, thu20, thu21, thu22, thu23, tue00, tue01, tue02, tue03, tue04, tue05, tue06, tue07, tue08, tue09, tue10, tue11, tue12, tue13, tue14, tue15, tue16, tue17, tue18, tue19, tue20, tue21, tue22, tue23, wed00, wed01, wed02, wed03, wed04, wed05, wed06, wed07, wed08, wed09, wed10, wed11, wed12, wed13, wed14, wed15, wed16, wed17, wed18, wed19, wed20, wed21, wed22, wed23) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, i?)"""


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
        print("UPDATE LOCAL MAP DATABASE FROM REMOTE COMPLETE")
        pg_cur.close()
        pg_dict_cur.close()
        remote_conn.close()

    if (remote_last_id < local_last_id):
        print("REMOTE IS BEHIND LOCAL; NO CHANGES")
        # CALL updateRemoteRowFromLocal bc from here?

    else:
        print("LOCAL IS EVEN WITH REMOTE FOR updateMapRow")




#----------------------BLOG------------------

def syncBlog(remote_conn, local_conn):
    remote_creds = remote_conn
    local_creds = local_conn

    remote_conn = create_pgsql_connection(remote_conn[0], remote_conn[1], remote_conn[2], remote_conn[3], remote_conn[4])
    local_conn = create_sqlite3_connection(local_conn)

    local_conn.row_factory = sqlite3.Row

    pg_dict_cur = remote_conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    pg_cur = remote_conn.cursor()
    l3_cur = local_conn.cursor()

    # grab latest update from remote and local.
    # if local latest time < remote latest, update all posts by pulling
    # if local latest time > remote latest, update all pots by pushing
    # if the last ids are not in sync, sync em

    pg_cur.execute("SELECT map_blog_entry.id FROM public.map_blog_entry ORDER BY public.map_blog_entry.id DESC LIMIT 1")
    l3_cur.execute("SELECT map_blog_entry.id FROM map_blog_entry ORDER BY map_blog_entry.id DESC LIMIT 1")

    #i suppose there's an issue where this fails where there are 0 entries in the database, but that won't happen except during setup...
    remote_last_id = pg_cur.fetchall()[0][0]
    local_last_id = l3_cur.fetchall()[0][0]


    if (remote_last_id < local_last_id):
#could pass the ids from here to reduce redundancy
        updateRemoteFromLocalBlog(remote_creds, local_creds)
    if (remote_last_id > local_last_id):
        updateLocalRowFromRemoteBlog(remote_creds, local_creds)

    # now for the timestamp sync
    # must order or else chance of mismatch
    pg_cur.execute("SELECT id, article_timestamp from public.map_blog_entry ORDER BY id ASC")
    l3_cur.execute("SELECT id, article_timestamp from map_blog_entry ORDER BY id ASC")

    remote_id_timestamps = pg_cur.fetchall()
    local_id_timestamps = l3_cur.fetchall()
    remote_id_timestamps = [(x[0], datetime.datetime.strptime(x[1], "%Y-%m-%d %H:%M:%S")) for x in remote_id_timestamps]
    local_id_timestamps = [(x[0], datetime.datetime.strptime(x[1], "%Y-%m-%d %H:%M:%S")) for x in local_id_timestamps]



    for i in range(len(remote_id_timestamps)):
        if (remote_id_timestamps[i][1] < local_id_timestamps[i][1]):
            print("blog local is ahead of remote for id " + str(remote_id_timestamps[i][0]))
            #grab local data, update remote with it
            l3_cur.execute("SELECT id, title, author_name, author_blurb, date, content, article_sources, article_timestamp, img_src FROM map_blog_entry WHERE id=?", (remote_id_timestamps[i][0],))
            data = l3_cur.fetchall()
            data = data[0]
            data = [data['title'], data['author_name'], data['author_blurb'], data['date'], data['content'], data['article_sources'], data['article_timestamp'], data['img_src'], data['id']]
            pg_cur.execute("UPDATE public.map_blog_entry SET title=%s, author_name=%s, author_blurb=%s, date=%s, content=%s, article_sources=%s, article_timestamp=%s, img_src=%s WHERE id=%s", data)
            remote_conn.commit()

        if (remote_id_timestamps[i][1] > local_id_timestamps[i][1]):
            print("blog remote is ahead of local for id " + str(remote_id_timestamps[i][0]))
            #grab remote data, update local with it
            pg_dict_cur.execute("SELECT id, title, author_name, author_blurb, date, content, article_sources, article_timestamp, img_src FROM map_blog_entry WHERE id=%s", (remote_id_timestamps[i][0],))
            data = pg_dict_cur.fetchall()[0]
            data = [data['title'], data['author_name'], data['author_blurb'], data['date'], data['content'], data['article_sources'], data['article_timestamp'], data['img_src'], data['id']]
            l3_cur.execute("UPDATE map_blog_entry SET title=?, author_name=?, author_blurb=?, date=?, content=?, article_sources=?, article_timestamp=?, img_src=? WHERE id=?", data)
            local_conn.commit()
    pg_cur.close()
    remote_conn.close()



def updateRemoteFromLocalBlog(remote_conn, local_conn):
    remote_conn = create_pgsql_connection(remote_conn[0], remote_conn[1], remote_conn[2], remote_conn[3], remote_conn[4])
    local_conn = create_sqlite3_connection(local_conn)

    local_conn.row_factory = sqlite3.Row

    pg_cur = remote_conn.cursor()
    l3_cur = local_conn.cursor()

    pg_cur.execute("SELECT public.map_blog_entry.id FROM public.map_blog_entry ORDER BY public.map_blog_entry.id DESC LIMIT 1")
    l3_cur.execute("SELECT map_blog_entry.id FROM map_blog_entry ORDER BY map_blog_entry.id DESC LIMIT 1")

    remote_last_id = pg_cur.fetchall()[0][0]
    local_last_id = l3_cur.fetchall()[0][0]


    ids_to_update = "("+", ".join([str(i) for i in range(remote_last_id+1, local_last_id+1)])+")"  #do not update local last id, be inclusive of upper bound
        #turn ids_to_update into a string bc of sqlite3 stuff

    l3_cur.execute("SELECT * FROM map_blog_entry WHERE map_blog_entry.id IN {row_ids}".format(row_ids=ids_to_update,))
    local_rows = l3_cur.fetchall()
    sql = "INSERT INTO public.map_blog_entry (id, title, author_name, author_blurb, date, content, article_sources, article_timestamp, img_src, image_blurb) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    for fetched_row in local_rows:
        data = [fetched_row['id'], fetched_row['title'], fetched_row['author_name'], fetched_row['author_blurb'], fetched_row['date'], fetched_row['content'], fetched_row['article_sources'], fetched_row['article_timestamp'], fetched_row['img_src'], fetched_row['image_blurb']]
        pg_cur.execute(sql, data)
    remote_conn.commit()

    pg_cur.close()
    remote_conn.close()
    print("UPDATE REMOTE blog_entry FROM LOCAL COMPLETE")


def updateLocalRowFromRemoteBlog(remote_conn, local_conn):
    remote_conn = create_pgsql_connection(remote_conn[0], remote_conn[1], remote_conn[2], remote_conn[3], remote_conn[4])
    local_conn = create_sqlite3_connection(local_conn)

    pg_dict_cur = remote_conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    pg_cur = remote_conn.cursor()
    l3_cur = local_conn.cursor()

    pg_cur.execute("SELECT public.map_blog_entry.id FROM public.map_blog_entry ORDER BY public.map_blog_entry.id DESC LIMIT 1")
    l3_cur.execute("SELECT map_blog_entry.id FROM map_blog_entry ORDER BY map_blog_entry.id DESC LIMIT 1")

    remote_last_id = pg_cur.fetchall()[0][0]
    local_last_id = l3_cur.fetchall()[0][0]


    ids_to_update = tuple([i for i in range(local_last_id+1, remote_last_id+1)])  #do not update local last id, be inclusive of upper bound
    pg_dict_cur.execute("SELECT * FROM public.map_blog_entry WHERE id in %s", (ids_to_update,))
    remote_rows = pg_dict_cur.fetchall()

    sql = "INSERT INTO map_blog_entry (id, title, author_name, author_blurb, date, content, article_sources, article_timestamp, img_src, image_blurb) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"


    for fetched_row in remote_rows:
        data = [fetched_row['id'], fetched_row['title'], fetched_row['author_name'], fetched_row['author_blurb'], fetched_row['date'], fetched_row['content'], fetched_row['article_sources'], fetched_row['article_timestamp'], fetched_row['img_src'], fetched_row['image_blurb']]
        l3_cur.execute(sql, data)

    local_conn.commit()
    pg_cur.close()
    remote_conn.close()
    print("UPDATE LOCAL blog_entry FROM REMOTE COMPLETE")




#----------------------ADs------------------

def syncAds(remote_conn, local_conn):
    remote_creds = remote_conn
    local_creds = local_conn


    remote_conn = create_pgsql_connection(remote_conn[0], remote_conn[1], remote_conn[2], remote_conn[3], remote_conn[4])
    local_conn = create_sqlite3_connection(local_conn)

    local_conn.row_factory = sqlite3.Row

    pg_dict_cur = remote_conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    pg_cur = remote_conn.cursor()
    l3_cur = local_conn.cursor()

    # grab latest update from remote and local.
    # if local latest time < remote latest, update all posts by pulling
    # if local latest time > remote latest, update all pots by pushing
    # if the last ids are not in sync, sync em

    pg_cur.execute("SELECT map_ad_placement.id FROM public.map_ad_placement ORDER BY public.map_ad_placement.id DESC LIMIT 1")
    l3_cur.execute("SELECT map_ad_placement.id FROM map_ad_placement ORDER BY map_ad_placement.id DESC LIMIT 1")

    #i suppose there's an issue where this fails where there are 0 entries in the database, but that won't happen except during setup...
    remote_last_id = pg_cur.fetchall()[0][0]
    local_last_id = l3_cur.fetchall()[0][0]


    if (remote_last_id < local_last_id):
#could pass the ids from here to reduce redundancy
        updateRemoteFromLocalAd(remote_creds, local_creds)
    if (remote_last_id > local_last_id):
        updateLocalRowFromRemoteAd(remote_creds, local_creds)

    # now for the timestamp sync
    # must order or else chance of mismatch
    pg_cur.execute("SELECT id, ad_timestamp from public.map_ad_placement ORDER BY id ASC")
    l3_cur.execute("SELECT id, ad_timestamp from map_ad_placement ORDER BY id ASC")


    remote_id_timestamps = pg_cur.fetchall()
    local_id_timestamps = l3_cur.fetchall()
    remote_id_timestamps = [(x[0], datetime.datetime.strptime(x[1], "%Y-%m-%d %H:%M:%S")) for x in remote_id_timestamps]
    local_id_timestamps = [(x[0], datetime.datetime.strptime(x[1], "%Y-%m-%d %H:%M:%S")) for x in local_id_timestamps]
    # print(remote_id_timestamps, "asdf", local_id_timestamps)
    for i in range(len(remote_id_timestamps)):
        if (remote_id_timestamps[i][1] < local_id_timestamps[i][1]):
            print("ad local is ahead of remote for id " + str(remote_id_timestamps[i][0]))
            #grab local data, update remote with it
            l3_cur.execute("SELECT id, ad_blurb, ad_img_src, ad_link, ad_timestamp, ad_city FROM map_ad_placement WHERE id=?", (remote_id_timestamps[i][0],))
            data = l3_cur.fetchall()
            data = data[0]
            data = [data['ad_blurb'], data['ad_img_src'], data['ad_link'], data['ad_timestamp'], data['ad_city'], data['id']]
            pg_cur.execute("UPDATE public.map_ad_placement SET ad_blurb=%s, ad_img_src=%s, ad_link=%s, ad_timestamp=%s, ad_city=%s WHERE id=%s", data)
            remote_conn.commit()

        if (remote_id_timestamps[i][1] > local_id_timestamps[i][1]):
            print("ad remote is ahead of local for id " + str(remote_id_timestamps[i][0]))
            #grab remote data, update local with it
            pg_dict_cur.execute("SELECT id, ad_blurb, ad_img_src, ad_link, ad_timestamp, ad_city FROM public.map_ad_placement WHERE id=%s", (remote_id_timestamps[i][0],))
            data = pg_dict_cur.fetchall()[0]
            data = [data['ad_blurb'], data['ad_img_src'], data['ad_link'], data['ad_timestamp'], data['ad_city'], data['id']]
            l3_cur.execute("UPDATE map_ad_placement SET ad_blurb=?, ad_img_src=?, ad_link=?, ad_timestamp=?, ad_city=? WHERE id=?", data)
            local_conn.commit()

    pg_cur.close()
    remote_conn.close()



def updateRemoteFromLocalAd(remote_conn, local_conn):
    remote_conn = create_pgsql_connection(remote_conn[0], remote_conn[1], remote_conn[2], remote_conn[3], remote_conn[4])
    local_conn = create_sqlite3_connection(local_conn)

    local_conn.row_factory = sqlite3.Row

    pg_cur = remote_conn.cursor()
    l3_cur = local_conn.cursor()

    ids_to_update = "("+", ".join([str(i) for i in range(remote_last_id+1, local_last_id+1)])+")"  #do not update local last id, be inclusive of upper bound
        #turn ids_to_update into a string bc of sqlite3 stuff

    l3_cur.execute("SELECT * FROM map_ad_placement WHERE map_ad_placement.id IN {row_ids}".format(row_ids=ids_to_update,))
    local_rows = l3_cur.fetchall()
    sql = "INSERT INTO public.map_ad_placement (id, ad_blurb, ad_img_src, ad_link, ad_timestamp, ad_city) VALUES (%s, %s, %s, %s, %s, %s)"

    for fetched_row in local_rows:
        data = [fetched_row['id'], fetched_row['ad_blurb'], fetched_row['ad_img_src'], fetched_row['ad_link'], fetched_row['ad_timestamp'], fetched_row['ad_city']]
        pg_cur.execute(sql, data)
    remote_conn.commit()

    pg_cur.close()
    remote_conn.close()
    print("UPDATE REMOTE AD_PLACEMENT FROM LOCAL COMPLETE")


def updateLocalRowFromRemoteAd(remote_conn, local_conn):
    remote_conn = create_pgsql_connection(remote_conn[0], remote_conn[1], remote_conn[2], remote_conn[3], remote_conn[4])
    local_conn = create_sqlite3_connection(local_conn)

    pg_dict_cur = remote_conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    pg_cur = remote_conn.cursor()
    l3_cur = local_conn.cursor()

    pg_cur.execute("SELECT public.map_ad_placement.id FROM public.map_ad_placement ORDER BY public.map_ad_placement.id DESC LIMIT 1")
    l3_cur.execute("SELECT map_ad_placement.id FROM map_ad_placement ORDER BY map_ad_placement.id DESC LIMIT 1")

    remote_last_id = pg_cur.fetchall()[0][0]
    local_last_id = l3_cur.fetchall()[0][0]


    ids_to_update = tuple([i for i in range(local_last_id+1, remote_last_id+1)])  #do not update local last id, be inclusive of upper bound
    pg_dict_cur.execute("SELECT * FROM public.map_ad_placement WHERE id in %s", (ids_to_update,))
    remote_rows = pg_dict_cur.fetchall()

    sql = "INSERT INTO map_ad_placement (id, ad_blurb, ad_img_src, ad_link, ad_timestamp, ad_city) VALUES (?, ?, ?, ?, ?, ?)"
    for fetched_row in remote_rows:
        data = [fetched_row['id'], fetched_row['ad_blurb'], fetched_row['ad_img_src'], fetched_row['ad_link'], fetched_row['ad_timestamp'], fetched_row['ad_city']]
        l3_cur.execute(sql, data)

    local_conn.commit()
    pg_cur.close()
    remote_conn.close()
    print("UPDATE LOCAL AD_PLACEMENT FROM REMOTE COMPLETE")







#---------------------------OLD-----BLOG-------------------

# def updateBlogStore(remote_conn, local_conn):
#     """

#     local(data) -> remote(data)

#     :param remote_conn: a psycopg2 connection (all remote connections for this task will be postgreSQL)
#     :param local_conn: a sqlite3 connection (all local connections for this task will be sqlite3)

#     Checks if there are rows in local not found on remote. If so, add those rows to remote.

#     """
#     remote_creds = remote_conn
#     local_creds = local_conn
#     remote_conn = create_pgsql_connection(remote_conn[0], remote_conn[1], remote_conn[2], remote_conn[3], remote_conn[4])
#     local_conn = create_sqlite3_connection(local_conn)

#     local_conn.row_factory = sqlite3.Row

#     pg_cur = remote_conn.cursor()
#     l3_cur = local_conn.cursor()

#     pg_cur.execute("SELECT map_blog_entry.id FROM public.map_blog_entry ORDER BY public.map_blog_entry.id DESC LIMIT 1")
#     l3_cur.execute("SELECT map_blog_entry.id FROM map_blog_entry ORDER BY map_blog_entry.id DESC LIMIT 1")

#     remote_last_id = pg_cur.fetchall()[0][0]
#     local_last_id = l3_cur.fetchall()[0][0]


#     if (remote_last_id < local_last_id):
#         ids_to_update = "("+", ".join([str(i) for i in range(remote_last_id+1, local_last_id+1)])+")"  #do not update local last id, be inclusive of upper bound
#         l3_cur.execute("SELECT * FROM map_blog_entry WHERE map_blog_entry.id IN {row_ids}".format(row_ids=ids_to_update,))
#         local_rows = l3_cur.fetchall()
#         sql = "INSERT INTO public.map_blog_entry (id, title, author_name, author_blurb, date, content, image_blurb, article_sources) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#         for fetched_row in local_rows:
#             data = [fetched_row['id'], fetched_row['title'], fetched_row['author_name'], fetched_row['author_blurb'], fetched_row['date'], fetched_row['content'], fetched_row['image_blurb'], fetched_row['article_sources']]
#             print(len(data))
#             pg_cur.execute(sql, data)
#         remote_conn.commit()
#         print("UPDATE REMOTE BLOG FROM LOCAL COMPLETE")
#         pg_cur.close()
#         remote_conn.close()

#     if (remote_last_id > local_last_id):
#         print("REMOTE IS AHEAD OF LOCAL; UPDATELOCALROWFROMREMOTEBLOG")
#         updateLocalRowFromRemoteBlog(remote_creds, local_creds)
#     else:
#         print("LOCAL IS EVEN WITH REMOTE")


# def updateLocalRowFromRemoteBlog(remote_conn, local_conn):
#     """

#     remote(data) --> local(data)

#     :param remote_conn: a psycopg2 connection (all remote connections for this task will be postgreSQL)
#     :param local_conn: a sqlite3 connection (all local connections for this task will be sqlite3)

#     Checks if there are rows in remote not found on local. If so, add those rows to local.

#     """
#     remote_conn = create_pgsql_connection(remote_conn[0], remote_conn[1], remote_conn[2], remote_conn[3], remote_conn[4])
#     local_conn = create_sqlite3_connection(local_conn)

#     pg_dict_cur = remote_conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
#     pg_cur = remote_conn.cursor()
#     l3_cur = local_conn.cursor()

#     pg_cur.execute("SELECT public.map_blog_entry.id FROM public.map_blog_entry ORDER BY public.map_blog_entry.id DESC LIMIT 1")
#     l3_cur.execute("SELECT map_blog_entry.id FROM map_blog_entry ORDER BY map_blog_entry.id DESC LIMIT 1")

#     remote_last_id = pg_cur.fetchall()[0][0]
#     local_last_id = l3_cur.fetchall()[0][0]


#     if (remote_last_id > local_last_id):
#         ids_to_update = tuple([i for i in range(local_last_id+1, remote_last_id+1)])  #do not update local last id, be inclusive of upper bound
#         pg_dict_cur.execute("SELECT * FROM public.map_blog_entry WHERE id in %s", (ids_to_update,))
#         remote_rows = pg_dict_cur.fetchall()

#         sql = "INSERT INTO map_blog_entry (id, title, author_name, author_blurb, date, content, image_blurb, article_sources) VALUES (?,?,?,?,?,?,?,?)"
#         for fetched_row in remote_rows:
#             data = [fetched_row['id'], fetched_row['title'], fetched_row['author_name'], fetched_row['author_blurb'], fetched_row['date'], fetched_row['content'], fetched_row['image_blurb'], fetched_row['article_sources']]
#             l3_cur.execute(sql, data)

#         local_conn.commit()
#         pg_cur.close()
#         remote_conn.close()
#         print("UPDATE LOCAL BLOG FROM REMOTE COMPLETE")

#     if (remote_last_id < local_last_id):
#         print("REMOTE IS BEHIND LOCAL; NO CHANGES")
#         # CALL updateRemoteRowFromLocal bc from here?

#     else:
#         print("LOCAL IS EVEN WITH REMOTE")


#--------------------------------------OLD-BLOG-END------------------------------------------







def updateBackup(remote_conn):

    remote_conn = create_pgsql_connection(remote_conn[0], remote_conn[1], remote_conn[2], remote_conn[3], remote_conn[4])
    pg_cur = remote_conn.cursor()

    sql = """
    insert into public.lpt_backup(row_id, place_id, name, lat, lng, live_busyness, city, timestamp)
    select id, place_id, name, lat, lng, live_busyness, city, now()
    from public.map_store where live_busyness is not null
    """
    pg_cur.execute(sql)
    remote_conn.commit()
    pg_cur.close()
    remote_conn.close()

#----------variables------------
# pg_creds = json.load(open('/home/bitnami/keys/postgreDB.json'))
# l3_dir = "/home/bitnami/apps/django/django_projects/GrocerCheck/grocercheck/db1.sqlite3"

# pg_conn = create_pgsql_connection(pg_creds['dbname'], pg_creds['user'], pg_creds['password'], pg_creds['host'], pg_creds['port'])

# l3_conn = create_sqlite3_connection(l3_dir)

#----------main----------------


