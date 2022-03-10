import telebot
from telebot import types
from menu_api import get_categories, get_products_by_category

token = "5091875742:AAGTnoYdTVf0J5LK57TrUTiSk1WV1NMxG5k"
bot = telebot.TeleBot(token)

base_labels = ["Menu", "Promos", "Order status"]


@bot.message_handler(commands=['start'])
def say_hello(message):
    bot.send_message(message.from_user.id, text="Hello, I'm a cafe bot. Run /help for help")


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.from_user.id, text="Здесь пока немного пустовато)")


@bot.message_handler(commands=['menu'])
def show_menu(message):
    send_keyboard(message.from_user.id, get_categories(), text="Что желаете посмотреть?")


def send_keyboard(chat_id, button_labels, text="What can I help for you?"):
    keyboard = types.ReplyKeyboardMarkup()

    for label in button_labels:
        button = types.KeyboardButton(label)
        keyboard.add(button)

    msg = bot.send_message(chat_id, text=text, reply_markup=keyboard)

    bot.register_next_step_handler(msg, assortment_handler)


def assortment_handler(call):
    products = get_products_by_category(call.text)
    send_products(products, call.chat.id)
    send_keyboard(call.chat.id, get_categories(), text='Что-нибудь еще желаете посмотреть?')


def send_products(products, chat_id):
    for product in products:
        bot.send_message(chat_id, f"{product.name} – {product.price}₽")


bot.polling()