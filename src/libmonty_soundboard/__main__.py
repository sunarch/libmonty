#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Soundboard
"""

# imports: library
from argparse import ArgumentParser
import logging
import sys
import tkinter  # no underscore, lowercase 't' for V3.0 and later
from tkinter import ttk

# imports: dependencies
from libmonty_logging.config.file_and_stream.v1 import config as logging_config
import libmonty_logging.helper as logging_helper
import libmonty_logging.message as logging_message

# imports: project
from libmonty_soundboard.config import Config
from libmonty_soundboard import sound
from libmonty_soundboard import version


def main() -> None:
    """Main"""

    logging_helper.apply_config(version.PROGRAM_NAME,
                                version.__version__,
                                logging_config)

    logging_message.program_header('libmonty Soundboard')

    parser = ArgumentParser(prog=version.PROGRAM_NAME)

    parser.add_argument('--version',
                        help='Display version',
                        action='store_true',
                        dest='version')

    parser.add_argument('--board',
                        help='Name of the board config',
                        action='store', default=None,
                        dest='board_name')

    args = parser.parse_args(sys.argv[1:])

    if args.version:
        print(f'libmonty Soundboard {version.__version__}')
        return

    config = Config(__file__)

    if args.board_name is None:
        logging.warning('No board specified. See the --board option.')
        logging.warning('Exiting.')
        return

    config.load(args.board_name)

    root = tkinter.Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()

    ttk.Label(frm, text=config.title).grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)

    for index, sound_item in enumerate(config.sound_items):
        sound_item_path = config.data_path_board(sound_item.filename)

        ttk.Button(frm,
                   text=sound_item.text,
                   command=sound.load_sound(sound_item_path).play
                   ).grid(column=0,
                          row=index + 1)

    root.mainloop()

    sound.deinit()


if __name__ == '__main__':
    main()
