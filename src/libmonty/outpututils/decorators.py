#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Output decorators with ASCII escape sequences
   Version 1.1

https://en.wikipedia.org/wiki/ANSI_escape_code
"""


def bold_text(arg_function):
    """Bold text"""

    def new_function(arg_printable):
        return f'\x1b[1m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def faint_text(arg_function):
    """Faint text"""

    def new_function(arg_printable):
        return f'\x1b[2m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def italic_text(arg_function):
    """Italic text"""

    def new_function(arg_printable):
        return f'\x1b[3m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def underlined_text(arg_function):
    """Underlined text"""

    def new_function(arg_printable):
        return f'\x1b[4m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def blinking_text(arg_function):
    """Blinking text"""

    def new_function(arg_printable):
        return f'\x1b[5m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def image_negative_text(arg_function):
    """Image negative text"""

    def new_function(arg_printable):
        return f'\x1b[7m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def primary_font_text(arg_function):
    """Primary font text"""

    def new_function(arg_printable):
        return f'\x1b[10m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def alternate_font_text(arg_function):
    """Alternate font text"""

    def new_function(arg_printable, arg_alternate_font_no):
        inserted_no = "1"
        if int(arg_alternate_font_no) in range(1, 10):  # 0 < x < 10 #
            inserted_no = str(arg_alternate_font_no)
        return f'\x1b[1{inserted_no}m{arg_function(arg_printable, arg_alternate_font_no)}\x1b[0m'

    return new_function


def black_text(arg_function):
    """Black text"""

    def new_function(arg_printable):
        return f'\x1b[30m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def red_text(arg_function):
    """Red text"""

    def new_function(arg_printable):
        return f'\x1b[31m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def green_text(arg_function):
    """Green text"""

    def new_function(arg_printable):
        return f'\x1b[32m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def yellow_text(arg_function):
    """Yellow text"""

    def new_function(arg_printable):
        return f'\x1b[33m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def blue_text(arg_function):
    """Blue text"""

    def new_function(arg_printable):
        return f'\x1b[34m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def magenta_text(arg_function):
    """Magenta text"""

    def new_function(arg_printable):
        return f'\x1b[35m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def cyan_text(arg_function):
    """Cyan text"""

    def new_function(arg_printable):
        return f'\x1b[36m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def white_text(arg_function):
    """White text"""

    def new_function(arg_printable):
        return f'\x1b[37m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def bg_black_text(arg_function):
    """Background black text"""

    def new_function(arg_printable):
        return f'\x1b[40m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def bg_red_text(arg_function):
    """Background red text"""

    def new_function(arg_printable):
        return f'\x1b[41m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def bg_green_text(arg_function):
    """Background green text"""

    def new_function(arg_printable):
        return f'\x1b[42m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def bg_yellow_text(arg_function):
    """Background yellow text"""

    def new_function(arg_printable):
        return f'\x1b[43m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def bg_blue_text(arg_function):
    """Background blue text"""

    def new_function(arg_printable):
        return f'\x1b[44m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def bg_magenta_text(arg_function):
    """Background magenta text"""

    def new_function(arg_printable):
        return f'\x1b[45m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def bg_cyan_text(arg_function):
    """Background cyan text"""

    def new_function(arg_printable):
        return f'\x1b[46m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def bg_white_text(arg_function):
    """Background white text"""

    def new_function(arg_printable):
        return f'\x1b[47m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def framed_text(arg_function):
    """Framed text"""

    def new_function(arg_printable):
        return f'\x1b[51m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def encircled_text(arg_function):
    """Encircled text"""

    def new_function(arg_printable):
        return f'\x1b[52m{arg_function(arg_printable)}\x1b[0m'

    return new_function


def overlined_text(arg_function):
    """Overlined text"""

    def new_function(arg_printable):
        return f'\x1b[53m{arg_function(arg_printable)}\x1b[0m'

    return new_function
