import main
import telebot
import requests
from datetime import date
TOKEN = '5608886795:AAFmBrGjxaNvnWl9HsrLPyDyqzxt7V2XWpo'
URL = 'https://api.telegram.org/bot'
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    if message.text == 'файл':
        main.equal_len_and_output()
        bot.send_document(chat_id=message.chat.id, document=open(f'D:/arm_parser_out/output{date.today()}.xlsx', 'rb'))



bot.polling(none_stop=True, interval=0)