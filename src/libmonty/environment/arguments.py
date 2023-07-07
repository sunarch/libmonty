#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Terminal - argument types
"""

# imports: library
from argparse import ArgumentTypeError
import os.path


def type_file_path(path: str) -> str:
    """Argument parser file path type"""

    if not os.path.isfile(path):
        raise ArgumentTypeError(f'Argument "{path}" is not a valid path')

    return path
