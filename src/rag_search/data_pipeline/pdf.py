import fitz


def pdf_txt_extracter(file_path):
    text = ""

    with fitz.open(file_path) as pdf_document:
        for pg_number in range(pdf_document.page_count):
            page = pdf_document[pg_number]
            text += page.get_text()

    return text
