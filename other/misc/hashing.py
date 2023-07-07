#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import hashlib


def hash_sha1(arg_object):
    return hashlib.sha1(arg_object).hexdigest()


def integer_hash(arg_hex_digest):
    return int(arg_hex_digest[:8], 16)  # 8 hex digits of precision
