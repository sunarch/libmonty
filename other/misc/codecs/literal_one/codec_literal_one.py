#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# codec_literal_one - encryption/decryption program "Literal One"

# Build-in module imports
import sys

# print("codec_literal_one\n")


# ==================================================================== #
# HELPER FUNCTIONS

def validate_chapter_no(arg_chapter_no):
    return_value = int(arg_chapter_no)
    if return_value < 1 or return_value > 31:
        exit_with_error('incorrect argument value')
    return return_value


def validate_verse_no(arg_verse_no, arg_verse_count):
    return_value = int(arg_verse_no)
    if return_value < 1 or return_value > arg_verse_count:
        exit_with_error('incorrect argument value')
    return return_value


def exit_with_error(text):
    print(text)
    sys.exit(1)


# ==================================================================== #
# MODE FUNCTIONS

def mode_quote(arg_chapter_no, arg_verse_no):

    # chapter_no, converted to int
    chapter_no = validate_chapter_no(arg_chapter_no)

    # convert to padded string
    chapter_no_str = str(chapter_no).zfill(2)

    # import chapter verses
    __import__(f'text.chapter_{chapter_no_str}')
    verses = eval(f'text.chapter_{chapter_no_str}.verses')

    # argument 3: verse_no, converted to int
    verse_no = validate_verse_no(arg_verse_no, verses['verseCount'])

    # print verse
    print(verses[verse_no])


def mode_encrypt(arg_chapter_no, arg_plain_text):
    pass


def mode_decrypt(arg_chapter_no, arg_code_text):
    pass


# ==================================================================== #

arguments = sys.argv

# remove caller name from arguments
caller = arguments.pop(0)

# determine whether exactly 3 arguments are given
if len(arguments) != 3:
    exit_with_error('incorrect number of arguments')

# argument 0: mode
mode = arguments[0]

if mode in ['quote', 'q']:
    mode_quote(arguments[1], arguments[2])

elif mode in ['encrypt', 'encode', 'enc', 'e']:
    mode_encrypt(arguments[1], arguments[2])

elif mode in ['decrypt', 'decode', 'dec', 'd']:
    mode_decrypt(arguments[1], arguments[2])

else:
    exit_with_error('incorrect argument value')

# ============================================================================ #
