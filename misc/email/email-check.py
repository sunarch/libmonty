from email_validator import validate_email, EmailNotValidError, EmailSyntaxError, EmailUndeliverableError 

ls_emails = [
   
]

with open("result.txt", "wt", encoding="utf-8") as f_result:
    
    for email in ls_emails:
    
        print("Checking: {}".format(email))
        
        try:
            # Validate.
            valid = validate_email(email)

            # Update with the normalized form.
            print("->  Valid: {}".format(valid.email))
            f_result.write("{:<31} => {}\n".format(email, valid.email))
            
        except EmailSyntaxError as e:
            # email is not valid, exception message is human-readable
            print(str(e))
            f_result.write("Invalid syntax: {}".format(email))
            
        except EmailUndeliverableError as e:
            print(str(e))
            f_result.write("Undeliverable: {}".format(email))
