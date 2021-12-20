#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


# start decorator: printResult ################################################

def print_result(arg_function):
    def new_function(arguments):
        result = arg_function(arguments)
        if result is not None:
            print(str(result))
    return new_function

# end decorator: printResult ##################################################
