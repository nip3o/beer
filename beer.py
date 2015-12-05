# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import datetime
import random

import requests
import click

from characteristic import attributes

from constants import USER_AGENTS, URLs


@click.command()
@click.argument('username', envvar='BEER_USERNAME')
@click.argument('password', envvar='BEER_PASSWORD')
def main(username, password):
    try:
        bot = BeerBot(username, password)
        print(bot.get_weblaunch_start())

    except LoginException as e:
        print(e.message)

    print()


class LoginException(Exception):
    pass


@attributes(['weblaunch_id', 'product_number', 'product_name', 'url'])
class WebLaunch(object):
    pass


class BeerBot(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()

    def login(self):
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
        }

        response = self.session.post(
            URLs.login,
            headers=headers,
            json={'Username': self.username, 'Password': self.password}
        )

        if not response.status_code == 200 or not response.json()['IsValid']:
            raise LoginException('Incorrect username or password.')

    def get_weblaunches(self):
        self.login()

        response = self.session.get(URLs.get_weblaunches)
        json = response.json()

        if not response.status_code == 200:
            assert False

        return json

    def get_weblaunch_start(self):
        json = self.get_weblaunches()
        if not json:
            return None

        return datetime.datetime.strptime(json[0]['StartDate'], '%Y-%m-%dT%H:%M:%S')

    def get_weblaunch_by_product(self, product_number):
        json = self.get_weblaunches()
        if not json:
            return None

        for item in json:
            if item['Product']['ProductNumber'] == product_number:
                url = URLs.base + item['Product']['ProductUrl']
                return WebLaunch(
                    url=url,
                    product_number=product_number,
                    product_name=item['Product']['ProductNameBold'],
                    weblaunch_id=item['WebLaunchId'],
                )

    def create_booking(self, weblaunch_id, quantity):
        self.login()

        data = {
            'WebLaunchId': weblaunch_id,
            'BookingQuantity': 1,
            'IsQueue': False,
        }
        response = self.session.post(URLs.booking_create, data=data)
        json = response.json()

        if not response.status_code == 200 or not json['IsValid']:
            assert False

        assert json['TotalBookedQuantity'] == quantity


if __name__ == '__main__':
    main()
