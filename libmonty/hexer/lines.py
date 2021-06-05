# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import Callable

from libmonty.formatting import number_str
from libmonty.formatting import char_str


COUNTER_DIGITS = 10


def print_header(bytes_per_line: int,
                 index_converter: Callable,
                 extra_width: int
                 ) -> None:

    s_counter = f"Offset ({index_converter(-1)})"
    s_line = f" {s_counter:^{COUNTER_DIGITS + extra_width}}  "

    b_unit = bytes(range(bytes_per_line))
    s_line += _part_bytes(b_unit, bytes_per_line, index_converter)

    s_line += "Decoded text"

    print(s_line, flush=True)


def print_data(b_unit: bytes,
               bytes_per_line: int,
               offset: int,
               index_converter: Callable,
               extra_width: int
               ) -> None:

    s = construct(b_unit, bytes_per_line, offset, index_converter, extra_width)

    print(s, flush=True)


def _pseudo_converter(x, y):
    return str(x).zfill(y)


def construct(b_unit: bytes,
              bytes_per_line: int,
              offset: int = 0,
              index_converter: Callable = _pseudo_converter,
              extra_width: int = 0
              ) -> str:

    s_line = _part_counter(offset, COUNTER_DIGITS + extra_width, index_converter)

    s_line += _part_bytes(b_unit, bytes_per_line, number_str.hexadecimal)

    s_line += _part_chars(b_unit)

    return s_line


def _part_counter(offset: int = 0,
                  digits: int = COUNTER_DIGITS,
                  index_formatter: Callable = _pseudo_converter,
                  ) -> str:

    return " " + index_formatter(offset, digits) + "  "


def _part_bytes(b_unit: bytes,
                bytes_per_line: int,
                number_converter: Callable = _pseudo_converter
                ) -> str:

    s_bytes = " ".join(map(lambda b: number_converter(b, 2), b_unit))

    s_format = "{:<" + str(bytes_per_line * 3) + "} "

    return s_format.format(s_bytes)


def _part_chars(b_unit: bytes) -> str:

    return "".join(map(char_str.byte_to_printable_or_space_or_dot, b_unit))

# -------------------------------------------------------------------- #
