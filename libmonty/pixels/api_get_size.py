# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests
import json


# Get Size

# Get the size of the pixels canvas.
# You can use the data this endpoint returns to build some cool scripts that can start the ducky uprising on the canvas!
# This endpoint doesn't require any authentication so dont worry about giving any headers.

API_URL = "https://pixels.pythondiscord.com/get_size"


def execute() -> dict:

    response = requests.get(API_URL)

    try:
        payload = response.json()
        data = response.json()
        data_type = "json"
    except json.JSONDecodeError:
        payload = {}
        data = response.text
        data_type = "text"

    try:
        width = payload["width"]
        height = payload["height"]
    except KeyError:
        width = None
        height = None

    d_result = {
        "request_name": "GET /get_size",
        "response": response,
        "data": data,
        "data_type": data_type,
        "data_encoding": response.encoding,
        "width": width,
        "height": height
    }

    return d_result

# -------------------------------------------------------------------- #
# Response: 200 - Successful Response
# application/json

# Schema

# {
#     width*: integer
#     height*: integer
# }

# Example

# {
#     width: 0,
#     height: 0
# }

# -------------------------------------------------------------------- #
