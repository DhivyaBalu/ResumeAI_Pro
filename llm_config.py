import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    raise ValueError("Missing OpenAI API Key! Please set OPENAI_API_KEY in the .env file.")

llm = ChatOpenAI(
    temperature=0,
    openai_api_key=openai_api_key,
    model_name="gpt-4o-mini"
)
