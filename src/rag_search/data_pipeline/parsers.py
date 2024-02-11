from langchain.text_splitter import RecursiveCharacterTextSplitter


class doc_parser:
    def __init__(self, text):
        self.text = text
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=0, length_function=len
        )

    def chunker(self):
        chunks = self.text_splitter.split_text(self.text)
        return chunks
