from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import pickle

with open('credentials/telegram.token', 'rb') as handle:
    TELEGRAM_TOKEN = pickle.load(handle)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def echo(bot, update):
    splited_text = update.message.text.lower()
    if 'biene' in splited_text:
        chat_id = update.message.chat.id
        update.message.reply_text("BIENE!")
        message = bot.send_video(video='http://cultofthepartyparrot.com/parrots/hd/parrot.gif',
                                 chat_id=chat_id)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater(TELEGRAM_TOKEN)

    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()