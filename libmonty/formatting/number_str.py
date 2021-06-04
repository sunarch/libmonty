# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


def hexadecimal(value: int,
                pad_to: int = 0,
                prefix: str = None,
                form: str = "f"
                ) -> str:

    if value < -1:
        raise ValueError("Negative value in number formatting: {}".format(value))

    if value == -1:
        return "h"

    # form == "f" / default
    s_output = format(value, 'x')  # 'ff'

    if form == "F":
        s_output = format(value, 'X')  # 'FF'

    s_output = s_output.zfill(pad_to)

    if prefix is not None:
        if prefix in ("", "x", "0x"):  # '0xff'
            # format(value, '#x') | hex(value)
            s_output = "0x" + s_output
        else:
            s_output = prefix + s_output

    return s_output


def decimal(value: int,
            pad_to: int = 0,
            prefix: str = None
            ) -> str:

    if value < -1:
        raise ValueError("Negative value in number formatting: {}".format(value))

    if value == -1:
        return "d"

    s_output = str(value)

    s_output = s_output.zfill(pad_to)

    if prefix is not None:
        s_output = prefix + s_output

    return s_output


def octal(value: int,
          pad_to: int = 0,
          prefix: str = None
          ) -> str:

    if value < -1:
        raise ValueError("Negative value in number formatting: {}".format(value))

    if value == -1:
        return "o"

    s_output = format(value, 'o')

    s_output = s_output.zfill(pad_to)

    if prefix is not None:
        if prefix in ("", "o", "0o"):  # '0o77'
            s_output = "0o" + s_output
        else:
            s_output = prefix + s_output

    return s_output


def binary(value: int,
           pad_to: int = 0,
           prefix: str = None
           ) -> str:

    if value < -1:
        raise ValueError("Negative value in number formatting: {}".format(value))

    if value == -1:
        return "b"

    s_output = format(value, 'b')

    s_output = s_output.zfill(pad_to)

    if prefix is not None:
        if prefix in ("", "b", "0b"):  # '0b11'
            s_output = "0b" + s_output
        else:
            s_output = prefix + s_output

    return s_output

# -------------------------------------------------------------------- #
