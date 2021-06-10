# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import queue
import threading

from libmonty.images import convert_from_stream as img_convert

from libmonty.pixels import config
from libmonty.pixels import output
from libmonty.pixels import files

from libmonty.pixels import api_get_pixel
from libmonty.pixels import api_get_pixels
from libmonty.pixels import api_get_size
from libmonty.pixels import api_set_pixel


NEXT_EXIT = "exit"
NEXT_FINISH = "finish"
NEXT_ABORT = "abort"


def main(args: list[str], kwargs: dict) -> None:

    task_queue = queue.Queue()

    abort = threading.Event()
    finish = threading.Event()

    task_worker = threading.Thread(target=task_queue_worker,
                                   daemon=True,
                                   args=[task_queue],
                                   kwargs={'abort': abort,
                                           'finish': finish}
                                   )
    task_worker.start()

    b_no_interactive = False
    if args:
        b_no_interactive = True

    config.load_token_env()

    files.archive_old_files()

    s_timestamp = files.log_filename()

    with open(files.log_path(s_timestamp), "wt", encoding="utf-8") as f_log:
        output.to_all(output.form_separator(), f_log)
        output.to_all(f"Pixels log: {s_timestamp}", f_log)
        output.to_all(output.form_separator(), f_log)

    while True:

        if not args:
            try:
                s_input = input("pixels $ ")
                output.to_console(output.form_separator())
            except KeyboardInterrupt:
                print("")  # input command empty => linebreak
                print("Type 'exit' to exit to main shell.")
                continue

            args = s_input.split(" ")

        if not args:
            continue

        command = args[0]
        ls_args = args[1:]

        try:
            s_next = process_command(command, ls_args, s_timestamp, False,
                                     task_queue=task_queue)
        except ValueError as err:
            s_next = "error"
            if str(err) != "":
                print(err)
                output.to_console(output.form_separator())
        else:
            task_queue.put((command, ls_args, s_timestamp))

        if s_next == NEXT_FINISH:
            finish.set()
            task_worker.join()
            break

        if s_next == NEXT_ABORT:
            abort.set()
            task_worker.join()
            break

        if b_no_interactive or s_next == NEXT_EXIT:
            task_queue.join()
            finish.set()
            task_worker.join()
            break

        args = []


def task_queue_worker(task_queue, **kwargs):

    abort = kwargs['abort']
    finish = kwargs['finish']

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

        try:
            process_command(command, ls_args, s_timestamp, True)
        except ValueError as err:
            if str(err) != "":
                print(err)
                output.to_console(output.form_separator())

        task_queue.task_done()


def process_command(command: str,
                    args: list[str],
                    timestamp: str,
                    execute: bool,
                    **kwargs) -> str:

    d_commands = {
        "exit": finish_all_and_exit,
        "finish": finish_queue_and_exit,
        "abort": abort_queue_and_exit,
        "queue": show_queue_size,
        "get": cmd_get,
        "img": cmd_image,
        "image": cmd_image,
        "size": cmd_size,
        "set": cmd_set
    }

    ls_args = []
    d_kwargs = {}

    for argument in args:

        if "=" not in argument:
            ls_args.append(argument)
            continue

        ls_pair = argument.split("=")

        if len(ls_pair) > 2:
            raise ValueError("Multiple '=' in keyword argument: {}".format(argument))

        d_kwargs[ls_pair[0]] = ls_pair[1]

    if command not in d_commands:
        raise ValueError("Unknown command: {}".format(command))

    try:
        task_queue = kwargs['task_queue']
    except KeyError:
        task_queue = None

    try:
        s_return = d_commands[command](ls_args, d_kwargs, timestamp, execute,
                                       task_queue=task_queue)
    except ValueError:
        raise

    return s_return


def finish_all_and_exit(args: list[str], kwargs: dict, timestamp: str, execute: bool, **kwargs2) -> str:
    return NEXT_EXIT


def finish_queue_and_exit(args: list[str], kwargs: dict, timestamp: str, execute: bool, **kwargs2) -> str:
    return NEXT_FINISH


def abort_queue_and_exit(args: list[str], kwargs: dict, timestamp: str, execute: bool, **kwargs2) -> str:
    return NEXT_ABORT


def show_queue_size(args: list[str], kwargs: dict, timestamp: str, execute: bool, **kwargs2) -> None:

    try:
        output.to_console(f"Items in queue: {kwargs2['task_queue'].qsize()}")
        output.to_console(output.form_separator())
    except AttributeError:
        pass


def cmd_get(args: list[str], kwargs: dict, timestamp: str, execute: bool, **kwargs2) -> None:

    if len(args) == 1 and args[0] == "head":
        if execute:
            result = api_get_pixel.headers()
            output.log_result(timestamp, result)
        else:
            s_request = output.form_request_input(api_set_pixel.API_NAME_HEAD, {})
            output.to_console(f"Queued: {s_request}")
            output.to_console(output.form_separator())
        return

    if len(args) == 2:
        if execute:
            result = api_get_pixel.execute(int(args[0]), int(args[1]))
            output.log_result(timestamp, result)
        else:
            d_args = dict(zip(["x", "y"], args))
            s_request = output.form_request_input(api_get_pixel.API_NAME_GET, d_args)
            output.to_console(f"Queued: {s_request}")
            output.to_console(output.form_separator())
        return

    raise ValueError("Invalid arguments.")


def cmd_image(args: list[str], kwargs: dict, timestamp: str, execute: bool, **kwargs2) -> None:

    if len(args) == 1 and args[0] == "head":
        if execute:
            result = api_get_pixels.headers()
            output.log_result(timestamp, result)
        else:
            s_request = output.form_request_input(api_get_pixels.API_NAME_HEAD, {})
            output.to_console(f"Queued: {s_request}")
            output.to_console(output.form_separator())
        return

    if len(args) == 0 and not kwargs:
        if execute:
            subcmd_image(timestamp)
        else:
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
    except KeyError:
        pass


def cmd_size(args: list[str], kwargs: dict, timestamp: str, execute: bool, **kwargs2) -> None:

    if len(args) == 0 and not kwargs:
        if execute:
            result = api_get_size.execute()
            output.log_result(timestamp, result)
        else:
            s_request = output.form_request_input(api_get_size.API_NAME_GET, {})
            output.to_console(f"Queued: {s_request}")
            output.to_console(output.form_separator())
        return

    raise ValueError("Invalid arguents.")


def cmd_set(args: list[str], kwargs: dict, timestamp: str, execute: bool, **kwargs2) -> None:

    if len(args) == 1 and args[0] == "head":
        if execute:
            result = api_set_pixel.headers()
            output.log_result(timestamp, result)
        else:
            s_request = output.form_request_input(api_set_pixel.API_NAME_HEAD, {})
            output.to_console(f"Queued: {s_request}")
            output.to_console(output.form_separator())
        return

    if len(args) == 3:
        if execute:
            result = api_set_pixel.execute(int(args[0]), int(args[1]), args[2])
            output.log_result(timestamp, result)
        else:
            d_args = dict(zip(["x", "y", "rgb"], args))
            s_request = output.form_request_input(api_set_pixel.API_NAME_POST, d_args)
            output.to_console(f"Queued: {s_request}")
            output.to_console(output.form_separator())
        return

    raise ValueError("Invalid arguents.")

# -------------------------------------------------------------------- #
