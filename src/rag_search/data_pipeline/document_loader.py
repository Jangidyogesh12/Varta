import os
from data_pipeline.pdf import pdf_txt_extracter
from data_pipeline.txt import load_text_file

from loguru import logger

compatible_file_types = [".txt", ".pdf"]


def load(file_path):
    # Extract the file extension
    _, file_extension = os.path.splitext(file_path.lower())
    file_type = file_extension

    if file_type in compatible_file_types:
        if file_type == ".txt":
            return load_text_file(file_path)

        elif file_type == ".pdf":
            return pdf_txt_extracter(file_path)

    else:
        return logger.error(
            f"Compatibility Error : The given file is not Compatible with this system \nuse :{compatible_file_types} file types"
        )
