import pymysql
from pymysql import IntegrityError
import pandas as pd
import random

db = pymysql.connect(host='westmoondbinstance.crbqchzceqdz.ap-southeast-1.rds.amazonaws.com',
                        port=3306,
                        user='westmoon',
                        passwd='surewhynot',
                        db='simpleatcitydb',
                        charset='utf8')

# get recipe by ingredients
def get_quickrecipe(ing_name_str):
    try:
        ## print('These are the inputs : {}'.format(ing_name_str))
        curs = db.cursor()
        # split ingredients_name to a list of ingredients_name
        ing_name_list = [x.replace(' ', '') for x in ing_name_str.split(',')]
        ## print('Below are the elements of the ing_name_list')
        ## for a in ing_name_list:
        ##        print(a)
        # convert ingredients_name to ingredients_id
        ing_id_list = [ing_name_to_id(e) for e in ing_name_list]
        ## print('Below are the elements of the ing_id_list')
        ## for b in ing_id_list:
        ##    print(b)
        # concatenate list of ingredients_id into a string
        ing_id_str = ','.join(map(str, ing_id_list))
        ## print('This is the concatenated string of ing_id : {}'.format(ing_id_str))
        sql = """
            SELECT DISTINCT
                r.instructions
            FROM
                recipes AS r
            JOIN main_ingredients AS mi ON r.rec_id = mi.rec_id
            JOIN ingredients AS i ON mi.ing_id = i.ing_id
            LEFT JOIN main_ingredients AS noIng ON r.rec_id = noIng.rec_id
                AND noIng.ing_id NOT IN ({})
            WHERE i.ing_id IN ({})
                AND noIng.id IS NULL;""".format(ing_id_str, ing_id_str)
        # execute SQL query
        curs.execute(sql)
        rows = curs.fetchall()
        # if no recipe exists
        if len(rows) == 0:
            return 'No recipe found :('
        else:
            return get_random(rows)
    except Exception as e:
        template = """
        An exception of type {0} occurred while retrieving quickrecipe suggestion.
        Arguments:\n{1!r}"""
        message = template.format(type(e).__name__, e.args)
        print(message)
        return 'Sorry, an unexpected error has occured. Please try again :('

def get_random(input):
    r = random.randint(0, len(input) - 1)
    return ''.join(str(input[r]))

def ing_name_to_id(ing_name_):
    try:
        curs = db.cursor()
        sql = """
        SELECT * FROM ingredients
        WHERE ing_name_1 = '{}'
            OR ing_name_2 = '{}'
            OR ing_name_3 = '{}'""".format(ing_name_, ing_name_, ing_name_)
        # execute SQL query
        curs.execute(sql)
        ing_row = curs.fetchone()
        # return first column 'ing_id'
        return ing_row[0]
    except Exception as e:
        template = """
        An exception of type {0} occurred while converting ingredient name to id.
        Arguments:\n{1!r}"""
        message = template.format(type(e).__name__, e.args)
        print(message)

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
