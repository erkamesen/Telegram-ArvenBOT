
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, Filters, filters, Updater,CallbackContext
from telegram import ForceReply, Update, ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
import os
from dotenv import load_dotenv
from responses import Response
import re

load_dotenv()

APIKEY = os.getenv("APIKey")
CHATID = os.getenv("chatID")


R = Response()


      
def start(update, source):

    """Send a message when the command /start is issued."""
    
    user = update.effective_user
    result = f"Hi ! {user.first_name} {user.last_name} Welcome."
    update.message.reply_text(result, parse_mode=ParseMode.HTML)


def earthquake(update, source):
    reply = R.last_ten_earthquake()
    update.message.reply_text(reply, parse_mode=ParseMode.HTML)


def currency(update, source):
    update.message.reply_text(f'<i>{R.currency()}</i>', parse_mode=ParseMode.HTML)


def standing(update, context):
    update.message.reply_text(f"<pre>{R.standing()}</pre>", parse_mode=ParseMode.HTML)

def epic_robot(update, context): # Babür

    chat_id = update.effective_user.id
    epic_photo = open('epic_robot.jpg', 'rb')
    context.bot.send_photo(chat_id=chat_id, photo=epic_photo)



def handle_message(update, context):
    text = str(update.message.text).lower()
    normal_text = str(update.message.text)
    chat_id = update.effective_user.id
    if text.startswith("-github/"):
        username = text.split("/")[1]
        response = R.github_nonFollowers(username)
        for resp in response:
            update.message.reply_text(f"https://github.com/{resp}")

    if text.startswith("-earthquake/"):
        city = text.split("/")[1].capitalize()
        reply = R.near_earthquakes(city_name=city)
        update.message.reply_text(reply, parse_mode=ParseMode.HTML)

    if text.startswith("-audio/https://youtu.be") or text.startswith("-audio/https://www.youtube.com"):
        url = normal_text.split("-audio/")[1]
        R.send_audio(URL=url)
        update.message.reply_text("İndirildi", parse_mode=ParseMode.HTML)
    


    



def main():

    update = Updater(APIKEY, use_context=True)
    disp = update.dispatcher

    disp.add_handler(CommandHandler("start", start))
    disp.add_handler(CommandHandler("earthquake", earthquake))
    disp.add_handler(CommandHandler("standing", standing))
    disp.add_handler(CommandHandler("currency", currency))
    disp.add_handler(CommandHandler("ensar", epic_robot))
    disp.add_handler(MessageHandler(Filters.text, handle_message))



    update.start_polling()
    update.idle()

if __name__ == "__main__":
   main()




""" 

daysList = ["Mon", "Tue", "Wen", "Thu", "Fri"]
def days_b():
    keyboard = [
    [
        InlineKeyboardButton("Mon", callback_data='0'),
        InlineKeyboardButton("Tue", callback_data='1'),
        InlineKeyboardButton("Wen", callback_data='2'),
        InlineKeyboardButton("Thu", callback_data='3'),
        InlineKeyboardButton("Fri", callback_data='4'),
          ],
    ]    
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

def week_command(update, context):
    update.message.reply_text("sa")
    update.message.reply_text(daysList[0], reply_markup=days_b())

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.edit_message_text(text=daysList[query.data], reply_markup=days_b())

 """