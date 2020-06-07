import telebot
import inspect
from enums import Diet
from classes import User
import dbhelper

TOKEN = "1117988587:AAERFRl23gsQ6rOqcyeO4nSWpPWGdz_1Bh0"

bot = telebot.TeleBot(TOKEN)


# User prompted to enter basic information
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

        *Misc.
        /acceptedingredients - display list of acceptable ingredients"""))

# User prompted to enter basic information
@bot.message_handler(commands=['myinfo'])
def send_welcome(message):
    try:
        chat_id = message.chat.id
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

    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

#dbhelper.close_db()

bot.polling()
