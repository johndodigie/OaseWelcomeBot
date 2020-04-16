import logging
import configparser
import os

from telegram import (Update, Sticker, StickerSet)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def send_message(update: Update, context: CallbackContext):
    message = "Hallo " + update.effective_message.new_chat_members[0].first_name +""", 
willkommen in der WohlfühlOase.
Bevor es los geht gibt es hier erst einmal paar Infos für dich.
1. Ab heute heißt du Patrick, genauso wie jede andere Person hier in der Gruppe.
2. Die Dichte an ITlern und kaputten Menschen ist sehr hoch, wir hoffen für dich dass du auch eine dieser Personen bist.
3. Robin tut immer so als wäre er "normal" und nicht durchgeknallt, einfach ignorieren

Und nun benötigen wir noch einige Infos von dir!
1. Deine Kreditkartendaten, wir müssen ja sicher gehen dass die Zahlungen an Robin auch ordnungsgemäß und zeitig ankommen. Wenn plötzlich komische Abbuchungen auftauchen musst du dich nicht wundern, ist alles normal.
2. Körbchengröße, frag nicht wieso, ist so.

Und jetzt herzlich willkommen unter den bekloppten Patrick!"""
    # print(message)
    context.bot.send_message(update.message.chat_id, message, disable_notification=True)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    configLocation = 'config.ini'

    if (not os.path.isfile(configLocation)):
        logger.fatal('Failed to open config file at %s', configLocation)
        exit(-1)

    config = configparser.ConfigParser()
    
    config.read(configLocation)

    updater = Updater(config['OaseWelcomeBot']['TelegramToken'], use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, send_message))

    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()