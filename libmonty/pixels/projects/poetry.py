# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from libmonty.images import colors_named

from libmonty.pixels import output
from libmonty.pixels import files

from libmonty.pixels import api_get_size
from libmonty.pixels import api_set_pixel


COMMAND = "poetry"


def command(execute: bool, timestamp: str, task_queue, **kwargs) -> None:

    if execute:
        pass

    if len(kwargs['args']) == 1:

        ls_lines = ['"The Colors of Poetry" by @sunarch']
        i_longest = len(ls_lines[0])

        with open(f"{files.FOLDER_DATA}/{kwargs['args'][0]}.txt", "rt") as f_data:

            for line in f_data:

                s_line = line.strip()
                ls_lines.append(s_line)

                if len(s_line) > i_longest:
                    i_longest = len(s_line)

        ls_lines = list(map(lambda x: line_to_adjusted_list_char(x, i_longest), ls_lines))

        ls_lines = list(map(lambda x: list_char_to_rgb(x), ls_lines))

        i_horizontal = i_longest + 2

        ls_top_bottom = [horizontal() for x in range(i_horizontal + 1)]
        ls_lines.insert(0, ls_top_bottom)
        ls_lines.append(ls_top_bottom)

        i_vertical = len(ls_lines)

        result_s = api_get_size.execute()
        output.log_result(timestamp, result_s)

        try:
            width = result_s['width']
            height = result_s['height']
        except KeyError:
            raise ValueError("Invalid size.")

        if width < i_horizontal:
            raise ValueError(f"Canvas not wide enough: {width} < {i_horizontal}")

        if height < i_vertical + 1:
            raise ValueError(f"Canvas not tall enough: {height} < {i_vertical + 1}")

        for i_row, ls_single_line in enumerate(ls_lines):

            for i_col, rgb in enumerate(ls_single_line):
                ls_args = [str(i_col), str(i_row + 1), rgb]

                # task_queue.put((api_set_pixel.COMMAND, ls_args, timestamp))
                d_args = dict(zip(["x", "y", "rgb"], ls_args))
                s_request = output.form_request_input(api_set_pixel.API_NAME_POST, d_args)
                output.to_console(f"Queued: {s_request}")

            output.to_console(output.form_separator())

        return

    raise ValueError("Invalid arguents.")


def line_to_adjusted_list_char(line: str, length: int) -> list[str]:

    return list(f"{line:<{length}}")


def list_char_to_rgb(line: list[str]) -> list[str]:

    ls_rgb = [char_to_color(char) for char in line]

    ls_rgb.insert(0, vertical())
    ls_rgb.append(vertical())

    return ls_rgb


def char_to_color(char: str) -> str:

    i_colors = len(colors_named.COLORS)
    ls_colors = list(colors_named.COLORS)

    i_char = ord(char) % i_colors

    return ls_colors[i_char]


def vertical() -> str:

    return format(ord("|"), "X") * 3


def horizontal() -> str:

    return format(ord("-"), "X") * 3

# -------------------------------------------------------------------- #
