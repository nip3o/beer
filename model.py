# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import os
import json


USERS_FILENAME = 'users.json'
BOOKINGS_FILENAME = 'bookings.json'
WEBLAUNCH_FILENAME = 'weblaunches.json'


def _load_weblaunch_subscriptions():
    if not os.path.exists(WEBLAUNCH_FILENAME):
        return {}

    with open(WEBLAUNCH_FILENAME, 'r') as f:
        return json.load(f)


def _save_weblaunch_subscriptions(value):
    with open(WEBLAUNCH_FILENAME, 'w') as f:
        json.dump(value, f)


def _load_weblaunch_bookings():
    if not os.path.exists(BOOKINGS_FILENAME):
        return {}

    with open(BOOKINGS_FILENAME, 'r') as f:
        return json.load(f)


def _save_weblaunch_bookings(value):
    with open(BOOKINGS_FILENAME, 'w') as f:
        json.dump(value, f)


def _load_users():
    if not os.path.exists(USERS_FILENAME):
        return {}

    with open(USERS_FILENAME, 'r') as f:
        return json.load(f)


def _save_users(value):
    with open(USERS_FILENAME, 'w') as f:
        json.dump(value, f)


def add_weblaunch_subscription(chat_id):
    subscriptions = _load_weblaunch_subscriptions()
    subscriptions[unicode(chat_id)] = None
    _save_weblaunch_subscriptions(subscriptions)


def add_weblaunch_booking(chat_id, weblaunch_id):
    bookings = _load_weblaunch_bookings()
    chat_bookings = bookings.get(unicode(chat_id), [])
    chat_bookings.append(weblaunch_id)

    bookings[unicode(chat_id)] = chat_bookings
    _save_weblaunch_bookings(bookings)


def add_user(chat_id, username, password):
    users = _load_users()
    users[unicode(chat_id)] = {
        'username': username,
        'password': password,
    }
    _save_users(users)


def get_user(chat_id):
    users = _load_users()
    return users.get(unicode(chat_id))
