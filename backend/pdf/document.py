# MIT License

# Copyright (c) 2023 Ruokun (Tommy) Niu

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pypdf
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter

def load_pdf_from_dir(dir_path):
    # langchain, does not work with our current deployment
    loader = PyPDFLoader(dir_path)
    document = loader.load()
    # pages = loader.load_and_split()

    return document


def split_document(document):
    # Split the document into pages
    
    text_splitter = CharacterTextSplitter(chunk_size = 30, chunk_overlap = 10)

    splitted_document = text_splitter.split_documents(document)

    return splitted_document

def load_pdf_into_str(dir_path):
    reader = pypdf.PdfReader(dir_path)

    extracted_text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        extracted_text += page.extract_text()

    return extracted_text

if __name__ == "__main__":
    extracted = load_pdf_into_str("../sample.pdf")
    # doc = load_pdf_from_dir("../sample.pdf")
    # splitted = split_document(doc)