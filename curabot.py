from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import time,threading
#import httplib2
#from httplib2 import Http
#import re


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

REFERRAL, CHOOSING, TYPING_REPLY, TYPING_REFER = range(4)


EMAIL = 'Email Address'
BCT = 'Bitcointalk or Altcoin Profile Link'
BCTUSER = 'Bitcointalk or Altcoin Username'
ETH = 'Ethereum Address'
REFER = 'Referral Link'
DONE = 'Done'
YES = "Referrer's Referral Link"
NO = 'No'

reply_keyboard = [[REFER],[BCT,BCTUSER],[EMAIL,ETH],[DONE]]
bool_keyboard = [[YES,NO]]

markup = ReplyKeyboardMarkup(reply_keyboard)
refer_markup = ReplyKeyboardMarkup([REFER])
bool_markup = ReplyKeyboardMarkup(bool_keyboard)
registered = []

#Edited now
def gspreadUpdater():
    global scope,client,sheet,worksheet,ID_List
    while True:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(credentials)
        sheet = client.open('Curaizon Official Bounty Campaign Sheets')
        worksheet = sheet.worksheet("Telegram")
        ID_List = worksheet.range("G2:G{}".format(worksheet.row_count))
        time.sleep(3590)

def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(bot, update):
	ID = update.message.from_user.id
	verify = [user.value for user in ID_List if user.value == str(ID)]
	if ID not in registered:
		if str(ID) not in verify:
			update.message.reply_text(
			    "Hi! I am Cura Bot.\n\n"
			    "Please follow these steps before proceeding...\n"
			    "Follow us on Twitter - https://twitter.com/curaizon\n"
			    "Follow us on Facebook - https://facebook.com/curaizon",
			    reply_markup=markup, resize_keyboard=True, disable_web_page_preview=True)

			return CHOOSING
		else:
			update.message.reply_text("You are currently registered in our database. \nPlease proceed to the channel if there are any problem")
	else:
			update.message.reply_text("You are currently registered in our database. \nPlease proceed to the channel if there are any problem")


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
    update.message.reply_text("{}".format(facts_to_str(user_data)), reply_markup=ReplyKeyboardMarkup([[BCT,BCTUSER],[EMAIL],[ETH],[DONE]]), resize_keyboard=True)
    return CHOOSING


def done(bot, update, user_data):
    refLink = "https://t.me/Cura_HelperBot?refLink=" + str(update.message.from_user.id)
    user = "@"+update.message.from_user.username.capitalize()
    link = user_data.get(BCT)
    userBCT = user_data.get(BCTUSER)
    ethaddress = user_data.get(ETH)
    emailaddress = user_data.get(EMAIL)
    ID = update.message.from_user.id
    numRef = 0
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    requiredInfo = [link,userBCT,ethaddress,emailaddress]
    name  = (str(update.message.from_user.first_name) + " " + str(update.message.from_user.last_name))
    referedBy = user_data.get(YES)
    #ref_List = worksheet.range("I2:I{}".format(worksheet.row_count))

    verify = [user.value for user in ID_List if user.value == str(ID)]

    if str(update.message.from_user.last_name) in name:
        name = name
    else:
        name = str(update.message.from_user.first_name)

    if None in requiredInfo:
        update.message.reply_text("Please fill up all the required informations.", reply_markup=ReplyKeyboardMarkup([[BCT,BCTUSER],[EMAIL],[ETH],[DONE]]))
        return CHOOSING

    else:
        if str(ID) not in verify:
            if referedBy != None:
                referedBy_Find = worksheet.find(referedBy)
                referedByCoords = f"{int(referedBy_Find.row)}{int(referedBy_Find.col)-7}"
                newReferedBy = worksheet.cell(int(referedByCoords[0]), int(referedByCoords[1])).value
                row = [timestamp,user,emailaddress,link,userBCT,ethaddress,ID,newReferedBy,refLink,numRef]
                update.message.reply_text(f"Yay! you are now done..\nHere's your referral link - {refLink} \nJoin now in our Main Channel - https://t.me/joinchat/ILiK_Q7VBLOByz_7mMUgsQ\n Bounty Channel - \nhttps://t.me/curaizonbounty", reply_markup=ReplyKeyboardRemove(reply_keyboard), disable_web_page_preview=True)
                registered.append(update.message.from_user.id)
                worksheet.append_row(row)
                return ConversationHandler.END
            else:
                row = [timestamp,user,emailaddress,link,userBCT,ethaddress,ID,referedBy,refLink,numRef]
                update.message.reply_text(f"Yay! you are now done..\nHere's your referral link - {refLink} \nJoin now in our Main Channel - https://t.me/joinchat/ILiK_Q7VBLOByz_7mMUgsQ\n Bounty Channel - \nhttps://t.me/curaizonbounty", reply_markup=ReplyKeyboardRemove(reply_keyboard), disable_web_page_preview=True)
                registered.append(update.message.from_user.id)
                worksheet.append_row(row)
                return ConversationHandler.END

        else:
            update.message.reply_text("Your account was already registered. You cannot create again.... ", reply_markup=ReplyKeyboardRemove(reply_keyboard))
            registered.append(update.message.from_user.id)
            return ConversationHandler.END

