import pdfplumber

with pdfplumber.open('test.pdf') as pdf:

    first_page = pdf.pages[0]
    
    print(len(pdf.pages))
    print('')
    
    print(first_page.extract_text())
