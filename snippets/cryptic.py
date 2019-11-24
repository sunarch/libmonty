#!/usr/bin/python3

import random

characters = "0123456789"
characters += "abcdefghijklmnopqrstuvwxyz"
characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
characters += "?:~=+-%/|\#&@$*"

characters_count = len(characters)

for n1 in range(0,40):
    output = ""
    for n2 in range(0,80):
        output += characters[random.randrange(0,characters_count)]
    print(output)
