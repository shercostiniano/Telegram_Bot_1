from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import time
import sys

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY = range(2)

reply_keyboard = [['Email Address'],
				  ['Bitcointalk or Altcoin Profile Link'],
                  ['Ethereum Address'],
                  ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(bot, update):
    update.message.reply_text(
        """
        Hi! I am Cura Bot.
        Please follow these steps before proceeding...
        Follow us on Twitter - https://twitter.com/curaizon
        Follow us on Facebook - https://facebook.com/curaizon
        """,
        reply_markup=markup)

    return CHOOSING


def regular_choice(bot, update, user_data):
    text = update.message.text
    user_data['choice'] = text
    update.message.reply_text('Please type your {}'.format(text.lower()))

    return TYPING_REPLY

def received_information(bot, update, user_data):
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']
    update.message.reply_text("{}".format(facts_to_str(user_data)), reply_markup=markup)
    return CHOOSING


def done(bot, update, user_data):
	update.message.reply_text("Yay! you are now done..\n Join now in our Channel - https://t.me/Curaizon")
	return writescore(user_data,update)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def writescore(user_data, update):
	name = update.message.from_user.first_name + " " + update.message.from_user.last_name
	user = "@"+update.message.from_user.username.capitalize()
	link = user_data.get('Bitcointalk or Altcoin Profile Link')
	ethaddress = user_data.get('Ethereum Address')
	emailaddress = user_data.get('Email Address')

	"""Spreadsheet works"""
	time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
	scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
	credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
	client = gspread.authorize(credentials)
	sheet = client.open('Cura Bot').sheet1
	row = [time,name,user,emailaddress,link,ethaddress]

	sheet.append_row(row)

	return ConversationHandler.END

def main():
	print("Cura Bot is running....")
    # Create the Updater and pass it your bot's token.
	updater = Updater("575053643:AAGK6nC_jTQhffuvK3OL7jTYY2mEvUa8BSw")

    # Get the dispatcher to register handlers
	dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
	conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [RegexHandler('^(Email Address|Bitcointalk or Altcoin Profile Link|Ethereum Address)$',
                                    regular_choice,
                                    pass_user_data=True),
                       ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information,
                                          pass_user_data=True),
                           ],
        },

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
    )

	dp.add_handler(conv_handler)

    # log all errors
	dp.add_error_handler(error)

    # Start the Bot
	updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()

if __name__ == '__main__':
    main()