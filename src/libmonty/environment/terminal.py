#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Terminal
"""

# imports: library
import os


def get_cols() -> int:
    """Get columns"""

    try:
        size = os.get_terminal_size()
        cols: int = size.columns
        # lines: int = size.lines
    except OSError:
        cols = 80
        # lines = 20

    return cols
