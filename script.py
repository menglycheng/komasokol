import os
from dotenv import load_dotenv
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import time

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
API = os.getenv('BOT_TOKEN')
LIVE_CHAT = os.getenv('LIVE_CHAT')
MINI_APP = os.getenv('MINI_APP')
HOSPITAL = os.getenv('HOSPITAL')
WELCOME_MSG = os.getenv('WELCOME_MESSAGE')

# Initialize bot
bot = Bot(token=API)

def create_main_keyboard():
    # Creating InlineKeyboardMarkup
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('💬 Live Chat', url=LIVE_CHAT)],
        [InlineKeyboardButton(f'📱 {HOSPITAL}', web_app=WebAppInfo(url=MINI_APP))]
    ])
    return keyboard

def start(update, context):
    # Send welcome message
    update.message.reply_text(
        WELCOME_MSG,
        reply_markup=create_main_keyboard()
    )

def warning_msg(update, context):
    # Handle non-command text messages
    message = update.message.text
    if message and message not in ['/start', '/group']:
        update.message.reply_text(
            "សូមអភ័យទោស! យើងមិនអាចទទួលបានសារពីអ្នកទេ។ សូមចុចលើប៊ូតុងខាងក្រោមដើម្បីទទួលបានសារពីយើង។",
            reply_markup=create_main_keyboard()
        )

def main():
    # Create the Updater and pass it your bot's token
    updater = Updater(API)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler('start', start))

    # Non-command message handler
    dp.add_handler(MessageHandler(Filters.text, warning_msg))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as ex:
            print(f"Bot polling failed: {ex}")
            logger.error(f"Bot polling failed: {ex}")
            time.sleep(15)
