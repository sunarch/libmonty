# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Easypass
"""

# imports: library
import functools
import logging
import os.path
import pkg_resources
import tkinter
from tkinter import ttk


def download_random(wordcount: int, count: int = 1):
    """Download random"""

    url = ('http://www.random.org/integers/'
           '?min=1&max=6&base=10&format=plain&rnd=new'
           f'&num={wordcount * count}&col={wordcount}'
           )
    raise NotImplementedError


def load_wordlist(wordlist_filename: str) -> dict:
    """Load wordlist"""

    resource_name = f'data/{wordlist_filename}.txt'

    if not pkg_resources.resource_exists(__name__, resource_name):
        raise ValueError('wordlist does not exist')

    with pkg_resources.resource_stream(__name__, resource_name) as wordlist_file:
        wordlist = wordlist_file.read().decode('UTF-8').strip().split('\n')

    return dict([item.strip().split('\t', -1)
                for item in wordlist])


def lookup(wordlist: dict, dice_ids: list[str]) -> list[str]:
    """Lookup"""

    return [wordlist[dice_id]
            for dice_id in dice_ids]


# actions

def action_load_wordlist(var_wordlist_filename: tkinter.StringVar) -> None:
    """Action: Load wordlist"""

    wordlist_file_name = os.path.join('data', f'{var_wordlist_filename.get()}.txt')

    if not pkg_resources.resource_exists(__name__, wordlist_file_name):
        logging.error('wordlist does not exist')
        return

    wordlist = pkg_resources.resource_stream(__name__, wordlist_file_name)
    wordlist_str = wordlist.read().decode('UTF-8')


def action_load_file(wordlist: dict,
                     var_filename: tkinter.StringVar,
                     var_result: tkinter.StringVar,
                     var_result_separator: tkinter.StringVar,
                     button_save_to_file: ttk.Button
                     ) -> None:
    """Action: Load file"""

    with open(f'{var_filename.get()}.txt', 'r', encoding='UTF-8') as source_file:
        dice_ids = [line.strip()
                    for line in source_file]

    dice_words: list[str] = lookup(wordlist, dice_ids)

    result_separator = var_result_separator.get()

    var_result.set(result_separator.join(dice_words))

    button_save_to_file.state(["!disabled"])


def action_save_to_file(var_result: tkinter.StringVar,
                        var_result_separator: tkinter.StringVar,
                        var_result_filename: tkinter.StringVar,
                        ) -> None:
    """Action: Save to file"""

    result_separator = var_result_separator.get()
    results = var_result.get().split(result_separator)

    with open(f'{var_result_filename.get()}.txt', 'w', encoding='UTF-8') as fh_result:
        fh_result.write(result_separator.join(results))


# GUI

def main():
    """Main"""

    # root
    root = tkinter.Tk()
    root.title('easypass')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # bound variables
    # var_wordlist_lang = tkinter.StringVar()
    # var_wordlist_lang.set('en')
    var_wordlist_filename = tkinter.StringVar()
    var_wordlist_filename.set('agr-wordlist-en-original')
    var_filename = tkinter.StringVar()
    var_filename.set('dice-sample')
    var_result_separator = tkinter.StringVar()
    var_result_separator.set(' ')
    var_result = tkinter.StringVar()
    var_result_filename = tkinter.StringVar()
    var_result_filename.set('dicewords')

    # load data
    wordlist: dict = load_wordlist(var_wordlist_filename.get())

    # named components
    frame_main = ttk.Frame(root, padding='3 3 12 12')
    entry_filename = ttk.Entry(frame_main, width=15, textvariable=var_filename)
    button_load_file = ttk.Button(frame_main, text='Load')
    button_save_to_file = ttk.Button(frame_main, text='Save to file')

    # action closures

    closure_action_load_file = functools.partial(action_load_file,
                                                 wordlist=wordlist,
                                                 var_filename=var_filename,
                                                 var_result=var_result,
                                                 var_result_separator=var_result_separator,
                                                 button_save_to_file=button_save_to_file)

    closure_action_save_to_file = functools.partial(action_save_to_file,
                                                    var_result=var_result,
                                                    var_result_separator=var_result_separator,
                                                    var_result_filename=var_result_filename)

    # bind commands
    button_load_file.configure(command=closure_action_load_file)
    button_save_to_file.configure(command=closure_action_save_to_file)

    # bind actions
    root.bind('<Return>', closure_action_load_file)

    # grid - main
    frame_main.grid(column=0, row=0)
    for row in range(0, 1):
        frame_main.columnconfigure(row, weight=1)
    for col in range(0, 4):
        frame_main.rowconfigure(col, weight=1)

    # grid - row 1
    ttk.Label(frame_main, text='File:')\
        .grid(column=1, row=1, padx=5, pady=5)
    entry_filename.grid(column=2, row=1, padx=5, pady=5)
    ttk.Label(frame_main, text='.txt')\
        .grid(column=3, row=1, padx=5, pady=5)
    button_load_file.grid(column=4, row=1, padx=5, pady=5)

    # grid - row 2
    ttk.Label(frame_main, text='Result:')\
        .grid(column=1, row=2, padx=5, pady=5)
    ttk.Label(frame_main, textvariable=var_result)\
        .grid(column=2, row=2, columnspan=2, padx=5, pady=5)
    button_save_to_file.grid(column=4, row=2, padx=5, pady=5)

    # set states and focus
    button_save_to_file.state(['disabled'])
    entry_filename.focus()

    # main program loop
    root.mainloop()


if __name__ == '__main__':
    main()
