#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Discord formatters
"""


def bold(text: str):
    """Bold"""

    return f'**{text}**'


def italic(text: str):
    """Italic"""

    return f'*{text}*'


def strikethrough(text: str):
    """Strike-through"""

    return f'~~{text}~~'


def quote(text: str):
    """Quote
    unofficial"""

    return f'"{text}"'


def code(text: str):
    """Code"""

    return f'`{text}`'


def hidden(text: str):
    """Hidden"""

    return f'||{text}||'
