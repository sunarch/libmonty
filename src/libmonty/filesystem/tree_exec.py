#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Tree exec
"""

# imports: library
import argparse
import os.path
import subprocess


DEBUG_INDENT: bool = True
DEBUG_PARENT_LAST: bool = True


class IndentItem:
    """IdentItem"""

    BeforeLast: str = '│   '
    AfterLast: str = '    '
    DirRoot: str = ''
    DirMiddle: str = '├── '
    DirLast: str = '└── '


def quoted(content) -> str:
    """Quoted"""

    return f'"{content}"'


def prefixed(content: str, indents: list[str] = None, tree: str = None) -> str:
    """Prefixed"""

    if indents is None:
        indents: list = []

    prefix: str = ''.join(indents[:-1])

    if tree is None:
        prefix += '-> '
    else:
        prefix += tree

    return prefix + content


def recursive_list(dir_name: str,
                   command: str = None,
                   indents: list[str] = None,
                   tree: str = None
                   ) -> None:
    """Recursive list"""

    if indents is None:
        indents: list = []

    if tree == IndentItem.DirRoot:
        display_name: str = dir_name
    else:
        display_name: str = os.path.basename(dir_name)

    print(prefixed(display_name, indents=indents, tree=tree))

    if command is not None:
        indents_comment: list[str] = indents + [IndentItem.AfterLast]
        indents_subcomment: list[str] = indents_comment + [IndentItem.AfterLast]

        try:
            dir_space_escaped: str = dir_name.replace(' ', '\\' + ' ')
            command_substituted: str = command.replace('$', dir_space_escaped)
            print(prefixed('applying ', indents=indents_comment) + quoted(command_substituted))
            sub_output = subprocess.check_output(command_substituted, shell=True)
        except subprocess.CalledProcessError as err:
            print(prefixed('Error code: ', indents=indents_comment) + quoted(err.returncode))
            print(prefixed('Error message: ', indents=indents_comment) + quoted(err.output))
        else:
            print(prefixed('Return code: ', indents=indents_comment) + quoted('0'))
            print(prefixed('Output: ', indents=indents_comment))
            output_items: list = sub_output.split(b'\n')
            if output_items[-1] == '':
                output_items: list = output_items[:-1]
            for item in output_items:
                item = str(item, encoding='UTF-8')
                print(prefixed(quoted(item), indents=indents_subcomment))

    try:
        dir_list: list[str] = [
            os.path.join(dir_name, item)
            for item in os.listdir(dir_name)
        ]
    except OSError:
        return

    dir_list_filtered: list[str] = [
        os.path.normpath(item)
        for item in dir_list
        if os.path.isdir(item)
    ]

    indents_before: list[str] = indents + [IndentItem.BeforeLast]
    for item in dir_list_filtered[:-1]:
        recursive_list(item, command,
                       indents=indents_before, tree=IndentItem.DirMiddle)

    if len(dir_list_filtered) > 0:
        indents_after: list[str] = indents + [IndentItem.AfterLast]
        recursive_list(dir_list_filtered[-1], command,
                       indents=indents_after, tree=IndentItem.DirLast)


def arg_type_dir_path(path: str) -> str:
    """Arg type: dir path"""

    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(f'Given argument "{path}" is not a valid directory path')

    return path


def main() -> None:
    """Main"""

    parser = argparse.ArgumentParser(description='Directory list with applied command.')

    parser.add_argument('--root', dest='root', default=os.getcwd(), type=arg_type_dir_path,
                        help='Root directory to recursively execute script from.')

    parser.add_argument('--command', dest='command', default=None,
                        help='Shell command to execute on every directory.')

    args = parser.parse_args()
    root: str = os.path.abspath(str(args.root, encoding='UTF-8'))

    recursive_list(root, command=args.command, tree=IndentItem.DirRoot)


if __name__ == '__main__':
    main()
