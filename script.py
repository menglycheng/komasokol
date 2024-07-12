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
from encryption import encrypt_message_ctr
from generate_qrcode import generate_qrcode,delete_qrcode,register_patient
from api.check_premium import checkPremium
from api.check_user import check_user_connect
from api.get_patient_username import get_patient_username
from api.get_doctor_timetable import get_doctor_timetable
load_dotenv()

# logging.basicConfig(leve=logging.INFO)
# logger = logging.getLogger(__name__)


API = os.getenv('BOT_TOKEN')
URL = os.getenv('URL')
LIVE_CHAT = os.getenv('LIVE_CHAT')
WELCOME_MSG = os.getenv('WELCOME_MESSAGE')
EHEALTH_URL = os.getenv('EHEALTH_URL')
HOSPITAL = os.getenv('HOSPITAL')
API_KEY = os.getenv("API_KEY")

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

# create ReplyKeyboardMarkup for restart bot
def create_restart_keyboard():
    restart_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    restart_keyboard.add(KeyboardButton('/start'))
    return restart_keyboard


def create_main_keyboard(chat_id):
    keyboard = InlineKeyboardMarkup()
    duty_staff_button = InlineKeyboardButton('🧑🏻‍⚕️ មើលបុគ្គលិកប្រចាំការនៅថ្ងៃនេះ', callback_data='duty_staff')
    service_button = InlineKeyboardButton('🛎️ សេវាកម្ម', callback_data='service')
    contact_button = InlineKeyboardButton('☎️ លេខទំនាក់ទំនង', callback_data='contact')
    about_button = InlineKeyboardButton('ℹ️ អំពីយើង', callback_data='about')
    location_button = InlineKeyboardButton('🏥 ទីតាំង', callback_data='location')
    live_chat_button = InlineKeyboardButton('💬 Live Chat',LIVE_CHAT)
    # premium
    connect_button = InlineKeyboardButton('🤖 ភ្ចាប់ជាមួយសារស្វ័យប្រវត្តិ', callback_data='connect')
    other_connect_button = InlineKeyboardButton('🤖 ភ្ចាប់ថ្មី', callback_data='connect')
    qrcode = InlineKeyboardButton('ចូលមើលអ្នកជំងឺ', callback_data='qrcode')
    disconnect_button = InlineKeyboardButton('❌ ផ្តាច់សារស្វ័យប្រវត្តិ', callback_data='disconnect')
    
    keyboard.row(duty_staff_button)
    keyboard.row(service_button,about_button, location_button)
    keyboard.row(contact_button,live_chat_button)

    isPremiun = checkPremium()
    if isPremiun == True:
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
    for username in usernames_list:
        qrcode = InlineKeyboardButton(f'🙍 {username}', callback_data=f'{username}') 
        keyboard.add(qrcode)
    keyboard.add(InlineKeyboardButton('⬅️ ត្រលប់ក្រោយ', callback_data='back'))
    return keyboard

def create_back_keyboard():
    back_button = InlineKeyboardMarkup()
    back_button.add(InlineKeyboardButton('⬅️ ត្រលប់ក្រោយ', callback_data='back'))
    return back_button

def view_detail_keyboard(chat_id,patient_name):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('🔗 ចូលមើលពត៍មានបន្ថែម',f'{EHEALTH_URL}/{encrypt_message_ctr(str(chat_id))}/{encrypt_message_ctr(str(patient_name))}/{encrypt_message_ctr(str(HOSPITAL))}'))
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
    
@bot.message_handler(commands=['group'])
def get_id(message):
    bot.send_message(message.chat.id, message.chat.id)

def handle_connect(chat_id, call_message, msg_id):
    username = get_username(call_message)
    generate_qrcode(chat_id, username)
    connect_telegram = bot.send_photo(chat_id, photo=open(f'{chat_id}.png', 'rb'), caption="សុំបង្ហាញ Qr-Code នេះទៅបុគ្គលិក។")
    connect_telegram_id = connect_telegram.message_id
    bot.delete_message(chat_id=chat_id, message_id=msg_id)
    time.sleep(15)
    bot.delete_message(chat_id=chat_id, message_id=connect_telegram_id)
    delete_qrcode(chat_id)

def handle_qrcode(chat_id, msg_id):
    bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text="📋សូមជ្រើសរើសឈ្មោះអ្នកជំងឺ", reply_markup=create_patient_qrcode(chat_id))

def handle_usernames_list(call_data, chat_id, usernames_list):
    if call_data in usernames_list:
        msg = bot.send_message(chat_id, f"កំពុងដំណើរការ សូមរង់ចាំ...")
        register_patient(chat_id, call_data)
        send_qrcode_registration_confirmation(chat_id, call_data, msg.message_id)


def handle_service_requests(call_data, chat_id, msg_id):
    # Assuming get_data_from_api is a function that fetches and sends data based on 'service', 'contact', etc.
    get_data_from_api(chat_id, msg_id, call_data)

