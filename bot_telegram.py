from dataclasses import dataclass
from telegram.ext import Updater, CommandHandler
from cfg import TOKEN

from transmission import TransmissionBroker
from yts import YtsApi

HELP = """Transmission Telegram Bot
Usage:
/help - display this help
/list - retrieve list of current torrents and theirs status
/add <URI> - add torrent and  start download 
/search <TITLE> - search by title and download
"""


@dataclass
class BotTransmission:
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    def start(self):
        start_handle = CommandHandler('start', self.help_command)
        self.dispatcher.add_handler(start_handle)
        add_handle = CommandHandler('add', self.add_command)
        self.dispatcher.add_handler(add_handle)
        list_handle = CommandHandler('list', self.list_command)
        self.dispatcher.add_handler(list_handle)
        search_handle = CommandHandler('search', self.search_command)
        self.dispatcher.add_handler(search_handle)
        self.updater.start_polling()
        self.updater.idle()

    @staticmethod
    def help_command(update, context):
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=HELP)

    @staticmethod
    def add_command(update, context):
        update.message.reply_text('Adding torrent to transmission!')
        data = (update.message.text.replace('/add ', ''))
        data = (data.replace(' ', ''))
        data = tuple(map(str, data.split(',')))
        response = TransmissionBroker.add_torrents(data)
        for torrent in response:
            if torrent:
                update.message.reply_text(f"{torrent} adding successful")
        update.message.reply_text('Want to add another torrents?')

    @staticmethod
    def list_command(update, context):
        response = TransmissionBroker.list_torrents()
        update.message.reply_text(response)
    
    @staticmethod
    def search_command(update, context):
        update.message.reply_text('Searching movies to YTS...')
        data = (update.message.text.replace('/search ', ''))
        data = (data.replace(' ', ''))
        title = tuple(map(str, data.split(',')))
        response = YtsApi.search_custom(title)
        update.message.reply_text(response)


if __name__ == '__main__':
    bot = BotTransmission()
    bot.start()
