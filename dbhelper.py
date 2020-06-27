import pymysql
from pymysql import IntegrityError
import pandas as pd
import random
from classes import Cache

db = pymysql.connect(host='westmoondbinstance.crbqchzceqdz.ap-southeast-1.rds.amazonaws.com',
                        port=3306,
                        user='westmoon',
                        passwd='surewhynot',
                        db='simpleatcitydb',
                        charset='utf8')


# get recipe based on ingredient input
def get_quickrecipe(ing_name_str):
    try:
        curs = db.cursor()
        # split ingredients_name to a list of ingredients_name
        ing_name_list = [x.replace(' ', '') for x in ing_name_str.split(',')]
        # convert ingredients_name to ingredients_id
        ing_id_list = [ing_name_to_id(e) for e in ing_name_list]
        # concatenate list of ingredients_id into a string
        ing_id_str = ','.join(map(str, ing_id_list))
        sql = """
            SELECT DISTINCT
                r.rec_name, r.instructions
            FROM
                recipes AS r
            JOIN recipes_main AS mi ON r.rec_id = mi.rec_id
            JOIN ingredients AS i ON mi.ing_id = i.ing_id
            LEFT JOIN recipes_main AS noIng ON r.rec_id = noIng.rec_id
                AND noIng.ing_id NOT IN ({})
            WHERE i.ing_id IN ({})
                AND noIng.id IS NULL;""".format(ing_id_str, ing_id_str)
        # execute SQL query
        curs.execute(sql)
        final_quickrec = curs.fetchall()
        # if no recipe exists
        if len(final_quickrec) == 0:
            return 'No recipe found :('
        else:
            return get_random(final_quickrec)
    except Exception as e:
        template = """
        An exception of type {0} occurred while retrieving quickrecipe suggestion.
        Arguments:\n{1!r}"""
        message = template.format(type(e).__name__, e.args)
        print(message)
        return 'Sorry, an unexpected error has occured. Please try again :('


# get recipe based on user information
def get_recipe(user):
    try:
        # retrieve list of user's ingredients
        ingredients = get_ingredients_from_user(user)
        # concatenate list of ingredients id into a string
        ing_id_str = ','.join(map(str, ingredients))
        # find all available recipes based on ingredients
        curs = db.cursor()
        sql = """
            SELECT DISTINCT
                r.rec_id
            FROM
                recipes AS r
            JOIN recipes_main AS mi ON r.rec_id = mi.rec_id
            JOIN ingredients AS i ON mi.ing_id = i.ing_id
            LEFT JOIN recipes_main AS noIng ON r.rec_id = noIng.rec_id
                AND noIng.ing_id NOT IN ({})
            WHERE i.ing_id IN ({})
                AND noIng.id IS NULL;""".format(ing_id_str, ing_id_str)
        curs.execute(sql)
        rec_by_ing = curs.fetchall()
        # if no recipe exists
        if len(rec_by_ing) == 0:
            return 'No recipe found :('
        rec_by_ing_str = query_result_to_str(rec_by_ing)

        # retrieve list of user's utensils
        utensils = get_utensils_from_user(user)
        # concatenate list of utensils id into a string
        ute_id_str = ','.join(map(str, utensils))
        # find all available recipes based on utensils
        curs = db.cursor()
        sql = """
        SELECT DISTINCT
            r.rec_id
        FROM
            recipes AS r
        JOIN recipes_utensils AS ru ON r.rec_id = ru.rec_id
        JOIN utensils AS u ON ru.uten_id = u.id
        LEFT JOIN recipes_utensils AS noUte ON r.rec_id = noUte.rec_id
            AND noUte.uten_id NOT IN ({})
        WHERE u.id IN ({})
            AND noUte.id IS NULL;""".format(ute_id_str, ute_id_str)
        curs.execute(sql)
        rec_by_ute = curs.fetchall()
        # if no recipe exists
        if len(rec_by_ing) == 0:
            return 'No recipe found :('
        rec_by_ute_str = query_result_to_str(rec_by_ute)

        # retrieve user's diet
        diet = get_diet_from_user(user)
        # convert diet_id to a string
        diet_id_str = str(diet[0])
        # find all available recipes based on ingreidents, utensils, and diet
        curs = db.cursor()
        sql = """
        SELECT r.rec_name, r.instructions FROM recipes r
            WHERE diet = {}
                AND rec_id IN ({})
                AND rec_id IN ({});
        """.format(diet_id_str, rec_by_ing_str, rec_by_ute_str)
        curs.execute(sql)
        final_rec = curs.fetchall()
        # if no recipe exists
        if len(final_rec) == 0:
            return 'No recipe found :('
        else:
            return get_random(final_rec)
    except Exception as e:
        template = """
        An exception of type {0} occurred while retrieving recipe suggestion.
        Arguments:\n{1!r}"""
        message = template.format(type(e).__name__, e.args)
        print(message)
        return 'Sorry, an unexpected error has occured. Please try again :('


# retrieve random element from input list
def get_random(input):
    r = random.randint(0, len(input) - 1)
    return 'Would you like to try "' + str(input[r][0]).lower() + '"?\n' + str(input[r][1])


