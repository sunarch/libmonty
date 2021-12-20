import PyPDF2

with open('test.pdf', 'rb') as pdf:

    pdf_reader = PyPDF2.PdfFileReader(pdf)

    page_one = pdf_reader.getPage(0)

    print(page_one.extractText())
