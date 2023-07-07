#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Email check
"""

# imports: library
from argparse import ArgumentParser, Namespace
import os.path

# imports: requirements
from email_validator import validate_email, EmailSyntaxError, EmailUndeliverableError

# imports: project
from libmonty.environment.arguments import type_file_path


def main():
    """Main"""

    parser = ArgumentParser()

    parser.add_argument('-i', '--input-file', metavar='PATH',
                        required=True, type=type_file_path,
                        dest='input_file')

    parser.add_argument('-o', '--output-file', metavar='PATH',
                        default=None, type=type_file_path,
                        dest='output_file')

    args: Namespace = parser.parse_args()

    print('Input file: ', args.input_file)
    with open(args.input_file, 'r', encoding='UTF-8') as fh_source:
        email_list: list[str] = fh_source.readlines()

    email_list: list[str] = list(map(lambda x: x.strip(), email_list))

    if args.output_file is None:
        input_file_part_name, input_file_part_ext = os.path.splitext(args.input_file)
        output_file = f'{input_file_part_name}-output{input_file_part_ext}'
    else:
        output_file = args.output_file

    with open(output_file, 'w', encoding='UTF-8') as fh_result:

        for email in email_list:

            print('Checking:', email)

            try:
                # Validate.
                valid = validate_email(email)

                # Update with the normalized form.
                print('->  Valid:', valid.email)
                fh_result.write(f'{email:<31} => {valid.email}\n')

            except EmailSyntaxError as exc:
                # email is not valid, exception message is human-readable
                print(str(exc))
                fh_result.write(f'Invalid syntax: {email}')

            except EmailUndeliverableError as exc:
                print(str(exc))
                fh_result.write(f'Undeliverable: {email}')


if __name__ == '__main__':
    main()
