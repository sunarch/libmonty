# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import dotenv
import os

from requests.structures import CaseInsensitiveDict


def load_token_once() -> None:

    dotenv.load_dotenv(f"libmonty/pixels/.env")


def get_token() -> str:

    return os.getenv("TOKEN")


def get_auth_headers() -> dict:

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    return headers


RATE_LIMIT_HEADER_LABELS = [

    "Requests-Remaining",  # (int)
    # How many requests you are still allowed to do before waiting.

    "Requests-Limit",  # (int)
    # How many requests you can do during a period.

    "Requests-Period",  # (int)
    # Duration, in seconds, of the ratelimit period.

    "Requests-Reset",  # (float)
    # How many seconds you must wait without sending a request
    # before getting all your requests back.
    # `0` if you still have all your requests.

    "Cooldown-Reset"
]


def parse_headers(headers: CaseInsensitiveDict) -> dict:

    d_headers_filtered = {}

    for s_header_tag in RATE_LIMIT_HEADER_LABELS:
        if s_header_tag in headers:
            d_headers_filtered[s_header_tag] = headers[s_header_tag]

    return d_headers_filtered

# -------------------------------------------------------------------- #
