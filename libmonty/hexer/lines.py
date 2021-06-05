# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import Callable

from libmonty.formatting import number_str
from libmonty.formatting import char_str


def print_header(bytes_per_line: int,
                 index_converter: Callable,
                 extra_width: int
                 ) -> None:

    s_counter = f"Offset ({index_converter(-1)})"
    s_line = f" {s_counter:^{10 + extra_width}}  "

    b_unit = bytes(range(bytes_per_line))
    s_line += part_bytes(b_unit, bytes_per_line, index_converter)

    s_line += "Decoded text"

    print(s_line, flush=True)


def print_data(b_unit: bytes,
               bytes_per_line: int,
               offset: int,
               index_converter: Callable,
               extra_width: int
               ) -> None:

    s_line = ""
    s_line += part_counter(offset, 10 + extra_width, index_converter)
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

    s_bytes = " ".join(map(lambda b: number_converter(b, 2), b_unit))

    s_format = "{:<" + str(bytes_per_line * 3) + "}  "

    return s_format.format(s_bytes)


def part_chars(b_unit: bytes,
               bytes_per_line: int
               ) -> str:

    s_chars = "".join(map(char_str.byte_to_printable_or_space_or_dot, b_unit))

    s_format = "{:<" + str(bytes_per_line) + "}"

    return s_format.format(s_chars)

# -------------------------------------------------------------------- #
