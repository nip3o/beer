# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import click
import telegram

import model

from utils import create_beerbot, datetime_to_string, string_to_datetime


@click.command()
@click.argument('api_token', envvar='BEER_TELEGRAM_API_TOKEN')
def main(api_token):
    beer_bot = create_beerbot()
    telegram_bot = telegram.Bot(api_token)

    start = beer_bot.get_weblaunch_start()
    if not start:
        return

    subscriptions = model.load_weblaunch_subscriptions()

    for chat_id, latest_weblaunch_date in subscriptions.iteritems():
        if start == string_to_datetime(latest_weblaunch_date):
            continue

        send_weblaunch_notification(start, chat_id, telegram_bot)
        subscriptions[chat_id] = datetime_to_string(start)

    model.save_weblaunch_subscriptions(subscriptions)


def send_weblaunch_notification(start, chat_id, telegram_bot):
    text = """
Hi there! It seems to be a web launch available (start {}).

https://www.systembolaget.se/fakta-och-nyheter/nyheter-i-sortimentet/webblanseringar/webblansering/
    """.format(start)

    telegram_bot.sendMessage(chat_id=chat_id,
                             text=text,
                             disable_web_page_preview=True)

if __name__ == '__main__':
    main()
