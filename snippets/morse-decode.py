#!/usr/bin/python3

'''
The MIT License (MIT)

Copyright (c) 2018 Németh András

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import sys

########################################################################

morse = dict([

# Letters

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

# Digits

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

# Punctuation Marks

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

########################################################################

argList = sys.argv
filename = argList.pop(0)
arguments = argList
argumentcount = len(arguments)

if argumentcount < 1:
    print("Error: missing command line argument")
    sys.exit(1)
##### BREAKPOINT #

########################################################################

morse_decode = dict()

for entry in morse.items():
    morse_decode[entry[1]] = entry[0]

########################################################################

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

########################################################################
