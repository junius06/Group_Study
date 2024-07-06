import os
import openai
import numpy as np
import pandas as pd
from numpy import dot
from numpy.linalg import norm
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env', 'dev.env'))
API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = API_KEY

def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

print(get_embedding('임베딩테스트'))