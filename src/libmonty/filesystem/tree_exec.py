#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os.path
import subprocess
import argparse

DEBUG_INDENT = True
DEBUG_PARENT_LAST = True


class IndentItem:
    BeforeLast = '│   '
    AfterLast = '    '
    DirRoot = ''
    DirMiddle = '├── '
    DirLast = '└── '


def quoted(content):
    return '"{}"'.format(content)


def prefixed(content, indents=None, tree=None):
    if indents is None:
        indents = []

    prefix_str = ''.join(indents[:-1])

    if tree is None:
        prefix_str += '-> '
    else:
        prefix_str += tree

    return prefix_str + content


def recursive_list(dir_name, command=None, indents=None, tree=None):
    if indents is None:
        indents = []

    if tree == IndentItem.DirRoot:
        display_name = dir_name
    else:
        display_name = os.path.basename(dir_name)

    print(prefixed(display_name, indents=indents, tree=tree))

    if command is not None:
        indents_comment = indents + [IndentItem.AfterLast]
        indents_subcomment = indents_comment + [IndentItem.AfterLast]

        try:
            dir_space_escaped = dir_name.replace(' ', '\\' + ' ')
            command_substituted = command.replace('$', dir_space_escaped)
            print(prefixed('applying ', indents=indents_comment) + quoted(command_substituted))
            sub_output = subprocess.check_output(command_substituted, shell=True)
        except subprocess.CalledProcessError as err:
            print(prefixed('Error code: ', indents=indents_comment) + quoted(err.returncode))
            print(prefixed('Error message: ', indents=indents_comment) + quoted(err.output))
        else:
            print(prefixed('Return code: ', indents=indents_comment) + quoted('0'))
            print(prefixed('Output: ', indents=indents_comment))
            output_items = sub_output.split(b'\n')
            if output_items[-1] == '':
                output_items = output_items[:-1]
            for item in output_items:
                item = str(item, encoding='UTF-8')
                print(prefixed(quoted(item), indents=indents_subcomment))

    try:
        dir_list = [os.path.join(dir_name, item)
                    for item in os.listdir(dir_name)]
    except OSError:
        return

    dir_list_filtered = [os.path.normpath(item)
                         for item in dir_list
                         if os.path.isdir(item)]

    indents_before = indents + [IndentItem.BeforeLast]
    for item in dir_list_filtered[:-1]:
        recursive_list(item, command, indents=indents_before, tree=IndentItem.DirMiddle)

    if len(dir_list_filtered) > 0:
        indents_after = indents + [IndentItem.AfterLast]
        recursive_list(dir_list_filtered[-1], command, indents=indents_after, tree=IndentItem.DirLast)


def arg_type_dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError('Given argument "{}" is not a valid directory path'.format(path))


def main():
    parser = argparse.ArgumentParser(description='Directory list with applied command.')

    parser.add_argument('--root', dest='root', default=os.getcwd(), type=arg_type_dir_path,
                        help='Root directory to recursively execute script from.')

    parser.add_argument('--command', dest='command', default=None,
                        help='Shell command to execute on every directory.')

    args = parser.parse_args()
    root = os.path.abspath(str(args.root, encoding='UTF-8'))

    recursive_list(root, command=args.command, tree=IndentItem.DirRoot)


if __name__ == '__main__':
    main()
