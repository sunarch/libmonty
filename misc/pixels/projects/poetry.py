#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random
import string

from libmonty.images import colors_named

from pixels import output
from pixels import files

from pixels import api_get_pixel
from pixels import api_get_pixels
from pixels import api_get_size
from pixels import api_set_pixel


COMMAND = "poetry"


def command(execute: bool, timestamp: str, task_queue, **kwargs) -> None:

    vertical_start = 100
    horizontal_start = 130

    if execute:
        pass

    if len(kwargs['args']) in (1, 2):

        s_creator_line = '"The Colors of Poetry" by @sunarch '

        b_test = False
        if len(kwargs['args']) == 2:
            b_test = True

        s_title_line = ""
        ls_lines = []
        i_longest = len(s_creator_line)

        with open(f"{files.FOLDER_DATA}/{kwargs['args'][0]}.txt", "rt") as f_data:

            for line in f_data:

                s_line = line.strip()

                if s_title_line == "":
                    s_title_line = s_line
                else:
                    ls_lines.append(s_line)

                if len(s_line) > i_longest:
                    i_longest = len(s_line)

        ls_lines = list(map(lambda x: line_to_adjusted_list_char(x, i_longest), ls_lines))

        ls_lines = list(map(lambda x: list_char_to_rgb(x), ls_lines))

        ls_lines = list(map(lambda x: list_char_add_vertical(x), ls_lines))

        i_horizontal = i_longest + 2

        ls_title = line_to_adjusted_list_text_triplets(s_title_line, i_longest, ' ')
        ls_title = list_char_add_vertical(ls_title)
        ls_lines.insert(0, ls_title)

        ls_top = line_to_adjusted_list_text_triplets(s_creator_line, i_longest, '/')
        ls_top = list_char_add_vertical(ls_top)
        ls_lines.insert(0, ls_top)

        ls_bottom = [horizontal()] * i_horizontal
        ls_lines.append(ls_bottom)

        i_vertical = len(ls_lines)

        result_s = api_get_size.execute()
        output.log_result(timestamp, result_s)

        try:
            width = result_s['width']
            height = result_s['height']
        except KeyError:
            raise ValueError("Invalid size.")

        if width < i_horizontal + horizontal_start:
            raise ValueError(f"Canvas not wide enough: {width} < {i_horizontal + horizontal_start}")

        if height < i_vertical + vertical_start:
            raise ValueError(f"Canvas not tall enough: {height} < {i_vertical + vertical_start}")

        for i_row, ls_single_line in enumerate(ls_lines):

            for i_col, rgb in enumerate(ls_single_line):

                if b_test:
                    ls_args = [str(i_col + horizontal_start), str(i_row + vertical_start)]
                    task_queue.put((api_get_pixel.COMMAND, ls_args, timestamp))
                    d_args = dict(zip(["x", "y"], ls_args))
                    s_request = output.form_request_input(api_get_pixel.API_NAME_GET, d_args)

                else:
                    ls_args = [str(i_col + horizontal_start), str(i_row + vertical_start), rgb]
                    task_queue.put((api_set_pixel.COMMAND, ls_args, timestamp))
                    d_args = dict(zip(["x", "y", "rgb"], ls_args))
                    s_request = output.form_request_input(api_set_pixel.API_NAME_POST, d_args)

                output.to_console(f"Queued: {s_request}")

            if not b_test:
                task_queue.put((api_get_pixels.COMMAND, [], timestamp))
                s_request = output.form_request_input(api_get_pixels.API_NAME_GET, {})
                output.to_console(f"Queued: {s_request}")

            output.to_console(output.form_separator())

        return

    raise ValueError("Invalid arguents.")


def line_to_adjusted_list_char(line: str, length: int, padder: str = ' ') -> list[str]:

    return list(f"{line:{padder}<{length}}")


def line_to_adjusted_list_text_triplets(line: str, length: int, padder: str = ' ') -> list[str]:

    s_triplet = ""
    ls_result = []

    if len(line) % 3 != 0:
        line += ' ' * (3 - (len(line) % 3))

    for i_char in range(len(line) + 1):

        try:
            s_triplet += f'{format(ord(line[i_char]), "X"):0>2}'
        except IndexError:
            pass

        if len(s_triplet) == 6:
            ls_result.append(s_triplet)
            s_triplet = ""

    while len(ls_result) < length:
        ls_result.append(format(ord(padder), "X") * 3)

    return ls_result


def list_char_to_rgb(line: list[str]) -> list[str]:

    return [char_to_color(char) for char in line]


def char_to_color(char: str) -> str:

    if char in string.printable:
        i_char = string.printable.index(char)
    else:
        i_char = random.randrange(len(string.printable))

    fl_char = i_char / len(string.printable)

    i_color = round(fl_char * len(colors_named.COLORS))

    ls_colors = list(colors_named.COLORS)

    return ls_colors[i_color]


def list_char_add_vertical(line: list[str]) -> list[str]:

    line.insert(0, vertical())
    line.append(vertical())

    return line


def vertical() -> str:

    return format(ord("|"), "X") * 3


def horizontal() -> str:

    return format(ord("-"), "X") * 3

# -------------------------------------------------------------------- #
