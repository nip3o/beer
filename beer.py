# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import datetime
import requests
import click


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


class URLs:
    base = 'https://www.systembolaget.se/api/'
    login = base + 'user/authenticate'
    get_weblaunches = base + 'weblaunch/getweblaunches'
    booking_create = base + 'weblaunch/createbooking'


class LoginException(Exception):
    pass


class BeerBot(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()

    def login(self):
        response = self.session.post(URLs.login, data={'Username': self.username, 'Password': self.password})

        if not response.status_code == 200 or not response.json()['IsValid']:
            raise LoginException('Incorrect username or password.')

    def get_weblaunch_start(self):
        self.login()

        response = self.session.get(URLs.get_weblaunches)
        json = response.json()

        if not response.status_code == 200:
            assert False

        if not json:
            return None

        return datetime.datetime.strptime(json[0]['StartDate'], '%Y-%m-%dT%H:%M:%S')

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
