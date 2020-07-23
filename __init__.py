import os
from flask import Flask, request
import telebot
from telebot import types
import inspect
from enums import Diet
from cache import Cache
import dbhelper
import random

TOKEN = '1117988587:AAERFRl23gsQ6rOqcyeO4nSWpPWGdz_1Bh0'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
dbhelper.cache_ingredients()
strlst = []
# print(Cache.ingred_dict)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.reply_to(message, 'Welcome to Simpleatcity!\n\n' + inspect.cleandoc(
        """
        Before I can start recommending simple dishes for you,
        if you want better-tailored dishes, please head on to
        /myinfo to start your initial setup. If you want to.
        get a recipe right away that can be made from several
        main ingredients that you have, head on to /quickrecipe.
        For a more detailed overview of the functionalities that this
        bot provides, use /help.""").replace('\n', ' '))

    try:
        chat_id = message.chat.id

        # if user does not exist in db, insert new User
        is_new_user = dbhelper.add_user(chat_id)
        if is_new_user is False:
            bot.reply_to(message, "You already have an account with us! Access /help for further instructions.")

    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)


# User guided on how to use the bot
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, inspect.cleandoc("""
        Welcome to Simpleatcity!

        You can control me with the following commands:

        \U0001F511 Set Up
        /start - set up user information
        /help - display a detailed manual

        \U0001F374 Recipes
        /recipe - suggest recipe based on current user information
        /quickrecipe - suggest recipe based on user input
        /upload - upload new recipes

        \U00002139 User Information
        /myinfo - display overall summary of user information
        /diet - maintain current dietary status
        /ingredients - maintain currently available ingredients
        /utensils - maintain currently available utensils
        /preferences - maintain current culinary preferences

        \U0001F4DC Miscellaneous
        /acceptedingredients - display list of acceptable ingredients"""))


# Handles the case where only recipe id is entered
@bot.message_handler(regexp="^0*[1-9]\d*$")
def send_rec_by_rec_id(message):
    bot.reply_to(message, dbhelper.get_recipe_with_id(message.text))


# Handles the case where diet is to be changed
@bot.message_handler(regexp="veg|vegan|nonveg")
def change_to_veg(message):
    chat_id = message.chat.id
    diet = -1

    if message.text.lower() == "veg":
        diet = 0
    elif message.text.lower() == "vegan":
        diet = 1
    elif message.text.lower() == "nonveg":
        diet = 2
    else:
        bot.reply_to(message, "Please check your input.")

    if diet != -1:
        dbhelper.change_diet_status(chat_id, diet)
        bot.reply_to(message, "Dietary status updated to " + message.text + ".")


# Handles the case where something is added
@bot.message_handler(regexp="\+")
def determine_type(message):
    if len(message.text) <= 2:
        bot.reply_to(message, "Please check your input.")
    elif message.text[1].lower() == "l":
        add_likes(message)
    elif message.text[1].lower() == "d":
        add_dislikes(message)
    elif message.text[2].isdigit():
        add_utensils(message)
    else:
        add_ingredients(message)

def add_likes(message):
    chat_id = message.chat.id
    text = message.text.lower()
    if len(text) <= 3:
        bot.reply_to(message, "Please check your input.")
    else:
        likeslst = text[3:].split(",")
        dbhelper.add_likes_to_user(chat_id, likeslst)
        bot.reply_to(message, "Likes added.")

def add_dislikes(message):
    chat_id = message.chat.id
    text = message.text.lower()
    if len(text) <= 3:
        bot.reply_to(message, "Please check your input.")
    else:
        dislikeslst = text[3:].split(",")
        dbhelper.add_dislikes_to_user(chat_id, dislikeslst)
        bot.reply_to(message, "Dislikes added.")

def add_utensils(message):
    chat_id = message.chat.id
    text = message.text.lower()
    utenlst = text[2:].split(",")
    dbhelper.add_utensils_to_user(chat_id, utenlst)
    bot.reply_to(message, "Utensils added.")

def add_ingredients(message):
    chat_id = message.chat.id
    text = message.text.lower()
    ingredlst = text[2:].split(",")
    str = dbhelper.add_ingredients_to_user(chat_id, ingredlst)
    bot.reply_to(message, str)


# Handles the case where something is removed
@bot.message_handler(regexp="\-")
def determine_type(message):
    if len(message.text) <= 2:
        bot.reply_to(message, "Please check your input.")
    elif message.text[1].lower() == "l":
        remove_likes(message)
    elif message.text[1].lower() == "d":
        remove_dislikes(message)
    elif message.text[2].isdigit():
        remove_utensils(message)
    else:
        remove_ingredients(message)

