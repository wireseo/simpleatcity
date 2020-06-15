import telebot
import inspect
from enums import Diet
from classes import User
import dbhelper

bot = telebot.TeleBot("1117988587:AAERFRl23gsQ6rOqcyeO4nSWpPWGdz_1Bh0")

user_list = []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.reply_to(message, 'Welcome to Simpleatcity!\n\n' + inspect.cleandoc(
        """
        Before I can start recommending simple dishes for you,
        if you want better-tailored dishes, please head on to
        /myinfo to start your initial setup. If you want to
        get a recipe right away that can be made from several
        main ingredients that you have, head on to /quickrecipe.
        For a better overview of the functionalities that this
        bot provides, use /help.""").replace('\n', ' '))
    # getMe -- hmm where is this needed
    #user_list.append(User())
    #user = tb.get_me()

    try:
        chat_id = message.chat.id
        user = User(chat_id)

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

        You can control me by sending these commands:

        *Set Up
        /start - set up user information
        /help - display a detailed manual

        *Recipes
        /recipe - suggest recipe based on current user information
        /quickrecipe - suggest recipe based on user input
        /upload - upload new recipes

        *User Information
        /myinfo - display overall summary of user information and access uploaded / liked recipes
        /diet - maintain current dietary status
        /ingredients - maintain currently available ingredients
        /utensils - maintain currently available utensils
        /preferences - maintain current culinary preferences

        *Miscellaneous
        /acceptedingredients - display list of acceptable ingredients"""))

# User prompted to enter basic information
@bot.message_handler(commands=['myinfo'])
def send_myinfo(message):
    chat_id = message.chat.id

    try:
        #chat_id = message.chat.id
        diet = dbhelper.get_diet(chat_id)

        if diet == 0:
            diet = "Vegetarian"
        elif diet == 1:
            diet = "Vegan"
        elif diet == 2: # TODO change these to enums
            diet = "Non-vegetarian"

        items = dbhelper.get_ingredients(chat_id)
        utensils = dbhelper.get_utensils(chat_id)
        likes = dbhelper.get_likes(chat_id)
        dislikes = dbhelper.get_dislikes(chat_id)
        num_rated = dbhelper.get_num_rated(chat_id)
        uploaded = dbhelper.get_recipes_uploaded(chat_id)
        liked = dbhelper.get_recipes_liked(chat_id)

        msg = bot.reply_to(message,
            "Dietary Preference: {}\n".format(diet) +
            "Items in Fridge: {}\n".format(items) +
            "Utensils: {}\n".format(utensils) +
            "Likes: {}\n".format(likes) +
            "Dislikes: {}\n".format(dislikes) +
            "# of Recipes Rated: {}\n".format(num_rated) +
            "Recipes Uploaded: {}\n".format(uploaded) +
            "Recipes Liked: {}\n".format(liked)
            )

        #bot.register_next_step_handler(msg, access_recipes)

    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)

def access_recipes(msg):
    if msg[0] == "u":
        recipes_uploaded = dbhelper.get_recipes_uploaded() # How to pass this from previous step?
    elif msg[0] == "l":
        recipes_liked = dbhelper.get_recipes_liked() # How to pass this from previous step?
    else:
        warning = bot.reply_to(msg, "Please check your input.")

# User prompted to manually enter available ingredients
@bot.message_handler(commands=['quickrecipe'])
def ask_ingredients(message):
    ingredients = bot.reply_to(message, inspect.cleandoc("""
        Please enter the available ingredients.

        Use singular form for ingredients and seperate with commas.
        ex) tomato, egg"""))
    bot.register_next_step_handler(ingredients, send_quickrecipe)

# Suggest recipe to the users
def send_quickrecipe(ingredients):
    recipe = dbhelper.get_quickrecipe(ingredients.text)
    bot.reply_to(ingredients, recipe)

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

#commented out due to InterfaceError
#dbhelper.close_db()


bot.polling()

#cool
