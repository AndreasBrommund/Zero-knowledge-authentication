import psycopg2
import psycopg2.extras
import sys
import json


class DatabaseConnection:
    def __init__(self):

        with open('db_conf.json') as json_data_file:
            data = json.load(json_data_file)

        db = data['postgresql']['db']
        user = data['postgresql']['user']
        host = data['postgresql']['host']
        password = data['postgresql']['password']

        self.__connect_str = "dbname=" + db + " user=" + user + " host=" + host + " password=" + password

    def connect(self):

        con = None

        try:
            # Maybe can do some pool stuff
            con = psycopg2.connect(self.__connect_str)
        except psycopg2.DatabaseError as e:
            if con:
                con.close()
            print('Error %s' % e)
            sys.exit(1)

        return con


def __cursor(con):
    try:
        return con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    except psycopg2.DatabaseError as e:
        if con:
            con.close()

        print('Error %s' % e)
        sys.exit(1)


def new_user(user_name, db):
    sql_string = "INSERT INTO public.user (user_name) VALUES (%s)"

    con = db.connect()
    cur = __cursor(con)

    try:
        cur.execute(sql_string, (user_name,))

        con.commit()
    except psycopg2.DatabaseError as e:
        if con:
            con.rollback()
        print('Error %s' % e)
        sys.exit(1)

    finally:
        if con:
            con.close()
        if cur:
            cur.close()


def new_fiat_shamir(key, db):
    sql_string = "INSERT INTO public.fiat_shamir (public_key) VALUES (decode(%s,'hex')) RETURNING id"

    con = db.connect()
    cur = __cursor(con)

    try:
        cur.execute(sql_string, (key[2:],))  # Remove \0x from the hex string
        index = cur.fetchone()['id']
        con.commit()
    except psycopg2.DatabaseError as e:
        if con:
            con.rollback()
        print('Error %s' % e)
        sys.exit(1)

    finally:
        if con:
            con.close()
        if cur:
            cur.close()

    return index


def get_fiat_shamir(index, db):
    sql_string = "SELECT public_key FROM fiat_shamir WHERE id = %s"

    con = db.connect()
    cur = __cursor(con)

    try:
        cur.execute(sql_string, (index,))
        public_key = cur.fetchone()['public_key']
    except psycopg2.DatabaseError as e:
        print('Error %s' % e)
        sys.exit(1)

    finally:
        if con:
            con.close()
        if cur:
            cur.close()

    return public_key
