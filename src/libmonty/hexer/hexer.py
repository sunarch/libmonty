#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from typing import Callable

from libmonty.environment import terminal

from libmonty.hexer import arguments
from libmonty.hexer import width
from libmonty.hexer import lines


def main(args: list[str], kwargs: dict) -> None:

    try:
        stream, char_converter = arguments.stream(kwargs, args, 0)
        i_bytes_per_line = arguments.bytes_per_line(kwargs, args, 1)
        i_sleep = arguments.sleep(kwargs, args, 2)
        index_converter = arguments.index_converter(kwargs, args, 3)
    except ValueError:
        raise

    try:
        run(stream, index_converter, char_converter, i_bytes_per_line, i_sleep)
    except ValueError:
        raise


def run(stream: Callable = None,
        index_converter: Callable = None,
        char_converter: Callable = None,
        bytes_per_line: int = 0,
        sleep: float = 0.1
        ) -> None:

    if stream is None:
        raise ValueError('No input stream specified!')

    if index_converter is None:
        raise ValueError('No index formatting method specified!')

    if char_converter is None:
        raise ValueError('No char conversion method specified!')

    print('')

    i_extra_width = 0

    if bytes_per_line <= 0:
        i_cols = terminal.get_cols()

        full_width = False
        if bytes_per_line <= -1:
            full_width = True

        bytes_per_line = width.determine_count_per_line(i_cols, full_width)

        if full_width:
            i_extra_width = i_cols - width.min_line_length(bytes_per_line)

    i_offset = 0

    lines.print_header(bytes_per_line, index_converter, i_extra_width)
    print('')

    for b_unit in stream(bytes_per_line):

        try:
            lines.print_data(b_unit,
                             bytes_per_line,
                             i_offset,
                             index_converter,
                             char_converter,
                             i_extra_width)
            time.sleep(sleep)

            i_offset += bytes_per_line

        except KeyboardInterrupt:
            break

    print('', flush=True)

# -------------------------------------------------------------------- #
