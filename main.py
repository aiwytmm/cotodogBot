from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.ext.dispatcher import run_async
import requests
import re

def get_url(type):
    if type == 1:
        contents = requests.get('https://random.dog/woof.json').json()
        url = contents['url']
    elif type == 2:
        contents = requests.get('https://api.thecatapi.com/v1/images/search').json()
        url = contents[0]['url']
    else:
        contents = requests.get('https://randomfox.ca/floof').json()
        url = contents['image']
    return url

def get_image_url(type):
    allowed_extension = ['jpg','jpeg','png','gif']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url(type)
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

@run_async
def start(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id,
                             text="Hi! I can send you a random animal pic to make your day a little bit better!\n" + "\n" +
                                "To get picture of cat press /cat\n" +
                                "To get picture of dog press /dog\n" +
                                "To get picture of fox press /fox\n")

def dog(update, context):
    url = get_image_url(1)
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)

def fox(update, context):
    url = get_image_url(0)
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)

def cat(update, context):
    url = get_image_url(2)
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)

def main():
    updater = Updater('TELEGRAM_BOT_TOKEN', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('dog',dog))
    dp.add_handler(CommandHandler('fox',fox))
    dp.add_handler(CommandHandler('cat',cat))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()