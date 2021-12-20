#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import queue
import time

from types import ModuleType

from pixels import output
from pixels import files

from pixels.cmd_process import process_command

from pixels import api_get_pixel
from pixels import api_get_pixels
from pixels import api_set_pixel
from pixels import api_headers


def task_queue_worker(task_queue, **kwargs):

    abort = kwargs['abort']
    finish = kwargs['finish']

    i_remaining_get = 0
    i_remaining_img = 0
    i_remaining_set = 0

    while True:

        if abort.is_set():
            output.to_console("Processing aborted.")
            output.to_console(output.form_separator())
            break

        try:
            command, ls_args, s_timestamp = task_queue.get_nowait()
        except queue.Empty:
            if finish.is_set():
                output.to_console("Queue finished.")
                output.to_console(output.form_separator())
                break
            else:
                # output.to_console("Queue empty. Waiting for tasks.")
                # output.to_console(output.form_separator())
                continue

        if command == api_get_pixel.COMMAND and "head" not in ls_args:
            i_remaining_get = ratelimit_if_needed(api_get_pixel, i_remaining_get, s_timestamp)

        elif command == api_get_pixels.COMMAND and "head" not in ls_args:
            i_remaining_img = ratelimit_if_needed(api_get_pixels, i_remaining_img, s_timestamp)

        elif command == api_set_pixel.COMMAND and "head" not in ls_args:
            i_remaining_set = ratelimit_if_needed(api_set_pixel, i_remaining_set, s_timestamp)

        try:
            process_command(command, ls_args, s_timestamp, execute=True)
        except ValueError as err:
            if str(err) != "":
                print(err)
                output.to_console(output.form_separator())

        if command == api_get_pixel.COMMAND and "head" not in ls_args:
            i_remaining_get -= 1
        elif command == api_get_pixels.COMMAND and "head" not in ls_args:
            i_remaining_img -= 1
        elif command == api_set_pixel.COMMAND and "head" not in ls_args:
            i_remaining_set -= 1

        task_queue.task_done()

        with open(files.log_path(s_timestamp), "at", encoding="utf-8") as f_log:
            output.to_all(f"Remaining in queue: {task_queue.qsize()}", f_log)
            output.to_all(output.form_separator(), f_log)


def ratelimit_if_needed(api_module: ModuleType, remaining: int, timestamp: str) -> int:

    if remaining > 0:
        return remaining

    else:
        # check time to reset

        headers_result = api_module.headers()
        output.log_result(timestamp, headers_result)

        # if cooldown is given, sleep until that is done

        if headers_result['cooldown'] is not None:
            delay(float(headers_result['cooldown']))
            with open(files.log_path(timestamp), "at", encoding="utf-8") as f_log:
                output.to_all(f"Cooldown: {headers_result['cooldown'] + ' ':|<62}", f_log)
                output.to_all(output.form_separator(), f_log)

        fl_reset = float(headers_result['rate_limits'][api_headers.RATE_LIMIT_TIME_RESET])

        with open(files.log_path(timestamp), "at", encoding="utf-8") as f_log:
            output.to_all(f"Sleep: {str(fl_reset) + ' ':|<65}", f_log)
            output.to_all(output.form_separator(), f_log)

        # sleep until reset

        delay(fl_reset)

        # check and return new remaining count

        headers_result = api_module.headers()
        output.log_result(timestamp, headers_result)

        return int(headers_result['rate_limits'][api_headers.RATE_LIMIT_COUNT_REMAINING])


def delay(seconds: float, margin: float = 0.1) -> None:

    target_time = time.time() + seconds + margin

    time.sleep(seconds + margin)

    # if sleep was shorter, ensure time
    while time.time() < target_time:
        pass

# -------------------------------------------------------------------- #