def send_qrcode_registration_confirmation(chat_id, patient_name, msg_id):
    qrcode_register = bot.send_photo(chat_id, photo=open(f'{chat_id}.png', 'rb'), caption=f"នេះជា Qr Code របស់ {patient_name}", reply_markup=view_detail_keyboard(chat_id,patient_name))
    bot.delete_message(chat_id=chat_id, message_id=msg_id)
    qrcode_register_id = qrcode_register.message_id
    time.sleep(10)
    delete_qrcode(chat_id)
    bot.delete_message(chat_id=chat_id, message_id=qrcode_register_id)


def get_username(message):
    if message.chat.username:
        return message.chat.username
    first_name = message.chat.first_name or ""
    last_name = message.chat.last_name or ""
    full_name = f"{first_name} {last_name}".strip()
    return full_name if full_name else f"User_{message.chat.id}"

def error_msg(e,chat_id,call):
    # logger.error(f"Error in callback_query: {e}")
    bot.send_message(chat_id=765185805, text=f"Bot polling failed:{chat_id}-{call.data}-{e}")
    bot.send_message(chat_id=chat_id, text="⚠️ ប្រព័ន្ធរបស់យើងប្រហែលជាមានបញ្ហាខ្លះ \nសូមព្យាយាមម្តងទៀតដោយចុចលើប៊ូតុងខាងក្រោម។", reply_markup=create_restart_keyboard())


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    if is_user_busy(chat_id, make_busy=True):
        bot.answer_callback_query(call.id, "Please wait for the current operation to complete.")
        return
    try:
        chat_id = call.message.chat.id
        msg_id = call.message.message_id

        if call.data == 'connect':
            try:
                msg = bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text="កំពុងដំណើរការ សូមរង់ចាំ...")
                handle_connect(chat_id, call.message, msg.message_id)
                bot.send_message(chat_id=chat_id, text=WELCOME_MSG, reply_markup=create_main_keyboard(chat_id))
            except Exception as e:
                error_msg(e,chat_id,call)
        elif call.data == 'qrcode':
            try:
                msg = bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text="កំពុងដំណើរការ សូមរង់ចាំ...")
                handle_qrcode(chat_id, msg_id)
            except Exception as e:
                error_msg(e,chat_id,call)
        elif call.data == 'disconnect':
            try:
                disconnect_user(chat_id)
            except Exception as e:
                error_msg(e,chat_id,call)
        elif call.data in ['service', 'contact', 'about', 'location']:
            try:
                bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text="កំពុងដំណើរការ សូមរង់ចាំ...")
                handle_service_requests(call.data, chat_id, msg_id)
            except Exception as e:
                error_msg(e,chat_id,call)
        elif call.data == 'duty_staff':
            # msg loading
            try:
                bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text="កំពុងដំណើរការ សូមរង់ចាំ...")
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
            except Exception as e:
                error_msg(e,chat_id,call)
        elif call.data == 'view_detail':
            print("view detail")
                
        elif call.data == 'back':
            try:
                bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text="🌟 សូមស្វាគមន៍មកកាន់ មន្ទីរពេទ្យកុមារសកល សារស្វ័យប្រវត្តិ របស់យើងនៅលើ Telegram! 🤖", reply_markup=create_main_keyboard(chat_id))
            except Exception as e:
                error_msg(e,chat_id,call)
        else:
            usernames = get_patient_username(chat_id)
            usernames_list = json.loads(usernames)
            handle_usernames_list(call.data, chat_id, usernames_list)
    except Exception as e:
        error_msg(e,chat_id,call)
    finally:
        free_user(chat_id)
 

# function to get doctor timetable


# function to disconnect user
def disconnect_user(chat_id):
    url = f'{URL}/v1/api/disconnectTelegram'
    data = {
        "jsonrpc": "2.0",
        "params": {
            'chat_id': chat_id
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json().get('result')
            print(result)
            if result == 'true':
                bot.send_message(chat_id=chat_id, text="អ្នកបានផ្តាច់ចេញពីសារស្វ័យប្រវត្តិរបស់យើងហើយ!")
                # resend welcome message with button again 
                bot.send_message(chat_id=chat_id, text=WELCOME_MSG, reply_markup=create_main_keyboard(chat_id))
            else:
                bot.send_message(chat_id=chat_id, text="សូមព្យាយាមម្តងទៀត.", reply_markup=create_back_keyboard())
        else:
            bot.send_message(chat_id=chat_id,text="ប្រព័ន្ធរបស់យើងប្រហែលជាមានបញ្ហាខ្លះ សូមព្យាយាមម្តងទៀត.", reply_markup=create_restart_keyboard())
            bot.send_message(chat_id=765185805, text=f"disconnectTelegram - Failed to send data to Odoo. Status code: {response.status_code}", reply_markup=create_back_keyboard())
        

    except requests.RequestException as e:
        bot.send_message(chat_id=chat_id, text=f"Request failed: {e}")

# function to get data from api
def get_data_from_api(chat_id,msg_id,model):
    url = f'{URL}/v1/api/getContent?content_type={model}'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json().get('result')
            # split result with '\n' to make new line
            msg = result.replace('"','').replace('\\n','\n')

            bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text=result, reply_markup=create_back_keyboard())
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
            print(f"Bot polling failed: {ex}")
            # logger.error(f"Bot polling failed: {ex}")
            time.sleep(15)