
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, Filters, filters, Updater
from telegram import ForceReply, Update, ParseMode
import os
from dotenv import load_dotenv

from responses import Response
import re

load_dotenv()

APIKEY = os.getenv("APIKey")
CHATID = os.getenv("chatID")

"""  """

R = Response()

def start(update, source):

    """Send a message when the command /start is issued."""
    
    first_name, last_name = update.effective_user.first_name, update.effective_user.last_name
    result = f"Hi ! {first_name} {last_name} Welcome."
    update.message.reply_text(result, parse_mode=ParseMode.HTML)


def earthquake(update, source):
    reply = R.last_ten_earthquake()
    update.message.reply_text(reply, parse_mode=ParseMode.HTML)


def currency(update, source):
    update.message.reply_text(f'<i>{R.currency()}</i>', parse_mode=ParseMode.HTML)


def standing(update, context):
    update.message.reply_text(f"<pre>{R.standing()}</pre>", parse_mode=ParseMode.HTML)


def handle_message(update, context):
    text = str(update.message.text).lower()
    if text.startswith("-github/"):
        username = text.split("/")[1]
        response = R.github_nonFollowers(username)
        for resp in response:
            update.message.reply_text(f"https://github.com/{resp}")

    if text.startswith("-earthquake/"):
        city = text.split("/")[1].capitalize()
        reply = R.near_earthquakes(city_name=city)
        update.message.reply_text(reply, parse_mode=ParseMode.HTML)





update = Updater(APIKEY, use_context=True)
disp = update.dispatcher

disp.add_handler(CommandHandler("start", start))
disp.add_handler(CommandHandler("earthquake", earthquake))
disp.add_handler(CommandHandler("standing", standing))
disp.add_handler(CommandHandler("currency", currency))
disp.add_handler(MessageHandler(Filters.text, handle_message))



update.start_polling()
update.idle()