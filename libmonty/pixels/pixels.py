# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import queue
import threading

from libmonty.pixels import config
from libmonty.pixels import output
from libmonty.pixels import files
from libmonty.pixels import commands


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
            s_next = process_command(command, ls_args, s_timestamp,
                                     execute=False,
                                     task_queue=task_queue)
        except ValueError as err:
            s_next = "error"
            if str(err) != "":
                print(err)
                output.to_console(output.form_separator())

        if s_next == commands.NEXT_FINISH:
            finish.set()
            task_worker.join()
            break

        if s_next == commands.NEXT_ABORT:
            abort.set()
            task_worker.join()
            break

        if b_no_interactive or s_next == commands.NEXT_EXIT:
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
            process_command(command, ls_args, s_timestamp, execute=True)
        except ValueError as err:
            if str(err) != "":
                print(err)
                output.to_console(output.form_separator())

        task_queue.task_done()


def process_command(command: str,
                    args: list[str],
                    timestamp: str,
                    execute: bool = False,
                    **kwargs) -> str:

    d_commands = {
        "exit": commands.finish_all_and_exit,
        "finish": commands.finish_queue_and_exit,
        "abort": commands.abort_queue_and_exit,
        "queue": commands.show_queue_size,
        "get": commands.cmd_get,
        "img": commands.cmd_image,
        "image": commands.cmd_image,
        "size": commands.cmd_size,
        "set": commands.cmd_set
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
        s_return = d_commands[command](execute, timestamp, task_queue,
                                       args=ls_args,
                                       kwargs=d_kwargs)
    except ValueError:
        raise

    return s_return

# -------------------------------------------------------------------- #
