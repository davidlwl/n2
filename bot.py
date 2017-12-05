import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import time
from telegram import InlineQueryResultArticle, ChatAction, InputTextMessageContent

bot = telegram.Bot(token='343469925:AAHrvVL-rW3ixMG95u2-ehzPus5k5qmvNTE')
updater = Updater(token='343469925:AAHrvVL-rW3ixMG95u2-ehzPus5k5qmvNTE')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater.start_polling()

def start(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    bot.sendMessage(chat_id=update.message.chat_id, text= "I'm ahbid, please talk to me! \nType /problem to tell me your problems, \nType /weather to get the weather, \nType /news to get the latest news, \nOr simple type anything to begin our conversation! ")
        
                    
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

    

    
