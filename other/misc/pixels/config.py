#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import dotenv
import os


def load_token_env() -> None:

    dotenv.load_dotenv('libmonty/pixels/.env')


def get_auth_headers() -> dict:

    token = os.getenv('TOKEN')

    headers = {
        'Authorization': f'Bearer {token}'
    }

    return headers

# -------------------------------------------------------------------- #
