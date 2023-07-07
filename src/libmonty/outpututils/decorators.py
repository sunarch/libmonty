#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Output decorators with ASCII escape sequences
   Version 1.1

https://en.wikipedia.org/wiki/ANSI_escape_code
"""

# imports: library
from typing import Callable


def bold_text(function: Callable) -> Callable:
    """Bold text"""

    def new_function(printable: str) -> str:
        return f'\x1b[1m{function(printable)}\x1b[0m'

    return new_function


def faint_text(function: Callable) -> Callable:
    """Faint text"""

    def new_function(printable: str) -> str:
        return f'\x1b[2m{function(printable)}\x1b[0m'

    return new_function


def italic_text(function: Callable) -> Callable:
    """Italic text"""

    def new_function(printable: str) -> str:
        return f'\x1b[3m{function(printable)}\x1b[0m'

    return new_function


def underlined_text(function: Callable) -> Callable:
    """Underlined text"""

    def new_function(printable: str) -> str:
        return f'\x1b[4m{function(printable)}\x1b[0m'

    return new_function


def blinking_text(function: Callable) -> Callable:
    """Blinking text"""

    def new_function(printable: str) -> str:
        return f'\x1b[5m{function(printable)}\x1b[0m'

    return new_function


def image_negative_text(function: Callable) -> Callable:
    """Image negative text"""

    def new_function(printable: str) -> str:
        return f'\x1b[7m{function(printable)}\x1b[0m'

    return new_function


def primary_font_text(function: Callable) -> Callable:
    """Primary font text"""

    def new_function(printable: str) -> str:
        return f'\x1b[10m{function(printable)}\x1b[0m'

    return new_function


def alternate_font_text(function: Callable) -> Callable:
    """Alternate font text"""

    def new_function(printable: str, arg_alternate_font_no) -> str:
        inserted_no = '1'
        if int(arg_alternate_font_no) in range(1, 10):  # 0 < x < 10 #
            inserted_no = str(arg_alternate_font_no)
        return f'\x1b[1{inserted_no}m{function(printable, arg_alternate_font_no)}\x1b[0m'

    return new_function


def black_text(function: Callable) -> Callable:
    """Black text"""

    def new_function(printable: str) -> str:
        return f'\x1b[30m{function(printable)}\x1b[0m'

    return new_function


def red_text(function: Callable) -> Callable:
    """Red text"""

    def new_function(printable: str) -> str:
        return f'\x1b[31m{function(printable)}\x1b[0m'

    return new_function


def green_text(function: Callable) -> Callable:
    """Green text"""

    def new_function(printable: str) -> str:
        return f'\x1b[32m{function(printable)}\x1b[0m'

    return new_function


def yellow_text(function: Callable) -> Callable:
    """Yellow text"""

    def new_function(printable: str) -> str:
        return f'\x1b[33m{function(printable)}\x1b[0m'

    return new_function


def blue_text(function: Callable) -> Callable:
    """Blue text"""

    def new_function(printable: str) -> str:
        return f'\x1b[34m{function(printable)}\x1b[0m'

    return new_function


def magenta_text(function: Callable) -> Callable:
    """Magenta text"""

    def new_function(printable: str) -> str:
        return f'\x1b[35m{function(printable)}\x1b[0m'

    return new_function


def cyan_text(function: Callable) -> Callable:
    """Cyan text"""

    def new_function(printable: str) -> str:
        return f'\x1b[36m{function(printable)}\x1b[0m'

    return new_function


def white_text(function: Callable) -> Callable:
    """White text"""

    def new_function(printable: str) -> str:
        return f'\x1b[37m{function(printable)}\x1b[0m'

    return new_function


def bg_black_text(function: Callable) -> Callable:
    """Background black text"""

    def new_function(printable: str) -> str:
        return f'\x1b[40m{function(printable)}\x1b[0m'

    return new_function


def bg_red_text(function: Callable) -> Callable:
    """Background red text"""

    def new_function(printable: str) -> str:
        return f'\x1b[41m{function(printable)}\x1b[0m'

    return new_function


def bg_green_text(function: Callable) -> Callable:
    """Background green text"""

    def new_function(printable: str) -> str:
        return f'\x1b[42m{function(printable)}\x1b[0m'

    return new_function


def bg_yellow_text(function: Callable) -> Callable:
    """Background yellow text"""

    def new_function(printable: str) -> str:
        return f'\x1b[43m{function(printable)}\x1b[0m'

    return new_function


def bg_blue_text(function: Callable) -> Callable:
    """Background blue text"""

    def new_function(printable: str) -> str:
        return f'\x1b[44m{function(printable)}\x1b[0m'

    return new_function


def bg_magenta_text(function: Callable) -> Callable:
    """Background magenta text"""

    def new_function(printable: str) -> str:
        return f'\x1b[45m{function(printable)}\x1b[0m'

    return new_function


def bg_cyan_text(function: Callable) -> Callable:
    """Background cyan text"""

    def new_function(printable: str) -> str:
        return f'\x1b[46m{function(printable)}\x1b[0m'

    return new_function


def bg_white_text(function: Callable) -> Callable:
    """Background white text"""

    def new_function(printable: str) -> str:
        return f'\x1b[47m{function(printable)}\x1b[0m'

    return new_function


def framed_text(function: Callable) -> Callable:
    """Framed text"""

    def new_function(printable: str) -> str:
        return f'\x1b[51m{function(printable)}\x1b[0m'

    return new_function


def encircled_text(function: Callable) -> Callable:
    """Encircled text"""

    def new_function(printable: str) -> str:
        return f'\x1b[52m{function(printable)}\x1b[0m'

    return new_function


def overlined_text(function: Callable) -> Callable:
    """Overlined text"""

    def new_function(printable: str) -> str:
        return f'\x1b[53m{function(printable)}\x1b[0m'

    return new_function
