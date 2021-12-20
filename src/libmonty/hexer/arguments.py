#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import Tuple, Callable

from libmonty.formatting import char_str, number_str

from libmonty.hexer import streams


def stream(kwargs: dict, args: list[str], args_index: int) -> Tuple[Callable, Callable]:

    # defaults
    f_stream = streams.random_data
    f_char_converter = char_str.byte_to_compact_printable_with_dots

    try:
        f_stream = kwargs['stream']

    except KeyError:
        if len(args) > args_index:
            s_stream_name = args[args_index]

            if s_stream_name == "random":
                f_stream = streams.random_data
                f_char_converter = char_str.byte_to_compact_printable_with_dots

            else:
                try:
                    f_stream = streams.create_from_file(s_stream_name)
                except FileNotFoundError as err:
                    raise ValueError(str(err))

                f_char_converter = char_str.byte_to_compact_printable_with_frames

    return f_stream, f_char_converter


def bytes_per_line(kwargs: dict, args: list[str], args_index: int) -> int:

    i_bytes_per_line = 0  # default
    s_bytes_per_line = ""
    b_process_bytes_per_line = False

    try:
        s_bytes_per_line = str(kwargs['bytes_per_line'])
    except KeyError:
        if len(args) > args_index:
            s_bytes_per_line = str(args[args_index])

            try:
                i_bytes_per_line = int(s_bytes_per_line)
            except (ValueError, TypeError):
                b_process_bytes_per_line = True
    else:
        b_process_bytes_per_line = True

    if s_bytes_per_line.lower() in ("0", "none"):
        return 0

    if b_process_bytes_per_line:
        print("Bad value for 'byte count per line': '{}'".format(s_bytes_per_line))

        s_input_tpl = "Do you wish to continue with the default [{}] ? (y/n) "
        s_confirm = input(s_input_tpl.format(i_bytes_per_line))
        if s_confirm.lower() not in ("y", "yes"):
            raise ValueError("")

    return i_bytes_per_line


def sleep(kwargs: dict, args: list[str], args_index: int) -> float:

    i_sleep = 0.01  # default
    s_sleep = ""
    b_process_sleep = False

    d_speeds = {
        "f": 0.01,
        "fast": 0.01,
        "m": 0.05,
        "med": 0.05,
        "medium": 0.05,
        "s": 0.1,
        "slow": 0.1,
        "step": 0.5
    }

    try:
        s_sleep = kwargs['sleep']
    except KeyError:
        if len(args) > args_index:
            s_sleep = args[args_index]

            if s_sleep in d_speeds:
                i_sleep = d_speeds[s_sleep]
            else:
                b_process_sleep = True
    else:
        b_process_sleep = True

    if b_process_sleep:
        try:
            i_sleep = float(s_sleep)
        except (ValueError, TypeError):
            print("Bad value for 'sleep': '{}'".format(s_sleep))

            s_confirm = input("Do you wish to continue with the default [{}] ? (y/n) ".format(i_sleep))
            if s_confirm.lower() not in ("y", "yes"):
                raise ValueError("Bad value for 'sleep': '{}'".format(s_sleep))

    return i_sleep


def index_converter(kwargs: dict, args: list[str], args_index: int) -> Callable:

    f_index_converter = number_str.hexadecimal  # default

    d_index_formats = {
        "h": number_str.hexadecimal,
        "hex": number_str.hexadecimal,
        "hexadecimal": number_str.hexadecimal,
        "d": number_str.decimal,
        "decimal": number_str.decimal,
        "o": number_str.octal,
        "octal": number_str.octal
    }

    try:
        f_index_converter = kwargs['index_converter']

    except KeyError:
        if len(args) > args_index:
            s_index_converter = args[args_index]

            try:
                f_index_converter = d_index_formats[s_index_converter]
            except KeyError:
                err = "Value for index format not recognized: '{}'".format(s_index_converter)

                print(err)

                s_confirm = input("Do you wish to continue with the default [hexadecimal] ? (y/n) ")
                if s_confirm.lower() not in ("y", "yes"):
                    raise ValueError(err)

    return f_index_converter

# -------------------------------------------------------------------- #
