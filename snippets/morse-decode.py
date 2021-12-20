#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# imports ######################################################################

import sys

################################################################################

morse = dict([

# Letters #

("A",".-"),
("B","-..."),
("C","-.-."),
("D","-.."),
("E","."),
("F","..-."),
("G","--."),
("H","...."),
("I",".."),
("J",".---"),
("K","-.-"),
("L",".-.."),
("M","--"),

("N","-."),
("O","---"),
("P",".--."),
("Q","--.-"),
("R",".-."),
("S","..."),
("T","-"),
("U","..-"),
("V","...-"),
("W",".--"),
("X","-..-"),
("Y","-.--"),
("Z","--.."),

# Digits #

("1",".----"),
("2","..---"),
("3","...--"),
("4","....-"),
("5","....."),
("6","-...."),
("7","--..."),
("8","---.."),
("9","----."),
("0","-----"),

# Punctuation Marks #

("&",".-..."),   # Ampersand
("'",".----."),  # Apostrophe
("@",".--.-."),  # At sign
(")","-.--.-"),  # Bracket, close (parenthesis)
("(","-.--."),   # Bracket, open (parenthesis)
(":","---..."),  # Colon
(",","--..--"),  # Comma
("=","-...-"),   # Equals sign
("!","-.-.--"),  # Exclamation mark - Not in ITU-R recommendation
(".",".-.-.-"),  # Full-stop (period)
("-","-....-"),  # Hyphen
("+",".-.-."),   # Plus sign
("\"",".-..-."), # Quotation marks
("?","..--.."),  # Question mark (query)
("/","-..-."),   # Slash

(";","-.-.-.")  # Semicolon - unofficial

])

################################################################################

argList = sys.argv
filename = argList.pop(0)
arguments = argList
argumentcount = len(arguments)

if argumentcount < 1:
    print("Error: missing command line argument")
    sys.exit(1)
### BREAKPOINT #

################################################################################

morse_decode = dict()

for entry in morse.items():
    morse_decode[entry[1]] = entry[0]

################################################################################

outfile = open("decoded-generated.txt",'w')

with open(arguments[0], 'r') as infile:
    clear_unit = ""
    code_unit = "x"

    for line in infile:
        clear_unit = " "
        code_unit = line.rstrip()

        if code_unit in morse_decode:
            clear_unit = morse_decode[code_unit]
        else:
            clear_unit = " "

        print(clear_unit, end='')

        outfile.write(clear_unit)


outfile.close()

# END ##########################################################################
