import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import time
from telegram import InlineQueryResultArticle, ChatAction, InputTextMessageContent
import calendar
from datetime import date

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
    my_date = date.today()
    
    update.message.reply_text(time + " " + calendar.day_name[my_date.weekday()] + "\n"  + "Current Temperature: " + quote[0].string  + '\n' + "weather: " + weath[0]['alt'] + '\n'
          "Range: " + quote[3].string + " - " + quote[2].string)
    
weather_handler = CommandHandler('weather', weather)
dispatcher.add_handler(weather_handler)
nltk.data.path.append('nltk_data')

def strip(word):
    return word.strip().strip(',').strip(':').strip('(').strip(')').lower()


def get_only_text(url):
    page = urllib.request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(page, 'lxml')
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return soup.title.text, text

def news(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    newsworthy = 'http://www.straitstimes.com/print/top-of-the-news/rss.xml'
    feed_xml = urllib.request.urlopen(newsworthy).read()
    feed = BeautifulSoup(feed_xml.decode('utf8'), 'lxml')
    to_summarize = list(map(lambda p: p.text, feed.find_all('guid')))

    for article_url in to_summarize[:10]:
        i = to_summarize[:10].index(article_url)
        title, text = get_only_text(article_url)
        bot.sendMessage(chat_id=update.message.chat_id, text='<b>' + str(i+1) + ". " + title[:-20] +'</b>' +'\n' + article_url, parse_mode=telegram.ParseMode.HTML)
        
        #take out specific stop words
        stop_words = set(stopwords.words('english'))
        #split input text into sentences
        input_text = sent_tokenize(text)
        #getting freq of each word into a dict  
        word_values = {}

        for sentence in input_text:
            words = sentence.split(' ')
            for word in words:
                word = strip(word)
                if not word in stop_words:
                    if not word in word_values:
                        word_values[word] = 1
                    else:
                        word_values[word] += 1


        sentence_values = []
        for sentence in input_text:
            sentence_value = 0   
            words = sentence.split(' ')
            for word in words:
            #counts the sentence value using word_values dictionary
                sentence_value += word_values.setdefault(word, 0)
            sentence_values.append(sentence_value)
            
            

        #how many sentences do you want = output_num
        for ii in range(0, 2):
            highest_val_ind = sentence_values.index(max(sentence_values))
            
            update.message.reply_text(input_text[highest_val_ind])
            del input_text[highest_val_ind]
            del sentence_values[highest_val_ind]

    bot.sendMessage(chat_id=update.message.chat_id, text='<a href="http://libproxy.smu.edu.sg/login/sto1">Free Access!</a>', parse_mode=telegram.ParseMode.HTML)
                      
news_handler = CommandHandler('news', news)
dispatcher.add_handler(news_handler)


def shows(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    reply_keyboard = [['Yes', 'No']]

    update.message.reply_text('Do you need suggestions?',
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
shows_handler = CommandHandler('shows', shows)
dispatcher.add_handler(shows_handler)


def echo(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING) 
    if update.message.text == 'Yes':
        update.message.reply_text("http://www.imdb.com/search/title?groups=top_250&sort=user_rating&my_ratings=exclude")
    elif update.message.text == 'No':
        update.message.reply_text('What movie/tv show would you like to watch today? ')
        pass
    else:
        update.message.reply_text('https://bmovies.is/search?keyword=' + update.message.text.replace(' ', '+'))
        update.message.reply_text('https://www.google.com.sg/search?ei=CmUmWtmXNcqMvQSRp6_QDA&q=site%3Atvshows4mobile.com+' + update.message.text.replace(' ', '+'))
        update.message.reply_text('https://www.google.com.sg/search?ei=72UmWseQA4XUvgTsv4CwDA&q=site%3Ahdmp4mania.mobi+' + update.message.text.replace(' ', '+'))

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)


#do command to clear all message 
#added last
def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

    
