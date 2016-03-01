# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import os
import click
import telegram
import datetime

import model

from time import sleep
from urllib2 import URLError

from utils import create_beerbot
from beer import BeerBot, LoginException


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
            response = get_responses_for(update)

            if response:
                bot.sendMessage(chat_id=update.message.chat_id, **response)

        except InvalidCommand as e:
            bot.sendMessage(chat_id=update.message.chat_id, text=e.message)

        update_id = update.update_id + 1

    return update_id


def authenticate(update):
    telegram_users = os.environ.get('BEER_TELEGRAM_USER')

    if telegram_users and update.message.from_user.username not in telegram_users:
        raise InvalidCommand('Invalid Telegram user. You shall not pass.')


def require_user(wrapped):
    def fn(update):
        if not model.get_user(update.message.chat_id):
            raise InvalidCommand('No user added. Run /register to add a user.')
        return wrapped(update)

    return fn


def get_responses_for(update):
    message = update.message

    if message.text == '/when':
        return command_when(update)

    if message.text.startswith('/add'):
        return command_add(update)

    if message.text.startswith('/start'):
        return command_start(update)

    if message.text.startswith('/register'):
        return command_register(update)


def command_start(update):
    model.add_weblaunch_subscription(update.message.chat_id)


def command_register(update):
    parts = update.message.text.split()

    if not len(parts) == 3:
        raise InvalidCommand('Usage: /register username password')

    username, password = parts[1:]
    try:
        BeerBot(username, password).get_weblaunch_start()
    except LoginException:
        return {'text': 'Invalid username or password.'}

    model.add_user(update.message.chat_id, username, password)
    return {'text': 'Created user.'}


@require_user
def command_when(update):
    try:
        start = create_beerbot(update.message.chat_id).get_weblaunch_start()
    except LoginException:
        return {'text': 'Could not log in.'}

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


@require_user
def command_add(update):
    message = update.message.text

    if not message:
        raise InvalidCommand('Usage: /add product-number')

    product_number = message[4:].strip()
    try:
        weblaunch = create_beerbot(update.message.chat_id).get_weblaunch_by_product(product_number)
    except LoginException:
        return {'text': 'Could not log in.'}

    if not weblaunch:
        return {'text': 'Could not find any web launch for that product.'}

    model.add_weblaunch_booking(update.message.chat_id, weblaunch.weblaunch_id)
    return {'text': 'Will book "{}"\n{}'.format(weblaunch.product_name, weblaunch.url)}


if __name__ == '__main__':
    main()
