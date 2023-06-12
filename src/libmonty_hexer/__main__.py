#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# imports: library
from argparse import ArgumentParser, Namespace
import sys
import time
from typing import Callable

# imports: dependencies
from libmonty_logging.config.file_and_stream.v1 import config as logging_config
import libmonty_logging.helper as logging_helper
# import libmonty_logging.message as logging_message

# imports: project
from libmonty.environment import terminal

from libmonty_hexer import version
from libmonty_hexer import arguments
from libmonty_hexer import width
from libmonty_hexer import lines


def main() -> None:

    logging_helper.apply_config(version.PROGRAM_NAME,
                                version.__version__,
                                logging_config)

    # logging_message.program_header(version.PROGRAM_NAME)

    parser = ArgumentParser(prog=version.PROGRAM_NAME)

    parser.add_argument('--version',
                        help='Display version',
                        action='store_true',
                        dest='version')

    arguments.create_arguments(parser)

    args = parser.parse_args(sys.argv[1:])

    if args.version:
        print(f'{version.PROGRAM_NAME} {version.__version__}')
        return

    main_lib(args)


def main_lib(args: Namespace) -> None:

    try:
        stream, char_converter = arguments.stream(args.stream)
        i_bytes_per_line = arguments.bytes_per_line(args.bytes_per_line)
        i_sleep = arguments.sleep(args.sleep)
        index_converter = arguments.index_converter(args.index_format)
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


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------- #
