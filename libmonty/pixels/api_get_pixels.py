# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests

from libmonty.pixels import config

# Get Pixels

# Get the current state of all pixels from the database.
# This endpoint requires an authentication token. See this page for how to authenticate with the API.

API_URL = "https://pixels.pythondiscord.com/get_pixels"


def execute() -> tuple[str, dict]:

    response = requests.get(
        API_URL,
        headers=config.get_auth_headers()
    )

    data = response.content

    d_return = {
        "response": response,
        "data": data
    }

    return "GET /get_pixels", d_return


def headers() -> tuple[str, dict]:

    response = requests.head(
        API_URL,
        headers=config.get_auth_headers()
    )

    d_return = {
        "response": response,
    }

    d_return.update(config.parse_headers(response.headers))

    return "HEAD /get_pixels", d_return

# -------------------------------------------------------------------- #
# Response: 200 - Successful Response
# application/octet-stream

# -------------------------------------------------------------------- #
# Example handling

# pixels = "... # Fetch pixel state from /get_pixels"

# first_pixel = pixels[0:3]
# b'\xfd\xd2\x81'

# r = first_pixel[0]  # 253
# g = first_pixel[1]  # 210
# b = first_pixel[2]  # 129

# -------------------------------------------------------------------- #
