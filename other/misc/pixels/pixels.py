#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import queue
import threading

from pixels import config
from pixels import output
from pixels import files
from pixels import commands

from pixels import worker

from pixels.cmd_process import process_command


def main(args: list[str], kwargs: dict) -> None:

    task_queue = queue.Queue()

    abort = threading.Event()
    finish = threading.Event()

    task_worker = threading.Thread(target=worker.task_queue_worker,
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

    with open(files.log_path(s_timestamp), 'wt', encoding='UTF-8') as f_log:
        output.to_all(output.form_separator(), f_log)
        output.to_all(f'Pixels log: {s_timestamp}', f_log)
        output.to_all(output.form_separator(), f_log)

    while True:

        if not args:
            try:
                s_input = input('pixels $ ')
                output.to_console(output.form_separator())
            except KeyboardInterrupt:
                print('')  # input command empty => linebreak
                print('Type \'exit\' to exit to main shell.')
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
            s_next = 'error'
            if str(err) != '':
                print(err)
                output.to_console(output.form_separator())

        if s_next == commands.COMMAND_FINISH:
            finish.set()
            task_worker.join()
            break

        if s_next == commands.COMMAND_ABORT:
            abort.set()
            task_worker.join()
            break

        if b_no_interactive or s_next == commands.COMMAND_EXIT:
            task_queue.join()
            finish.set()
            task_worker.join()
            break

        args = []

# -------------------------------------------------------------------- #
