import requests
from bs4 import BeautifulSoup
import telegram
from telegram.ext import Updater, CommandHandler

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! Send me the name of a song to download from Saavn.")

def download_song(update, context):
    song_name = ' '.join(context.args)
    saavn_url = 'https://www.saavn.com/search/{}'.format(song_name.replace(' ', '%20'))
    response = requests.get(saavn_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    song_url = soup.select_one('.song-wrap a').get('href')
    response = requests.get(song_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    download_url = soup.select_one('.download')[0].get('href')
    context.bot.send_message(chat_id=update.effective_chat.id, text="Downloading {}...".format(song_name))
    context.bot.send_audio(chat_id=update.effective_chat.id, audio=download_url)

updater = Updater('6183906442:AAE6PduZy5Ppemwy0lWRf5Y8b_XZFHgvWek', use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('download', download_song))
updater.start_polling()
updater.idle()
