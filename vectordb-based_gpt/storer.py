import os
import sys
import json
import logging
import inspect
import pprint
from datetime import datetime
from dotenv import load_dotenv

from llama_index import (
    VectorStoreIndex,
    SimpleKeywordTableIndex,
    SimpleDirectoryReader,
    StringIterableReader,
    LLMPredictor,
    ServiceContext,
)
from langchain.llms.openai import OpenAIChat
from llama_index.storage.storage_context import StorageContext
from llama_index.vector_stores import PineconeVectorStore

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
load_dotenv('.env')

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


class IndexCreator:
    def __init__(self, pinecone_index_name=None, pinecone_environment=None, model_name=None):
        self.pinecone_index_name = pinecone_index_name
        self.pinecone_environment = pinecone_environment
        self.llm = OpenAIChat(temperature=0, model=model_name)
        self.service_context = ServiceContext.from_defaults(llm=self.llm)

    # ベクトルデータの保存先を作成
    def _create_vector_store(self):
        return PineconeVectorStore(
            index_name=self.pinecone_index_name,
            environment=self.pinecone_environment,
        )
    
    # ベクトルデータを作成、保存
    def _create_vector_store_index(self, article, vector_store):
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        return VectorStoreIndex.from_documents(
            article,
            storage_context=storage_context,
            service_context=self.service_context,
        )

    def insert_to_pinecone(self, article):
        vector_store = self._create_vector_store()
        vector_store_index = self._create_vector_store_index(article, vector_store)
        nodes = vars(vector_store_index)['_nodes']
        return nodes


def create_index(article_summary, article):
    pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")
    pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
    model_name = "text-embedding-ada-002"
    index_creator = IndexCreator(pinecone_index_name, pinecone_environment, model_name)
    index_creator.insert_to_pinecone(article)


def create_index_from_string(article_summary, text):
    article = StringIterableReader().load_data(texts=[text])
    create_index(article_summary, article)
