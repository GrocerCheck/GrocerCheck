import time
import psycopg2
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
    method w/ looped update commands
    :param remote_conn: a psycopg2 connection (all remote connections for this task will be postgreSQL)
    :param local_conn: a sqlite3 connection (all local connections for this task will be sqlite3)
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
    creates json dump, updates in remote, runs SQL script to apply update
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
    parses json from lpt_buffer, updates map_store
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



#----------variables------------
pg_creds = json.load(open('/home/ihasdapie/keys/postgreDB.json'))
l3_dir = "db1.sqlite3" #obviously this is just for now

pg_conn = create_pgsql_connection(pg_creds['dbname'], pg_creds['user'], pg_creds['password'], pg_creds['host'], pg_creds['port'])

l3_conn = create_sqlite3_connection(l3_dir)

#----------main----------------

updateRemoteDump(pg_conn, l3_conn)