def remove_likes(message):
    chat_id = message.chat.id
    text = message.text.lower()
    if len(text) <= 3:
        bot.reply_to(message, "Please check your input.")
    else:
        likeslst = text[3:].split(",")
        dbhelper.remove_likes_from_user(chat_id, likeslst)
        bot.reply_to(message, "Likes removed.")

def remove_dislikes(message):
    chat_id = message.chat.id
    text = message.text.lower()
    if len(text) <= 3:
        bot.reply_to(message, "Please check your input.")
    else:
        dislikeslst = text[3:].split(",")
        dbhelper.remove_dislikes_from_user(chat_id, dislikeslst)
        bot.reply_to(message, "Dislikes removed.")

def remove_utensils(message):
    chat_id = message.chat.id
    text = message.text.lower()
    utenlst = text[2:].split(",")
    dbhelper.remove_utensils_from_user(chat_id, utenlst)
    bot.reply_to(message, "Utensils removed.")

def remove_ingredients(message):
    chat_id = message.chat.id
    text = message.text.lower()
    ingredlst = text[2:].split(",")
    str = dbhelper.remove_ingredients_from_user(chat_id, ingredlst)
    bot.reply_to(message, str)


# User prompted to enter & view basic information
@bot.message_handler(commands=['myinfo'])
def send_myinfo(message):
    chat_id = message.chat.id

    try:
        diet = dbhelper.get_diet(chat_id)
        items = dbhelper.get_ingredients(chat_id)
        utensils = dbhelper.get_utensils(chat_id)
        likes = dbhelper.get_likes(chat_id)
        dislikes = dbhelper.get_dislikes(chat_id)
        uploaded = dbhelper.get_recipes_uploaded(chat_id)
        fav = dbhelper.get_recipes_liked(chat_id)

        msg = bot.reply_to(message,
            "*Dietary Preference:* \n{}\n\n".format(diet) +
            "*Items in Fridge:* \n{}\n\n".format(items) +
            "*Utensils:* \n{}\n\n".format(utensils) +
            "*Likes:* \n{}\n\n".format(likes) +
            "*Dislikes:* \n{}\n\n".format(dislikes) +
            "*Favourites:* \n\t\t{}\n\n".format(liked) +
            "*Recipes Uploaded:* \n\t\t{}\n\n".format(uploaded) +
            "\nTo access the recipes above, type in the recipe id (i.e. number" +
            " displayed before recipe name). You can only prompt for one recipe at a time.\n" +
            "\nTo maintain ingredients, go to /ingredients. To maintain" +
            " utensils, go to /utensils. To adjust preferences, go to /preferences. To change dietary status, go to /diet."
            , parse_mode='Markdown')

    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)


# User can change dietary status
@bot.message_handler(commands=['diet'])
def send_accepted_ingredients(message):
    chat_id = message.chat.id
    diet = dbhelper.get_diet(chat_id)
    msg = bot.reply_to(message, "*Dietary Preference:* \n{}\n\n".format(diet) +
    "Dietary status can be changed by typing 'veg' (dairy dishes recommended)" +
    ", 'vegan' (dairy dishes not recommended), or 'nonveg'.\n", parse_mode='Markdown')


# User can view all accepted ingredients
@bot.message_handler(commands=['acceptedingredients'])
def send_accepted_ingredients(message):
    msg = bot.reply_to(message, Cache.ingred_string)


# User can view and update ingredients
@bot.message_handler(commands=['ingredients'])
def send_ingredients(message):
    chat_id = message.chat.id
    items = dbhelper.get_ingredients(chat_id)

    msg = bot.reply_to(message, "*Items in Fridge:* \n{}\n\n".format(items) +
    "To add ingredients, type in a list of ingredients with a '+' in front of it." +
    " Make sure that each is separated with a comma and are in singular form" +
    " without spaces in between (e.g. + avocado,soymilk,lettuce).\n\n" +
    "To remove existing ingredients, type in a list of ingredients with a '-' in front of it.\n\n" +
    "If the bot does not recognize your input, try inputting a more general version of it" +
    " (ex. portobello to mushroom) or try searching for it in /acceptedingredients.\n\n" +
    "Do not attempt to remove and add at the same time.", parse_mode='Markdown')


# User can view and update utensils
@bot.message_handler(commands=['utensils'])
def send_utensils(message):
    chat_id = message.chat.id
    utensils = dbhelper.get_utensils(chat_id)
    all_utensils = dbhelper.get_all_utensils()

    msg = bot.reply_to(message, "*Utensils in Kitchen:* \n{}\n\n".format(utensils) +
    "*Available Utensils:* \n\t\t{}\n\n".format(all_utensils) +
    "To add utensils, type in a list of utensil ids with a '+' in front of it." +
    " Make sure that each is separated with a comma without spaces in between (e.g. + 1,2,3).\n\n" +
    "To remove existing utensils, type in a list of utensil ids with a '-' in front of it.\n\n" +
    "Do not attempt to remove and add at the same time.", parse_mode='Markdown')


