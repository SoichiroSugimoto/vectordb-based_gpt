import os
import sys
import logging
import pinecone_client as pinecone
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
    pinecone_instance = pinecone.PineconeClient(
        os.getenv("PINECONE_API_KEY"),
        os.getenv("PINECONE_ENVIRONMENT"),
        os.getenv("PINECONE_INDEX_NAME"))
    vector_store = PineconeVectorStore(pinecone_instance.index, namespace=namespace)
    index = GPTVectorStoreIndex.from_vector_store(vector_store=vector_store)
    return index


def setup_retriever():
    documents = StringIterableReader().load_data("exec not to store docs, but to setup retriever")
    llm = OpenAI(temperature=0, model="gpt-4")
    service_context = ServiceContext.from_defaults(llm=llm)
    VectorStoreIndex.from_documents(
            documents=documents,
            llm_predictor=LLMPredictor(),
            service_context=service_context
        )
    return None


def create_query_engine():
    setup_retriever()
    index = create_index_from_pinecone()
    query_engine = index.as_query_engine()
    return query_engine
