#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Char str
"""

# imports: library
import string


def pseudo(value: int = ord('.')) -> str:
    """Pseudo"""

    return chr(value)


def _byte_to_printable_non_ws_or_space(value: int,
                                       default: str = '.',
                                       space: str = ' ',
                                       ) -> str:
    """Byte to printable non-WS or space"""

    char: str = chr(value)

    if char in ('\r', '\n'):
        return chr(0x21B5)  # ↵ Downwards Arrow with Corner Leftwards

    if char == ' ':
        return space

    if char in string.printable and char not in string.whitespace:
        return char

    return default


def byte_to_compact_printable_with_dots(value: int) -> str:
    """Byte to compact printable with dots"""

    default: str = '.'
    space: str = chr(0x22C5)  # ⋅ Dot Operator

    return _byte_to_printable_non_ws_or_space(value, default, space)


def byte_to_compact_printable_with_frames(value: int) -> str:
    """Byte to compact printable with frames"""

    default: str = chr(0x2395)  # ⎕ Apl Functional Symbol Quad
    space: str = chr(0x02FD)  # ⋅˽ Modifier Letter Shelf

    return _byte_to_printable_non_ws_or_space(value, default, space)
