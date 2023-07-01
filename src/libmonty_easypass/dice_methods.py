#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Dice methods
"""

import secrets
from typing import List
from codetiming import Timer

N = 100000


def measure_one(measure_count: int):
    """Measure one"""

    def randlist_l_1(count: int) -> list[int]:
        return [int(''.join([str(secrets.randbelow(6) + 1)
                             for _2 in range(5)]))
                for _1 in range(count)]

    print(f'{"One: ":<10}', end='')
    measuring = Timer()
    measuring.start()
    _ = randlist_l_1(measure_count)
    measuring.stop()


def measure_parts(measure_count: int):
    """Measure parts"""

    def throws():
        return [(secrets.randbelow(6) + 1) for _ in range(5)]

    def int_join(throw_list: list):
        return int(''.join([str(i_throw) for i_throw in throw_list]))

    def randlist_l_2(count: int):
        return [int_join(throws()) for _ in range(count)]

    print(f'{"Parts: ":<10}', end='')
    measuring = Timer()
    measuring.start()
    _ = randlist_l_2(measure_count)
    measuring.stop()


def measure_detailed(measure_count: int):
    """Measure detailed"""

    def randlist(count: int) -> List[int]:
        ls_random = []

        for _1 in range(count):
            ls_throws = []

            for _2 in range(5):
                i_random = secrets.randbelow(6) + 1
                s_random = str(i_random)
                ls_throws.append(s_random)

            s_id = ''.join(ls_throws)
            i_id = int(s_id)

            ls_random.append(i_id)

        return ls_random

    print('Detailed: ', end='')
    measuring = Timer()
    measuring.start()
    _ = randlist(measure_count)
    measuring.stop()


def main(count: int = N) -> None:
    """Main"""

    print('')
    print('Method measurements:')
    print('')
    measure_one(count)
    measure_parts(count)
    measure_detailed(count)


if __name__ == '__main__':
    main()
