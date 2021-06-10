# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests
import json

from libmonty.pixels import config
from libmonty.pixels import api_headers

# Get Pixel

# Get a single pixel given the x and y coordinates.
# This endpoint requires an authentication token. See this page for how to authenticate with the API.

API_URL = "https://pixels.pythondiscord.com/get_pixel"


def execute(x: int = None, y: int = None, **kwargs: dict) -> dict:

    d_arguments = {
        "x": x,
        "y": y
    }

    if None in (x, y):

        if kwargs is not None and "x" in kwargs and "y" in kwargs:
            d_arguments['x'] = kwargs['x']
            d_arguments['y'] = kwargs['y']

        else:
            raise ValueError("Missing parameter!")

    response = requests.get(
        API_URL,
        headers=config.get_auth_headers(),

        # Note: coordinates as query string parameters,
        #       not in the JSON body
        params=d_arguments
    )

    try:
        payload = response.json()
        data = response.json()
        data_type = "json"
    except json.JSONDecodeError:
        payload = {}
        data = response.text
        data_type = "text"

    try:
        rgb = payload["rgb"]
    except KeyError:
        rgb = None

    d_result = {
        "request_name": "GET /get_pixel",
        "request_arguments": d_arguments,
        "response": response,
        "data": data,
        "data_type": data_type,
        "data_encoding": response.encoding,
        "rgb": rgb
    }

    d_result.update(api_headers.sort_by_type(response.headers))

    return d_result


def headers() -> dict:

    return api_headers.request(API_URL, "HEAD /get_pixel")

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
