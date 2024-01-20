import os
import telebot 
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from dotenv import load_dotenv
load_dotenv()

API =os.getenv('BOT_TOKEN')
# Replace YOUR_TOKEN with your bot token obtained from BotFather
bot = telebot.TeleBot(API)

# create button for user to click
connect_keyboard = InlineKeyboardMarkup()
disconnect_keyboard = InlineKeyboardMarkup()

service = InlineKeyboardButton('សេវាកម្ម', callback_data='service')
contact = InlineKeyboardButton('លេខទំនាក់ទំនង', callback_data='contact')
about = InlineKeyboardButton('អំពីយើង', callback_data='about')
location = InlineKeyboardButton('ទីតាំងរបស់ពួកយើង', callback_data='location')

# make above btn into a column of two buttons
connect = InlineKeyboardButton('ភ្ចាប់ជាមួយសារស្វ័យប្រវត្តិ', callback_data='connect')
logout = InlineKeyboardButton('ចាកចេញពីសារស្វ័យប្រវត្តិ់', callback_data='logout')

connect_keyboard.add(service, contact, about, location, connect)
disconnect_keyboard.add(service, contact, about, location, logout)
# back button from connect with hospital to main menu
                                           
back_button = InlineKeyboardMarkup()
back_button.add(InlineKeyboardButton('ត្រលប់ក្រោយ', callback_data='back'))

@bot.message_handler(commands=['start']) 
def welcome_msg(message):
    bot.send_message(message.chat.id, "🌟 សូមស្វាគមន៍មកកាន់ មន្ទីរពេទ្យកុមារសកល សារស្វ័យប្រវត្តិ របស់យើងនៅលើ Telegram! 🤖", reply_markup=check_user_connect(message.chat.id))

# funcution to handle the callback data from the button for Connect with Hospital is wait user input serect code to verify user and user can cancel back to main menu
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        chat_id = call.message.chat.id
        msg_id = call.message.message_id
        if call.data == 'logout':
            disconnect_user_from_api(chat_id)
    
        elif call.data == 'connect':
            bot.send_message(call.message.chat.id, "ភ្ចាប់ជាមួយសារស្វ័យប្រវត្តិលោកអ្នកនឹងទទួលបានការជូនដំណឹងពីពួកយើងដូចខាងក្រោម៖ \n 1. ទទួលបានសាររាល់ការណាត់ \n2. អ្នកនឹងទទួលបានដំណឹងផ្សេងៗទៀត")
            bot.send_message(call.message.chat.id, "ដើម្បីទទួលបានលេខសម្ងាត់សូមទៅកាន់កន្លែងទទួលភ្ញៀវ")
            bot.send_message(call.message.chat.id, "សូមបញ្ជូនលេខសម្ងាត់:", reply_markup=back_button)
            bot.register_next_step_handler(call.message, send_data_to_api)
        elif call.data == 'service':
            get_data_from_api(chat_id,msg_id,'service')
        elif call.data == 'contact':
            get_data_from_api(chat_id,msg_id,'contact')

        elif call.data == 'about':
            get_data_from_api(chat_id,msg_id,'about')
        elif call.data == 'location':
            get_data_from_api(chat_id,msg_id,'location')
        elif call.data == 'back':
            bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text="🌟 សូមស្វាគមន៍មកកាន់ មន្ទីរពេទ្យកុមារសកល សារស្វ័យប្រវត្តិ របស់យើងនៅលើ Telegram! 🤖", reply_markup=check_user_connect(chat_id))
    except Exception as e:
        print(repr(e))
        bot.send_message(call.message.chat.id, "សូមស្វាគមន៍មកកាន់ មន្ទីរពេទ្យកុមារសកល សារស្វ័យប្រវត្តិ របស់យើងនៅលើ Telegram!", reply_markup=check_user_connect(chat_id))

# function to check user connect or not 
def check_user_connect(chat_id):
    url = 'http://localhost:8069/api/checkUser'
    data = {
        "jsonrpc": "2.0",
        "params": {
            "chat_id": chat_id,
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json().get('result')
            if result == 'true':
                keyboard = disconnect_keyboard
            else:
                keyboard = connect_keyboard
            return keyboard
        else:
            return connect_keyboard
    except requests.RequestException as e:
        return f"Request failed: {e}"

# function to send data to api
def send_data_to_api(message):
    secret_code = message.text
    chat_id = message.chat.id
    url = 'http://localhost:8069/api/getChatID'
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
                bot.send_message(chat_id=chat_id, text="លេខសម្ងាត់ត្រូវបានផ្ទៀងផ្ទាត់ត្រឹមត្រូវ!")
                # resend welcome message with button again 
                bot.send_message(chat_id=chat_id, text="🌟 សូមស្វាគមន៍មកកាន់ មន្ទីរពេទ្យកុមារសកល សារស្វ័យប្រវត្តិ របស់យើងនៅលើ Telegram! 🤖", reply_markup=check_user_connect(chat_id))
            else:
                bot.send_message(chat_id=chat_id, text="លេខសម្ងាត់មិនត្រឹមត្រូវ. សូម​ព្យាយាម​ម្តង​ទៀត.", reply_markup=back_button)
        else:
            bot.send_message(chat_id=chat_id, text=f"Failed to send data to Odoo. Status code: {response.status_code}", reply_markup=back_button)
        

    except requests.RequestException as e:
        bot.send_message(chat_id=chat_id, text=f"Request failed: {e}")

# function to disconnect user from api


# function to get data from api
def get_data_from_api(chat_id,msg_id,model):
    url = 'http://localhost:8069/api/getContent'
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

            bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text=msg, reply_markup=back_button)
            return result
        else:
            return f"Failed to get data from Odoo. Status code: {response.status_code}"
    except requests.RequestException as e:
        return f"Request failed: {e}"

bot.polling()
