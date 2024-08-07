import os
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
import requests
import logging
import time
import datetime
import json 
load_dotenv()

# logging.basicConfig(leve=logging.INFO)
# logger = logging.getLogger(__name__)


API = os.getenv('BOT_TOKEN')
LIVE_CHAT = os.getenv('LIVE_CHAT')
MINI_APP = os.getenv('MINI_APP')
HOSPITAL = os.getenv('HOSPITAL')
WELCOME_MSG = os.getenv('WELCOME_MESSAGE')
bot = telebot.TeleBot(API)

user_states = {}

def is_user_busy(chat_id, make_busy=False):
    """Check if the user is busy with an ongoing operation. 
    If make_busy is True, set the user's state to busy."""
    if chat_id in user_states:
        if user_states[chat_id] == 'busy':
            return True
        if make_busy:
            user_states[chat_id] = 'busy'
            return False
    else:
        if make_busy:
            user_states[chat_id] = 'busy'
        return False

def free_user(chat_id):
    """Set the user's state to free."""
    user_states[chat_id] = 'free'


def create_main_keyboard(chat_id):
    keyboard = InlineKeyboardMarkup()
   
    live_chat_button = InlineKeyboardButton('💬 Live Chat',LIVE_CHAT)
    mini_app_button = InlineKeyboardButton(f'📱 {HOSPITAL}',MINI_APP)
    keyboard.add(live_chat_button)
    keyboard.add(mini_app_button)

    return keyboard



@bot.message_handler(commands=['start'])
def welcome_msg(message):
    try:
        bot.send_message(message.chat.id,WELCOME_MSG, reply_markup=create_main_keyboard(message.chat.id))
    except Exception as e:
        print(repr(e))
        bot.send_message(message.chat.id, WELCOME_MSG, reply_markup=create_main_keyboard(message.chat.id))
# warning user if they send message to bot
@bot.message_handler(func=lambda message: True)
def warning_msg(message):
    # skip if user send location or command
    if message.text != '/start' or message.text != '/group':
        
        bot.send_message(message.chat.id, f"សូមអភ័យទោស! យើងមិនអាចទទួលបានសារពីអ្នកទេ។ សូមចុចលើប៊ូតុងខាងក្រោមដើម្បីទទួលបានសារពីយើង។", reply_markup=create_main_keyboard(message.chat.id))




if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as ex:
            print(f"Bot polling failed: {ex}")
            # logger.error(f"Bot polling failed: {ex}")
            time.sleep(15)