# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


def hexadecimal(value: int, form: str = "f") -> str:

    if value < -1:
        raise ValueError("Negative value in number formatting: {}".format(value))

    if value == -1:
        return "h"

    # "f" in form / default
    s_output = format(value, 'x')  # 'ff'

    if "F" in form:
        s_output = format(value, 'X')  # 'FF'

    i_target_len = len(form.strip("x"))
    s_output = s_output.zfill(i_target_len)

    if "x" in form:  # '0xff'
        # format(value, '#x') | hex(value)
        s_output = "0x" + s_output

    return s_output


def decimal(value: int, form: str = "0") -> str:

    if value < -1:
        raise ValueError("Negative value in number formatting: {}".format(value))

    if value == -1:
        return "d"

    # "0" in form / default
    s_output = str(value)

    i_target_len = len(form)
    s_output = s_output.zfill(i_target_len)

    return s_output


def octal(value: int, form: str = "8") -> str:

    if value < -1:
        raise ValueError("Negative value in number formatting: {}".format(value))

    if value == -1:
        return "o"

    # "8" in form / default
    s_output = format(value, 'o')

    i_target_len = len(form.strip("o"))
    s_output = s_output.zfill(i_target_len)

    if "o" in form:  # '0o88'
        # format(value, '#x') | hex(value)
        s_output = "0o" + s_output

    return s_output


def binary(value: int, form: str = "2") -> str:

    if value < -1:
        raise ValueError("Negative value in number formatting: {}".format(value))

    if value == -1:
        return "b"

    # "b" in form / default
    s_output = format(value, 'b')

    i_target_len = len(form.strip("b"))
    s_output = s_output.zfill(i_target_len)

    if "b" in form:  # '0b11'
        # format(value, '#x') | hex(value)
        s_output = "0b" + s_output

    return s_output

# -------------------------------------------------------------------- #
