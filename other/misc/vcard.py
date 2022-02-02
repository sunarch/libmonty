#!/usr/bin/env python3

import argparse
from dataclasses import dataclass, field, InitVar
import sys


class FieldMissingError(KeyError):
    pass


@dataclass
class FlaggedItem:
    value: InitVar[list[str]]
    flags: list[str] = field(default_factory=list)
    
    def __post_init__(self, value):
        self.values = value.split(';')
    
    def export(self):
        return f'{self._export_flags()}:{self._export_value()}'
    
    def _export_value(self):
        return ';'.join(self.values)
    
    def _export_flags(self):
        return (';' if len(self.flags) > 0 else '') + ';'.join(self.flags)


@dataclass
class VCard:

    name: FlaggedItem = None
    full_name: str = None
    emails: list[FlaggedItem] = field(default_factory=list)
    phones: list[FlaggedItem] = field(default_factory=list)
    org: str = None
    birthday: str = None
    
    def export_full(self) -> str:
        content = ''
        
        content += self._export_begin()
        content += self._export_version()
        content += self._export_name()
        content += self._export_full_name()
        content += self._export_emails()
        content += self._export_phones()
        content += self._export_org()
        content += f'BDAY:{self.birthday}\n' if self.birthday else ''
        content += self._export_end()
        
        return content
        
    def export_email(self):
        if len(self.emails) == 0:
            raise FieldMissingError('No email in contact')
    
        content = ''
        content += self._export_begin()
        content += self._export_version()
        content += self._export_name()
        content += self._export_full_name()
        content += self._export_org()
        content += self._export_emails()
        content += self._export_end()
        return content
        
    def export_phone(self):
        if len(self.phones) == 0:
            raise FieldMissingError('No phone number in contact')
    
        content = ''
        content += self._export_begin()
        content += self._export_version()
        content += self._export_name()
        content += self._export_full_name()
        content += self._export_org()
        content += self._export_phones()
        content += self._export_end()
        return content

    def _export_begin(self):
        return 'BEGIN:VCARD\n'
    
    def _export_version(self):
        return 'VERSION:2.1\n'

    def _export_end(self):
        return 'END:VCARD\n'
        
    def _export_name(self):
        return f'N{self.name.export()}\n' if self.name else ''
        
    def _export_full_name(self):
        return f'FN:{self.full_name}\n' if self.full_name else ''
        
    def _export_org(self):
        return f'ORG:{self.org}\n' if self.org else ''
        
    def _export_emails(self):
        content = ''
        for email in self.emails:
            content += f'EMAIL{email.export()}\n'
        return content
        
    def _export_phones(self):
        content = ''
        for phone in self.phones:
            content += f'TEL{phone.export()}\n'
        return content


def main():

    parser = argparse.ArgumentParser(description='vCard')
    parser.add_argument('--input', metavar='PATH',
                        help='input file path',
                        dest='filename',
                        required=True)

    args = parser.parse_args()

    vcards = []

    try:
        with open(args.filename, 'r') as fh_in:
        
            for line in fh_in:

                try:
                    key, value = line.strip().split(':')
                except ValueError as err:
                    print(err)
                    print(line)
                    continue
                    
                key_elements = key.split(';')
                field_name = key_elements[0]
                field_flags = key_elements[1:]

                if field_name == 'BEGIN':
                    vcard = VCard()
                
                elif field_name == 'N':
                    vcard.name = FlaggedItem(value, field_flags)
                    
                elif field_name == 'FN':
                    vcard.full_name = value
                
                elif field_name == 'EMAIL':
                    vcard.emails.append(FlaggedItem(value, field_flags))
                
                elif field_name == 'TEL':
                    vcard.phones.append(FlaggedItem(value, field_flags))
                
                elif field_name == 'ORG':
                    vcard.org = value
                
                elif field_name == 'BDAY':
                    vcard.birthday = value
                
                elif field_name == 'END':
                    vcards.append(vcard)

    except FileNotFoundError as err:
        print(err)
        sys.exit(1)
        
    with open('export-full.vcf', 'w') as fh_out:
        for vcard in vcards:
            fh_out.write(vcard.export_full())
    
    with open('export-phone.vcf', 'w') as fh_out:
        for vcard in vcards:
            try:
                fh_out.write(vcard.export_phone())
            except FieldMissingError as err:
                print(err)
    
    with open('export-email.vcf', 'w') as fh_out:
        for vcard in vcards:
            try:
                fh_out.write(vcard.export_email())
            except FieldMissingError as err:
                print(err)


if __name__ == '__main__':
    main()

