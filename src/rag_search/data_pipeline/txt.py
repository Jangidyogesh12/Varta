import chardet


def load_text_file(file_path):
    with open(file_path, "rb") as file:
        result = chardet.detect(file.read())

    encoding = result["encoding"]

    with open(file_path, "r", encoding=encoding) as file:
        docs = file.read()

    return docs
