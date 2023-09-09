import os
import json
import retriever
import pinecone_client as pinecone
from dynamodb_client import DynamoDBTable
from http_request_handler import app

res = app.test_client().post('/post-chat/002')
# print(res.data)

# retriever.do_test(["002"])
