import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import datetime

# Replace YOUR_TOKEN with your bot token obtained from BotFather
bot = telebot.TeleBot('5868931768:AAGgTaJBbhGt-tG09tI1jSVAplJD-r5n96g')

info_keyboard_kh = InlineKeyboardMarkup()
today_button_kh = InlineKeyboardButton(text="វេជ្ជបណ្ឌិតសំរាប់ថ្ងៃនេះ", callback_data='today')
tomorrow_button_kh = InlineKeyboardButton(text="វេជ្ជបណ្ឌិតសំរាប់ថ្ងៃស្អែក", callback_data='tomorrow')
info_keyboard_kh.row(today_button_kh, tomorrow_button_kh)


# back button 
back_keyboard = InlineKeyboardMarkup()
back_button = InlineKeyboardButton(text="ត្រឡប់ទំព័រមុខវិញ", callback_data='back')
back_keyboard.row(back_button)


@bot.message_handler(commands=['start'])
def start_message(message):
    username = message.from_user.username

    bot.send_message(chat_id=message.chat.id, text=f'👋សូមស្វាគមន៍មកកាន់មន្ទីពេទ្យកុមារសកល, {username}! 😊 \n')
    bot.send_message(chat_id=message.chat.id, text='👇សូមចុចលើប៊ូតុងខាងក្រោមដើម្បីបានព័ត៌មាន៖ 📝', reply_markup=info_keyboard_kh)

list_doctor = [
    {
    'name': "Dara",
    'start_work': "10:00",
    'end_work': "03:00",
    'tel': '01234567'
    },
    {
    'name': "Dara",
    'start_work': "10:00",
    'end_work': "03:00",
    'tel': '01234567'
    }
]
@bot.callback_query_handler(func=lambda call: call.data in ['today', 'tomorrow','back'])
def handle_date_selection(call):
    # Get the selected date
    date = call.data
    if date == 'today':
        doc = ''
        for i in range (0,len(list_doctor)):
            doc = doc + f"\n🧑🏻‍⚕️ ឈ្មោះវេជ្ជបណ្ឌិត: <b>{list_doctor[i]['name']}</b>\n🕐 ម៉ោងធ្វើការងារ: {list_doctor[i]['start_work']} - {list_doctor[i]['end_work']}\n -------------------------------"
        te = datetime.date.today().strftime('%A, %B %d, %Y')
        today_doctor = f'''{te}\n<b>🗓️ តារាងវេជ្ជបណ្ឌិតថ្ងៃនេះ</b> \n-------------------------------{doc}'''
        response = today_doctor
    elif date == 'tomorrow':
        tmr_doctor = '12'
        response = tmr_doctor
    elif date == 'back':
        response = '👇សូមចុចលើប៊ូតុងខាងក្រោមដើម្បីបានព័ត៌មាន៖ 📝'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{response}.",parse_mode='HTML', reply_markup=info_keyboard_kh)
        return

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{response}.",parse_mode='HTML', reply_markup=back_keyboard)
    
    

# Start the bot
bot.polling()