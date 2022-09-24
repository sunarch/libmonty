# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


# imports ######################################################################

import os
import tkinter
from tkinter import ttk


# set working directory to script location ####################################################################

if __file__:
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

# constants ####################################################################

IS_DEBUG_MODE = True

# variables ####################################################################

dice_words = ["ERROR"]
dice_words_count = len(dice_words)
dice_words_result = "ERROR"

# wordListLang = "en"
# randomSiteUrl = "http://www.random.org/integers/?num=30&min=1&max=6&col=5&base=10&format=plain&rnd=new"

# wordlist #####################################################################

wordlist_file_name = 'data/agr-wordlist-en-original.txt'
wordlist_dict = {}
wordlist_dict_keys = wordlist_dict.keys()


def get_wordlist_file_path():
    global wordlist_file_name
    return os.path.join('data', wordlist_file_name)


# source file ##################################################################

source_file_name = ""
source_dice_ids = []


def set_source_file_name(arg_source_file_name):
    global source_file_name
    source_file_name = arg_source_file_name
    debug("source_file_name = {0}".format(source_file_name))


def get_source_file_path():
    global source_file_name
    return os.path.join("data", "{0}.txt".format(source_file_name))


# result file ##################################################################

def get_result_file_path():
    global source_file_name
    return os.path.join("output", "{0}-result.txt".format(source_file_name))


# functions ####################################################################

def debug(message):
    global IS_DEBUG_MODE

    if IS_DEBUG_MODE:
        print(message)


# def load_wordlist ############################################################

def load_wordlist():

    global wordlist_dict
    global wordlist_dict_keys

    try:
        wordlist_file = open(get_wordlist_file_path(), 'r')
    except IOError:
        print('error, file not found')
    else:
        with wordlist_file:

            for line in wordlist_file:
                key, value = line.rstrip().split("\t", -1)
                wordlist_dict[key] = value

            wordlist_dict_keys = wordlist_dict.keys()


# def lookup ###################################################################

def lookup():

    global wordlist_dict
    global wordlist_dict_keys
    global source_dice_ids
    global dice_words
    global dice_words_count
    global dice_words_result

    debug("START: matching wordListValues to fileValues and setting diceWords")

    if len(source_dice_ids) > 0:
        dice_words = list()
        dice_words_count = len(dice_words)
        dice_words_result = str()

    for dice_id in source_dice_ids:
        # debug("dice_id '{0}'".format(dice_id))
        if dice_id in wordlist_dict_keys:
            debug("wordlist_dict['{0}'] : '{1}'".format(dice_id, wordlist_dict[dice_id]))
            dice_words.append(wordlist_dict[dice_id])

    debug("dice_words = {0}".format(dice_words))

    dice_words_count = len(dice_words)

    result_word_separator = " "

    dice_words_result = result_word_separator.join(dice_words)

    debug("dice_words_result = {0}".format(dice_words_result))

    # for n3 in range( diceWordsCount ):
    #     dice_words_result = dice_words_result + str( diceWords[n3] )
    #     if n3 != diceWordsCount - 1:
    #         dice_words_result = dice_words_result + " "


# def display_result ###########################################################

def display_result():
    var_result.set(dice_words_result)


# bound action function ########################################################

def action_load_file():
    global source_dice_ids

    set_source_file_name(var_filename.get())
    source_lines = []

    try:
        source_file = open(get_source_file_path(), 'r+')
    except IOError:
        print('error, file not found')
        return
    else:
        with source_file:
            for line in source_file:
                source_lines.append(line.strip())

    source_dice_ids = source_lines

    debug(source_dice_ids)

    lookup()

    display_result()

    button_save_to_file.state(["!disabled"])


def action_save_to_file():
    global dice_words_result

    try:
        result_file = open(get_result_file_path(), 'w')
    except IOError:
        print('error, file could not be opened for writing')
    else:
        with result_file:
            result_file.write(dice_words_result)


# set up the GUI ###############################################################

# root #
root = tkinter.Tk()
root.title("easypass")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.bind('<Return>', action_load_file)

# bound variables #
var_filename = tkinter.StringVar()
var_filename.set("dice-sample")
var_result = tkinter.StringVar()

# main frame #
frame_main = ttk.Frame(root, padding="3 3 12 12")
frame_main.grid(column=0, row=0)
for row in range(0, 1):
    frame_main.columnconfigure(row, weight=1)
for col in range(0, 4):
    frame_main.rowconfigure(col, weight=1)

# row 1 #
ttk.Label(frame_main, text="File:").grid(column=1, row=1, padx=5, pady=5)
entry_filename = ttk.Entry(frame_main, width=15, textvariable=var_filename)
entry_filename.grid(column=2, row=1, padx=5, pady=5)
ttk.Label(frame_main, text=".txt").grid(column=3, row=1, padx=5, pady=5)
ttk.Button(frame_main, text="Load", command=action_load_file).grid(column=4, row=1, padx=5, pady=5)

# row 2 #
ttk.Label(frame_main, text="Result:").grid(column=1, row=2, padx=5, pady=5)
ttk.Label(frame_main, textvariable=var_result).grid(column=2, row=2, columnspan=2, padx=5, pady=5)
button_save_to_file = ttk.Button(frame_main, text="Save to file", command=action_save_to_file)
button_save_to_file.grid(column=4, row=2, padx=5, pady=5)
button_save_to_file.state(["disabled"])

# main program loop #
load_wordlist()
entry_filename.focus()
debug("Debug mode is on")
root.mainloop()


# END ##########################################################################
