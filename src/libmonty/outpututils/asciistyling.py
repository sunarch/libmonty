#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

""" Output styling with ASCII escape sequences
    Version 1.1

    https://en.wikipedia.org/wiki/ANSI_escape_code

    Python utilites
    https://github.com/sunarch/libmonty
    'utils' folder
"""


# style ########################################################################

class AsciiStyle:
    """ASCII style"""

    @staticmethod
    def bold(arg_printable):
        """Bold"""

        return f'\x1b[1m{arg_printable}\x1b[0m'

    @staticmethod
    def faint(arg_printable):
        """Faint"""

        return f'\x1b[2m{arg_printable}\x1b[0m'

    @staticmethod
    def italic(arg_printable):
        """Italic"""

        return f'\x1b[3m{arg_printable}\x1b[0m'

    @staticmethod
    def underlined(arg_printable):
        """Underlined"""

        return f'\x1b[4m{arg_printable}\x1b[0m'

    @staticmethod
    def blink(arg_printable):
        """Blink"""

        return f'\x1b[5m{arg_printable}\x1b[0m'

    @staticmethod
    def image_negative(arg_printable):
        """Image negative"""

        return f'\x1b[7m{arg_printable}\x1b[0m'

    @staticmethod
    def framed(arg_printable):
        """Framed"""

        return f'\x1b[51m{arg_printable}\x1b[0m'

    @staticmethod
    def encircled(arg_printable):
        """Encircled"""

        return f'\x1b[52m{arg_printable}\x1b[0m'

    @staticmethod
    def overlined(arg_printable):
        """Overlined"""

        return f'\x1b[53m{arg_printable}\x1b[0m'


# font #########################################################################

class AsciiFont:
    """ASCII font"""

    @staticmethod
    def primary(arg_printable):
        """Primary"""

        return f'\x1b[10m{arg_printable}\x1b[0m'

    @staticmethod
    def alternate(arg_printable, arg_alternate_font_no):
        """Alternate"""

        inserted_no = '1'

        if int(arg_alternate_font_no) in range(1, 10):  # 0 < x < 10 #
            inserted_no = str(arg_alternate_font_no)

        return f'\x1b[1{inserted_no}m{arg_printable}\x1b[0m'


# color ########################################################################

class AsciiColor:
    """ASCII color"""

    @staticmethod
    def black(arg_printable):
        """Black"""

        return f'\x1b[30m{arg_printable}\x1b[0m'

    @staticmethod
    def red(arg_printable):
        """Red"""

        return f'\x1b[31m{arg_printable}\x1b[0m'

    @staticmethod
    def green(arg_printable):
        """Green"""

        return f'\x1b[32m{arg_printable}\x1b[0m'

    @staticmethod
    def yellow(arg_printable):
        """Yellow"""

        return f'\x1b[33m{arg_printable}\x1b[0m'

    @staticmethod
    def blue(arg_printable):
        """Blue"""

        return f'\x1b[34m{arg_printable}\x1b[0m'

    @staticmethod
    def magenta(arg_printable):
        """Magenta"""

        return f'\x1b[35m{arg_printable}\x1b[0m'

    @staticmethod
    def cyan(arg_printable):
        """Cyan"""

        return f'\x1b[36m{arg_printable}\x1b[0m'

    @staticmethod
    def white(arg_printable):
        """White"""

        return f'\x1b[37m{arg_printable}\x1b[0m'


# background ###################################################################

class AsciiBackground:
    """ASCII background"""

    @staticmethod
    def black(arg_printable):
        """Black"""

        return f'\x1b[40m{arg_printable}\x1b[0m'

    @staticmethod
    def red(arg_printable):
        """Red"""

        return f'\x1b[41m{arg_printable}\x1b[0m'

    @staticmethod
    def green(arg_printable):
        """Green"""

        return f'\x1b[42m{arg_printable}\x1b[0m'

    @staticmethod
    def yellow(arg_printable):
        """Yellow"""

        return f'\x1b[43m{arg_printable}\x1b[0m'

    @staticmethod
    def blue(arg_printable):
        """Blue"""

        return f'\x1b[44m{arg_printable}\x1b[0m'

    @staticmethod
    def magenta(arg_printable):
        """Magenta"""

        return f'\x1b[45m{arg_printable}\x1b[0m'

    @staticmethod
    def cyan(arg_printable):
        """Cyan"""

        return f'\x1b[46m{arg_printable}\x1b[0m'

    @staticmethod
    def white(arg_printable):
        """White"""

        return f'\x1b[47m{arg_printable}\x1b[0m'
