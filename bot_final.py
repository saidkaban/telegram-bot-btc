import logging
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from tzlocal import get_localzone
from datetime import datetime
import schedule, time, threading

local = get_localzone()

TOKEN = "yourtokenhere"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text('Let\'s get started!')

def help(update, context):
    update.message.reply_text('You don\'t need help!')

def getInfo(update, context):
    data = requests.get('https://dev-api.shrimpy.io/v1/exchanges/coinbasepro/candles?quoteTradingSymbol=USDT&baseTradingSymbol=BTC&interval=1H')
    candles = data.json()[-5:]
    candles = list(map(lambda obj: obj["close"], candles))
    maxValue = max(candles)
    output = "Son 5 saatteki en yüksek mum kapanışları\n\n{}\n{}\n{}\n{}\n{}\n\nEn yüksek kapanış: {}".format(candles[0],candles[1],candles[2],candles[3],candles[4],maxValue)
    update.message.reply_text(output)
    print("deneme")


def run_continuously(interval=1):
    cease_continuous_run = threading.Event()
    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)
    
    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

def timer(update, context):
    getInfo(update, context)
    schedule.every().hour.at(":02").do(getInfo,update=update, context=context)
    stop_run_continuously = run_continuously()
    
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = Updater(TOKEN, use_context=True) 

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("timer",timer))
    dp.add_handler(CommandHandler("test",getInfo))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()