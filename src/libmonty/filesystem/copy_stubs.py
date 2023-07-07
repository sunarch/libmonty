#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Copy stubs
"""

# imports: library
import os


def copy_stubs(from_dir: str, to_dir: str, change: tuple[str, str]) -> None:
    """Copy stubs"""

    from_dir, to_dir = map(lambda x: x.strip(), (from_dir, to_dir))
    change_from, change_to = map(lambda x: x.strip(), change)

    if not os.path.exists(to_dir) or not os.path.isdir(to_dir):
        raise RuntimeError(f'TO dir does not exist: {to_dir}')

    try:
        file_list: list[str] = os.listdir(from_dir)
    except FileNotFoundError as exc:
        raise RuntimeError(f'FROM dir does not exist: {from_dir}') from exc
    except NotADirectoryError as exc:
        raise RuntimeError(f'FROM dir is not a directory: {from_dir}') from exc

    for filename_old in file_list:

        print('')
        print(' ' * 3, filename_old)

        filename, _ = os.path.splitext(filename_old)

        filename_new: str = filename.replace(change_from, change_to) + '.txt'

        print(' ->', filename_new)

        path_new: str = os.path.join(to_dir, filename_new)

        if os.path.isfile(path_new):
            print(' ', '#', 'Already existed.')
            continue

        with open(path_new, 'w', encoding='UTF-8') as fh_new:
            print('', file=fh_new)

        print(' ', '#', 'Done.')

    print('')


def main() -> None:
    """Main"""

    src_dir: str = input('Source dir: ')
    dest_dir: str = input('Destination dir: ')

    replace: str = input('Replace: ')
    replace_with: str = input('Replace with: ')

    try:
        copy_stubs(src_dir, dest_dir, (replace, replace_with))
    except RuntimeError as err:
        print(err)


if __name__ == '__main__':
    main()
