#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Directory
"""

# imports: library
import os
import re

# fields and initial values ####################################################

BASE_DIR: str = '~'
DATA_FILE_DICT_DELIMITER: str = '='


# operations ###################################################################

def join(path_1: str, path_2: str) -> str:
    """Join two directory paths"""

    return os.path.join(path_1, path_2)


# current directory information ################################################

def get_current_dir() -> str:
    """Get current dir"""

    return os.path.basename(os.getcwd())


def get_current_dir_path() -> str:
    """Get current dir path"""

    return os.getcwd()


def get_current_dir_content() -> dict:
    """Get current dir content"""

    content_list = os.listdir(os.getcwd())

    return {
        'list': content_list,
        'count': len(content_list)
    }


def get_current_dir_content_list() -> list[str]:
    """Get current dit content list"""

    return os.listdir(os.getcwd())


def get_current_dir_content_count() -> int:
    """Get current dir content count"""

    return len(os.listdir(os.getcwd()))


# checks #######################################################################

def is_dir(arg_path) -> bool:
    """Is dir?"""

    return os.path.isdir(arg_path)


def is_file(arg_path) -> bool:
    """Is file?"""

    return os.path.isfile(arg_path)


# navigation ###################################################################

def navigate(arg_path) -> None:
    """Navigate"""

    os.chdir(arg_path)


def nav_parent() -> None:
    """Navigate to parent"""

    os.chdir("../")


def nav_base_dir() -> None:
    """Navigate to base dir"""

    os.chdir(BASE_DIR)


# creation #####################################################################

def create_dir(name: str) -> None:
    """Create dir"""

    os.mkdir(name)


def create_file(name: str) -> None:
    """Create file"""

    with open(name, 'x', encoding='UTF-8') as _:
        pass


# special getters ##############################################################

def get_int_from_file(path: str) -> int:
    """Get int from file"""

    with open(path, 'r', encoding='UTF-8') as fh_value:
        return int(fh_value.readlines()[0].splitlines()[0])


def get_string_from_file(path: str) -> str:
    """Get string from file"""

    with open(path, 'r', encoding='UTF-8') as fh_value:
        return fh_value.readlines()[0].splitlines()[0]


def get_list_from_file(path: str) -> list[str]:
    """Get list from file"""

    with open(path, 'r', encoding='UTF-8') as fh_value:
        lines: list[str] = fh_value.readlines()

    return_list: list[str] = []

    for line in lines:
        line_content: str = line.splitlines()[0]

        non_data_content: re.Match = re.fullmatch('^[.*]?$', line_content)

        if not non_data_content and line_content != '':
            return_list.append(line.splitlines()[0].strip())

    return return_list


def get_dict_from_file(path: str) -> dict:
    """Get dict from file"""

    with open(path, "r", encoding='UTF-8') as fh_value:
        lines: list[str] = fh_value.readlines()

    return_dict: dict = {}

    for line in lines:
        line_content: str = line.splitlines()[0]

        non_data_content: re.Match = re.fullmatch('^[.*]?$', line_content)

        if not non_data_content and line_content != '':

            new_kv_pair: list[str] = line_content.split(DATA_FILE_DICT_DELIMITER)
            new_key: str = new_kv_pair[0].strip()
            new_value: str = new_kv_pair[1].strip()
            return_dict[new_key] = new_value

    return return_dict
