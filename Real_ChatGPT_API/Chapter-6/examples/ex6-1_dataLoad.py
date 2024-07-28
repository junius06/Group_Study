import os
import openai
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import retrieval_qa
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
from collections import Counter
from dotenv import load_dotenv

# API_KEY from the .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env', 'dev.env'))
API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY

# Data directory path
data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')

loader = DirectoryLoader(data_dir, glob="*.txt", loader_cls=TextLoader)
documents = loader.load()
print('문서의 개수 : ', len(documents))

print('1번 문서 : ', documents[1])
print('-' * 20)
print('1번 문서 : ', documents[21])
print('-' * 20)