#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from dataclasses import dataclass, InitVar
import os
from typing import Callable


LINE_LIMIT = 72


@dataclass
class Language:

    name: str
    extension: str
    header_form: str
    footer: str
    data_line: Callable
    
    def header(self, var_name: str) -> str:
        return self.header_form.format(var_name)


def javascript_data_line(new: str, passthrough: str) -> tuple[str]:

    global LINE_LIMIT

    unit = f' \'{new}\','

    if new is None:
        current = passthrough[0:-1]
        passthrough = None
    elif (len(passthrough) + len(unit)) > LINE_LIMIT:
        current = passthrough
        passthrough = (' ' * 3) + unit
    else:
        current = None
        passthrough += unit

    return current, passthrough


languages = [
    Language(
        name='JavaScript',
        extension='js',
        header_form='const {} = [',
        footer='];',
        data_line=javascript_data_line
    )
]


for letter_count in range(2, 9):

    filename = f'{letter_count}-letter'
    var_name = f'words_with_{letter_count}_letters'
    filename_src = filename + '.txt'

    with open(filename_src, 'r') as fh_in:
        print('Input file', ':', filename_src)
    
        for language in languages:
        
            print('Language', ':', language.name)
            print('Extension', ':', language.extension)
            
            try:
                os.makedirs(language.extension, exist_ok = True)
            except OSError as err:
                raise RuntimeError(f'Directory \'{folder}\' can not be created')
            
            filename_new = f'{filename}.{language.extension}'
            path_new = os.path.join(language.extension, filename_new)
            
            with open(path_new, 'w') as fh_out:
                print('Output path', ':', path_new)

                # write header to file
                print(language.header(var_name), file=fh_out)
                
                passthrough = ' ' * 3
                
                while(True):
                
                    line = fh_in.readline().strip()
                    print('Line:', line)
                    
                    new = None if line == '' else line

                    current, passthrough = language.data_line(new, passthrough)
                    
                    if current is not None:
                        print(current, file=fh_out)
                        print('Current:', current)
                        
                    if new is None:
                        break
                
                # write footer to file
                print(language.footer, file=fh_out)

