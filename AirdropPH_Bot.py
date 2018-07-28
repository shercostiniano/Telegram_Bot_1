from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler)

import logging
from textwrap import dedent

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

CHOOSING, MENU_REQ, MENU_REM, MENU_FAQ = range(4)

REQ = 'Requirements'
REM = 'Safety Reminders'
FAQ = 'Frequently Asked Questions'
WALLETS = "1.Wallets"
SOCIAL = "2.Social Media Accounts"
MESSAGE = "3.Messaging Platform"
KYC = "4.For KYC Airdrops"
GMAIL = "5.Gmail Accounts"
EXCHANGE = "6.Exchanges where to swap your airdrops"
BOUNTY = "7.Bounty Extensions"
TUTORIAL = "8.Tutorial Links"

#MENU REQUIREMENT
REQ_info_1 = ("""1. Wallets
   -Ethereum Wallet 
      https://mycrypto.com/account
   -Stellar Wallet
      https://www.stellar.org/lumens/wallets/
   -Wave Wallet
      https://wavesplatform.com/
	""")
REQ_info_2 =("""2. Social Media Account
   -Facebook
   -Twitter
   -Bitcointalk
      https://bitcointalk.org
   -Reddit
	""")
REQ_info_3 =("""3.Messaging Platform
   -Discord
   -Telegram
	""")
REQ_info_4 =("""4.For "KYC Airdrops"
   Accepted
      -Passport
      -Drivers License
	"For security purposes use a watermark on every picture that you upload"
	""")
REQ_info_5 =("""5. Gmail Account
	-Create a new one
	-Avoid using your personal mail
	""")
REQ_info_6 =("""6. Exchanges where to swap your airdrops
	-IDEX
	-Forkdelta
	-Gate
	-Hotbit
	-Bilaxy

	"Exchanges will be announced by the team behind the project"
	""")
REQ_info_7 =("""7. Bounty Extensions
	Bountyhive
		https://bit.ly/2mhQcCW
	""")
REQ_info_8 =("""8. Tutorial Links
	Creating your Ethereum Wallet 
	https://drive.google.com/open?id=17DFJ33hfwFRuMusOe7PSAKmE3QyUtqQ_
	""")

inline_keyboard = [[InlineKeyboardButton(WALLETS, callback_data='1')],
			   [InlineKeyboardButton(SOCIAL, callback_data='2')],
			   [InlineKeyboardButton(MESSAGE, callback_data='3')],
			   [InlineKeyboardButton(KYC, callback_data='4')],
			   [InlineKeyboardButton(GMAIL, callback_data='5')],
			   [InlineKeyboardButton(EXCHANGE, callback_data='6')],
			   [InlineKeyboardButton(BOUNTY, callback_data='7')],
			   [InlineKeyboardButton(TUTORIAL, callback_data='8')]]
main_keyboard = [[REQ],[REM],[FAQ]]
inline_markup = InlineKeyboardMarkup(inline_keyboard)
markup = ReplyKeyboardMarkup(main_keyboard)

def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="I'm SherBot!")
	update.message.reply_text(
        "Hi! I am Stephen Airdrop Bot, deployed by the Aliens.\n"
        "My job is to give you a ride to the moon!\n"
        "I don’t want to bore you with the details, so go ahead and check out this walkthrough guide before interacting with me!\n"
        "\n-------------------Lets Get Started-----------------",
        reply_markup = (markup), disable_web_page_preview=True)

	return CHOOSING

def requirement(bot, update):

	update.message.reply_text("Hi what do you wanna know?", reply_markup=(inline_markup), disable_web_page_preview=True)

def menu_requirements(bot, update):
	query = update.callback_query
	if query.data == '1':
		bot.edit_message_text(text=REQ_info_1, chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=inline_markup, disable_web_page_preview=True)
	elif query.data == '2':
		bot.edit_message_text(text=REQ_info_2, chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=inline_markup, disable_web_page_preview=True)
	elif query.data == '3':
		bot.edit_message_text(text=REQ_info_3, chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=inline_markup, disable_web_page_preview=True)
	elif query.data == '4':
		bot.edit_message_text(text=REQ_info_4, chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=inline_markup, disable_web_page_preview=True)
	elif query.data == '5':
		bot.edit_message_text(text=REQ_info_5, chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=inline_markup, disable_web_page_preview=True)
	elif query.data == '6':
		bot.edit_message_text(text=REQ_info_6, chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=inline_markup, disable_web_page_preview=True)
	elif query.data == '7':
		bot.edit_message_text(text=REQ_info_7, chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=inline_markup, disable_web_page_preview=True)
	else:
		bot.edit_message_text(text=REQ_info_8, chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=inline_markup, disable_web_page_preview=True)	

def reminder(bot, update):
	update.message.reply_text(""" 
		------------------Safety Reminders---------------

		-Airdrop PH will not send you a message asking for payments, personal information, & Etc,.

		-Airdrop PH is not accountable for the security measures as always "Do your Own Research" when it comes to clicking website and filling up forms 
		We will do our best to provide a safe airdrop links but always stay on guard at all times.

		-Avoid storing your private key below your public key to avoid being hacked dont fill up forms that requires private key an airdrop does not need a private key 

		-Avoid airdrops that requires you to send a portion of ethereum or any cryptocurrency assets.

		""")

def faq(bot, update):

	update.message.reply_text(""" 
		-----------Mostly Asked Questions----------
		Q: When Moon ?
		A: Ride A Rocket Then Moon
		""")

def main():
	updater = Updater("655485042:AAFmWGTiqhzNyh0-FJX1myCtF5wf-VQJZYk")
	dp = updater.dispatcher
	conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING:[RegexHandler('^(' + REQ + ')$', requirement),
            		  RegexHandler('^(' + REM + ')$', reminder),
            		  RegexHandler('^(' + FAQ + ')$', faq),
                     ],
        },

        fallbacks=[CommandHandler('start', start)]
    )
    
	dp.add_handler(CallbackQueryHandler(menu_requirements))
	dp.add_handler(conv_handler)
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
    main()