# -*- coding: utf-8 -*-
from __future__ import unicode_literals

USER_AGENTS = [
    'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36',  # noqa
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',  # noqa
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
]


class URLs:
    base = 'https://www.systembolaget.se'
    api_base = base + '/api/'
    login = api_base + 'user/authenticate/'
    get_weblaunches = api_base + 'weblaunch/getweblaunches'
    booking_create = api_base + 'weblaunch/createbooking'