def checkReferral(bot, update):
	update.message.reply_text("Did someone referred you or not?", reply_markup=bool_markup, resize_keyboard=True)

	return CHOOSING

def refBool(bot,update,user_data):
	text = update.message.text
	user_data['choice'] = text

	if text == YES:
		update.message.reply_text("Please type the referrer's referral link", reply_markup=ReplyKeyboardRemove(bool_markup))
		return TYPING_REFER
	else:
		update.message.reply_text("Please skip this step...", reply_markup=ReplyKeyboardMarkup([[BCT,BCTUSER],[EMAIL],[ETH]]))
		return CHOOSING

def received_refer(bot,update,user_data):
	text = update.message.text
	ref_category = user_data['choice']
	user_data[ref_category] = text
	del user_data['choice']

	referral_link = user_data.get(YES)
	ref_List = worksheet.range("I2:I{}".format(worksheet.row_count))
	ref_verify = [user.value for user in ref_List if user.value == referral_link]
	ID = update.message.from_user.id
	verify = [user.value for user in ID_List if user.value == str(ID)]

	if str(ID) not in verify:
		if referral_link in ref_verify:
			refLink_List = worksheet.find(referral_link)
			refCoords = f"{refLink_List.row}{refLink_List.col}"
			changeID = refCoords
			addRefNumber = worksheet.cell(int(changeID[0]),(int(changeID[1])+1)).value

			update.message.reply_text("{}".format(facts_to_str(user_data)), reply_markup=ReplyKeyboardMarkup([[BCT,BCTUSER],[EMAIL],[ETH],[DONE]]))
			worksheet.update_cell(int(changeID[0]),int(changeID[1])+1, int(addRefNumber)+1)
			return CHOOSING
		else:
			update.message.reply_text("Invalid refer", reply_markup=bool_markup)
			return CHOOSING
	else:
		update.message.reply_text("Sorry but you're already been invited by someone's referral link", reply_markup=ReplyKeyboardMarkup([[BCT,BCTUSER],[EMAIL],[ETH],[DONE]]))
		return CHOOSING

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
	print("Cura Bot is running....")
    # Create the Updater and pass it your bot's token.
	updater = Updater("BOT FATHER TOKEN)

    # Get the dispatcher to register handlers
	dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
	conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING:[RegexHandler('^(' + EMAIL + ')$', regular_choice, pass_user_data=True),
            		  RegexHandler('^(' + BCT + ')$', regular_choice, pass_user_data=True),
            		  RegexHandler('^(' + BCTUSER + ')$', regular_choice, pass_user_data=True),
            		  RegexHandler('^(' + ETH + ')$', regular_choice, pass_user_data=True),
            		  RegexHandler('^(' + REFER + ')$', checkReferral),
            		  RegexHandler('^(' + YES + ')$', refBool, pass_user_data=True),
            		  RegexHandler('^(' + NO + ')$', refBool, pass_user_data=True),
                     ],

            TYPING_REPLY:[MessageHandler(Filters.text, received_information, pass_user_data=True)],
            TYPING_REFER:[MessageHandler(Filters.text, received_refer, pass_user_data=True)]
        },

        fallbacks=[RegexHandler('^(' + DONE + ')$', done, pass_user_data=True)]
    )

	dp.add_handler(conv_handler)

    # log all errors
	dp.add_error_handler(error)

    # Start the Bot
	updater.start_polling()
    #Refresh the token every 1 hour
	gsUpdateThread = threading.Thread(target=gspreadUpdater)
	gsUpdateThread.daemon = True
	gsUpdateThread.start()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()

if __name__ == '__main__':
    main()
