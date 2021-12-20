#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import Tuple, Callable, Union

from libmonty.formatting import char_str, number_str

from libmonty_hexer import streams


def create_arguments(parser_hexer):

    parser_hexer.add_argument('-s', '--stream',
                              help='Stream',
                              action='store', type=str, default='random',
                              dest='stream')

    parser_hexer.add_argument('-b', '--bytes-per-line',
                              help='Bytes per line',
                              action='store', type=int, default=16,
                              dest='bytes_per_line')

    parser_hexer.add_argument('-p', '--sleep',
                              help='Sleep time between lines',
                              action='store', type=float, default=0.01,
                              dest='sleep')

    parser_hexer.add_argument('-i', '--index-format',
                              help='Index format',
                              action='store', type=str, default='hexadecimal',
                              dest='index_format')


def stream(source: Union[Callable, str]) -> Tuple[Callable, Callable]:

    if isinstance(source, Callable):
        f_stream = source
        f_char_converter = char_str.byte_to_compact_printable_with_dots

    else:
        if source == 'random':
            f_stream = streams.random_data
            f_char_converter = char_str.byte_to_compact_printable_with_dots

        else:
            try:
                f_stream = streams.create_from_file(source)
            except FileNotFoundError as err:
                raise ValueError(str(err))

            f_char_converter = char_str.byte_to_compact_printable_with_frames

    return f_stream, f_char_converter


def bytes_per_line(count: int) -> int:

    if count < 1:
        raise ValueError

    return count


def sleep(speed: Union[float, int, str]) -> float:

    d_speeds = {
        'f': 0.01,
        'fast': 0.01,
        'm': 0.05,
        'med': 0.05,
        'medium': 0.05,
        's': 0.1,
        'slow': 0.1,
        'step': 0.5
    }

    if isinstance(speed, int):
        speed = float(speed)

    if isinstance(speed, float) or isinstance(speed, int):
        if speed <= 0:
            raise ValueError

    elif isinstance(speed, str):
        try:
            speed = d_speeds[speed]
        except KeyError:
            print(f'Bad value for \'sleep\': \'{speed}\'')
            speed = 0.01
            print(f'Using default value for \'sleep\': \'{speed}\'')

    return speed


def index_converter(converter: Union[Callable, str]) -> Callable:

    d_index_formats = {
        'h': number_str.hexadecimal,
        'hex': number_str.hexadecimal,
        'hexadecimal': number_str.hexadecimal,

        'd': number_str.decimal,
        'dec': number_str.decimal,
        'decimal': number_str.decimal,

        'o': number_str.octal,
        'oct': number_str.octal,
        'octal': number_str.octal
    }

    if isinstance(converter, Callable):
        return converter

    try:
        return d_index_formats[converter]
    except KeyError:
        print(f'Value for index format not recognized: \'{converter}\'')
        converter = 'hexadecimal'
        print(f'Using default value for index format: \'{converter}\'')
        return d_index_formats[converter]

# -------------------------------------------------------------------- #
