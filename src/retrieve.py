import os
import sys
import logging
import pinecone
import openai
from dotenv import load_dotenv

from llama_index import (
    VectorStoreIndex,
    SimpleKeywordTableIndex,
    SimpleDirectoryReader,
    LLMPredictor,
    ServiceContext,
)
from llama_index.indices.composability.graph import ComposableGraph
from llama_index.indices.vector_store import GPTVectorStoreIndex
from langchain.llms.openai import OpenAIChat
from llama_index.storage.storage_context import StorageContext
from llama_index.vector_stores import PineconeVectorStore

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


def get_index_from_pinecone(ids):
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
    pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")
    pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)
    vector_store = PineconeVectorStore(pinecone.Index(pinecone_index_name))
    index = GPTVectorStoreIndex.from_vector_store(vector_store=vector_store, ids=ids)
    return index


def get_vector_store_ids_from_dynamo_db():
    index_summary = "Article about boston"
    id = "006ab22f-e40d-4112-8baa-523606e3a9d2"
    return [{"id": id, "index_summary": index_summary}]


def build_composable_graph():
    data_set = get_vector_store_ids_from_dynamo_db()
    indices = get_index_from_pinecone([item["id"] for item in data_set])
    graph = ComposableGraph.from_indices(
        SimpleKeywordTableIndex,
        # [index for _, index in indices.items()],
        [indices],
        [item["index_summary"] for item in data_set],
        max_keywords_per_chunk=50,
    )
    return graph


def create_query_engine():
    graph = build_composable_graph()
    llm = OpenAIChat(temperature=0, model="gpt-3.5-turbo")
    service_context = ServiceContext.from_defaults(llm=llm)
    custom_query_engines = {
        graph.root_id: graph.root_index.as_query_engine(retriever_mode="simple", service_context=service_context)
    }
    query_engine = graph.as_query_engine(
        custom_query_engines=custom_query_engines,
    )
    return query_engine
