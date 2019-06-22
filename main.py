from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
import datetime
from generate_gifs import make_fun_gif


TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def echo(bot, update):
    images = update.message.photo
    image_path = ""
    print(image_path)

    if len(images) > 0:
        try:
            image_path = bot.get_file(images[-1].file_id)
        except Exception as e:
            print(
                "Exception occured at create_new_qrcode_continue, image_path is not initialized ({})".format(e))
            image_path = ""

    output_file = 'user-image-%s.gif' % datetime.datetime.now().strftime('%Y-%M-%d-%H-%M-%S')

    newFile = bot.getFile(image_path)
    newFile.download(output_file)


    url = make_fun_gif(output_file)

    chat_id = update.message.chat.id
    update.message.reply_text("Держи!")
    message = bot.send_video(video=url,
                             chat_id=chat_id)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater(TELEGRAM_TOKEN)

    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.photo, echo))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()