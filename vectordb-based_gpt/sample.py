import os
import json
import retriever
import pinecone_client as pinecone
from http_request_handler import app

params = {'chat_content': '株主総会議事録って何ですか？'}
res = app.test_client().post('/chat/001', query_string=params)
print(res.data)