# convert ingredient name to ingredient id
def ing_name_to_id(ing_name_):
    try:
        curs = db.cursor()
        sql = """
        SELECT * FROM ingredients
        WHERE ing_name_1 = '{}'
            OR ing_name_2 = '{}'
            OR ing_name_3 = '{}'
            OR ing_name_4 = '{}'
            OR ing_name_5 = '{}'
        """.format(ing_name_, ing_name_, ing_name_, ing_name_, ing_name_)
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
        sql = "INSERT INTO users (user_id) VALUES (" + str(chat_id) + ")"
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
        sql = "SELECT (diet) FROM users WHERE (user_id) = '" + str(chat_id) + "'"
        curs.execute(sql)

        # fetch data
        data = curs.fetchone()
        if data == None:
            print("Nope")

        diet = data[0]

        if diet == 0:
            diet = "Vegetarian"
        elif diet == 1:
            diet = "Vegan"
        elif diet == 2:
            diet = "Non-vegetarian"

        return diet
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)


# retrieve user's diet from user information
def get_diet_from_user(user):
    try:
        curs = db.cursor()
        # execute SQL query
        sql = "SELECT diet FROM users WHERE user_id = {}".format(user)
        curs.execute(sql)
        # fetch data
        data = curs.fetchall()
        return [x[0] for x in data]
    except Exception as e:
        template = "An exception of type {0} occurred while retrieving diet from user. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)


def get_ingredients(chat_id):
    try:
        curs = db.cursor()

        # execute SQL query
        sql = "SELECT (ing_name_1) FROM users_ingredients A JOIN ingredients B ON A.ing_id = B.ing_id JOIN users C ON A.user_id = C.id WHERE (C.user_id) = '" + str(chat_id) + "'"
        curs.execute(sql)

        # fetch data
        data = curs.fetchall()
        if not data:
            print("Nope - ingredients " + str(data))
        else:
            data = ', '.join([i for tup in data for i in tup])
            return data
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)


# retrieve a list of ingredient_id from user information
def get_ingredients_from_user(user):
    try:
        curs = db.cursor()
        # execute SQL query
        sql = "SELECT ing_id FROM users a JOIN users_ingredients b ON a.id = b.user_id WHERE a.user_id = {}".format(user)
        curs.execute(sql)
        # fetch data
        data = curs.fetchall()
        return [x[0] for x in data]
    except Exception as e:
        template = "An exception of type {0} occurred while retrieving ingredients from user. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)


def get_utensils(chat_id):
    try:
        curs = db.cursor()

        # execute SQL query
        sql = "SELECT (B.name) FROM users_utensils A JOIN utensils B ON A.uten_id = B.id JOIN users C ON A.user_id = C.id WHERE (C.user_id) = '" + str(chat_id) + "'"
        curs.execute(sql)

        # fetch data
        data = curs.fetchall()
        if not data:
            print("Nope - utensils" + str(data))
        else:
            data = ', '.join([i for tup in data for i in tup])
            return data
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)


# retrieve user's utensils from user information
def get_utensils_from_user(user):
    try:
        curs = db.cursor()
        # execute SQL query
        sql = "SELECT uten_id FROM users a JOIN users_utensils b ON a.id = b.user_id WHERE a.user_id = {}".format(user)
        curs.execute(sql)
        # fetch data
        data = curs.fetchall()
        return [x[0] for x in data]
    except Exception as e:
        template = "An exception of type {0} occurred while retrieving utensils from user. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)


def get_likes(chat_id):
    try:
        curs = db.cursor()

        # execute SQL query
        sql = "SELECT (B.name) FROM users_likes A JOIN categories B ON A.cat_id = B.id JOIN users C ON A.user_id = C.id WHERE (C.user_id) = '" + str(chat_id) + "'"
        curs.execute(sql)

        # fetch data
        data = curs.fetchall()
        if not data:
            print("Nope - likes" + str(data))
        else:
            data = ', '.join([i for tup in data for i in tup])
            return data
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)


def get_dislikes(chat_id):
    try:
        curs = db.cursor()

        # execute SQL query
        sql = "SELECT (B.name) FROM users_dislikes A JOIN categories B ON A.cat_id = B.id JOIN users C ON A.user_id = C.id WHERE (C.user_id) = '" + str(chat_id) + "'"
        curs.execute(sql)

        # fetch data
        data = curs.fetchall()
        if not data:
            print("Nope - dislikes" + str(data))
        else:
            data = ', '.join([i for tup in data for i in tup])
            return data
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)


def get_num_rated(chat_id):
    try:
        curs = db.cursor()

        # execute SQL query
        sql = "SELECT (num_rated) FROM users WHERE (user_id) = '" + str(chat_id) + "'"
        curs.execute(sql)

        # fetch data
        data = curs.fetchone()
        if data == None:
            print("Nope - num rated")
        return data[0]
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)


