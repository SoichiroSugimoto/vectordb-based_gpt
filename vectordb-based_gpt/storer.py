import os
import sys
import json
import logging
from dotenv import load_dotenv

from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
)
# from langchain.llms.openai import OpenAIChat
from langchain_community.chat_models import ChatOpenAI
from llama_index.readers.string_iterable import StringIterableReader
from llama_index.storage.storage_context import StorageContext
from llama_index.vector_stores import PineconeVectorStore

dir_path = os.path.join(os.path.dirname(__file__), "root/data")

# ANSI escape codes for colored text
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED
}

class ColoredFormatter(logging.Formatter):
    def __init__(self, msg):
        logging.Formatter.__init__(self, msg)

    def format(self, record):
        levelname = record.levelname
        if levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)

logger = logging.getLogger()
handler = logging.StreamHandler(stream=sys.stdout)
formatter = ColoredFormatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

load_dotenv('.env')

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

class IndexCreator:
    def __init__(self, pinecone_index_name=None, pinecone_environment=None, model_name=None):
        self.pinecone_index_name = pinecone_index_name
        self.pinecone_environment = pinecone_environment
        self.llm = OpenAIChat(temperature=0, model=model_name)
        self.service_context = ServiceContext.from_defaults(llm=self.llm)

    def _create_vector_store(self):
        return PineconeVectorStore(
            index_name=self.pinecone_index_name,
            environment=self.pinecone_environment,
        )
    
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

class LocalFileReader:
    def __init__(self, directory_path='../data'):
        self.directory_path = directory_path

    def execute(self):
        files = self.list_files_in_directory(self.directory_path)
        if files is not None:
            store_text_files_as_vector(files)

    def list_files_in_directory(self, directory_path):
        try:
            files = []
            with os.scandir(directory_path) as entries:
                for entry in entries:
                    if entry.is_file():
                        files.append(entry.name)
            return files
        except FileNotFoundError:
            logger.error(f"{directory_path} が見つかりません。")
            return None
        except PermissionError:
            logger.error(f"{directory_path} へのアクセス許可がありません。")
            return None

def store_text_files_as_vector(files):
    try:
        for file in files:
            article_summary = f"Artile about {file.replace('.txt', '')}"
            print(article_summary)
            article = SimpleDirectoryReader(input_files=[f"../data/{file}"]).load_data()
            create_index(article_summary, article)
    except Exception as e:
        logger.error
