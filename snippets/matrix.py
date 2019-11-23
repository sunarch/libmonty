#!/usr/bin/python3

import random

for n1 in range(0,40):
    output = ""
    for n2 in range(0,80):
        output += str(random.randrange(0,2))
    print(output)

