import logging
import os
import json
import pinecone


class PineconeClient:
    def __init__(self, api_key, environment, index_name):
        pinecone.init(api_key=api_key, environment=environment)
        self.index = pinecone.Index(index_name)
        self.logger = logging.getLogger(__name__)

    def get_text_from_id(self, id, namespace=''):
        try:
            result = self.index.fetch(
                ids=[id],
                namespace=namespace
            )
            parsed_data = json.loads(result['vectors'][id]['metadata']['_node_content'])
            return parsed_data['text']

        except Exception as e:
            self.logger.error(f"Error fetch text: {e}")

    def fetch_vector_data_with_id(self, ids, namespace=''):
        try:
            response = self.index.fetch(
                ids=ids,
                namespace=namespace
            )
            return (response)

        except Exception as e:
            self.logger.error(f"Error fetch text: {e}")

    def delete_vector_data_with_id(self, id, namespace=''):
        try:
            response = self.index.delete(
                ids=[id],
                namespace=namespace
            )
            return (response)
        except Exception as e:
            self.logger.error(f"Error delete vector data: {e}")
