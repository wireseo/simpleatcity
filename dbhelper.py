import pymysql
from pymysql import IntegrityError
import pandas as pd

db = pymysql.connect(host='moondb.crbqchzceqdz.ap-southeast-1.rds.amazonaws.com',
                        port=3306,
                        user='westmoon',
                        passwd='surewhynot',
                        db='simpleatcitydb',
                        charset='utf8')


def display_recipe():
    try:
        curs = db.cursor()

        # execute SQL query
        sql = "SELECT * from recipes"
        curs.execute(sql)

        # fetch data
        rows = curs.fetchall()

        # all rows
        print(rows[0])
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)
        

def add_user(chat_id):
    try:
        curs = db.cursor()

        # execute SQL query
        sql = "INSERT INTO users (id) VALUES (" + str(chat_id) + ")"
        curs.execute(sql)

        # commit
        db.commit()
    except IntegrityError as ie:
        return False
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)

#
#def close_db():
    # close connection
#    db.close()
