# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import os
import click
import telegram
import datetime

from time import sleep
from urllib2 import URLError

from beer import BeerBot


class InvalidCommand(Exception):
    pass


@click.command()
@click.argument('api_token', envvar='BEER_TELEGRAM_API_TOKEN')
def main(api_token):
    bot = telegram.Bot(api_token)
    update_id = 0

    while True:
        try:
            update_id = fetch_and_handle_messages(bot, update_id)

        except telegram.TelegramError as e:
            # These are network problems with Telegram.
            if e.message in ("Bad Gateway", "Timed out"):
                sleep(1)
            else:
                raise e

        except URLError as e:
            # These are network problems on our end.
            sleep(1)


def fetch_and_handle_messages(bot, update_id):
    for update in bot.getUpdates(offset=update_id, timeout=10):
        print(update.message)

        try:
            authenticate(update)
            response = get_responses_for(update.message)

            if response:
                bot.sendMessage(chat_id=update.message.chat_id, **response)

        except InvalidCommand as e:
            bot.sendMessage(chat_id=update.message.chat_id, text=e.message)

        update_id = update.update_id + 1

    return update_id


def authenticate(update):
    telegram_user = os.environ.get('BEER_TELEGRAM_USER')

    if telegram_user and not update.message.from_user.username == telegram_user:
        raise InvalidCommand('I do not know you. You shall not pass.')


def get_responses_for(message):
    if message.text == '/when':
        return when()

    if message.text.startswith('/add'):
        return add(message.text)


def create_beerbot():
    username = os.environ['BEER_USERNAME']
    password = os.environ['BEER_PASSWORD']
    return BeerBot(username, password)


def when():
    start = create_beerbot().get_weblaunch_start()

    if not start:
        return {'text': 'There are no planned events right now.'}

    if start >= datetime.datetime.now():
        days = (start - datetime.datetime.now()).days
        text = 'Next event opens at {} ({} days).'.format(start, days)
    else:
        text = 'There is an open event right now (started at {}).'.format(start)

    return {'disable_web_page_preview': True, 'text': """
{}

https://www.systembolaget.se/fakta-och-nyheter/nyheter-i-sortimentet/webblanseringar/webblansering/
""".format(text)}


def add(message):
    product_number = message[4:].strip()

    if not product_number:
        return {'text': 'Which product number should be added?', 'force_reply': True}

    weblaunch = create_beerbot().get_weblaunch_by_product(product_number)

    if not weblaunch:
        return {'text': 'Could not find any web launch for that product.'}

    add_weblaunch(weblaunch.weblaunch_id)

    return {'text': 'Will book "{}"\n{}'.format(weblaunch.product_name, weblaunch.url)}


def add_weblaunch(weblaunch_id):
    pass


if __name__ == '__main__':
    main()
