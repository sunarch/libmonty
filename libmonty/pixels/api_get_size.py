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


def execute():

    response = requests.get(API_URL)

    width, height = _parse(response)

    d_return = {
        "response": response,
        "width": width,
        "height": height
    }

    return "GET /get_size", d_return


def _parse(response) -> tuple[str, str]:

    try:
        payload = response.json()
    except json.JSONDecodeError:
        payload = {"width": "", "height": ""}

    return payload["width"], payload["height"]

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
