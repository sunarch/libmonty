# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
import traceback

from libmonty.hexer import hexer


def main(args: list[str]) -> None:

    b_debug = False
    ls_input = args[1:]

    while True:

        if len(ls_input) == 0:
            try:
                s_input = input("libmonty $ ")
            except KeyboardInterrupt:
                print("")  # input command empty => linebreak
                print("Type 'exit' to exit interactive mode.")
                continue

            ls_input = s_input.split(" ")

        if len(ls_input) < 1:
            continue

        command = ls_input[0]
        ls_args = ls_input[1:]

        try:
            s_next = process_command(command, ls_args)
        except ValueError as err:
            if str(err) != "":
                print(err)
            if b_debug:
                traceback.print_exc()
        else:
            if s_next == "debug":
                if b_debug:
                    b_debug = False
                    print("Debug disabled.")
                else:
                    b_debug = True
                    print("Debug enabled.")

            elif s_next is not None:
                break

        ls_input = []


def process_command(command: str, args: list[str]) -> str:

    d_commands = {
        "exit": exit_interactive,
        "debug": toggle_debug,
        "hexer": hexer.main,
        "pixels": pixels.main
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
        s_return = d_commands[command](ls_args, d_kwargs)
    except ValueError:
        raise

    return s_return


def exit_interactive(args: list[str], kwargs: dict) -> str:
    return "break"


def toggle_debug(args: list[str], kwargs: dict) -> str:
    return "debug"


if __name__ == "__main__":
    main(sys.argv)

# -------------------------------------------------------------------- #
