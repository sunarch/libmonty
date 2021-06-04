# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os


def get_terminal_cols() -> int:

    i_cols = 80

    try:
        o_size = os.get_terminal_size()
        i_cols = o_size.columns
        # i_lines = o_size.lines
    except OSError:
        pass

    return i_cols

# -------------------------------------------------------------------- #
