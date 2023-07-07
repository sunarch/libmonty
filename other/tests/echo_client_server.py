#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
from contextlib import contextmanager
import logging.config
import socket
import time

from enum import Enum


class RunType(Enum):
    SERVER = 'server'
    CLIENT = 'client'


LOCALHOST = '127.0.0.1'
DEFAULT_PORT = 65432
DEFAULT_DATA_LIMIT = 1024
DEFAULT_RETRY_INTERVAL_SECS = 1

LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'form01': {
            'format': '[%(asctime)s] [%(levelname)-8s] %(message)s',
            'datefmt': '%H:%M:%S'
        }
    },
    'handlers': {
        'hand01': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'form01',
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        'root': {
            'level': 'NOTSET',
            'handlers': ['hand01']
        }
    }
}


def main():
    logging.config.dictConfig(LOGGING_CONFIG)

    parser = argparse.ArgumentParser()

    parser.add_argument('--host',
                        help='Host',
                        action='store',
                        dest='host', default=LOCALHOST)

    parser.add_argument('--port',
                        help='Port',
                        action='store',
                        dest='port', default=DEFAULT_PORT)

    parser.add_argument('--limit',
                        help='Data limit',
                        action='store', type=int,
                        dest='data_limit', default=DEFAULT_DATA_LIMIT)

    parser.add_argument('--retry',
                        help='Connection retry interval, in seconds',
                        action='store', type=int,
                        dest='retry_interval_secs', default=DEFAULT_RETRY_INTERVAL_SECS)

    group_type = parser.add_mutually_exclusive_group()

    group_type.add_argument('--server',
                            help='Run server',
                            action='store_const', const=RunType.SERVER,
                            dest='run_type')

    group_type.add_argument('--client',
                            help='Run client',
                            action='store_const', const=RunType.CLIENT,
                            dest='run_type')

    args = parser.parse_args()

    match args.run_type:
        case RunType.SERVER:
            server(args.host, args.port, args.data_limit)
        case RunType.CLIENT:
            client(args.host, args.port, args.data_limit, args.retry_interval_secs)
        case _:
            print('Echo server/client. See --help for options.')


@contextmanager
def socket_handler(*args, **kwargs):

    logging.info('Creating socket.')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            yield sock
        finally:
            sock.close()
            logging.info('Socket shut down.')


def client(host: str, port: int, data_limit: int, retry_interval: int) -> None:

    with socket_handler() as sock_h:

        logging.info('Connecting to: %s:%s', host, port)
        success = False
        while not success:
            try:
                sock_h.connect((host, port))
            except ConnectionRefusedError:
                logging.error('Connection refused, retrying.')
                time.sleep(retry_interval)
            else:
                success = True

        finished = False
        while not finished:
            try:
                data_out = input('Data to send: ').strip()
                logging.info('Sending data ...')
                sock_h.sendall(data_out.encode('UTF-8'))
                logging.info('... sent.')

                logging.info('Waiting for data back...')
                data_in = sock_h.recv(data_limit)
                logging.info('... received: %s', data_in.decode('UTF-8'))

            except BrokenPipeError:
                logging.warning('Connection to server broken, exiting...')
                finished = True

            except KeyboardInterrupt:
                logging.warning('Keyboard interrupt received, exiting...')
                finished = True


def server(host: str, port: int, data_limit: int) -> None:

    with socket_handler() as sock_h:

        logging.info('Binding %s:%s', host, port)
        success = False
        while not success:
            try:
                sock_h.bind((host, port))
            except OSError as err:
                logging.warning('OS error: %s', err)
                logging.info('Forcing socket reuse...')
                sock_h.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                time.sleep(2)
            else:
                success = True

        logging.info('Starting to listen.')
        sock_h.listen()

        finished = False
        while not finished:
            try:
                logging.info('Waiting for connection ...')
                conn, addr = sock_h.accept()

                with conn:
                    logging.info('... connected by %s', f'{addr[0]}:{addr[1]}')

                    while True:
                        logging.info('Waiting for data ...')
                        data = conn.recv(data_limit)
                        if not data:
                            break

                        logging.info('... received: %s', data.decode('UTF-8'))

                        logging.info('Sending data back...')
                        conn.sendall(data)
                        logging.info('... sent.')

            except KeyboardInterrupt:
                logging.warning('Keyboard interrupt received, exiting.')
                finished = True


if __name__ == '__main__':
    main()