# User can view and update preferences
@bot.message_handler(commands=['preferences'])
def send_preferences(message):
    chat_id = message.chat.id
    likes = dbhelper.get_likes(chat_id)
    dislikes = dbhelper.get_dislikes(chat_id)
    all_cats = dbhelper.get_all_categories()

    msg = bot.reply_to(message, "*Likes:* {}\n\n".format(likes) + "*Dislikes:* {}\n\n".format(dislikes) +
    "*All Categories:* \n{}\n\n".format(all_cats) +
    "To like categories, type in a list of category ids with a '+L' in front of it." +
    " Make sure that each is separated with a comma without spaces in between (e.g. +L 1,2). " +
    "To un-like categories, type in a list of category ids with a '-L' in front of it.\n\n" +
    "To dislike categories, the keyword is '+D'. To un-dislike, the keyword is '-D'."
    "\n\nDo not attempt to remove and add at the same time.", parse_mode='Markdown')


# user can upload their own recipes
@bot.message_handler(commands=['upload'])
def ask_recipe_name(message):
    print(strlst)
    rec_name = bot.reply_to(message, inspect.cleandoc("""
        Please enter the name of the recipe."""))
    bot.register_next_step_handler(rec_name, ask_recipe_cat)

def ask_recipe_cat(message):
    print(strlst)
    if len(strlst) == 0:
        strlst.append(message.text) # recipe name [0]
    all_cats = dbhelper.get_all_categories()
    cat = bot.reply_to(message, "Please enter the index of the category this recipe belongs to.\n\nAll Categories: \n{}".format(all_cats))
    bot.register_next_step_handler(cat, ask_recipe_diet)

def ask_recipe_diet(message):
    print(strlst)
    if not message.text.isdigit():
        bot.reply_to(message, "Please check your input and retry.")
        ask_recipe_cat(message)
    else:
        if len(strlst) == 1:
            strlst.append(message.text) # category index [1]
        diet = bot.reply_to(message, inspect.cleandoc("""
            Please enter the index of the dietary restriction of the recipe.\n\n   0. Vegetarian\n   1. Vegan\n   2. Non-vegetarian"""))
        bot.register_next_step_handler(diet, ask_uten)

def ask_uten(message):
    print(strlst)
    if message.text.isdigit() and (int(message.text) == 0 or int(message.text) == 1 or int(message.text) == 2):
        if len(strlst) == 2:
            strlst.append(message.text) # diet index [2]
        all_utensils = dbhelper.get_all_utensils()
        uten = bot.reply_to(message, "Please enter any necessary utensils for the recipe.\n\n*Available Utensils:* \n\t\t{}\n\nMake sure that each is separated with a comma without spaces in between (e.g. 1,2).".format(all_utensils))
        bot.register_next_step_handler(uten, ask_main_ing)
    else:
        bot.reply_to(message, "Please check your input and retry.")
        ask_recipe_diet(message)

def ask_main_ing(message):
    print(strlst)
    if len(strlst) == 3:
        strlst.append(message.text) # "list" of uten index [3]
    main_ing = bot.reply_to(message, inspect.cleandoc("""
        Please enter the main ingredients of the recipe. They should be absolutely
integral to the recipe (i.e. recipe cannot be attempted without them).\n
Make sure that each is separated with a comma and are in singular form
without spaces in between (e.g. avocado,soymilk,lettuce).\n
If the bot does not recognize your input, try inputting a more general version of it (ex. portobello to mushroom) or try searching for it in /acceptedingredients."""))
    bot.register_next_step_handler(main_ing, ask_sub_ing)

def ask_sub_ing(message):
    print(strlst)
    text = message.text.lower()
    ingredlst = text[0:].split(",")
    contin = True
    for ingred in ingredlst:
        id = Cache.ingred_dict.get(ingred)
        if id == None:
            bot.reply_to(message, "Please check your input and retry. One or more ingredients are not recognized.")
            contin = False
            break
    if not contin:
        ask_main_ing(message)
    else:
        if len(strlst) == 4:
            strlst.append(message.text) # "list" of main ing names [4]
        sub_ing = bot.reply_to(message, inspect.cleandoc("""
            Please enter the sub ingredients of the recipe. They should be ingredients
that are not strictly necessary to the recipe (i.e. recipe still can be attempted without them).\n
Make sure that each is separated with a comma and are in singular form without spaces in between (e.g. avocado,soymilk,lettuce).\n
If the bot does not recognize your input, try inputting a more general version of it (ex. portobello to mushroom) or try searching for it in /acceptedingredients."""))
        bot.register_next_step_handler(sub_ing, ask_instructions)

