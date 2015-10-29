# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import requests
import click


class URLs:
    base = 'https://www.systembolaget.se/api/'
    login = base + 'user/authenticate'
    get_weblaunches = base + 'weblaunch/getweblaunches'
    booking_create = base + 'weblaunch/createbooking'


class LoginException(Exception):
    pass


def login(session, username, password):
    response = session.post(URLs.login, data={'Username': username, 'Password': password})

    if not response.status_code == 200 or not response.json()['IsValid']:
        raise LoginException('Incorrect username or password.')


def create_booking(session, weblaunch_id, quantity):
    data = {
        'WebLaunchId': weblaunch_id,
        'BookingQuantity': 1,
        'IsQueue': False,
    }
    response = session.post(URLs.booking_create, data=data)
    json = response.json()

    if not response.status_code == 200 or not json['IsValid']:
        assert False

    assert json['TotalBookedQuantity'] == quantity


@click.command()
@click.argument('username', envvar='BEER_USERNAME')
@click.argument('password', envvar='BEER_PASSWORD')
def main(username, password):
    session = requests.Session()

    try:
        login(session, username, password)
        print('Successfully logged in!')

        create_booking(session, weblaunch_id=336, quantity=1)
        print('Booked')

    except LoginException as e:
        print(e.message)

    print()


if __name__ == '__main__':
    main()
