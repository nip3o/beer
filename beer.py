# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import requests
import click


class URLs:
    base = 'https://www.systembolaget.se/api/'
    login = base + 'user/authenticate'


class LoginException(Exception):
    pass


def login(session, username, password):
    response = session.post(URLs.login, data={'Username': username, 'Password': password})

    if not response.status_code == 200 or response.json()['IsValid'] is False:
        raise LoginException('Incorrect username or password.')


@click.command()
@click.argument('username', envvar='BEER_USERNAME')
@click.argument('password', envvar='BEER_PASSWORD')
def main(username, password):
    session = requests.Session()

    try:
        login(session, username, password)
        print('Successfully logged in!')

    except LoginException as e:
        print(e.message)

    print()


if __name__ == '__main__':
    main()
