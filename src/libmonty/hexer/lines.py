#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

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

    try:
        b_unit = bytes(range(bytes_per_line))
    except ValueError:
        if bytes_per_line > 256:
            full = bytes(range(256)) * (bytes_per_line // 256)
            fraction = bytes(range(bytes_per_line % 256))
            b_unit = full + fraction
        else:
            raise

    s_line += _part_bytes(b_unit, bytes_per_line, index_converter)

    s_line += "Decoded text"

    print(s_line, flush=True)


def print_data(b_unit: bytes,
               bytes_per_line: int,
               offset: int,
               index_converter: Callable,
               char_converter: Callable,
               extra_width: int
               ) -> None:

    s = construct(b_unit,
                  bytes_per_line,
                  offset,
                  index_converter,
                  char_converter,
                  extra_width)

    print(s, flush=True)


def construct(b_unit: bytes,
              bytes_per_line: int,
              offset: int = 0,
              index_converter: Callable = number_str.pseudo,
              char_converter: Callable = char_str.pseudo,
              extra_width: int = 0
              ) -> str:

    s_counter = _part_counter(offset, COUNTER_DIGITS + extra_width, index_converter)

    s_bytes = _part_bytes(b_unit, bytes_per_line, number_str.hexadecimal)

    s_chars = _part_chars(b_unit, char_converter)

    return s_counter + s_bytes + s_chars


def _part_counter(offset: int = 0,
                  digits: int = COUNTER_DIGITS,
                  index_formatter: Callable = number_str.pseudo,
                  ) -> str:

    return " " + index_formatter(offset, digits) + "  "


def _part_bytes(b_unit: bytes,
                bytes_per_line: int,
                number_converter: Callable = number_str.pseudo
                ) -> str:

    s_bytes = " ".join(map(lambda b: number_converter(b, 2), b_unit))

    if len(b_unit) < bytes_per_line:
        s_format = "{:<" + str((bytes_per_line * 3) - 1) + "}"
        s_bytes = s_format.format(s_bytes)

    return s_bytes + "  "


def _part_chars(b_unit: bytes,
                char_converter: Callable = char_str.pseudo,
                ) -> str:

    return "".join(map(char_converter, b_unit))

# -------------------------------------------------------------------- #
