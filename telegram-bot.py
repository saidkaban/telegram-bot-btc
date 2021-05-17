#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import logging
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from tzlocal import get_localzone
from datetime import datetime
import schedule, time

local = get_localzone()
# Bot tokeni buraya
TOKEN = "yourtokenhere"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    """ start fonksiyonu """
    update.message.reply_text('Let\'s get started!')

def help(update, context):
    """ Help fonksiyonu"""
    update.message.reply_text('You don\'t need help!')

def getInfo(update, context):
    """ Gereken verileri çekip yazdırıyor """
    data = requests.get('https://dev-api.shrimpy.io/v1/exchanges/coinbasepro/candles?quoteTradingSymbol=USDT&baseTradingSymbol=BTC&interval=1H')
    candles = data.json()[-5:]
    candles = list(map(lambda obj: obj["high"], candles))
    candles = list(map(lambda x: round(float(x), 2), candles))
    maxValue = max(candles)
    output = "Son 5 saatteki en yüksek mum kapanışları\n\n{}\n{}\n{}\n{}\n{}\n\nEn yüksek kapanış: {}".format(candles[0], candles[1], candles[2], candles[3], candles[4], maxValue)
    update.message.reply_text(output)

def timer(update, context):
    getInfo(update, context)
    schedule.every(10).seconds.do(getInfo, update=update, context=context)
    i = 0
    while i < 5:
        schedule.run_pending()
        time.sleep(1)
        i += 1

def error(update, context):
    """ Hata loglama fonksiyonu"""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """ Botun çalıştırıldığı yer"""
    updater = Updater(TOKEN, use_context=True) 

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("test",timer))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

