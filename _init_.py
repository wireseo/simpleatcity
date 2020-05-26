import telebot

bot = telebot.TeleBot("1117988587:AAERFRl23gsQ6rOqcyeO4nSWpPWGdz_1Bh0")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """Welcome to Simpleatcity!

    Before I can start recommending simple dishes for you,
    if you want better-tailored dishes, please head on to
    /fridge and /utensils to fill out the current state of
    your kitchen and then prompt /recipe. If you want to
    get a recipe right away that can be made from several
    main ingredients that you have, head on to /quickrecipe.
    For a better overview of the functionalities that this
    bot provides, use /help.""")
bot.polling()

#cool
