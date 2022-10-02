import main
import telebot
from telebot import types
from datetime import date
import os.path
TOKEN = '5608886795:AAFmBrGjxaNvnWl9HsrLPyDyqzxt7V2XWpo'
URL = 'https://api.telegram.org/bot'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    user = f'Здравствуйте, {message.from_user.first_name}, чем я могу помочь?'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    all_prices = types.KeyboardButton('Прислать все цены')
    our_prices = types.KeyboardButton('Прислать наши цены')
    markup.add(all_prices, our_prices)
    bot.send_message(chat_id=message.chat.id, text=user, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    if message.text == 'Прислать все цены':
        prices_file = f'D:/arm_parser_out/output{date.today()}.xlsx'
        if not os.path.exists(prices_file):
            main.equal_len_and_output()
        else:
            bot.send_document(chat_id=message.chat.id, document=open(prices_file, 'rb'))
    elif message.text == 'Прислать наши цены':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        retail = types.KeyboardButton('Розница')
        wholesale = types.KeyboardButton('Опт')
        back = types.KeyboardButton('В главное меню')
        markup.add(wholesale, retail, back)
        bot.send_message(message.from_user.id, 'Вас интересуют оптовые или розничные цены?', reply_markup=markup)
    elif message.text == 'Розница':
        bot.send_message(message.from_user.id, text=main.armplast('retail'))
    elif message.text == 'Опт':
        bot.send_message(message.from_user.id, text=main.armplast('wholesale'))
    elif message.text == 'В главное меню':
        markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        all_prices = types.KeyboardButton('Прислать все цены')
        our_prices = types.KeyboardButton('Прислать наши цены')
        markup_menu.add(all_prices, our_prices)
        menu_message = f'{message.from_user.first_name}, чем я могу помочь?'
        bot.send_message(message.from_user.id, menu_message, reply_markup=markup_menu)


@bot.message_handler(commands=['file'])
def file(message):
    main.equal_len_and_output()
    bot.send_document(chat_id=message.chat.id, document=open(f'D:/arm_parser_out/output{date.today()}.xlsx', 'rb'))


bot.polling(none_stop=True, interval=0)
