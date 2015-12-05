# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import os
import json


WEBLAUNCH_FILENAME = 'weblaunches.json'


def load_weblaunch_subscriptions():
    if not os.path.exists(WEBLAUNCH_FILENAME):
        return {}

    with open(WEBLAUNCH_FILENAME, 'r') as f:
        return json.load(f)


def save_weblaunch_subscriptions(value):
    with open(WEBLAUNCH_FILENAME, 'w') as f:
        json.dump(value, f)


def add_weblaunch_subscription(chat_id):
    subscriptions = load_weblaunch_subscriptions()
    subscriptions[chat_id] = None
    save_weblaunch_subscriptions(subscriptions)
