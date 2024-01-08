import os
import sys
import logging
from pinecone_client import PineconeClient
import openai
from dotenv import load_dotenv

from llama_index import (
    VectorStoreIndex,
    StringIterableReader,
    LLMPredictor,
    ServiceContext,
)

from llama_index.indices.vector_store import GPTVectorStoreIndex
from langchain.llms.openai import OpenAIChat
from llama_index.vector_stores import PineconeVectorStore
from llama_index.llms import OpenAI

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
load_dotenv('.env')

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")


def create_index_from_pinecone(namespace):
    pinecone_instance = PineconeClient(
        os.getenv("PINECONE_API_KEY"),
        os.getenv("PINECONE_ENVIRONMENT"),
        os.getenv("PINECONE_INDEX_NAME"))
    vector_store = PineconeVectorStore(pinecone_instance.index)
    llm = OpenAI(temperature=0, model="gpt-4")
    service_context = ServiceContext.from_defaults(llm=llm)
    index = GPTVectorStoreIndex.from_vector_store(vector_store=vector_store, service_context=service_context)
    return index


def create_query_engine(similarity_top_k=1):
    index = create_index_from_pinecone()
    query_engine = index.as_query_engine(similarity_top_k=1)
    return query_engine
