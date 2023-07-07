#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


def encode(arg_object):
    return arg_object.encode('UTF-8')


def decode(arg_object):
    return arg_object.decode('UTF-8')
