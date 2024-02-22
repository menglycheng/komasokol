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
from generate_qrcode import generate_qrcode,delete_qrcode
load_dotenv()



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


API = os.getenv('BOT_TOKEN')
URL = os.getenv('URL')

bot = telebot.TeleBot(API)


def create_main_keyboard(chat_id):
    keyboard = InlineKeyboardMarkup()
    duty_staff_button = InlineKeyboardButton('🧑🏻‍⚕️ មើលបុគ្គលិកប្រចាំការនៅថ្ងៃនេះ', callback_data='duty_staff')
    service_button = InlineKeyboardButton('🛎️ សេវាកម្ម', callback_data='service')
    contact_button = InlineKeyboardButton('☎️ លេខទំនាក់ទំនង', callback_data='contact')
    about_button = InlineKeyboardButton('ℹ️ អំពីយើង', callback_data='about')
    location_button = InlineKeyboardButton('🏥 ទីតាំង', callback_data='location')
    live_chat_button = InlineKeyboardButton('💬 Live Chat',url='https://t.me/komasakol_livechat')
    connect_button = InlineKeyboardButton('🤖 ភ្ចាប់ជាមួយសារស្វ័យប្រវត្តិ', callback_data='connect')
    other_connect_button = InlineKeyboardButton('🤖 ភ្ចាប់ថ្មី', callback_data='connect')
    qrcode = InlineKeyboardButton('🔗 កូដ QR', callback_data='qrcode')
    

    disconnect_button = InlineKeyboardButton('❌ ផ្តាច់សារស្វ័យប្រវត្តិ', callback_data='disconnect')
    keyboard.row(duty_staff_button)
    keyboard.row(service_button,about_button, location_button)
    keyboard.row(contact_button,live_chat_button,qrcode)
    if check_user_connect(chat_id) == 'false':
        keyboard.row(connect_button)
    else:
        keyboard.row(disconnect_button,other_connect_button)

    return keyboard

def create_back_keyboard():
    back_button = InlineKeyboardMarkup()
    back_button.add(InlineKeyboardButton('⬅️ ត្រលប់ក្រោយ', callback_data='back'))
    return back_button


@bot.message_handler(commands=['start'])
def welcome_msg(message):
    try:
        bot.send_message(message.chat.id, "🌟 សូមស្វាគមន៍មកកាន់ មន្ទីរពេទ្យកុមារសកល សារស្វ័យប្រវត្តិ របស់យើងនៅលើ Telegram! 🤖", reply_markup=create_main_keyboard(message.chat.id))
    except Exception as e:
        print(repr(e))
        bot.send_message(message.chat.id, "សូមស្វាគមន៍មកកាន់ មន្ទីរពេទ្យកុមារសកល សារស្វ័យប្រវត្តិ របស់យើងនៅលើ Telegram!", reply_markup=create_main_keyboard(message.chat.id))
# warning user if they send message to bot
@bot.message_handler(func=lambda message: True)
def warning_msg(message):
    # skip if user send location or command
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
            generate_qrcode(str(chat_id),call.message.chat.username)
            # send photo with text 

            photo_message = bot.send_photo(chat_id, photo=open(f'{chat_id}.png', 'rb'), caption="Give this Qr code to the staff to connect with us.")
            msg_id = photo_message.message_id
            time.sleep(15)
            bot.delete_message(chat_id=chat_id, message_id=msg_id)

            delete_qrcode()
   

        elif call.data == 'disconnect':
            disconnect_user(chat_id)
        elif call.data == 'service':
            get_data_from_api(chat_id,msg_id,'service')
            # getUpdates
        elif call.data == 'contact':
            get_data_from_api(chat_id,msg_id,'contact')
        elif call.data == 'about':
            get_data_from_api(chat_id,msg_id,'about')
        elif call.data == 'location':
            get_data_from_api(chat_id,msg_id,'location')
        elif call.data == 'duty_staff':
            current_date = datetime.datetime.now().strftime("%d/%m/%Y")
            morning_timetable = "\nវេនពេលព្រឹក៖ \n"
            afternoon_timetable = "\nវេនពេលរសៀល៖ \n"
            night_timetable = "\nវេនពេលយប់៖ \n"
            doctor_timetable = json.loads(get_doctor_timetable())
            for doctor in doctor_timetable['morning_shift']:
                morning_timetable += f"🧑🏻‍⚕️ Dr. {doctor} \n"
            for doctor in doctor_timetable['afternoon_shift']:
                afternoon_timetable += f"🧑🏻‍⚕️ Dr. {doctor} \n"
            for doctor in doctor_timetable['night_shift']:
                night_timetable += f"🧑🏻‍⚕️ Dr. {doctor} \n"

            msg = f'🧑🏻‍⚕️គ្រូពេទ្យប្រចាំការថ្ងៃនេះ : \n🗓️ {current_date} \n --------------------\n{morning_timetable} {afternoon_timetable} {night_timetable} \n⚠️៖​ មន្ទីរពេទ្យយើងរក្សាសិទ្ធិក្នុងការផ្លាស់ប្តូរដោយពុំបាច់ជូនដំណឹងជាមុន '
            bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text=msg, reply_markup=create_back_keyboard())
        elif call.data == 'back':
            bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text="🌟 សូមស្វាគមន៍មកកាន់ មន្ទីរពេទ្យកុមារសកល សារស្វ័យប្រវត្តិ របស់យើងនៅលើ Telegram! 🤖", reply_markup=create_main_keyboard(chat_id))
    except Exception as e:
        logger.error(f"Error in callback_query: {e}")
        bot.send_message(call.message.chat.id, "សូមស្វាគមន៍មកកាន់ មន្ទីរពេទ្យកុមារសកល សារស្វ័យប្រវត្តិ របស់យើងនៅលើ Telegram!", reply_markup=create_main_keyboard(chat_id))

# function to get doctor timetable
def get_doctor_timetable():
    url = f'{URL}/api/doctor_timetable'
    # get current month 
    now = datetime.datetime.now()
    current_month = now.strftime("%B")
    print(current_month)
    data = {
        "jsonrpc": "2.0",
        "params": {
            'month': current_month
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
    # get username
    username = message.from_user.username
    url = f'{URL}/api/getChatID'
    if username == None:
        username = message.from_user.first_name + ' ' + message.from_user.last_name
    data = {
        "jsonrpc": "2.0",
        "params": {
            "secret_code": secret_code,
            'chat_id': chat_id,
            'username': username 
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
if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as ex:
            logger.error(f"Bot polling failed: {ex}")
            time.sleep(15)

