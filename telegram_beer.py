# -*- coding: utf-8 -*-
from __future__ import print_function

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
            update_id = whatever(bot, update_id)

        except telegram.TelegramError as e:
            # These are network problems with Telegram.
            if e.message in ("Bad Gateway", "Timed out"):
                sleep(1)
            else:
                raise e

        except URLError as e:
            # These are network problems on our end.
            sleep(1)


def whatever(bot, update_id):
    for update in bot.getUpdates(offset=update_id, timeout=10):
        print(update.message)

        try:
            authenticate(update)
            responses = get_responses_for(bot, update.message)

            for response in (responses or []):
                bot.sendMessage(chat_id=update.message.chat_id, text=response)

        except InvalidCommand as e:
            bot.sendMessage(chat_id=update.message.chat_id, text=e.message)

        update_id = update.update_id + 1

    return update_id


def authenticate(update):
    telegram_user = os.environ.get('BEER_TELEGRAM_USER')

    if telegram_user and not update.message.from_user.username == telegram_user:
        raise InvalidCommand('I do not know you. You shall not pass.')


def get_responses_for(bot, message):
    if message.text == '/when':
        return when(bot)


def when(bot):
    username = os.environ['BEER_USERNAME']
    password = os.environ['BEER_PASSWORD']

    remote = BeerBot(username, password)
    start = remote.get_weblaunch_start()

    if not start:
        return ['There are no planned events right now.']

    if start >= datetime.datetime.now():
        days = (start - datetime.datetime.now()).days
        text = 'Next event opens at {} ({} days).'.format(start, days)
    else:
        text = 'There is an open event right now (started at {}).'.format(start)

    return ["""
{}

https://www.systembolaget.se/fakta-och-nyheter/nyheter-i-sortimentet/webblanseringar/webblansering/
""".format(text)]


if __name__ == '__main__':
    main()
