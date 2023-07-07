#!/usr/bin/env python3

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
    def bold(printable: str) -> str:
        """Bold"""

        return f'\x1b[1m{printable}\x1b[0m'

    @staticmethod
    def faint(printable: str) -> str:
        """Faint"""

        return f'\x1b[2m{printable}\x1b[0m'

    @staticmethod
    def italic(printable: str) -> str:
        """Italic"""

        return f'\x1b[3m{printable}\x1b[0m'

    @staticmethod
    def underlined(printable: str) -> str:
        """Underlined"""

        return f'\x1b[4m{printable}\x1b[0m'

    @staticmethod
    def blink(printable: str) -> str:
        """Blink"""

        return f'\x1b[5m{printable}\x1b[0m'

    @staticmethod
    def image_negative(printable: str) -> str:
        """Image negative"""

        return f'\x1b[7m{printable}\x1b[0m'

    @staticmethod
    def framed(printable: str) -> str:
        """Framed"""

        return f'\x1b[51m{printable}\x1b[0m'

    @staticmethod
    def encircled(printable: str) -> str:
        """Encircled"""

        return f'\x1b[52m{printable}\x1b[0m'

    @staticmethod
    def overlined(printable: str) -> str:
        """Overlined"""

        return f'\x1b[53m{printable}\x1b[0m'


# font #########################################################################

class AsciiFont:
    """ASCII font"""

    @staticmethod
    def primary(printable: str) -> str:
        """Primary"""

        return f'\x1b[10m{printable}\x1b[0m'

    @staticmethod
    def alternate(printable: str, arg_alternate_font_no) -> str:
        """Alternate"""

        inserted_no = '1'

        if int(arg_alternate_font_no) in range(1, 10):  # 0 < x < 10 #
            inserted_no = str(arg_alternate_font_no)

        return f'\x1b[1{inserted_no}m{printable}\x1b[0m'


# color ########################################################################

class AsciiColor:
    """ASCII color"""

    @staticmethod
    def black(printable: str) -> str:
        """Black"""

        return f'\x1b[30m{printable}\x1b[0m'

    @staticmethod
    def red(printable: str) -> str:
        """Red"""

        return f'\x1b[31m{printable}\x1b[0m'

    @staticmethod
    def green(printable: str) -> str:
        """Green"""

        return f'\x1b[32m{printable}\x1b[0m'

    @staticmethod
    def yellow(printable: str) -> str:
        """Yellow"""

        return f'\x1b[33m{printable}\x1b[0m'

    @staticmethod
    def blue(printable: str) -> str:
        """Blue"""

        return f'\x1b[34m{printable}\x1b[0m'

    @staticmethod
    def magenta(printable: str) -> str:
        """Magenta"""

        return f'\x1b[35m{printable}\x1b[0m'

    @staticmethod
    def cyan(printable: str) -> str:
        """Cyan"""

        return f'\x1b[36m{printable}\x1b[0m'

    @staticmethod
    def white(printable: str) -> str:
        """White"""

        return f'\x1b[37m{printable}\x1b[0m'


# background ###################################################################

class AsciiBackground:
    """ASCII background"""

    @staticmethod
    def black(printable: str) -> str:
        """Black"""

        return f'\x1b[40m{printable}\x1b[0m'

    @staticmethod
    def red(printable: str) -> str:
        """Red"""

        return f'\x1b[41m{printable}\x1b[0m'

    @staticmethod
    def green(printable: str) -> str:
        """Green"""

        return f'\x1b[42m{printable}\x1b[0m'

    @staticmethod
    def yellow(printable: str) -> str:
        """Yellow"""

        return f'\x1b[43m{printable}\x1b[0m'

    @staticmethod
    def blue(printable: str) -> str:
        """Blue"""

        return f'\x1b[44m{printable}\x1b[0m'

    @staticmethod
    def magenta(printable: str) -> str:
        """Magenta"""

        return f'\x1b[45m{printable}\x1b[0m'

    @staticmethod
    def cyan(printable: str) -> str:
        """Cyan"""

        return f'\x1b[46m{printable}\x1b[0m'

    @staticmethod
    def white(printable: str) -> str:
        """White"""

        return f'\x1b[47m{printable}\x1b[0m'
