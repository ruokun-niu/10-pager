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
from langchain.chat_models import ChatOpenAI


OPENAI_API_TYPE="azure"
OPENAI_API_VERSION="2023-05-15"



def client_init(api_key, endpoint, deployment="gpt-35-turbo-16k"):
    # Uses langchain.llms.OpenAI to create an OpenAI instance

    # Create an instance of Azure OpenAI
    llm = AzureOpenAI(
        deployment_name= deployment,
        openai_api_type=OPENAI_API_TYPE,
        openai_api_version=OPENAI_API_VERSION,
        openai_api_key=api_key,
        openai_api_base=endpoint
    )

    print(llm)
    llm("Tell me a joke")


    # Starting with a simple chat model??
    # chat = ChatOpenAI(openai_api_key=api_key, model_name=deployment_name)





if __name__ == "__main__":
    client_init("***REMOVED***", "***REMOVED***", "gpt-35-turbo-16k")