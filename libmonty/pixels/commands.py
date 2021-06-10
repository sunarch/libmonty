# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from libmonty.images import convert_from_stream as img_convert

from libmonty.pixels import output
from libmonty.pixels import files

from libmonty.pixels import api_get_pixel
from libmonty.pixels import api_get_pixels
from libmonty.pixels import api_get_size
from libmonty.pixels import api_set_pixel


COMMAND_EXIT = "exit"
COMMAND_FINISH = "finish"
COMMAND_ABORT = "abort"


def finish_all_and_exit(execute: bool, timestamp: str, task_queue, **kwargs) -> str:
    return COMMAND_EXIT


def finish_queue_and_exit(execute: bool, timestamp: str, task_queue, **kwargs) -> str:
    return COMMAND_FINISH


def abort_queue_and_exit(execute: bool, timestamp: str, task_queue, **kwargs) -> str:
    return COMMAND_ABORT


def show_queue_size(execute: bool, timestamp: str, task_queue, **kwargs) -> None:

    try:
        output.to_console(f"Items in queue: {task_queue.qsize()}")
        output.to_console(output.form_separator())
    except AttributeError:
        pass


def cmd_get(execute: bool, timestamp: str, task_queue, **kwargs) -> None:

    if len(kwargs['args']) == 1 and kwargs['args'][0] == "head":
        if execute:
            result = api_get_pixel.headers()
            output.log_result(timestamp, result)
        else:
            task_queue.put((api_get_pixel.COMMAND, kwargs['args'], timestamp))
            s_request = output.form_request_input(api_get_pixel.API_NAME_HEAD, {})
            output.to_console(f"Queued: {s_request}")
            output.to_console(output.form_separator())
        return

    if len(kwargs['args']) == 2:
        if execute:
            result = api_get_pixel.execute(int(kwargs['args'][0]), int(kwargs['args'][1]))
            output.log_result(timestamp, result)
        else:
            task_queue.put((api_get_pixel.COMMAND, kwargs['args'], timestamp))
            d_args = dict(zip(["x", "y"], kwargs['args']))
            s_request = output.form_request_input(api_get_pixel.API_NAME_GET, d_args)
            output.to_console(f"Queued: {s_request}")
            output.to_console(output.form_separator())
        return

    raise ValueError("Invalid arguments.")


def cmd_image(execute: bool, timestamp: str, task_queue, **kwargs) -> None:

    if len(kwargs['args']) == 1 and kwargs['args'][0] == "head":
        if execute:
            result = api_get_pixels.headers()
            output.log_result(timestamp, result)
        else:
            task_queue.put((api_get_pixels.COMMAND, kwargs['args'], timestamp))
            s_request = output.form_request_input(api_get_pixels.API_NAME_HEAD, {})
            output.to_console(f"Queued: {s_request}")
            output.to_console(output.form_separator())
        return

    if len(kwargs['args']) == 0 and not kwargs['kwargs']:
        if execute:
            subcmd_image(timestamp)
        else:
            task_queue.put((api_get_pixels.COMMAND, kwargs['args'], timestamp))
            s_request = output.form_request_input(api_get_pixels.API_NAME_GET, {})
            output.to_console(f"Queued: {s_request}")
            output.to_console(output.form_separator())
        return

    raise ValueError("Invalid arguents.")


def subcmd_image(timestamp: str) -> None:

    result_s = api_get_size.execute()
    output.log_result(timestamp, result_s)

    result_p = api_get_pixels.execute()
    output.log_result(timestamp, result_p)

    try:
        img_convert.rgb(files.FOLDER_IMG,
                        timestamp,
                        result_p['bytes'],
                        (result_s['width'], result_s['height']),
                        scale=8)

        with open(f"{files.FOLDER_IMG}/{timestamp}.bin", "wb") as f_bin:
            f_bin.write(result_p['bytes'])

    except KeyError:
        pass


def cmd_size(execute: bool, timestamp: str, task_queue, **kwargs) -> None:

    if len(kwargs['args']) == 0 and not kwargs['kwargs']:
        if execute:
            result = api_get_size.execute()
            output.log_result(timestamp, result)
        else:
            task_queue.put((api_get_size.COMMAND, kwargs['args'], timestamp))
            s_request = output.form_request_input(api_get_size.API_NAME_GET, {})
            output.to_console(f"Queued: {s_request}")
            output.to_console(output.form_separator())
        return

    raise ValueError("Invalid arguents.")


def cmd_set(execute: bool, timestamp: str, task_queue, **kwargs) -> None:

    if len(kwargs['args']) == 1 and kwargs['args'][0] == "head":
        if execute:
            result = api_set_pixel.headers()
            output.log_result(timestamp, result)
        else:
            task_queue.put((api_set_pixel.COMMAND, kwargs['args'], timestamp))
            s_request = output.form_request_input(api_set_pixel.API_NAME_HEAD, {})
            output.to_console(f"Queued: {s_request}")
            output.to_console(output.form_separator())
        return

    if len(kwargs['args']) == 3:
        if execute:
            result = api_set_pixel.execute(int(kwargs['args'][0]), int(kwargs['args'][1]), kwargs['args'][2])
            output.log_result(timestamp, result)
        else:
            task_queue.put((api_set_pixel.COMMAND, kwargs['args'], timestamp))
            d_args = dict(zip(["x", "y", "rgb"], kwargs['args']))
            s_request = output.form_request_input(api_set_pixel.API_NAME_POST, d_args)
            output.to_console(f"Queued: {s_request}")
            output.to_console(output.form_separator())
        return

    raise ValueError("Invalid arguents.")

# -------------------------------------------------------------------- #
