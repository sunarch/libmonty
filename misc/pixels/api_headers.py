#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests

from requests.structures import CaseInsensitiveDict

from pixels import config


def request(api_url: str, request_name: str) -> dict:

    response = requests.head(
        api_url,
        headers=config.get_auth_headers()
    )

    d_result = {
        'request_name': request_name,
        'response': response,
        'data': response.text,
        'data_type': "none",
        'data_encoding': response.encoding
    }

    d_result.update(sort_by_type(response.headers))

    return d_result


RATE_LIMIT_COUNT_REMAINING = 'Requests-Remaining'  # (int)
# How many requests you are still allowed to do before waiting.

RATE_LIMIT_COUNT_LIMIT = 'Requests-Limit'  # (int)
# How many requests you can do during a period.

RATE_LIMIT_TIME_RESET = 'Requests-Reset'  # (float)
# How many seconds you must wait without sending a request
# before getting all your requests back.
# `0` if you still have all your requests.

RATE_LIMIT_TIME_PERIOD = 'Requests-Period'  # (int)
# Duration, in seconds, of the ratelimit period.

RATE_LIMIT_COOLDOWN = 'Cooldown-Reset'

RATE_LIMIT_HEADER_LABELS = [
    RATE_LIMIT_COUNT_REMAINING,
    RATE_LIMIT_COUNT_LIMIT,
    RATE_LIMIT_TIME_RESET,
    RATE_LIMIT_TIME_PERIOD
]


def sort_by_type(headers: CaseInsensitiveDict) -> dict:

    d_rate_limit_info = {}
    s_rate_limit_cooldown = None
    d_regular_headers = {}

    for s_header_tag in headers:
        if s_header_tag in RATE_LIMIT_HEADER_LABELS:
            d_rate_limit_info[s_header_tag] = headers[s_header_tag]
        elif s_header_tag == RATE_LIMIT_COOLDOWN:
            s_rate_limit_cooldown = headers[s_header_tag]
        else:
            d_regular_headers[s_header_tag] = headers[s_header_tag]

    return {
        'rate_limits': d_rate_limit_info,
        'cooldown': s_rate_limit_cooldown,
        'headers': d_regular_headers
    }

# -------------------------------------------------------------------- #
