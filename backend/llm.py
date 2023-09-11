from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI


def openAI():
    llm = OpenAI(openai_api_key="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")
    chat_model = ChatOpenAI()
    
    text = "What would be a good company name for a company that makes colorful socks?"

    llm.predict(text)


if __name__ == "__main__":
    openAI()