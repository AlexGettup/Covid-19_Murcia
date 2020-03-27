import os
import datetime
import logging
from telegram.ext import CommandHandler, Updater
import bs4
import requests

TOKEN = '1083509739:AAH5Txt9Zq_zJ6ooLQFF5nmIGO7ryOunfsA'
PORT = int(os.environ.get('PORT', '8443'))


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Envia /info para saber la informacion actual de "
                                                                    "los afectados por coronavirus en la región "
                                                                    "de Murcia.")


def info(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Descargando información, un momento...")

    # Get the day
    dt = datetime.datetime.today()
    date = dt.strftime("%d_%m_%y")

    # Retrieve the image url
    res = requests.get('http://www.murciasalud.es/pagina.php?id=458440')
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    div = soup.find('div', id='coronavirus')
    soup = bs4.BeautifulSoup(str(div), "html.parser")
    ases = soup.find_all('a')
    href = ases[len(ases) - 1]['href']
    href += '&?a=' + datetime.datetime.now().isoformat()

    # Save the image♂
    # res = requests.get('http://www.murciasalud.es/' + href, allow_redirects=True)
    # print(res.text)
    # open(filename, 'wb').write(res.content)

    # Send image
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=('http://www.murciasalud.es/' + href))
    context.bot.send_message(chat_id=update.effective_chat.id, text=date)


# Updater
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Handler
start_handler = CommandHandler('start', start)
info_handler = CommandHandler('info', info)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(info_handler)

# Start
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
updater.bot.set_webhook("https://coronavirusmurciabot.herokuapp.com/" + TOKEN)
updater.idle()
