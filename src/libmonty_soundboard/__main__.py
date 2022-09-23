#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# imports: library
from argparse import ArgumentParser
import configparser
import logging
import logging.config
import pkg_resources
import sys
import tkinter  # no underscore, lowercase 't' for V3.0 and later
from tkinter import ttk

# imports: project
from libmonty_soundboard.config import Config
from libmonty_soundboard import sound
from libmonty_soundboard.version import __version__


def main() -> None:

    logger_config_name = 'data/logger.ini'

    if not pkg_resources.resource_exists(__name__, logger_config_name):
        logging.error('logger config does not exist')
        return

    logger_config = pkg_resources.resource_stream(__name__, logger_config_name)
    logger_config_str = logger_config.read().decode('UTF-8')
    logger_config_parser = configparser.ConfigParser()
    logger_config_parser.read_string(logger_config_str)
    logging.config.fileConfig(logger_config_parser)

    logging.info('libmonty Soundboard')
    logging.info('----------')

    parser = ArgumentParser(prog='libmonty-soundboard')

    parser.add_argument('--version',
                        help='Display version',
                        action='store_const', const=True, default=False,
                        dest='version')

    parser.add_argument('--board',
                        help='Name of the board config',
                        action='store', default=None,
                        dest='board_name')

    args = parser.parse_args(sys.argv[1:])

    if args.version:
        print(f'libmonty Soundboard {__version__}')
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
