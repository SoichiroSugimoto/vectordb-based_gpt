import logging
import os
import json
import pinecone
from pinecone import Pinecone


class PineconeClient:
    def __init__(self, api_key, index_name):
        pc = Pinecone(api_key=api_key)
        self.index = pc.Index(index_name)
        self.logger = logging.getLogger(__name__)
