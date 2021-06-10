# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests
import json

from libmonty.pixels import config

# Set Pixel

# Override the pixel at the specified position with the specified color.
# This endpoint requires an authentication token. See this page for how to authenticate with the API.

API_URL = "https://pixels.pythondiscord.com/set_pixel"


def execute(x: int = None, y: int = None, rgb: str = None, **kwargs: dict) -> dict:

    data = {
        "x": x,  # 80
        "y": y,  # 45
        "rgb": rgb  # "00FF00"
    }

    if None in (x, y, rgb):

        if kwargs is not None and "x" in kwargs and "y" in kwargs and "rgb" in kwargs:
            data['x'] = kwargs['x']
            data['y'] = kwargs['y']
            data['rgb'] = kwargs['rgb']

        else:
            raise ValueError("Missing parameter!")

    # Note: POST method, not a GET method
    response = requests.post(
        API_URL,
        json=data,
        headers=config.get_auth_headers(),
    )

    try:
        payload = response.json()
    except json.JSONDecodeError:
        payload = {"message": ""}

    # e.g. "added pixel at x=123,y=12 of color 87CEEB"
    try:
        message = payload["message"]
    except KeyError:
        message = ""

    d_result = {
        "request_name": "POST /set_pixel",
        "response": response,
        "message": message
    }

    return d_result


def headers() -> dict:

    response = requests.head(
        API_URL,
        headers=config.get_auth_headers()
    )

    d_result = {
        "request_name": "HEAD /set_pixel",
        "response": response,
    }

    d_result.update(config.parse_headers(response.headers))

    return d_result

# -------------------------------------------------------------------- #
# Request

# REQUEST BODY * application/json

# Schema

# A pixel as used by the api.
# {
#     x*: integer
#     y*: integer
#     rgb*: string
# }

# Example

# {
#     "x": 120,
#     "y": 67,
#     "rgb": "00FF00"
# }

# -------------------------------------------------------------------- #
# Response: 200 - Successful Response
# application/json

# Schema

# {
#   detail: [{
#     loc*: [string]
#     msg*: string
#     type*: string
#   }]
# }

# Example

# {
#  "detail": [
#    {
#      "loc": [
#        "string"
#      ],
#      "msg": "string",
#      "type": "string"
#    }
#  ]
# }

# -------------------------------------------------------------------- #
# Response: 422 - Validation Error
# application/json

# Schema

# {
#   detail: [{
#     loc*: [string]
#     msg*: string
#     type*: string
#   }]
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
