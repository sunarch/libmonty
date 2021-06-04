# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random
import time
import os.path

from typing import Callable, Generator

from hexer import hexer_lib


def main(args: list[str]) -> None:

    i_bytes_per_line = None
    i_sleep = 0.01

    if len(args) == 0:
        stream = stream_gen_random

    if len(args) > 0:
        if args[0] == "random":
            stream = stream_gen_random
        else:
            try:
                stream = create_stream_file(args[0])
            except FileNotFoundError as err:
                print(str(err))
                return

    if len(args) > 1:
        try:
            i_bytes_per_line = int(args[1])
        except (ValueError, TypeError):
            print("Bad value for 'byte count per line': '{}'".format(args[1]))

            s_bytes_per_line = str(i_bytes_per_line)
            if i_bytes_per_line is None:
                s_bytes_per_line = "full width"

            s_confirm = input("Do you wish to continue with the default [{}] ? (y/n) ".format(s_bytes_per_line))
            if s_confirm.lower() not in ("y", "yes"):
                return

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

    if len(args) > 2:
        if args[2] in d_speeds:
            i_sleep = d_speeds[args[2]]
        else:
            try:
                i_sleep = float(args[2])
            except (ValueError, TypeError):
                print("Bad value for 'sleep': '{}'".format(args[2]))

                s_confirm = input("Do you wish to continue with the default [{}] ? (y/n) ".format(i_sleep))
                if s_confirm.lower() not in ("y", "yes"):
                    return

    run(stream, i_bytes_per_line, i_sleep)


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


def run(stream_gen: Generator = None,
        bytes_per_line: int = None,
        sleep: float = 0.1
        ) -> None:

    if stream_gen is None:
        print("No input stream specified!")
        return

    print("")

    if bytes_per_line is None:
        i_cols = hexer_lib.get_terminal_cols()
        bytes_per_line = hexer_lib.determine_count_per_line(i_cols, full=True)

    i_offset = 0

    hexer_lib.print_header(bytes_per_line)
    print("")

    for b_unit in stream_gen(bytes_per_line):

        try:
            hexer_lib.print_line(b_unit, bytes_per_line, i_offset)
            time.sleep(sleep)

            i_offset += bytes_per_line

        except KeyboardInterrupt:
            break

    print("", flush=True)

# -------------------------------------------------------------------- #
