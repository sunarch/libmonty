# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys

from libmonty.hexer import hexer


def main(args: list[str]) -> None:

    ls_input = args[1:]

    while True:

        if len(ls_input) == 0:
            s_input = input("libmonty $ ")
            ls_input = s_input.split(" ")

        if len(ls_input) < 1:
            continue

        command = ls_input[0]
        ls_args = ls_input[1:]

        try:
            process_command(command, ls_args)
        except ValueError as err:
            print(err)

        ls_input = []


def process_command(command: str, args: list[str]) -> None:

    d_commands = {
        "hexer": hexer.main
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

    if command in d_commands:
        d_commands[command](args, d_kwargs)


if __name__ == "__main__":
    main(sys.argv)

# -------------------------------------------------------------------- #
