import os
import telebot
from dotenv import load_dotenv
import requests
import logging
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


API = os.getenv('BOT_TOKEN')
URL = os.getenv('URL')

bot = telebot.TeleBot(API)

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