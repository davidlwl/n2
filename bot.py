import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import time
from telegram import InlineQueryResultArticle, ChatAction, InputTextMessageContent

import requests
from bs4 import BeautifulSoup
import random
import datetime
import emoji
import urllib.request
import json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import time
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords


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


def weather(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    url = 'https://www.google.com.sg/search?q=show+singapore+weather&oq=show+singapore+weather&aqs=chrome..69i57.3136j0j7&sourceid=chrome&ie=UTF-8'
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'lxml')
    quote = soup.find_all('span', attrs={'class':'wob_t'})
    weath = soup.find_all('img', alt=True)

    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d")
    bot.sendMessage(chat_id=update.message.chat_id, text= time + "\n"  + "Current Temperature: " + quote[0].string  + '\n' + "weather: " + weath[0]['alt'] + '\n'
          "Range: " + quote[3].string + " - " + quote[2].string)
    
weather_handler = CommandHandler('weather', weather)
dispatcher.add_handler(weather_handler)
    

    
