import logging
import configparser
import os

from telegram import (Update, Sticker, StickerSet)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def handle_voice_note(update: Update, context: CallbackContext):
    if (update.effective_user.id in context.bot_data['jenny_ids']
        or context.bot_data['everyone_is_jenny']):
        context.bot.send_sticker(update.message.chat_id, context.bot_data['sticker_id'], disable_notification=True, reply_to_message_id=update.message.message_id)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    configLocation = os.environ.get('JENNYBOT_CONFIG_LOCATION', './config.ini')

    if (not os.path.isfile(configLocation)):
        logger.fatal('Failed to open config file at %s', configLocation)
        exit(-1)

    config = configparser.ConfigParser()
    
    config.read(configLocation)

    updater = Updater(config['JennyBot']['TelegramToken'], use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.bot_data = {
        'jenny_ids': [int(x) for x in config['JennyBot']['JennyIds'].split(",")],
        'sticker_id': config['JennyBot']['StickerId'],
        'everyone_is_jenny': config['JennyBot'].get('EveryoneIsJenny', 'no') == 'yes'
    }

    dispatcher.add_handler(MessageHandler(Filters.voice, handle_voice_note))

    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()