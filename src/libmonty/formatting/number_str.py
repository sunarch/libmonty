#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Number str
"""


def pseudo(value: int,
           pad_to: int = 0,
           prefix: str = '',
           ) -> str:
    """Pseudo"""

    return prefix + str(value).zfill(pad_to)


def _number_str(name: str,
                base: str,
                value: int,
                pad_to: int = 0,
                prefix: str = None,
                ) -> str:
    """Number str"""

    if value < -1:
        raise ValueError(f'Negative value in number formatting: {value}')

    if value == -1:
        return name

    s_output = format(value, base)

    s_output = s_output.zfill(pad_to)

    if prefix is not None:
        if prefix in ('', base, f'0{base}'):
            s_output = f'0{base}' + s_output
        else:
            s_output = prefix + s_output

    return s_output


def hexadecimal(value: int,
                pad_to: int = 0,
                prefix: str = None,
                ) -> str:
    """Hexadecimal"""

    return hexadecimal_lower(value, pad_to, prefix)


def hexadecimal_lower(value: int,
                      pad_to: int = 0,
                      prefix: str = None,
                      ) -> str:
    """Hexadecimal - lower"""

    return _number_str('h', 'x', value, pad_to, prefix)


def hexadecimal_upper(value: int,
                      pad_to: int = 0,
                      prefix: str = None,
                      ) -> str:
    """Hexadecimal - upper"""

    return _number_str('h', 'X', value, pad_to, prefix)


def decimal(value: int,
            pad_to: int = 0,
            prefix: str = None
            ) -> str:
    """Decimal"""

    return _number_str('d', 'd', value, pad_to, prefix)


def octal(value: int,
          pad_to: int = 0,
          prefix: str = None
          ) -> str:
    """Octal"""

    return _number_str('o', 'o', value, pad_to, prefix)


def binary(value: int,
           pad_to: int = 0,
           prefix: str = None
           ) -> str:
    """Binary"""

    return _number_str('b', 'b', value, pad_to, prefix)
