# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random
import time
import os.path

from typing import Callable, Generator

from libmonty.hexer import hexer_lib
from libmonty.formatting import number_str


def main(args: list[str], kwargs: dict) -> None:

    try:
        stream = _arg_stream(kwargs, args, 0)
    except ValueError:
        raise

    try:
        i_bytes_per_line = _arg_bytes_per_line(kwargs, args, 1)
    except ValueError:
        raise

    try:
        i_sleep = _arg_sleep(kwargs, args, 2)
    except ValueError:
        raise

    try:
        index_converter = _arg_index_converter(kwargs, args, 3)
    except ValueError:
        raise

    try:
        run(stream, i_bytes_per_line, i_sleep, index_converter)
    except ValueError:
        raise


def _arg_stream(kwargs: dict, args: list[str], args_index: int) -> Callable:

    stream = stream_gen_random  # default

    try:
        stream = kwargs['stream']

    except KeyError:
        if len(args) > args_index:
            s_stream = args[args_index]

            if s_stream == "random":
                stream = stream_gen_random
            else:
                try:
                    stream = create_stream_file(s_stream)
                except FileNotFoundError as err:
                    raise ValueError(str(err))

    return stream


def _arg_bytes_per_line(kwargs: dict, args: list[str], args_index: int) -> int:

    i_bytes_per_line = None  # default
    s_bytes_per_line = ""
    b_process_bytes_per_line = False

    try:
        s_bytes_per_line = kwargs['bytes_per_line']
    except KeyError:
        if len(args) > args_index:
            s_bytes_per_line = args[args_index]

            try:
                i_bytes_per_line = int(s_bytes_per_line)
            except (ValueError, TypeError):
                b_process_bytes_per_line = True
    else:
        b_process_bytes_per_line = True

    if b_process_bytes_per_line:
        print("Bad value for 'byte count per line': '{}'".format(s_bytes_per_line))

        s_bytes_per_line = str(i_bytes_per_line)
        if i_bytes_per_line is None:
            s_bytes_per_line = "full width"

        s_confirm = input("Do you wish to continue with the default [{}] ? (y/n) ".format(s_bytes_per_line))
        if s_confirm.lower() not in ("y", "yes"):
            raise ValueError("Bad value for 'byte count per line': '{}'".format(s_bytes_per_line))

    return i_bytes_per_line


def _arg_sleep(kwargs: dict, args: list[str], args_index: int) -> float:

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


def _arg_index_converter(kwargs: dict, args: list[str], args_index: int) -> Callable:

    index_converter = number_str.hexadecimal  # default

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
        index_converter = kwargs['index_converter']

    except KeyError:
        if len(args) > args_index:
            s_index_converter = args[args_index]

            try:
                index_converter = d_index_formats[s_index_converter]
            except KeyError:
                err = "Value for index format not recognized: '{}'".format(s_index_converter)

                print(err)

                s_confirm = input("Do you wish to continue with the default [hexadecimal] ? (y/n) ")
                if s_confirm.lower() not in ("y", "yes"):
                    raise ValueError(err)

    return index_converter


def create_stream_file(path: str) -> Callable:

    if not os.path.isfile(path):
        raise FileNotFoundError("File not found: '{}'".format(path))

    def stream_gen_file(bytes_per_line: int) -> Generator:
        with open(path, "rb") as f_stream:

            while True:
                try:
                    data = f_stream.read(bytes_per_line)
                except KeyboardInterrupt:
                    break

                if not data:
                    break

                yield data

    return stream_gen_file


def stream_gen_random(bytes_per_line: int) -> Generator:

    while True:
        yield random.randbytes(bytes_per_line)


def run(stream_gen: Callable = None,
        bytes_per_line: int = None,
        sleep: float = 0.1,
        index_converter: Callable = None
        ) -> None:

    if stream_gen is None:
        raise ValueError("No input stream specified!")

    if index_converter is None:
        raise ValueError("No index formatting method specified!")

    print("")

    if bytes_per_line is None:
        i_cols = hexer_lib.get_terminal_cols()
        bytes_per_line = hexer_lib.determine_count_per_line(i_cols, full=True)

    i_offset = 0

    hexer_lib.print_header(bytes_per_line, index_converter)
    print("")

    for b_unit in stream_gen(bytes_per_line):

        try:
            hexer_lib.print_line(b_unit, bytes_per_line, i_offset, index_converter)
            time.sleep(sleep)

            i_offset += bytes_per_line

        except KeyboardInterrupt:
            break

    print("", flush=True)

# -------------------------------------------------------------------- #
