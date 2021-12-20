#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pixels import commands

from pixels import api_get_pixel
from pixels import api_get_pixels
from pixels import api_get_size
from pixels import api_set_pixel

from pixels.projects import poetry as project_poetry


def process_command(command: str,
                    args: list[str],
                    timestamp: str,
                    execute: bool = False,
                    **kwargs) -> str:

    d_commands = {
        commands.COMMAND_EXIT: commands.finish_all_and_exit,
        commands.COMMAND_FINISH: commands.finish_queue_and_exit,
        commands.COMMAND_ABORT: commands.abort_queue_and_exit,
        'queue': commands.show_queue_size,
        'q': commands.show_queue_size,
        api_get_pixel.COMMAND: commands.cmd_get,
        api_get_pixels.COMMAND: commands.cmd_image,
        'img': commands.cmd_image,
        api_get_size.COMMAND: commands.cmd_size,
        api_set_pixel.COMMAND: commands.cmd_set,
        project_poetry.COMMAND: project_poetry.command
    }

    ls_args = []
    d_kwargs = {}

    for argument in args:

        if '=' not in argument:
            ls_args.append(argument)
            continue

        ls_pair = argument.split('=')

        if len(ls_pair) > 2:
            raise ValueError(f'Multiple \'=\' in keyword argument: {argument}')

        d_kwargs[ls_pair[0]] = ls_pair[1]

    if command not in d_commands:
        raise ValueError(f'Unknown command: {command}')

    try:
        task_queue = kwargs['task_queue']
    except KeyError:
        task_queue = None

    try:
        s_return = d_commands[command](execute, timestamp, task_queue,
                                       args=ls_args,
                                       kwargs=d_kwargs)
    except ValueError:
        raise

    return s_return

# -------------------------------------------------------------------- #
