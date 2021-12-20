#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random
import os.path

from typing import Callable, Generator


def create_from_file(path: str) -> Callable:

    if not os.path.isfile(path):
        raise FileNotFoundError('File not found: \'{path}\'')

    def file_contents(bytes_per_line: int) -> Generator:
        with open(path, 'rb') as f_stream:

            while True:
                try:
                    data = f_stream.read(bytes_per_line)
                except KeyboardInterrupt:
                    break

                if not data:
                    break

                yield data

    return file_contents


def random_data(bytes_per_line: int) -> Generator:

    while True:
        yield random.randbytes(bytes_per_line)

# -------------------------------------------------------------------- #