def ask_instructions(message):
    print(strlst)
    text = message.text.lower()
    ingredlst = text[0:].split(",")
    contin = True
    for ingred in ingredlst:
        id = Cache.ingred_dict.get(ingred)
        if id == None:
            strlst.clear()
            bot.reply_to(message, "Please check your input and retry. One or more ingredients are not recognized.")
            contin = False
            break
    if not contin:
        ask_sub_ing(message)
    else:
        if len(strlst) == 5:
            strlst.append(message.text) # "list" of sub ing names [5]
        instructions = bot.reply_to(message, inspect.cleandoc("""
            Please enter instructions for the recipe. You can either paste a link
to the recipe or type it out in a list format. For the latter, make
sure you number the steps and outline the process as clearly as possible."""))
        bot.register_next_step_handler(instructions, upload_recipe)

def upload_recipe(message):
    print(strlst)
    strlst.append(message.text) # link or recipe instructions [6]
    print(strlst)
    bot.reply_to(message, "Please wait until the recipe is uploaded.")
    str = dbhelper.upload_recipe(strlst)
    bot.reply_to(message, str)


# user prompted to manually enter available ingredients
@bot.message_handler(commands=['quickrecipe'])
def ask_ingredients(message):
    ingredients = bot.reply_to(message, inspect.cleandoc("""
        Please enter the available ingredients.

        Use singular form for ingredients and seperate different ingredients with commas.
        ex) avocado, bacon, cauliflower"""))
    bot.register_next_step_handler(ingredients, send_quickrecipe)


# suggest recipe based on given ingredients
def send_quickrecipe(ingredients):
    user_id = dbhelper.get_uid_with_chat_id(ingredients.chat.id)
    recipe = dbhelper.get_quickrecipes(ingredients.text)
    if recipe == 'norec':
        bot.reply_to(ingredients, '\U0001F645 No recipe found')
    elif recipe == 'error':
        bot.reply_to(ingredients, '\U0001F937 Sorry, an unexpected error has occured.\nPlease try again.')
    else:
        # set the global variable to store list of recipe
        Cache.rec_list_dict[user_id] = recipe
        gen_recipe(ingredients, recipe)


# user given recipe based on user information
@bot.message_handler(commands=['recipe'])
def send_recipe(message):
    user_id = dbhelper.get_uid_with_chat_id(message.chat.id)
    recipe = dbhelper.get_recipes(user_id)
    #
    if recipe == 'norec':
        bot.reply_to(message, '\U0001F645 No recipe found.')
    elif recipe == 'norec_ing':
        bot.reply_to(message, '\U0001F645 No recipe found.\nPlease add more ingredients.')
    elif recipe == 'norec_ute':
        bot.reply_to(message, '\U0001F645 No recipe found.\nPlease add more utensils.')
    elif recipe == 'error':
        bot.reply_to(message, '\U0001F937 Sorry, an unexpected error has occured.\nPlease try again.')
    else:
        # set the global variable to store list of recipe
        Cache.rec_list_dict[user_id] = recipe
        gen_recipe(message, recipe)


# process response from user 1) like 2) dislike 3) another
def process_callback(cb):
    user_id = dbhelper.get_uid_with_chat_id(cb.chat.id)
    if cb.text == u'\U00002764 Add to favourites':
        # function to add recipe to favourites
        return bot.reply_to(cb, dbhelper.add_to_fav(cb))
    elif cb.text == u'\U0001F500 Show another recipe':
        return gen_recipe(cb, Cache.rec_list_dict[user_id])
    elif cb.text == u'\U0000274C Cancel':
         return
    else:
        # default
        return


# show another recipe to the user
def gen_recipe(message, recipe_list):
    user_id = dbhelper.get_uid_with_chat_id(message.chat.id)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    itembtn_like = types.KeyboardButton('\U00002764 Add to favourites')
    itembtn_another = types.KeyboardButton('\U0001F500 Show another recipe')
    itembtn_cancel = types.KeyboardButton('\U0000274C Cancel')
    markup.row(itembtn_like, itembtn_another)
    markup.row(itembtn_cancel)
    rand_idx = get_random_index(recipe_list)
    Cache.rec_list_dict[user_id] = recipe_list
    Cache.rec_tup_dict[user_id] = recipe_list[rand_idx]
    rand_rec = get_random_recipe_str(recipe_list, rand_idx)
    callback = bot.reply_to(message, rand_rec, reply_markup=markup)
    bot.register_next_step_handler(callback, process_callback)


# retrieve random element from input list
def get_random_index(input):
    return random.randint(0, len(input) - 1)


def get_random_recipe_str(input, idx):
    return 'Would you like to try "{}"?\n{}'.format(str(input[idx][1]).lower(), str(input[idx][4]))


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
# bot.polling()

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://simpleatcity-bot.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
