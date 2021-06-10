# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests

from libmonty.pixels import config


def generic(api_url: str, request_name: str) -> dict:

    response = requests.head(
        api_url,
        headers=config.get_auth_headers()
    )

    d_result = {
        "request_name": request_name,
        "response": response,
        "data": response.text,
        "data_type": "none",
        "data_encoding": response.encoding
    }

    d_result.update(config.parse_headers(response.headers))

    return d_result

# -------------------------------------------------------------------- #
