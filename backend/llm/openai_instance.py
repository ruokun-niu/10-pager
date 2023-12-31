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

import openai
from langchain.llms import OpenAI, AzureOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA, AnalyzeDocumentChain
from langchain.chains.summarize import load_summarize_chain

import sys
sys.path.append('../') 
from pdf.document import load_pdf_from_dir, split_document, load_pdf_into_str

OPENAI_API_TYPE="azure"
OPENAI_API_VERSION="2023-05-15"
DEPLOYMENT_NAME='gpt-35-turbo-16k'

PATH_TO_PDF = "uploads/sample.pdf"

class OpenAIInstance:
    openai = openai
    api_key = None
    endpoint = None


    def __init__(self):
        pass

    def openai_auth(self, api_key, endpoint):
        self.openai.api_key = api_key
        self.openai.api_base = endpoint
        self.openai.api_type = OPENAI_API_TYPE
        self.openai.api_version = OPENAI_API_VERSION # this may change in the future


    def pdf_assistant(self, user_input):
        pdf_str = load_pdf_into_str(PATH_TO_PDF)
        response = self.openai.ChatCompletion.create(
                engine=DEPLOYMENT_NAME, 
                max_tokens=1250,
                messages=[
                    {"role": "system", "content": "You are an assistant that will analyze and answer questions based on an input pdf. Users will now supply the pdf as a string and will then ask questions"},
                    {"role": "user", "content": pdf_str},
                    {"role": "user", "content": user_input}
                ]
            )
        assistant_response = response['choices'][0]['message']['content']
        return assistant_response
    

    def summary(self):
        pdf_str = load_pdf_into_str("../sample.pdf")

        # test: Ask openAI to summarize the pdf
        response = openai.ChatCompletion.create(
            engine=DEPLOYMENT_NAME, 
            max_tokens=750,
            messages=[
                {"role": "system", "content": "You are an assistant that will analyze and answer questions based on an input pdf. Users will now supply the pdf as a string and will then ask questions"},
                {"role": "user", "content": pdf_str},
                {"role": "user", "content": "Provide a short summary of the pdf in 1-2 sentences"}
            ]
        )

        print("Summary: " + response['choices'][0]['message']['content'])


    def openai_instance(self, user_input):
        user_input = user_input.strip().lower()
            
        response = openai.ChatCompletion.create(
            engine=DEPLOYMENT_NAME, 
            max_tokens=1250,
            messages=[
                {"role": "system", "content": "You are an assistant that will analyze and answer questions"},
                {"role": "user", "content": user_input}
            ]
        )
        assistant_response = response['choices'][0]['message']['content']
        print("Assistant: " + assistant_response)

        return assistant_response




def init_instance(api_key, endpoint, deployment="gpt-35-turbo-16k"):
    # Uses langchain.llms.OpenAI to create an OpenAI instance

    # Create an instance of Azure OpenAI
    llm = AzureOpenAI(
        deployment_name= deployment,
        openai_api_type=OPENAI_API_TYPE,
        openai_api_version=OPENAI_API_VERSION,
        openai_api_key=api_key,
        openai_api_base=endpoint,
        # engine='text-davinci-002' # OR text-davinci-003
    )

    print(llm)
    return llm

def init_llm_chain(api_key, endpoint, deployment="gpt-35-turbo-16k"):
    # DOES NOT WORK
    # gpt-35-turbo-16k does not support embeddings


    embeddings = OpenAIEmbeddings(
        openai_api_key=api_key,
        model="text-embedding-ada-002", #text-davinci-002
        openai_api_base=endpoint,
        openai_api_type=OPENAI_API_TYPE,
        deployment=deployment
    )

    pdf_doc = load_pdf_from_dir("../sample.pdf")
    splitted_doc = split_document(pdf_doc)
    doc_search = Chroma.from_documents(splitted_doc, embeddings) #doc_search is a chroma vector store

    azure_llm = init_instance(api_key, endpoint, deployment)
    print("hi")
    chain = RetrievalQA.from_chain_type(llm=azure_llm, chain_type="stuff", retriever=doc_search.as_retriever())


def pdf_assistant_local():
    pdf_str = load_pdf_into_str("../sample.pdf")

    print("Initiating pdf assistant...")

    while True:
        user_input = input("Ask a question: ")

        user_input = user_input.strip().lower()

        if user_input == "exit":
            print("Exiting pdf assistant...")
            break
            
        response = openai.ChatCompletion.create(
            engine=DEPLOYMENT_NAME, 
            max_tokens=1250,
            messages=[
                {"role": "system", "content": "You are an assistant that will analyze and answer questions based on an input pdf. Users will now supply the pdf as a string and will then ask questions"},
                {"role": "user", "content": pdf_str},
                {"role": "user", "content": user_input}
            ]
        )
        assistant_response = response['choices'][0]['message']['content']
        print("Assistant: " + assistant_response)

