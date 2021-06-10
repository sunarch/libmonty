# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from libmonty.images import convert_from_stream as img_convert

from libmonty.pixels import config
from libmonty.pixels import output
from libmonty.pixels import files

from libmonty.pixels import api_get_pixel
from libmonty.pixels import api_get_pixels
from libmonty.pixels import api_get_size
from libmonty.pixels import api_set_pixel


def main(args: list[str], kwargs: dict) -> None:

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
            s_next = process_command(command, ls_args, s_timestamp)
        except ValueError as err:
            if str(err) != "":
                print(err)
        else:
            if s_next is not None:
                break

        if b_no_interactive:
            break

        args = []


def process_command(command: str, args: list[str], timestamp: str) -> str:

    output.to_console(output.form_separator())

    d_commands = {
        "exit": exit_interactive,
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
        s_return = d_commands[command](ls_args, d_kwargs, timestamp)
    except ValueError:
        raise

    return s_return


def exit_interactive(args: list[str], kwargs: dict, timestamp: str) -> str:
    return "break"


def cmd_get(args: list[str], kwargs: dict, timestamp: str) -> None:

    if len(args) == 1 and args[0] == "head":
        result = api_get_pixel.headers()
        output.log_result(timestamp, result)

    if len(args) == 2:
        result = api_get_pixel.execute(int(args[0]), int(args[1]))
        output.log_result(timestamp, result)


def cmd_image(args: list[str], kwargs: dict, timestamp: str) -> None:

    if len(args) == 1 and args[0] == "head":
        result = api_get_pixels.headers()
        output.log_result(timestamp, result)

    if len(args) == 0 and not kwargs:
        subcmd_image(timestamp)


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


def cmd_size(args: list[str], kwargs: dict, timestamp: str) -> None:

    if len(args) == 0 and not kwargs:
        result = api_get_size.execute()
        output.log_result(timestamp, result)


def cmd_set(args: list[str], kwargs: dict, timestamp: str) -> None:

    if len(args) == 1 and args[0] == "head":
        result = api_set_pixel.headers()
        output.log_result(timestamp, result)

    if len(args) == 3:
        result = api_set_pixel.execute(int(args[0]), int(args[1]), args[2])
        output.log_result(timestamp, result)

# -------------------------------------------------------------------- #
