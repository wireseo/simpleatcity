import pymysql
from pymysql import IntegrityError
import pandas as pd

db = pymysql.connect(host='westmoondbinstance.crbqchzceqdz.ap-southeast-1.rds.amazonaws.com',
                        port=3306,
                        user='westmoon',
                        passwd='surewhynot',
                        db='simpleatcitydb',
                        charset='utf8')


# get recipe by ingredients
def get_quickrecipe(ing_list):
    try:
        curs = db.cursor()
        # execute SQL query
        sql = """
            SELECT DISTINCT
                r.rec_name
            FROM
                recipes AS r
            JOIN main_ingredients AS mi ON r.rec_id = mi.rec_id
            JOIN ingredients AS i ON mi.ing_id = i.ing_id
            LEFT JOIN main_ingredients AS noIng ON r.rec_id = noIng.rec_id
                AND noIng.ing_id NOT IN (1,2,3)
            WHERE i.ing_id IN (1,2,3)
                AND noIng.id IS NULL;"""
        sql_2 = "SELECT * FROM recipes WHERE rec_id = 1"
        curs.execute(sql)
        rows = curs.fetchall()

        if len(rows) == 0:
            return 'No recipe found :('
        else:
            return ''.join(str(x) for x in rows)

    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)
        return 'Sorry, an unexpected error has occured.\n Please try again :('

def display_recipe():
    try:
        curs = db.cursor()
# fetch data
#rows = curs.fetchall()

        # execute SQL query
        sql = "SELECT * from recipes"
        curs.execute(sql)
# all rows
#print(rows[0])

        # fetch data
        rows = curs.fetchall()
# print column names of 'users' table
#sql2 = 'SHOW COLUMNS FROM users'
#curs.execute(sql2)

#col_name = curs.fetchall()

#for name in col_name:
#    print(name[0])

# close connection
#db.close()

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


# veg = 0, vegan = 1, non veg = 2
def get_diet(chat_id):
    try:
        curs = db.cursor()

        # execute SQL query
        sql = "SELECT (diet) FROM users WHERE (id) = '" + str(chat_id) + "'"
        curs.execute(sql)

        # fetch data
        data = curs.fetchone()
        if data == None:
            print("Nope")
        return data[0]
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)


def get_ingredients(chat_id):
    try:
        curs = db.cursor()

        # execute SQL query
        sql = "SELECT (ingredients) FROM users WHERE (id) = '" + str(chat_id) + "'"
        curs.execute(sql)

        # fetch data
        data = curs.fetchone()
        if data == None:
            print("Nope")
        return data[0]
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)


def get_utensils(chat_id):
    try:
        curs = db.cursor()

        # execute SQL query
        sql = "SELECT (utensils) FROM users WHERE (id) = '" + str(chat_id) + "'"
        curs.execute(sql)

        # fetch data
        data = curs.fetchone()
        if data == None:
            print("Nope")
        return data[0]
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)


def get_likes(chat_id):
    try:
        curs = db.cursor()

        # execute SQL query
        sql = "SELECT (likes) FROM users WHERE (id) = '" + str(chat_id) + "'"
        curs.execute(sql)

        # fetch data
        data = curs.fetchone()
        if data == None:
            print("Nope")
        return data[0]
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)


def get_dislikes(chat_id):
    try:
        curs = db.cursor()

        # execute SQL query
        sql = "SELECT (dislikes) FROM users WHERE (id) = '" + str(chat_id) + "'"
        curs.execute(sql)

        # fetch data
        data = curs.fetchone()
        if data == None:
            print("Nope")
        return data[0]
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)


def get_num_rated(chat_id):
    try:
        curs = db.cursor()

        # execute SQL query
        sql = "SELECT (num_rated) FROM users WHERE (id) = '" + str(chat_id) + "'"
        curs.execute(sql)

        # fetch data
        data = curs.fetchone()
        if data == None:
            print("Nope")
        return data[0]
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)


def get_recipes_uploaded(chat_id):
    try:
        curs = db.cursor()

        # execute SQL query
        sql = "SELECT (recipes_uploaded) FROM users WHERE (id) = '" + str(chat_id) + "'"
        curs.execute(sql)

        # fetch data
        data = curs.fetchone()
        if data == None:
            print("Nope")
        return data[0]
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)


def get_recipes_liked(chat_id):
        try:
            curs = db.cursor()

            # execute SQL query
            sql = "SELECT (recipes_liked) FROM users WHERE (id) = '" + str(chat_id) + "'"
            curs.execute(sql)

            # fetch data
            data = curs.fetchone()
            if data == None:
                print("Nope")
            return data[0]
        except Exception as e:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            print(message)


def close_db():
    # close connection
    db.close()
