# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests

from libmonty.pixels import config
from libmonty.pixels import api_headers

# Get Pixels

# Get the current state of all pixels from the database.
# This endpoint requires an authentication token. See this page for how to authenticate with the API.

API_URL = "https://pixels.pythondiscord.com/get_pixels"

API_NAME_GET = "GET /get_pixels"
API_NAME_HEAD = "HEAD /get_pixels"


def execute() -> dict:

    response = requests.get(
        API_URL,
        headers=config.get_auth_headers()
    )

    d_result = {
        "request_name": API_NAME_GET,
        "response": response,
        "data": f"#length: {len(response.content)}",
        "data_type": "octet-stream",
        "data_encoding": "raw",
        "bytes": response.content
    }

    d_result.update(api_headers.sort_by_type(response.headers))

    return d_result


def headers() -> dict:

    return api_headers.request(API_URL, API_NAME_HEAD)

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
