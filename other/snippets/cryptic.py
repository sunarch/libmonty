#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

characters = '0123456789'
characters += 'abcdefghijklmnopqrstuvwxyz'
characters += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
characters += '?:~=+-%/|\\#&@$*'

characters_count = len(characters)

for n1 in range(0, 40):
    output = ""
    for n2 in range(0, 80):
        output += characters[random.randrange(0, characters_count)]
    print(output)
