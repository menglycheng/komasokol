import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import datetime
import json 

with open('schudule.json', 'r') as f:
    data = json.load(f)


# Replace YOUR_TOKEN with your bot token obtained from BotFather
bot = telebot.TeleBot('5868931768:AAG3lgfxqM873yYfc3skJWxAwroVXwtcQXM')



info_keyboard_kh = InlineKeyboardMarkup()

# line 1
today_button_kh = InlineKeyboardButton(text="🕐 វេជ្ជបណ្ឌិតសំរាប់ថ្ងៃនេះ", callback_data='today')
tomorrow_button_kh = InlineKeyboardButton(text="🕐 វេជ្ជបណ្ឌិតសំរាប់ថ្ងៃស្អែក", callback_data='tomorrow')


info_keyboard_kh.row(today_button_kh, tomorrow_button_kh)

# line 2 
location_button = InlineKeyboardButton(text="🗺️ ទីតាំង", callback_data='location')
info_keyboard_kh.row(location_button)


# back button 
back_keyboard = InlineKeyboardMarkup()
back_button = InlineKeyboardButton(text="ត្រឡប់ទំព័រមុខវិញ", callback_data='back')
back_keyboard.row(back_button)


@bot.message_handler(commands=['start'])
def start_message(message):
    username = message.from_user.username

    bot.send_message(chat_id=message.chat.id, text=f'👋សូមស្វាគមន៍មកកាន់មន្ទីពេទ្យកុមារសកល, {username}! 😊 \n')
    bot.send_message(chat_id=message.chat.id, text='👇សូមចុចលើប៊ូតុងខាងក្រោមដើម្បីបានព័ត៌មាន៖', reply_markup=info_keyboard_kh)

def schudule(today):
    list_doctor=[]
    for i in data:
            if i['date'] == str(today):
                print(i)
                list_doctor.append(i)
    doc = ''
    for i in range (0,len(list_doctor)):
            doc = doc + f"\n🧑🏻‍⚕️ ឈ្មោះវេជ្ជបណ្ឌិត: <b>{list_doctor[i]['name']}</b>\n🕐 ម៉ោងធ្វើការងារ: {list_doctor[i]['work_time']}\n -------------------------------"
    today_doctor = f'''<b>🗓️ តារាងវេជ្ជបណ្ឌិតថ្ងៃ {today}</b> \n-------------------------------{doc}'''
    return today_doctor

@bot.callback_query_handler(func=lambda call: call.data in ['today', 'tomorrow','location','back'])
def handle_date_selection(call):
    # Get the selected date
    date = call.data
    today = datetime.date.today()
    if date == 'today':
    
        response = schudule(today)
    elif date == 'tomorrow':
    
        tmr = datetime.date.today() + datetime.timedelta(days=1)
        
        response = schudule(tmr)
       
    elif date == 'location':
        response = "ទីតាំង: ផ្ទះ១២០២ និង ១១៩៨ ​​​ផ្លូវ អភិវឌ្ឍន៍ 1​  សង្កាត់ ជ្រោយចង្វា​រ​ ខណ្ឌ ជ្រោយចង្វា​រ រាជធានី​ ភ្នំពេញ\n<b>Google map</b>: https://goo.gl/maps/MyGHpj8c7EoynNbX8"
    elif date == 'back':
        response = '👇សូមចុចលើប៊ូតុងខាងក្រោមដើម្បីបានព័ត៌មាន៖ 📝'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{response}.",parse_mode='HTML', reply_markup=info_keyboard_kh)
        return

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{response}.",parse_mode='HTML', reply_markup=back_keyboard)
    
    

# Start the bot
bot.polling()