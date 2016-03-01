# -*- coding: utf-8 -*-
import datetime

import model


def create_beerbot(chat_id):
    from beer import BeerBot

    user = model.get_user(chat_id)
    return BeerBot(user['username'], user['password'])


def string_to_datetime(string):
    return datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%S')


def datetime_to_string(obj):
    return obj.strftime('%Y-%m-%dT%H:%M:%S')
