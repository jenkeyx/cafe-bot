import shutil
import tempfile
from urllib import request
import ssl

import telebot
from telebot import types
from menu_api import get_categories, get_products_by_category, create_order, get_order_by_chat_id

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

TOKEN = "5091875742:AAGTnoYdTVf0J5LK57TrUTiSk1WV1NMxG5k"
S3_BUCKET_URL = "https://cafe-bot-product-images.s3.eu-north-1.amazonaws.com/"
INVOKE_URL = "https://h366s2k3l2.execute-api.eu-north-1.amazonaws.com/v0/bot_handler5091875742:AAGTnoYdTVf0J5LK57TrUTiSk1WV1NMxG5k"

bot = telebot.TeleBot(TOKEN)

base_labels = ["Menu", "Promos", "Order status"]

bot.set_webhook(INVOKE_URL)


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
        # receiving photo from AWS S3 bucket and store data in temporary file
        response = request.urlopen(S3_BUCKET_URL + product.image_uri, context=ctx)
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        shutil.copyfileobj(response, tmp_file)

        # adding a button to make an order
        inline_markup = types.InlineKeyboardMarkup(row_width=1)
        order_button = types.InlineKeyboardButton(text='купить', callback_data=product.name)
        inline_markup.add(order_button)

        bot.send_photo(chat_id, open(tmp_file.name, "rb"))
        bot.send_message(chat_id, f"{product.name} – {product.price}₽", reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda callback: callback.data)
def handle_order(call):
    create_order(call.message.chat.id)
    order_number = get_order_by_chat_id(call.message.chat.id)
    bot.send_message(call.message.chat.id, f"ваш заказ №{order_number}")


