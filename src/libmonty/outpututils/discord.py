#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Discord formatters
"""


def bold(text: str) -> str:
    """Bold"""

    return f'**{text}**'


def italic(text: str) -> str:
    """Italic"""

    return f'*{text}*'


def strikethrough(text: str) -> str:
    """Strike-through"""

    return f'~~{text}~~'


def quote(text: str) -> str:
    """Quote
    unofficial"""

    return f'"{text}"'


def code(text: str) -> str:
    """Code"""

    return f'`{text}`'


def hidden(text: str) -> str:
    """Hidden"""

    return f'||{text}||'
