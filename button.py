from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import os
from dotenv import load_dotenv
load_dotenv()
import requests
import json

URL = os.getenv('URL')
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
    keyboard.row(contact_button,live_chat_button)
    if check_user_connect(chat_id) == 'false':
        keyboard.row(connect_button)
    else:
        keyboard.row(disconnect_button,other_connect_button)
        keyboard.row(qrcode)


    return keyboard
def create_patient_qrcode(chat_id):
    keyboard = InlineKeyboardMarkup()
    usernames = get_patient_username(chat_id)
    usernames_list = json.loads(usernames)
    # Create a button for each username
    for username in usernames_list:
        qrcode = InlineKeyboardButton(f'🙍 {username}', callback_data=f'{username}')  # Use some way to associate the username with the callback data
        keyboard.add(qrcode)
    keyboard.add(InlineKeyboardButton('⬅️ ត្រលប់ក្រោយ', callback_data='back'))
    return keyboard

def create_back_keyboard():
    back_button = InlineKeyboardMarkup()
    back_button.add(InlineKeyboardButton('⬅️ ត្រលប់ក្រោយ', callback_data='back'))
    return back_button


def get_patient_username(chat_id):
    url = f'{URL}/api/getPatient'
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