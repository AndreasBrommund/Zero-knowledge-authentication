import psycopg2
import psycopg2.extras
import sys


class DatabaseConnection:

    def __init__(self,db_name,user,host,password):
        self.__connect_str = "dbname="+db_name+" user="+user+" host="+host+" password="+password

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


def new_user(user_name,db):

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


