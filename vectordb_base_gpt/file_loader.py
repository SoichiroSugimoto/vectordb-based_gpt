import os
import logging
import storer
import retriever
from dynamo_db import DynamoDBTable
from llama_index import SimpleDirectoryReader, StringIterableReader


dir_path = os.path.join(os.path.dirname(__file__), "/root/data")

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

# Initialize logging
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = ColoredFormatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def list_files_in_directory(directory_path):
    try:
        files = []
        with os.scandir(directory_path) as entries:
            for entry in entries:
                if entry.is_file():
                    files.append(entry.name)
        return files
    except FileNotFoundError:
        for h in logger.handlers[:-1]:
            logger.removeHandler(h)
        logger.error(f"{directory_path} が見つかりません。")
        return None
    except PermissionError:
        for h in logger.handlers[:-1]:
            logger.removeHandler(h)
        logger.error(f"{directory_path} へのアクセス許可がありません。")
        return None

def store_text_files_as_vector(files):
    try:
        for file in files:
            article_title = f"Artile about {file.replace('.txt', '')}"
            print(article_title)
            documents = SimpleDirectoryReader(input_files=[f"../data/{file}"]).load_data()
            storer.create_index(article_title, documents, "001")
    except Exception as e:
        for h in logger.handlers[:-1]:
            logger.removeHandler(h)
        logger.error(f"An error occurred: {e}")
        return None


directory_path = '../data'
files = list_files_in_directory(directory_path)
if files is not None:
    store_text_files_as_vector(files)
