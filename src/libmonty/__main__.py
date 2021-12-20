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
import traceback

# imports: project
from libmonty import version
from libmonty.hexer import hexer


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

    logging.info(version.program_name)
    logging.info('-' * len(version.program_name))

    parser = ArgumentParser(prog=version.program_name)

    parser.add_argument('--version',
                        help='Display version',
                        action='store_const', const=True, default=False,
                        dest='version')

    parser.add_argument('--debug',
                        help='Enable debug output',
                        action='store_const', const=True, default=False,
                        dest='debug')

    subparsers = parser.add_subparsers(help='command',
                                       dest='command',
                                       metavar='COMMAND')

    hexer.create_arguments(subparsers)

    args = parser.parse_args(sys.argv[1:])

    if 'command' not in vars(args):

        if args.version:
            print(f'{version.program_name} {version.__version__}')
            return

    else:
        try:
            if args.command == 'hexer':
                hexer.main(args)
        except ValueError as err:
            if str(err) != "":
                print(err)
            if args.debug:
                traceback.print_exc()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------- #
