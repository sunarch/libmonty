# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from libmonty.hexer import lines


def determine_count_per_line(cols: int = 80,
                             full_width: bool = False
                             ) -> int:

    if full_width:
        for count in range(1, cols):
            if min_line_length(count) > cols:
                return count - 1

    if cols < min_line_length(16):  # 78
        return 8

    if cols < min_line_length(24):  # 110
        return 16

    if cols < min_line_length(32):  # 142
        return 24

    return 32


def min_line_length(bytes_per_line: int) -> int:

    def pseudo_converter(x, y):
        return str(x).zfill(y)

    part_counter = len(lines.part_counter(0, 10, pseudo_converter))
    part_bytes = len(lines.part_bytes(bytes(bytes_per_line), bytes_per_line, pseudo_converter))
    part_chars = len(lines.part_chars(bytes(bytes_per_line), bytes_per_line))
    line_end = 1

    return part_counter + part_bytes + part_chars + line_end

# -------------------------------------------------------------------- #
