#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class ListUtils:

    @staticmethod
    def new_list(arg_tuple):
        return_list = list()
        for argument in arg_tuple:
            if type(argument) in (list, tuple, bytearray, range, set, frozenset):
                return_list.extend(argument)
            elif type(argument) is dict:
                for key, value in argument.items():
                    new_entry = str(key) + "=" + str(value)
                    return_list.append(new_entry)
            else:
                return_list.append(argument)
        return return_list
