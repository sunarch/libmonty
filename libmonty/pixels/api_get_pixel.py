# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests
import json

from libmonty.pixels import config

# Get Pixel

# Get a single pixel given the x and y coordinates.
# This endpoint requires an authentication token. See this page for how to authenticate with the API.

API_URL = "https://pixels.pythondiscord.com/get_pixel"


def execute(x: int = None, y: int = None, **kwargs: dict) -> tuple[str, dict]:

    if None in (x, y):

        if kwargs is not None and "x" in kwargs and "y" in kwargs:
            x = kwargs['x']
            y = kwargs['y']

        else:
            raise ValueError("Missing parameter!")

    response = requests.get(
        API_URL,
        headers=config.get_auth_headers(),

        # Note: coordinates as query string parameters,
        #       not in the JSON body
        params={
            "x": x,
            "y": y
        }
    )

    try:
        payload = response.json()
    except json.JSONDecodeError:
        payload = {"rgb": ""}

    try:
        rgb = payload["rgb"]
    except KeyError:
        rgb = ""

    d_return = {
        "response": response,
        "rgb": rgb
    }

    return "GET /get_pixel", d_return


def headers() -> tuple[str, dict]:

    response = requests.head(
        API_URL,
        headers=config.get_auth_headers()
    )

    d_return = {
        "response": response,
    }

    d_return.update(config.parse_headers(response.headers))

    return "HEAD /get_pixel", d_return

# -------------------------------------------------------------------- #
# Response: 200 - Successful Response
# application/json

# Schema

# A pixel as used by the api.
# {
#     x*: integer
#     y*: integer
#     rgb*: string
# }

# Example

# {
#   "x": 120,
#   "y": 67,
#   "rgb": "00FF00"
# }

# -------------------------------------------------------------------- #
# Response: 422 - Validation Error
# application/json

# Schema

# {
#     detail: [{
#         loc*: [string]
#         msg*: string
#         type*: string
#     }]
# }

# Example

# {
#   "detail": [
#     {
#       "loc": [
#         "string"
#       ],
#       "msg": "string",
#       "type": "string"
#     }
#   ]
# }

# -------------------------------------------------------------------- #
