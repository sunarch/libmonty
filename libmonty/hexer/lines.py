# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import Callable

from libmonty.formatting import number_str
from libmonty.formatting import char_str


def print_header(bytes_per_line: int,
                 index_converter: Callable
                 ) -> None:

    s_line = ""
    s_line += "Offset ({}) ".format(index_converter(-1))
    b_unit = bytes(range(bytes_per_line))
    s_line += part_bytes(b_unit, bytes_per_line, index_converter)
    s_line += "Decoded text"

    print(s_line, flush=True)


def print_data(b_unit: bytes,
               bytes_per_line: int,
               offset: int,
               index_converter: Callable
               ) -> None:

    s_line = ""
    s_line += part_counter(offset, 8, index_converter)
    s_line += part_bytes(b_unit, bytes_per_line, number_str.hexadecimal)
    s_line += part_chars(b_unit, bytes_per_line)

    print(s_line, flush=True)


def part_counter(offset: int,
                 digits: int,
                 index_formatter: Callable
                 ) -> str:

    return " " + index_formatter(offset, digits) + "  "


def part_bytes(b_unit: bytes,
               bytes_per_line: int,
               number_converter: Callable
               ) -> str:

    s_bytes = ""

    for i_byte in b_unit:
        s_bytes += number_converter(i_byte, 2) + " "

    s_format = "{:<" + str(bytes_per_line * 3) + "} "
    return s_format.format(s_bytes)


def part_chars(b_unit: bytes,
               bytes_per_line: int
               ) -> str:

    s_chars = ""

    for i_byte in b_unit:
        s_chars += char_str.byte_to_printable_or_space_or_dot(i_byte)

    s_format = "{:<" + str(bytes_per_line) + "} "

    return s_format.format(s_chars)

# -------------------------------------------------------------------- #
