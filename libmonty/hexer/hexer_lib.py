# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import string


def get_terminal_cols() -> int:

    i_cols = 80

    try:
        o_size = os.get_terminal_size()
        i_cols = o_size.columns
        # i_lines = o_size.lines
    except OSError:
        pass

    return i_cols


def _line_part_counter(offset: int = 0, digits: int = 8) -> str:

    s_format = " {:0>" + str(digits) + "}  "

    return s_format.format(get_hex_output(offset, "ff"))


def _line_part_bytes(b_unit: bytes,
                     bytes_per_line: int
                     ) -> str:

    s_bytes = ""

    for i_byte in b_unit:
        s_bytes += "{} ".format(get_hex_output(i_byte, "ff"))

    s_format = "{:<" + str(bytes_per_line * 3) + "} "

    return s_format.format(s_bytes)


def _line_part_chars(b_unit: bytes,
                     bytes_per_line: int
                     ) -> str:

    s_chars = ""

    for i_byte in b_unit:
        s_chars += get_char_output(i_byte)

    s_format = "{:<" + str(bytes_per_line) + "} "

    return s_format.format(s_chars)


def print_line(b_unit: bytes,
               bytes_per_line: int,
               offset: int = 0
               ) -> None:

    s_line = ""
    s_line += _line_part_counter(offset)
    s_line += _line_part_bytes(b_unit, bytes_per_line)
    s_line += _line_part_chars(b_unit, bytes_per_line)

    print(s_line, flush=True)


def print_header(bytes_per_line: int) -> None:

    s_line = ""
    s_line += "Offset (h) "
    b_unit = bytes(range(bytes_per_line))
    s_line += _line_part_bytes(b_unit, bytes_per_line)
    s_line += "Decoded text"

    print(s_line, flush=True)


def _min_line_length(bytes_per_line: int) -> int:

    part_counter = len(_line_part_counter())
    part_bytes = len(_line_part_bytes(bytes(bytes_per_line), bytes_per_line))
    part_chars = len(_line_part_chars(bytes(bytes_per_line), bytes_per_line))
    line_end = 1

    return part_counter + part_bytes + part_chars + line_end


def determine_count_per_line(cols: int = 80,
                             full: bool = False
                             ) -> int:

    if full:
        for count in range(1, cols):
            if _min_line_length(count) > cols:
                return count - 1

    if cols < _min_line_length(16):  # 78
        return 8

    if cols < _min_line_length(24):  # 110
        return 16

    if cols < _min_line_length(32):  # 142
        return 24

    return 32


def get_char_output(value: int) -> str:

    s_char = chr(value)

    if s_char in string.printable:

        if s_char in string.whitespace and s_char != ' ':
            return "."

        return s_char

    return "."


def get_hex_output(value: int,
                   formatting: str = "ff"
                   ) -> str:

    if formatting == "FF":
        s_output = format(value, 'X')  # 'FF'

    # formatting == "ff" or "0x" / default
    s_output = format(value, 'x')  # 'ff'

    if len(s_output) % 2 != 0:
        s_output = '0' + s_output

    if formatting == "0x":  # '0xff'
        # format(value, '#x') | hex(value)
        s_output = "0x" + s_output

    return s_output


def get_int_from_byte(value: bytes) -> int:

    return int(value)


def get_int_from_char(value: str = '.') -> int:

    return ord(value)

# -------------------------------------------------------------------- #
