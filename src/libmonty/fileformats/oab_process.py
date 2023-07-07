#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""OAB processing
"""

# imports: library
from argparse import ArgumentParser, Namespace
import codecs
import re
from typing import Generator

# where to get the input file:
# C:\Users\%username%\AppData\Local\Microsoft\Outlook
# -> Offline Address Books

DEFAULT_INPUT_FILE_PATH: str = 'aa-private-data/udetails-adjusted.oab'
DEFAULT_OUTPUT_UNITS_FILE_PATH: str = 'zz-private-output/contact-list-units.txt'
DEFAULT_OUTPUT_UNITS_SPLIT_FILE_PATH: str = 'zz-private-output/contact-list-units-split.txt'
DEFAILT_OUTPUT_ELEMENTS_FILE_PATH: str = 'zz-private-output/contact-list-elements.csv'
SRC_DELIMITER: str = '/o='


# functions

def file_len(filename: str) -> int:
    """File length"""

    with codecs.open(filename, 'r', encoding='UTF-8', errors='replace') as file:
        for index, _ in enumerate(file):
            pass
    return index + 1


def generator_by_line(filename: str) -> Generator:
    """Generator by line"""

    with open(filename, 'w', encoding='UTF-8') as fh_out:

        while True:
            row: str or bool = (yield True)

            if row is None:
                continue

            if row is False:
                fh_out.close()
                break

            fh_out.write(row)


def next_by_line(generator: Generator, content: str or None) -> None:
    """Next by line"""

    generator.send(content)


def end_by_line(generator: Generator) -> None:
    """End by line"""

    try:
        generator.send(False)
    except StopIteration:
        pass


def is_identifier(item: str) -> bool:
    """Is identifier?"""

    item_list: list = item.split("-")

    if len(item_list) >= 5 and len(item_list[0]) == 8:
        return True

    return False


def elements_line_compose(item_count: int,
                          item_elements: dict,
                          id_label_org: str,
                          id_label_tech: str) -> str:
    """Elements line compose"""

    composed: str = str(item_count)

    composed += f';{item_elements[id_label_tech]}'
    composed += f';{item_elements["full_name"]}'
    try:
        composed += f';{item_elements[id_label_org]}'
    except KeyError:
        composed += ";"
    composed += f';{item_elements["first_name"]}'
    composed += f';{item_elements["last_name"]}'

    composed += '\n'

    return composed


def output_elements_line(content_item_count: int,
                         content_item_elements: dict,
                         gen_file_elements: Generator,
                         id_label_org: str,
                         id_label_tech: str) -> int:
    """Output elements line"""

    # add to items count and print status
    content_item_count += 1
    print(f'Item written. (No. {content_item_count})')

    output: str = elements_line_compose(content_item_count,
                                        content_item_elements,
                                        id_label_org,
                                        id_label_tech)
    next_by_line(gen_file_elements, output)

    return content_item_count


def process(org, id_label_org: str, id_label_tech: str) -> None:
    """Process"""

    # length of data file

    data_file_line_count: int = file_len(DEFAULT_INPUT_FILE_PATH)
    print(f"{data_file_line_count} lines in data file.")

    # variables

    is_end_of_file: bool = False
    line_count: int = 0

    is_content_unit_found: bool = False
    content_unit_count: int = 0

    is_unit_type_org_added: bool = False

    content_item_count: int = 0
    content_item_elements: dict = {}

    search_text: str = ''

    # create elements file generator
    gen_file_elements: Generator = generator_by_line(DEFAILT_OUTPUT_ELEMENTS_FILE_PATH)
    # start the generator
    next_by_line(gen_file_elements, None)

    # loop

    with codecs.open(DEFAULT_INPUT_FILE_PATH, 'r', encoding='UTF-8', errors='replace') as file_in, \
         open(DEFAULT_OUTPUT_UNITS_FILE_PATH, "w", encoding='UTF-8') as file_out_units, \
         open(DEFAULT_OUTPUT_UNITS_SPLIT_FILE_PATH, "w", encoding='UTF-8') as file_out_units_split:

        while True:

            if is_end_of_file:
                break

            # if next unit not yet found: get next line from file
            if not is_content_unit_found:

                line = file_in.readline()

                # if line is empty end of file is reached
                if not line:
                    is_end_of_file = True
                else:
                    line_count += 1
                    print(f'Processing line {line_count} of {data_file_line_count}')

                    search_text += line

            # search for the beginning of the unit

            i_search_1 = search_text.find(SRC_DELIMITER)

            # if unit beginning not found: skip to processing next line
            if i_search_1 == -1:
                is_content_unit_found = False
                continue

            # search for the beginning of the next unit (~ end of the current one)

            i_search_2 = search_text.find(SRC_DELIMITER, i_search_1 + 1)

            if i_search_2 == -1 and not is_end_of_file:
                is_content_unit_found = False
                continue

            # else
            is_content_unit_found = True

            # add to units count and print status
            content_unit_count += 1
            print(f'Content unit identified. (No. {content_unit_count})')

            # isolate current content unit
            content_unit_text: str = search_text[i_search_1:i_search_2 - 1]

            # write to 'units' file
            file_out_units.write(f'[{content_unit_count:>6}] \'{content_unit_text}\'\n')

            # remove current content unit from search string
            search_text: str = search_text[i_search_2:len(search_text)-1]

            # split content unit string by NUL separators
            content_unit_list: list = content_unit_text.split('\u0000')

            # write to 'units_split' file
            line: str = ''
            for index, unit_item_text in enumerate(content_unit_list):
                if line == '':
                    line += f'[#{content_unit_count:>6}] \'{unit_item_text}\'\n'
                else:
                    line += f'        [{index:>2}] \'{unit_item_text}\'\n'
            file_out_units_split.write(line)

            if f'/o={org}/' in content_unit_list[0]:

                # if next ORG line reached but an ORG line is already added
                # but elements not yet output because ID-ORG missing: output to elements
                if is_unit_type_org_added:
                    content_item_count = output_elements_line(
                        content_item_count,
                        content_item_elements,
                        gen_file_elements,
                        id_label_org,
                        id_label_tech)
                    is_unit_type_org_added = False

                # szervezeti bejegyzés átugrása
                if content_unit_list[1].find('org_') == 0:
                    continue

                # túl rövid, egyéb típusú bejegyzés átugrása
                if len(content_unit_list) < 5:
                    line = f'Nincs elég elem az {org}-s sorban! ({line_count}.)\n'
                    line += f'{content_unit_list}'
                    print(line)
                    continue

                # empty content elements list
                content_item_elements = {}

                # ha szám van a i4 elemben, akkor a vezetéknév és keresztnév nincs külön

                # old check
                # if (re.findall("[0-9]", content_unit_list[4]) and
                #         not re.findall("[(][A-Z0-9]{6}[)]", content_unit_list[4])):

                if is_identifier(content_unit_list[4]):

                    id_tech: str = content_unit_list[2]
                    full_name: str = content_unit_list[3]
                    first_name: str = ''
                    last_name: str = ''

                else:
                    first_name: str = content_unit_list[1]
                    last_name: str = content_unit_list[2]
                    id_tech: str = content_unit_list[3]
                    full_name: str = content_unit_list[4]

                    if re.findall('[(][A-Z0-9]{6}[)]', full_name):
                        full_name: str = "".join(re.split('[(][A-Z0-9]{6}[)]', full_name))
                        full_name: str = full_name.strip()

                # hozzáadás az elemlistához
                content_item_elements[id_label_tech] = id_tech
                content_item_elements['full_name'] = full_name
                content_item_elements['first_name'] = first_name
                content_item_elements['last_name'] = last_name

                is_unit_type_org_added = True

            # check for ID-ORG in all content units

            id_org: str = ''

            for unit_item_text in content_unit_list:

                if len(unit_item_text) == 6 and re.findall('[A-Z0-9]{6}', unit_item_text):
                    id_org: str = unit_item_text

            if len(id_org) != 0:
                content_item_elements[id_label_org] = id_org

            # if ID-ORG found and ORG line already added: output to elements

            if is_unit_type_org_added and len(id_org) != 0:
                content_item_count = output_elements_line(
                    content_item_count,
                    content_item_elements,
                    gen_file_elements,
                    id_label_org,
                    id_label_tech)
                is_unit_type_org_added = False

    # end elements generator
    end_by_line(gen_file_elements)


def main() -> None:
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

    args: Namespace = parser.parse_args()

    process(org=args.org,
            id_label_org=args.id_label_org,
            id_label_tech=args.id_label_tech)


if __name__ == '__main__':
    main()
