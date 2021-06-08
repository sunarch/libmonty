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


def execute(x: int = None, y: int = None, rgb: str = None, struct: dict = None) -> tuple[str, dict]:

    data = {
        "x": x,  # 80
        "y": y,  # 45
        "rgb": rgb  # "00FF00"
    }

    if None in (x, y, rgb):

        if struct is not None and "x" in struct and "y" in struct and "rgb" in struct:
            data['x'] = struct['x']
            data['x'] = struct['y']
            data['x'] = struct['rgb']

            response, message = _request_get(data)

        else:
            raise ValueError("Missing parameter!")

    else:
        response, message = _request_get(data)

    d_return = {
        "response": response,
        "message": message
    }

    return "POST /set_pixel", d_return


def headers() -> tuple[str, dict]:

    response = requests.head(
        API_URL,
        headers=config.get_auth_headers()
    )

    d_return = {
        "response": response,
    }

    d_return.update(config.parse_headers(response.headers))

    return "HEAD /set_pixel", d_return


def _request_get(data: dict):

    # remember, this is a POST method not a GET method.
    response = requests.post(
        API_URL,
        json=data,
        headers=config.get_auth_headers(),
    )

    message = _parse(response)
    # added pixel at x=123,y=12 of color 87CEEB

    return response, message


def _parse(response):

    try:
        payload = response.json()
    except json.JSONDecodeError:
        payload = {"message": ""}

    try:
        s_return = payload["message"]
    except KeyError:
        s_return = ""

    return s_return

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
