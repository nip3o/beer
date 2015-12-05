# -*- coding: utf-8 -*-
import os
import datetime


def create_beerbot():
    from beer import BeerBot

    username = os.environ['BEER_USERNAME']
    password = os.environ['BEER_PASSWORD']
    return BeerBot(username, password)


def string_to_datetime(string):
    return datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%S')


def datetime_to_string(obj):
    return obj.strftime('%Y-%m-%dT%H:%M:%S')
