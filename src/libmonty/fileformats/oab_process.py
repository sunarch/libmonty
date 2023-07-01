#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""OAB processing
"""

# imports: library
from argparse import ArgumentParser
import codecs
import re

# where to get the input file:
# C:\Users\%username%\AppData\Local\Microsoft\Outlook
# -> Offline Address Books

DEFAULT_INPUT_FILE_PATH = "aa-private-data/udetails-adjusted.oab"
DEFAULT_OUTPUT_UNITS_FILE_PATH = "zz-private-output/contact-list-units.txt"
DEFAULT_OUTPUT_UNITS_SPLIT_FILE_PATH = "zz-private-output/contact-list-units-split.txt"
DEFAILT_OUTPUT_ELEMENTS_FILE_PATH = "zz-private-output/contact-list-elements.csv"
SRC_DELIMITER = "/o="


# functions

def file_len(s_file_name):
    """File length"""

    with codecs.open(s_file_name, 'r', encoding='UTF-8', errors='replace') as file:
        for i, l in enumerate(file):
            pass
    return i + 1


def generator_by_line(s_filename):
    """Generator by line"""

    with open(s_filename, 'w', encoding='UTF-8') as fh_out:

        while True:
            s_row = (yield True)

            if s_row is None:
                continue

            if s_row is False:
                fh_out.close()
                break

            fh_out.write(s_row)


def next_by_line(o_generator, s_content):
    """Next by line"""

    o_generator.send(s_content)


def end_by_line(o_generator):
    """End by line"""

    try:
        o_generator.send(False)
    except StopIteration:
        pass


def is_identifier(s_item):
    """Is identifier?"""

    ls_item = s_item.split("-")

    if len(ls_item) >= 5 and len(ls_item[0]) == 8:
        return True

    return False


def elements_line_compose(i_items, d_item_elements, id_label_org, id_label_tech):
    """Elements line compose"""

    s_return = str(i_items)

    s_return += f';{d_item_elements[id_label_tech]}'
    s_return += f';{d_item_elements["full_name"]}'
    try:
        s_return += f';{d_item_elements[id_label_org]}'
    except KeyError:
        s_return += ";"
    s_return += f';{d_item_elements["first_name"]}'
    s_return += f';{d_item_elements["last_name"]}'

    s_return += "\n"

    return s_return


def output_elements_line(i_content_items,
                         d_content_item_elements,
                         o_gen_file_elements,
                         id_label_org,
                         id_label_tech):
    """Output elements line"""

    # add to items count and print status
    i_content_items += 1
    print(f"Item written. (No. {i_content_items})")

    s_output = elements_line_compose(i_content_items,
                                     d_content_item_elements,
                                     id_label_org,
                                     id_label_tech)
    next_by_line(o_gen_file_elements, s_output)

    return i_content_items


def process(org, id_label_org, id_label_tech):
    """Process"""

    # length of data file

    i_data_file_lines = file_len(DEFAULT_INPUT_FILE_PATH)
    print(f"{i_data_file_lines} lines in data file.")

    # variables

    b_end_of_file = False
    i_lines = 0

    b_content_unit_found = False
    i_content_units = 0

    b_unit_type_org_added = False

    i_content_items = 0
    d_content_item_elements = {}

    s_search = ""

    # create elements file generator
    o_gen_file_elements = generator_by_line(DEFAILT_OUTPUT_ELEMENTS_FILE_PATH)
    # start the generator
    next_by_line(o_gen_file_elements, None)

    # loop

    with codecs.open(DEFAULT_INPUT_FILE_PATH, 'r', encoding='UTF-8', errors='replace') as file_in, \
         open(DEFAULT_OUTPUT_UNITS_FILE_PATH, "w", encoding='UTF-8') as file_out_units, \
         open(DEFAULT_OUTPUT_UNITS_SPLIT_FILE_PATH, "w", encoding='UTF-8') as file_out_units_split:

        while True:

            if b_end_of_file:
                break

            # if next unit not yet found: get next line from file
            if not b_content_unit_found:

                line = file_in.readline()

                # if line is empty end of file is reached
                if not line:
                    b_end_of_file = True
                else:
                    i_lines += 1
                    print(f'Processing line {i_lines} of {i_data_file_lines}')

                    s_search += line

            # search for the beginning of the unit

            i_search_1 = s_search.find(SRC_DELIMITER)

            # if unit beginning not found: skip to processing next line
            if i_search_1 == -1:
                b_content_unit_found = False
                continue

            # search for the beginning of the next unit (~ end of the current one)

            i_search_2 = s_search.find(SRC_DELIMITER, i_search_1 + 1)

            if i_search_2 == -1 and not b_end_of_file:
                b_content_unit_found = False
                continue

            # else
            b_content_unit_found = True

            # add to units count and print status
            i_content_units += 1
            print(f'Content unit identified. (No. {i_content_units})')

            # isolate current content unit
            s_content_unit = s_search[i_search_1:i_search_2 - 1]

            # write to 'units' file
            file_out_units.write(f'[{i_content_units:>6}] \'{s_content_unit}\'\n')

            # remove current content unit from search string
            s_search = s_search[i_search_2:len(s_search)-1]

            # split content unit string by NUL separators
            ls_content_unit = s_content_unit.split('\u0000')

            # write to 'units_split' file
            s_line = ""
            for _, s_unit_item in enumerate(ls_content_unit):
                if s_line == '':
                    s_line += f'[#{i_content_units:>6}] \'{s_unit_item}\'\n'
                else:
                    s_line += '        [{i_x:>2}] \'{s_unit_item}\'\n'
            file_out_units_split.write(s_line)

            if f'/o={org}/' in ls_content_unit[0]:

                # if next ORG line reached but an ORG line is already added
                # but elements not yet output because ID-ORG missing: output to elements
                if b_unit_type_org_added:
                    i_content_items = output_elements_line(
                        i_content_items,
                        d_content_item_elements,
                        o_gen_file_elements,
                        id_label_org,
                        id_label_tech)
                    b_unit_type_org_added = False

                # szervezeti bejegyzés átugrása
                if ls_content_unit[1].find('org_') == 0:
                    continue

                # túl rövid, egyéb típusú bejegyzés átugrása
                if len(ls_content_unit) < 5:
                    s_line = f'Nincs elég elem az {org}-s sorban! ({i_lines}.)\n{ls_content_unit}'
                    print(s_line)
                    continue

                # empty content elements list
                d_content_item_elements = {}

                # ha szám van a i4 elemben, akkor a vezetéknév és keresztnév nincs külön

                # old check
                # if (re.findall("[0-9]", ls_content_unit[4]) and
                #         not re.findall("[(][A-Z0-9]{6}[)]", ls_content_unit[4])):

                if is_identifier(ls_content_unit[4]):

                    s_id_tech = ls_content_unit[2]
                    s_full_name = ls_content_unit[3]
                    s_first_name = ""
                    s_last_name = ""

                else:
                    s_first_name = ls_content_unit[1]
                    s_last_name = ls_content_unit[2]
                    s_id_tech = ls_content_unit[3]
                    s_full_name = ls_content_unit[4]

                    if re.findall('[(][A-Z0-9]{6}[)]', s_full_name):
                        s_full_name = "".join(re.split('[(][A-Z0-9]{6}[)]', s_full_name))
                        s_full_name = s_full_name.strip()

                # hozzáadás az elemlistához
                d_content_item_elements[id_label_tech] = s_id_tech
                d_content_item_elements['full_name'] = s_full_name
                d_content_item_elements['first_name'] = s_first_name
                d_content_item_elements['last_name'] = s_last_name

                b_unit_type_org_added = True

            # check for ID-ORG in all content units

            s_id_org = ""

            for s_unit_item in ls_content_unit:

                if len(s_unit_item) == 6 and re.findall('[A-Z0-9]{6}', s_unit_item):
                    s_id_org = s_unit_item

            if len(s_id_org) != 0:
                d_content_item_elements[id_label_org] = s_id_org

            # if ID-ORG found and ORG line already added: output to elements

            if b_unit_type_org_added and len(s_id_org) != 0:
                i_content_items = output_elements_line(
                    i_content_items,
                    d_content_item_elements,
                    o_gen_file_elements,
                    id_label_org,
                    id_label_tech)
                b_unit_type_org_added = False

    # end elements generator
    end_by_line(o_gen_file_elements)


def main():
    """Main"""

    parser = ArgumentParser(prog='OAB processing')

    parser.add_argument('-o', '--org',
                        help='Organization',
                        required=True,
                        dest='org')

    parser.add_argument('-i', '--id-label-org',
                        help='ID label (organization)',
                        required=True,
                        dest='id_label_org')

    parser.add_argument('-t', '--id-label-tech',
                        help='ID label (tech)',
                        required=True,
                        dest='id_label_tech')

    args = parser.parse_args()

    process(org=args.org,
            id_label_org=args.id_label_org,
            id_label_tech=args.id_label_tech)


if __name__ == '__main__':
    main()
