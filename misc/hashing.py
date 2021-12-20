#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import hashlib


def hashSHA1(argObject):
    return hashlib.sha1(argObject).hexdigest()

def integerHash(argHexDigest):
    return int(argHexDigest[:8], 16) # 8 hex digits of precision
