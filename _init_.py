import telebot
import inspect

TOKEN = "1117988587:AAERFRl23gsQ6rOqcyeO4nSWpPWGdz_1Bh0"

bot = telebot.TeleBot(TOKEN)

# User prompted to enter basic information
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Welcome to Simpleatcity!\n\n' + inspect.cleandoc(
        """
        Before I can start recommending simple dishes for you,
        if you want better-tailored dishes, please head on to
        /fridge and /utensils to fill out the current state of
        your kitchen and then prompt /recipe. If you want to
        get a recipe right away that can be made from several
        main ingredients that you have, head on to /quickrecipe.
        For a better overview of the functionalities that this
        bot provides, use /help.""").replace('\n', ' '))

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
        /myinfo - display overall summary of user information
        /acceptedingredients - display list of acceptable ingredients
        /ingredients - maintain current available ingredients
        /utensils - maintain current available utensils
        /preferences - maintain current dietary preferences"""))

bot.polling()
