from flask import Flask, request, jsonify
import awsgi
import pkg_resources
import os
import slack_client as slack
import logging
import json
import storer
import retriever
import constants as const
import pinecone_client as pinecone
from dynamodb_client import DynamoDBTable
from urllib import parse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)


@app.route("/index-list", methods=["GET"])
def get_list():
    try:
        index_data = []
        pinecone_instance = pinecone.PineconeClient(
            os.getenv("PINECONE_API_KEY"),
            os.getenv("PINECONE_ENVIRONMENT"),
            os.getenv("PINECONE_INDEX_NAME"))
        article_table = DynamoDBTable(
            table_name="Article",
            region_name="ap-northeast-1",
            partition_key_name="category_id",
            sort_key_name="deleted"
        )
        records = article_table.get_alive_records()
        if records is not None:
            for record in records:
                text = pinecone_instance.get_text_from_id(record["pinecone_id"], namespace='')
                index_data.append({'category_id': record["category_id"],
                                    'pinecone_id': record["pinecone_id"],
                                    'text': text})
        print(index_data)
        return (json.dumps(index_data))
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return jsonify({"msg": "An error occurred"}), 500


@app.route("/get-list/<int:page>", methods=["GET"])
def get_list_page(page):
    return jsonify({"msg": "get_list_page method"})


@app.route("/get-index", methods=["GET"])
def get_index():
    return jsonify({"msg": "get_index method"})


@app.route("/store-article", methods=["POST"])
def store_article():
    return jsonify({"msg": "store_article method"})


@app.route("/post-chat", methods=["POST"])
def post_chat():
    try: 
        data = request.json
        if 'type' in data and data['type'] == 'url_verification':
            return json.dumps( {'challenge': data['challenge'] } )
        elif request.headers['X-Slack-Retry-Num'] == '1':
            print(data)
            content = data['event']['text']
            ts = data['event']['ts']
            channel_id = data['event']['channel']
            elements = data['event']['blocks'][0]['elements'][0]['elements']
            texts = [element['text'] for element in elements if element['type'] == 'text']
            slack_instance = slack.SlackClient(os.getenv("SLACK_BOT_TOKEN"))
            slack_instance.post_reply_message(channel_id, ts, const.MESSAGE_PLEASE_WAITING + f" \n\n>>>{content}")
            query_engine = retriever.create_query_engine()
            query_response = query_engine.query(const.FORMATTED_PROMPT_TEXT %texts[0])
            chat_completion = vars(query_response)['response']
            print(chat_completion)
            if chat_completion is None:
                chat_completion = const.MESSAGE_ANSWER_UNGENERATED
            slack_instance.post_reply_message(channel_id, ts, f"{chat_completion}")
            return jsonify({"msg": chat_completion})
        else:
            return jsonify({"msg": "Retry"})
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return jsonify({"msg": "An error occurred"}), 500


@app.route("/delete-index/<int:id>", methods=["DELETE"])
def delete_index(id):
    return jsonify({"msg": "delete_index method"})


def lambda_handler(event, context):
    result = awsgi.response(app, event, context)
    print(result)
    return result
