import pymysql
from pymysql import IntegrityError
import telebot
import pandas as pd
import random
from cache import Cache

db = pymysql.connect(host='westmoondbinstance.crbqchzceqdz.ap-southeast-1.rds.amazonaws.com',
                        port=3306,
                        user='westmoon',
                        passwd='surewhynot',
                        db='simpleatcitydb',
                        charset='utf8')

# get recipe based on ingredient input
def get_quickrecipes(ing_name_str):
    try:
        curs = db.cursor()
        # split ingredients_name to a list of ingredients_name
        ing_name_list = [x.replace(' ', '') for x in ing_name_str.lower().split(',')]
        # convert ingredients_name to ingredients_id
        ing_id_list = [ing_name_to_id(e) for e in ing_name_list]
        # concatenate list of ingredients_id into a string
        ing_id_str = ','.join(map(str, ing_id_list))

        sql = """
            SELECT DISTINCT
                *
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
        # handles a case when no recipe exists
        if len(final_quickrec) == 0:
            return 'norec'
        else:
            print(list(final_rec))
            return list(final_quickrec)
    except Exception as e:
        print("An exception of type {0} occurred while retrieving quickrecipe. Arguments:\n{1!r}".format(type(e).__name__, e.args))
        return 'error'


# get recipe based on user information
def get_recipes(user_id):
    try:
        # retrieve list of user's ingredients
        ingredients = get_ingredients_from_user(user_id)
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
            return 'norec_ing'
        rec_by_ing_str = query_result_to_str(rec_by_ing)

        # retrieve list of user's utensils
        utensils = get_utensils_from_user(user_id)
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
            return 'norec_ute'
        rec_by_ute_str = query_result_to_str(rec_by_ute)

        # retrieve user's diet
        diet = get_diet_from_user(user_id)
        # convert diet_id to a string
        diet_id_str = str(diet[0])
        # process diet_id to include all available diet
        processed_diet_id_str = process_diet(diet_id_str)
        # retrieve list of user's disliked categories
        # dislikes = get_dislikes_from_user(user_id)
        # concatenate list of utensils id into a string
        # dislikes_id_str = ','.join(map(str, dislikes))

        # find all available recipes based on ingreidents, utensils, diet, and preferences
        curs = db.cursor()
        sql = """
        SELECT * FROM recipes r
            WHERE diet IN ({})
                AND rec_id IN ({})
                AND rec_id IN ({});
        """.format(processed_diet_id_str, rec_by_ing_str, rec_by_ute_str)
        curs.execute(sql)
        final_rec = curs.fetchall()
        # handles a case when no recipe exists
        if len(final_rec) == 0:
            return 'norec'
        else:
            print(list(final_rec))
            return list(final_rec)
    except Exception as e:
        print("An exception of type {0} occurred while retrieving recipe. Arguments:\n{1!r}".format(type(e).__name__, e.args))
        return 'error'


# process diet_id to include all available diets
def process_diet(diet_id):
    if diet_id == "0":
        return "0"
    elif diet_id == "1":
        return "0, 1"
    elif diet_id == "2":
        return "0, 1, 2"


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
        print("An exception of type {0} occurred while retrieving recipe. Arguments:\n{1!r}".format(type(e).__name__, e.args))


# display all recipes
def display_recipe():
    try:
        curs = db.cursor()
        sql = "SELECT * from recipes"
        curs.execute(sql)
        rows = curs.fetchall()
        print(rows[0])
    except Exception as e:
        print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))


# add user to database
def add_user(chat_id):
    try:
        curs = db.cursor()
        sql = "INSERT INTO users (user_id) VALUES (" + str(chat_id) + ")"
        curs.execute(sql)
        db.commit()
    except IntegrityError as ie:
        return False
    except Exception as e:
        print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))


# retrieve user's diet
def get_diet(chat_id):
    try:
        curs = db.cursor()
        sql = "SELECT (diet) FROM users WHERE (user_id) = '" + str(chat_id) + "'"
        curs.execute(sql)
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
        print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))


# retrieve user's diet from user information
def get_diet_from_user(user_id):
    try:
        curs = db.cursor()
        sql = "SELECT diet FROM users WHERE id = {}".format(user_id)
        curs.execute(sql)
        data = curs.fetchall()
        return [x[0] for x in data]
    except Exception as e:
        print("An exception of type {0} occurred while retrieving diet from user. Arguments:\n{1!r}".format(type(e).__name__, e.args))


# retrieve user's list of ingredients
def get_ingredients(chat_id):
    try:
        curs = db.cursor()
        sql = "SELECT (ing_name_1) FROM users_ingredients A JOIN ingredients B ON A.ing_id = B.ing_id JOIN users C ON A.user_id = C.id WHERE (C.user_id) = '" + str(chat_id) + "'"
        curs.execute(sql)
        data = curs.fetchall()
        if not data:
            print("Nope - ingredients " + str(data))
        else:
            data = ', '.join([i for tup in data for i in tup])
            return data
    except Exception as e:
        print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))


# retrieve ingredients with user_id
def get_ingredients_from_user(user_id):
    try:
        curs = db.cursor()
        sql = "SELECT ing_id FROM users_ingredients WHERE user_id = {}".format(user_id)
        curs.execute(sql)
        data = curs.fetchall()
        return [x[0] for x in data]
    except Exception as e:
        print("An exception of type {0} occurred while retrieving ingredients from user. Arguments:\n{1!r}".format(type(e).__name__, e.args))


# retrieve user's list of utensils
def get_utensils(chat_id):
    try:
        curs = db.cursor()
        sql = "SELECT (B.name) FROM users_utensils A JOIN utensils B ON A.uten_id = B.id JOIN users C ON A.user_id = C.id WHERE (C.user_id) = '" + str(chat_id) + "'"
        curs.execute(sql)
        data = curs.fetchall()
        if not data:
            print("Nope - utensils" + str(data))
        else:
            data = ', '.join([i for tup in data for i in tup])
            return data
    except Exception as e:
        print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))


# retrieve all available utensils
def get_all_utensils():
    try:
        curs = db.cursor()
        sql = "SELECT * FROM utensils"
        curs.execute(sql)
        data = curs.fetchall()
        if not data:
            print("Nope - get all utensils" + str(data))
            return "There are no utensils in the db. Please contact the administrator."
        else:
            newdata = []
            for i, (id, name, alt_name) in enumerate(data):
                newdata.append((str(id) + ". " + str(name) + ("" if not alt_name else (" / " + alt_name))))
            newdata = '\n\t\t'.join(newdata)
            return newdata

    except Exception as e:
        print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))


# retrieve user's utensils with user_id
def get_utensils_from_user(user_id):
    try:
        curs = db.cursor()
        sql = "SELECT uten_id FROM users_utensils WHERE user_id = {}".format(user_id)
        curs.execute(sql)
        data = curs.fetchall()
        return [x[0] for x in data]
    except Exception as e:
        print("An exception of type {0} occurred while retrieving utensils from user. Arguments:\n{1!r}".format(type(e).__name__, e.args))


# retrieve user's likes
def get_likes(chat_id):
    try:
        curs = db.cursor()
        sql = "SELECT (B.name) FROM users_likes A JOIN categories B ON A.cat_id = B.id JOIN users C ON A.user_id = C.id WHERE (C.user_id) = '" + str(chat_id) + "'"
        curs.execute(sql)
        data = curs.fetchall()
        if not data:
            print("Nope - likes" + str(data))
        else:
            data = ', '.join([i for tup in data for i in tup])
            return data
    except Exception as e:
        print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))


# retrieve user's dislikes with user_id
def get_dislikes(chat_id):
    try:
        curs = db.cursor()
        sql = "SELECT (B.name) FROM users_dislikes A JOIN categories B ON A.cat_id = B.id JOIN users C ON A.user_id = C.id WHERE (C.user_id) = '" + str(chat_id) + "'"
        curs.execute(sql)
        data = curs.fetchall()
        if not data:
            print("Nope - dislikes" + str(data))
        else:
            data = ', '.join([i for tup in data for i in tup])
            return data
    except Exception as e:
        print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))


# retrieve user's dislikes from user information
def get_dislikes_from_user(user_id):
    try:
        curs = db.cursor()
        sql = "SELECT cat_id FROM users_dislikes WHERE user_id = {}".format(user_id)
        curs.execute(sql)
        data = curs.fetchall()
        return [x[0] for x in data]
    except Exception as e:
        print("An exception of type {0} occurred while retrieving dislikes from user. Arguments:\n{1!r}".format(type(e).__name__, e.args))


# retrieve all categories
def get_all_categories():
    try:
        curs = db.cursor()
        sql = "SELECT * FROM categories ORDER BY id"
        curs.execute(sql)
        data = curs.fetchall()
        if not data:
            print("Nope - get all categories" + str(data))
            return "There are no categories in the db. Please contact the administrator."
        else:
            newdata = []
            for i, (id, name) in enumerate(data):
                newdata.append(str(id) + ". " + str(name))
            newdata = ', '.join(newdata)
            return newdata

    except Exception as e:
        print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))


# retrieve user's number of dishes rated
# def get_num_rated(chat_id):
#     try:
#         curs = db.cursor()
#         sql = "SELECT (num_rated) FROM users WHERE (user_id) = '" + str(chat_id) + "'"
#         curs.execute(sql)
#         data = curs.fetchone()
#         if data == None:
#             print("Nope - num rated")
#         return data[0]
#     except Exception as e:
#         print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))


# retrieve user's list of recipes uploaded
def get_recipes_uploaded(chat_id):
    try:
        curs = db.cursor()
        sql = "SELECT B.rec_name, B.rec_id FROM users_uploaded A JOIN recipes B ON A.rec_id = B.rec_id JOIN users C ON A.user_id = C.id WHERE (C.user_id) = '" + str(chat_id) + "'"
        curs.execute(sql)
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
        print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))


# retrieve user's favourites
def get_fav(chat_id):
    try:
        curs = db.cursor()
        sql = "SELECT B.rec_name, B.rec_id FROM users_fav A JOIN recipes B ON A.rec_id = B.rec_id JOIN users C ON A.user_id = C.id WHERE (C.user_id) = '" + str(chat_id) + "'"
        curs.execute(sql)
        data = curs.fetchall()
        if not data:
            print("Nope - favourites" + str(data))
        else:
            newdata = []
            for i, (name, id) in enumerate(data):
                newdata.append((str(id) + ". " + str(name)))
            newdata = '\n\t\t'.join(newdata)
            return newdata
    except Exception as e:
        print("An exception of type {0} occurred while retrieving favourites. Arguments:\n{1!r}".format(type(e).__name__, e.args))


# retrieve user's list of recipes liked
# def get_recipes_disliked(chat_id):
#     try:
#         curs = db.cursor()
#         sql = "SELECT B.rec_name, B.rec_id FROM users_disliked A JOIN recipes B ON A.rec_id = B.rec_id JOIN users C ON A.user_id = C.id WHERE (C.user_id) = '" + str(chat_id) + "'"
#         curs.execute(sql)
#         data = curs.fetchall()
#         if not data:
#             print("Nope - recipes disliked" + str(data))
#         else:
#             newdata = []
#             for i, (name, id) in enumerate(data):
#                 newdata.append((str(id) + ". " + str(name)))
#             newdata = '\n\t\t'.join(newdata)
#             return newdata
#     except Exception as e:
#         print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))


# update user's dietary status
def change_diet_status(chat_id, diet):
    try:
        curs = db.cursor()
        sql = "UPDATE users SET diet = '" + str(diet) + "' WHERE (user_id) = '" + str(chat_id) + "'"
        curs.execute(sql)
    except Exception as e:
        print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))


# get a recipe from the db with its id
def get_recipe_with_id(rid):
    try:
        curs = db.cursor()
        sql = "SELECT rec_name, instructions FROM recipes WHERE (recipes.rec_id) = '" + str(rid) + "'"
        curs.execute(sql)
        data = curs.fetchone()
        if not data:
            print("Nope - recipes with id" + str(data))
            return "There are no recipes with this id."
        else:
            return data[0] + "\n\n" + data[1]
    except Exception as e:
        print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))


# cache a dictionary of ingredients by name and id
def cache_ingredients():
    try:
        curs = db.cursor()
        sql = "SELECT ing_id, ing_name_1, ing_name_2, ing_name_3, ing_name_4, ing_name_5 FROM ingredients ORDER BY ing_name_1"
        curs.execute(sql)
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
        print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))


# add ingredients to user
def add_ingredients_to_user(chat_id, ingredlst):
    user_id = get_uid_with_chat_id(chat_id)
    for ingred in ingredlst:
        id = Cache.ingred_dict.get(ingred)
        if id is None:
            return "Please check your input. One or more ingredients are not recognized."
        print(id)
        try:
            curs = db.cursor()
            sql = "INSERT IGNORE INTO users_ingredients (user_id, ing_id) VALUES (" + str(user_id) + ", " + str(id) +")"
            curs.execute(sql)
            db.commit()
        except Exception as e:
            print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))
    return "Ingredients added: " + ', '.join(ingredlst)


# remove ingredients from user
def remove_ingredients_from_user(chat_id, ingredlst):
    user_id = get_uid_with_chat_id(chat_id)
    for ingred in ingredlst:
        id = Cache.ingred_dict.get(ingred)
        if id is None:
            return "Please check your input. One or more ingredients are not recognized."
        print(id)
        try:
            curs = db.cursor()
            sql = "DELETE FROM users_ingredients WHERE (user_id = " + str(user_id) + ") AND (ing_id = " + str(id) + ")"
            curs.execute(sql)
            db.commit()
        except Exception as e:
            print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))
    return "Ingredients removed: " + ', '.join(ingredlst)


# add utensils to user
def add_utensils_to_user(chat_id, utenlst):
    user_id = get_uid_with_chat_id(chat_id)
    for uten in utenlst:
        try:
            curs = db.cursor()
            sql = "INSERT IGNORE INTO users_utensils (user_id, uten_id) VALUES (" + str(user_id) + ", " + str(uten) +")"
            curs.execute(sql)
            db.commit()
        except Exception as e:
            print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))
    return "Utensils added: " + ', '.join(utenlst)


# remove utensils from user
def remove_utensils_from_user(chat_id, utenlst):
    user_id = get_uid_with_chat_id(chat_id)
    for uten in utenlst:
        try:
            curs = db.cursor()
            sql = "DELETE FROM users_utensils WHERE (user_id = " + str(user_id) + ") AND (uten_id = " + str(uten) + ")"
            curs.execute(sql)
            db.commit()
        except Exception as e:
            print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))
    return "Utensils removed: " + ', '.join(utenlst)


# add likes to user
def add_likes_to_user(chat_id, likeslst):
    user_id = get_uid_with_chat_id(chat_id)
    for like in likeslst:
        try:
            curs = db.cursor()
            sql = "INSERT IGNORE INTO users_likes (user_id, cat_id) VALUES (" + str(user_id) + ", " + str(like) +")"
            curs.execute(sql)
            db.commit()
        except Exception as e:
            print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))
    return "Likes added: " + ', '.join(likeslst)


# remove likes from user
def remove_likes_from_user(chat_id, likeslst):
    user_id = get_uid_with_chat_id(chat_id)
    for like in likeslst:
        try:
            curs = db.cursor()
            sql = "DELETE FROM users_likes WHERE (user_id = " + str(user_id) + ") AND (cat_id = " + str(like) + ")"
            curs.execute(sql)
            db.commit()
        except Exception as e:
            print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))
    return "Likes removed: " + ', '.join(likeslst)


# add dislikes to user
def add_dislikes_to_user(chat_id, dislikeslst):
    user_id = get_uid_with_chat_id(chat_id)
    for dislike in dislikeslst:
        try:
            curs = db.cursor()
            sql = "INSERT IGNORE INTO users_dislikes (user_id, cat_id) VALUES (" + str(user_id) + ", " + str(dislike) +")"
            curs.execute(sql)
            db.commit()
        except Exception as e:
            print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))
    return "Dislikes added: " + ', '.join(dislikeslst)


# remove dislikes from user
def remove_dislikes_from_user(chat_id, dislikeslst):
    user_id = get_uid_with_chat_id(chat_id)
    for dislike in dislikeslst:
        try:
            curs = db.cursor()
            sql = "DELETE FROM users_dislikes WHERE (user_id = " + str(user_id) + ") AND (cat_id = " + str(dislike) + ")"
            curs.execute(sql)
            db.commit()
        except Exception as e:
            print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))
    return "Dislikes removed: " + ', '.join(dislikeslst)


# add the recipe to the user's liked list
def add_to_fav(call):
    user_id = get_uid_with_chat_id(call.from_user.id)
    try:
        selected_recipe = Cache.rec_tup_dict[user_id]
        curs = db.cursor()
        # check if the recipe is already in disliked list
        sql_check = """SELECT EXISTS
            (SELECT
                *
            FROM
                users_fav
            WHERE user_id = {}
                AND rec_id = {})""".format(user_id, selected_recipe[0])
        curs.execute(sql_check)
        duplicate = curs.fetchall()
        if duplicate[0][0] == 1:
            return '\U0001F645 You have already added "{}" to your favourites.'.format(str(selected_recipe[1]))
        else:
            sql_fav = "INSERT IGNORE INTO users_fav (user_id, rec_id) VALUES ({}, {})".format(str(user_id), str(selected_recipe[0]))
            curs.execute(sql_fav)
            db.commit()
            return '\U0001F44D You have successfully added "{}" to your favourites!'.format(str(selected_recipe[1]))
    except Exception as e:
        print("An exception of type {0} occurred while adding recipe to favourites. Arguments:\n{1!r}".format(type(e).__name__, e.args))


# add a new recipe
def upload_recipe(strlst):
    try:
        curs = db.cursor()
        sql = "INSERT IGNORE INTO recipes (`rec_name`, `category`, `diet`, `instructions`, `pending_approval`) VALUES ('{0}',{1},{2},'{3}',1)".format(str(strlst[0]), str(strlst[1]), str(strlst[2]), str(strlst[6]))
        curs.execute(sql)
        db.commit()

        # get recipe id of the above
        curs2 = db.cursor()
        sql2 = "SELECT LAST_INSERT_ID()"
        curs2.execute(sql2)
        data = curs2.fetchone()
        rec_id = data[0]
        print(rec_id)

        # upload utensils
        text = str(strlst[3]).replace(" ", "")
        utenlst = text.split(',')
        for uten in utenlst:
            try:
                curs = db.cursor()
                sql = "INSERT IGNORE INTO recipes_utensils (rec_id, uten_id) VALUES (" + str(rec_id) + ", " + str(uten) +")"
                curs.execute(sql)
                db.commit()
            except Exception as e:
                print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))

        # upload main ingredients
        mainlst = strlst[4].split(',')
        for main in mainlst:
            try:
                id = Cache.ingred_dict.get(main.lower())
                curs = db.cursor()
                sql = "INSERT IGNORE INTO recipes_main (rec_id, ing_id) VALUES (" + str(rec_id) + ", " + str(id) +")"
                curs.execute(sql)
                db.commit()
            except Exception as e:
                print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))

        # upload sub ingredients
        sublst = strlst[5].split(',')
        for sub in sublst:
            try:
                id = Cache.ingred_dict.get(sub.lower())
                curs = db.cursor()
                sql = "INSERT IGNORE INTO recipes_sub (rec_id, ing_id) VALUES (" + str(rec_id) + ", " + str(id) +")"
                curs.execute(sql)
                db.commit()
            except Exception as e:
                print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))

        return "Recipe uploaded. It may take a few days for the admin to approve the recipe."

    except Exception as e:
        print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))
        return "An error occurred. Please check your input and try again."


# get user db uid from chat_id
def get_uid_with_chat_id(chat_id):
    curs = db.cursor()
    sql = "SELECT id FROM users WHERE user_id = {}".format(chat_id)
    curs.execute(sql)
    return curs.fetchone()[0]


# convert query results(list of tuples) to a string
def query_result_to_str(list):
    flat_list = [str(x[0]) for x in list]
    return ','.join(map(str, flat_list))


# close db connection
def close_db():
    db.close()
