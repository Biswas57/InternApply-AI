import PyPDF2

with open('app/resources/resume.pdf', 'rb') as file:
    reader = PyPDF2.PdfReader(file)

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text = page.extract_text()
        

with open('app/resources/email_template.txt', 'r') as file:
    print(file.read())
