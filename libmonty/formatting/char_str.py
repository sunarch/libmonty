# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import string


def byte_to_printable_or_space_or_dot(value: int) -> str:

    s_char = chr(value)

    if s_char in string.printable:

        if s_char in string.whitespace and s_char != ' ':
            return "."

        return s_char

    return "."

# -------------------------------------------------------------------- #
