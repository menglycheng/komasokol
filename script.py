import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
import requests

load_dotenv()

API = os.getenv('BOT_TOKEN')
URL = os.getenv('URL')

bot = telebot.TeleBot(API)


def create_main_keyboard(chat_id):
    keyboard = InlineKeyboardMarkup()

    service_button = InlineKeyboardButton('សេវាកម្ម', callback_data='service')
    contact_button = InlineKeyboardButton('លេខទំនាក់ទំនង', callback_data='contact')
    about_button = InlineKeyboardButton('អំពីយើង', callback_data='about')
    location_button = InlineKeyboardButton('ទីតាំងរបស់ពួកយើង', callback_data='location')
    live_chat_button = InlineKeyboardButton('Live Chat',url='https://t.me/komasakol')
    connect_button = InlineKeyboardButton('ភ្ចាប់ជាមួយសារស្វ័យប្រវត្តិ', callback_data='connect')
    disconnect_button = InlineKeyboardButton('ផ្តាច់ចេញពីសារស្វ័យប្រវត្តិ', callback_data='disconnect')

    keyboard.row(service_button,about_button, location_button)
    keyboard.row(contact_button,live_chat_button)
    if check_user_connect(chat_id) == 'false':
        keyboard.row(connect_button)
    else:
        keyboard.row(disconnect_button)

    return keyboard

def create_back_keyboard():
    back_button = InlineKeyboardMarkup()
    back_button.add(InlineKeyboardButton('⬅️ ត្រលប់ក្រោយ', callback_data='back'))
    return back_button

@bot.message_handler(commands=['start'])
def welcome_msg(message):
    bot.send_message(message.chat.id, "🌟 សូមស្វាគមន៍មកកាន់ មន្ទីរពេទ្យកុមារសកល សារស្វ័យប្រវត្តិ របស់យើងនៅលើ Telegram! 🤖", reply_markup=create_main_keyboard(message.chat.id))

# warning user if they send message to bot
@bot.message_handler(func=lambda message: True)
def warning_msg(message):
    bot.send_message(message.chat.id, "សូមអភ័យទោស! យើងមិនអាចទទួលបានសារពីអ្នកទេ។ សូមចុចលើប៊ូតុងខាងក្រោមដើម្បីទទួលបានសារពីយើង។", reply_markup=create_main_keyboard(message.chat.id))
@bot.message_handler(commands=['group'])
def get_id(message):
    bot.send_message(message.chat.id, message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        chat_id = call.message.chat.id
        msg_id = call.message.message_id
        if call.data == 'connect':
            bot.send_message(call.message.chat.id, "ភ្ចាប់ជាមួយសារស្វ័យប្រវត្តិលោកអ្នកនឹងទទួលបានការជូនដំណឹងពីពួកយើងដូចខាងក្រោម៖ \n 1. ទទួលបានសាររាល់ការណាត់ \n2. អ្នកនឹងទទួលបានដំណឹងផ្សេងៗទៀត")
            bot.send_message(call.message.chat.id, "ដើម្បីទទួលបានលេខសម្ងាត់សូមទៅកាន់កន្លែងទទួលភ្ញៀវ")
            bot.send_message(call.message.chat.id, "សូមបញ្ជូនលេខសម្ងាត់:", reply_markup=create_back_keyboard())
            bot.register_next_step_handler(call.message, send_data_to_api)
        elif call.data == 'disconnect':
            disconnect_user(chat_id)
        elif call.data == 'service':
            get_data_from_api(chat_id,msg_id,'service')
        elif call.data == 'contact':
            get_data_from_api(chat_id,msg_id,'contact')
        elif call.data == 'about':
            get_data_from_api(chat_id,msg_id,'about')
        elif call.data == 'location':
            get_data_from_api(chat_id,msg_id,'location')
        elif call.data == 'back':
            bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text="🌟 សូមស្វាគមន៍មកកាន់ មន្ទីរពេទ្យកុមារសកល សារស្វ័យប្រវត្តិ របស់យើងនៅលើ Telegram! 🤖", reply_markup=create_main_keyboard(chat_id))
    except Exception as e:
        print(repr(e))
        bot.send_message(call.message.chat.id, "សូមស្វាគមន៍មកកាន់ មន្ទីរពេទ្យកុមារសកល សារស្វ័យប្រវត្តិ របស់យើងនៅលើ Telegram!", reply_markup=create_main_keyboard(chat_id))

# function to disconnect user
def disconnect_user(chat_id):
    url = f'{URL}/api/disconnectTelegram'
    data = {
        "jsonrpc": "2.0",
        "params": {
            'chat_id': chat_id
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json().get('result')
            print(result)
            if result == 'true':
                bot.send_message(chat_id=chat_id, text="អ្នកបានផ្តាច់ចេញពីសារស្វ័យប្រវត្តិរបស់យើងហើយ!")
                # resend welcome message with button again 
                bot.send_message(chat_id=chat_id, text="🌟 សូមស្វាគមន៍មកកាន់ មន្ទីរពេទ្យកុមារសកល សារស្វ័យប្រវត្តិ របស់យើងនៅលើ Telegram! 🤖", reply_markup=create_main_keyboard(chat_id))
            else:
                bot.send_message(chat_id=chat_id, text="សូមព្យាយាមម្តងទៀត.", reply_markup=create_back_keyboard())
        else:
            bot.send_message(chat_id=chat_id, text=f"Failed to send data to Odoo. Status code: {response.status_code}", reply_markup=create_back_keyboard())
        

    except requests.RequestException as e:
        bot.send_message(chat_id=chat_id, text=f"Request failed: {e}")
# function to send data to api
def send_data_to_api(message):
    secret_code = message.text
    chat_id = message.chat.id
    url = f'{URL}/api/getChatID'
    data = {
        "jsonrpc": "2.0",
        "params": {
            "secret_code": secret_code,
            'chat_id': chat_id
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json().get('result')
            print(result)
            if result == 'true':
                bot.send_message(chat_id=chat_id, text="លេខសម្ងាត់ត្រូវបានផ្ទៀងផ្ទាត់ត្រឹមត្រូវ!",reply_markup=create_main_keyboard(chat_id))
            else:
                bot.send_message(chat_id=chat_id, text="លេខសម្ងាត់មិនត្រឹមត្រូវ. សូម​ព្យាយាម​ម្តង​ទៀត.", reply_markup=create_back_keyboard())
        else:
            bot.send_message(chat_id=chat_id, text=f"Failed to send data to Odoo. Status code: {response.status_code}", reply_markup=create_back_keyboard())
        

    except requests.RequestException as e:
        bot.send_message(chat_id=chat_id, text=f"Request failed: {e}")

# function to check user connect or not 
def check_user_connect(chat_id):
    url = f'{URL}/api/checkUser'
    data = {
        "jsonrpc": "2.0",
        "params": {
            'chat_id': chat_id
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json().get('result')
            return result
        else:
            return f"Failed to get data from Odoo. Status code: {response.status_code}"
    except requests.RequestException as e:
        return f"Request failed: {e}"



# function to get data from api
def get_data_from_api(chat_id,msg_id,model):
    url = f'{URL}/api/getContent'
    data = {
        "jsonrpc": "2.0",
        "params": {
            "content_type": model,
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json().get('result')
            # split result with '\n' to make new line
            msg = result.replace('"','').replace('\\n','\n')

            bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text=msg, reply_markup=create_back_keyboard())
            return result
        else:
            return f"Failed to get data from Odoo. Status code: {response.status_code}"
    except requests.RequestException as e:
        return f"Request failed: {e}"



bot.polling()
