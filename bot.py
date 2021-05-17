import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from tracker import get_info

telegram_bot_token = "yourtokenhere"

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher

def test(update, context):
    chat_id = update.effective_chat.id
    message = get_info()

    context.bot.send_message(chat_id=chat_id, text=message)

dispatcher.add_handler(CommandHandler("test", test))
updater.start_polling()