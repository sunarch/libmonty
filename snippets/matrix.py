#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random


for n1 in range(0, 40):
    output = ""
    for n2 in range(0, 80):
        output += str(random.randrange(0, 2))
    print(output)
