import os
import sys
import logging
from tools.pinecone_client import PineconeClient
import openai
from dotenv import load_dotenv

from llama_index import ServiceContext
from llama_index.indices.vector_store import GPTVectorStoreIndex
from langchain_community.chat_models import ChatOpenAI
from llama_index.vector_stores import PineconeVectorStore
from llama_index.llms import OpenAI

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
# logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
load_dotenv('.env')

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
notion_page_path = os.getenv("NOTION_PAGE_PATH")


def create_index_from_pinecone():
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


def get_chat_response(query_response):
    return vars(query_response)['response']


def get_reference_urls(query_response):
    reference_urls = ''

    source_nodes = vars(query_response).get('source_nodes')
    if not source_nodes:
        return reference_urls
    for source_node in source_nodes:
        node = vars(source_node).get('node')
        metadata = vars(node).get('metadata')
        if metadata:
            page_id = metadata.get('page_id')
            if page_id is not None:
                reference_urls += f"- {notion_page_path}{page_id}\n"

    return reference_urls
