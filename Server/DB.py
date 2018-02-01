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


def __execute(tasks, db):
    con = db.connect()
    cur = __cursor(con)

    try:
        return_value = tasks(con, cur)
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

    return return_value


def new_user(user_name, key, fiat_shamir_id, db):
    def execute(con, cur):
        sql_string = "INSERT INTO public.user (user_name) VALUES (%s) RETURNING id"
        cur.execute(sql_string, (user_name,))
        user_index = cur.fetchone()['id']
        sql_string = "INSERT INTO public.public_key (fiat_shamir_id, user_id, key) VALUES (%s,%s,%s)"
        cur.execute(sql_string, (fiat_shamir_id, user_index, __int_to_bytes(key)))
        con.commit()
        return user_index

    return __execute(execute, db)


def new_fiat_shamir(key, db):
    def execute(con, cur):
        sql_string = "INSERT INTO public.fiat_shamir (public_key) VALUES (%s) RETURNING id"
        cur.execute(sql_string, (__int_to_bytes(key),))
        index = cur.fetchone()['id']
        con.commit()
        return index

    return __execute(execute, db)


def get_fiat_shamir(index, db):
    def execute(_, cur):
        sql_string = "SELECT public_key FROM fiat_shamir WHERE id = %s"
        cur.execute(sql_string, (index,))
        res = cur.fetchone()
        if res is not None:
            return __int_from_bytes(res['public_key'])
        else:
            return None

    return __execute(execute, db)


def public_key_exist(key, db):
    def execute(_, cur):
        """ 
        We could add "AND public.public_key.fiat_shamir_id = %s". Because we only require that the key is unique in a
        fiat_shamir instance. But the DB schema require that every row is unique for now
        """
        sql_string = "SELECT EXISTS(SELECT 1 FROM public.public_key WHERE  key = %s) AS exists"
        cur.execute(sql_string, (__int_to_bytes(key),))
        exist = cur.fetchone()['exists']
        return exist

    return __execute(execute, db)


def __int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def __int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')