def get_recipes_uploaded(chat_id):
    try:
        curs = db.cursor()

        # execute SQL query
        sql = "SELECT B.rec_name, B.rec_id FROM users_uploaded A JOIN recipes B ON A.rec_id = B.rec_id JOIN users C ON A.user_id = C.id WHERE (C.user_id) = '" + str(chat_id) + "'"
        curs.execute(sql)

        # fetch data
        data = curs.fetchall()
        if not data:
            print("Nope - recipes uploaded" + str(data))
        else:
            newdata = []
            for i, (name, id) in enumerate(data):
                newdata.append((str(id) + ". " + str(name)))
            newdata = '\n\t\t'.join(newdata)
            return newdata
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)


def get_recipes_liked(chat_id):
    try:
        curs = db.cursor()

        # execute SQL query
        sql = "SELECT B.rec_name, B.rec_id FROM users_liked A JOIN recipes B ON A.rec_id = B.rec_id JOIN users C ON A.user_id = C.id WHERE (C.user_id) = '" + str(chat_id) + "'"
        curs.execute(sql)

        # fetch data
        data = curs.fetchall()
        if not data:
            print("Nope - recipes liked" + str(data))
        else:
            newdata = []
            for i, (name, id) in enumerate(data):
                newdata.append((str(id) + ". " + str(name)))
            newdata = '\n\t\t'.join(newdata)
            return newdata
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)


def change_diet_status(chat_id, diet):
    try:
        curs = db.cursor()

        # execute SQL query
        sql = "UPDATE users SET diet = '" + str(diet) + "' WHERE (user_id) = '" + str(chat_id) + "'"
        curs.execute(sql)
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)


def get_recipe_with_id(rid):
    try:
        curs = db.cursor()

        # execute SQL query
        sql = "SELECT rec_name, instructions FROM recipes WHERE (recipes.rec_id) = '" + str(rid) + "'"
        curs.execute(sql)

        # fetch data
        data = curs.fetchone()
        if not data:
            print("Nope - recipes with id" + str(data))
            return "There are no recipes with this id."
        else:
            return data[0] + "\n\n" + data[1]
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)


def cache_ingredients():
    try:
        curs = db.cursor()

        # execute SQL query
        sql = "SELECT ing_id, ing_name_1, ing_name_2, ing_name_3, ing_name_4, ing_name_5 FROM ingredients"
        curs.execute(sql)

        # fetch data
        data = curs.fetchall()
        if not data:
            print("Nope - get all ingredients" + str(data))
            __init__.ingred_string = "There are no ingredients in the db. Please contact the administrator."
        else:
            newdata = []
            for tup in data:
                newdata.append(' | '.join(filter(None, tup[1:])))
                for i in range (0, 5):
                    if tup[i]:
                        Cache.ingred_dict[str(tup[i + 1])] = tup[0]
                    i = i + 1
            Cache.ingred_string = '\n'.join(newdata)

    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)


def add_ingredients_to_user(chat_id, ingredlst):
    for ingred in ingredlst:
        id = Cache.ingred_dict.get(ingred)
        print(id)
        try:
            curs1 = db.cursor()

            # execute SQL query
            sql1 = "SELECT (B.id) FROM users_ingredients A JOIN users B ON A.user_id = B.id WHERE B.user_id = " + str(chat_id)

            curs1.execute(sql1)
            db.commit()
            user_id = curs1.fetchone()[0]
            print("uid: " + str(user_id))

            curs2 = db.cursor()
            sql2 = "INSERT IGNORE INTO users_ingredients (user_id, ing_id) VALUES (" + str(user_id) + ", " + str(id) +")"
            curs2.execute(sql2)
            db.commit()
        except Exception as e:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            print(message)


def remove_ingredients_from_user(chat_id, ingredlst):
    for ingred in ingredlst:
        id = Cache.ingred_dict.get(ingred)
        print(id)
        try:
            curs1 = db.cursor()

            # execute SQL query
            sql1 = "SELECT (B.id) FROM users_ingredients A JOIN users B ON A.user_id = B.id WHERE B.user_id = " + str(chat_id)

            curs1.execute(sql1)
            db.commit()

            user_id = curs1.fetchone()[0]
            print("uid: " + str(user_id))

            curs2 = db.cursor()
            sql = "DELETE FROM users_ingredients WHERE (user_id = " + str(user_id) + ") AND (ing_id = " + str(id) + ")"
            curs2.execute(sql)

            # commit
            db.commit()
        except Exception as e:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            print(message)


# Necessary for quick access to ing_id...
def setup_ingred_dictionary():
    dict = {}
    try:
        curs = db.cursor()
        # execute SQL query
        sql = "SELECT * FROM ingredients"
        curs.execute(sql)

        # fetch data
        data = curs.fetchone()
        if not data:
            print("Nonexistent ingredient " + str(ingred))
        else:
            newdata = []
            for tup in data:
                print(tup)
                newdata.append(' | '.join(filter(None, tup)))
                print(newdata)
            str = '\n'.join(newdata)
            return str

    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)
    return None

# convert query results(list of tuples) to a string
def query_result_to_str(list):
    flat_list = [str(x[0]) for x in list]
    return ','.join(map(str, flat_list))


def close_db():
    # close connection
    db.close()
