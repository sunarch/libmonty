#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from email_validator import validate_email, EmailSyntaxError, EmailUndeliverableError
# EmailNotValidError

ls_emails = [
   
]

with open('result.txt', 'wt', encoding='UTF-8') as f_result:
    
    for email in ls_emails:
    
        print('Checking:', email)
        
        try:
            # Validate.
            valid = validate_email(email)

            # Update with the normalized form.
            print('->  Valid:', valid.email)
            f_result.write(f'{email:<31} => {valid.email}\n')
            
        except EmailSyntaxError as e:
            # email is not valid, exception message is human-readable
            print(str(e))
            f_result.write(f'Invalid syntax: {email}')
            
        except EmailUndeliverableError as e:
            print(str(e))
            f_result.write(f'Undeliverable: {email}')