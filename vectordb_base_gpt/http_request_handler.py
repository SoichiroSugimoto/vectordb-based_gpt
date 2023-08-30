from flask import Flask, request, jsonify
import awsgi
import pkg_resources
import os
import slack
import logging
import json
import storer
import retriever
from urllib import parse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)

@app.route("/get-list", methods=["GET"])
def get_list():
    return jsonify({"msg": "get_list method"})

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
    if request.is_json:
        data = request.json
        if 'type' in data and data['type'] == 'url_verification':
            return json.dumps( {'challenge': data['challenge'] } )
        else:
            try: 
                data = request.json
                content = data['event']['text']
                ts = data['event']['ts']
                channel_id = data['event']['channel']
                elements = data['event']['blocks'][0]['elements'][0]['elements']
                texts = [element['text'] for element in elements if element['type'] == 'text']
                slack_instance = slack.Slack(os.getenv("SLACK_BOT_TOKEN"))
                slack_instance.post_reply_message(channel_id, ts, f"The message is received. Please wait while the answer is being generated: \n\n>>>{content}")
                query_engine = retriever.create_query_engine()
                print(texts[0])
                query_response = query_engine.query(texts[0])
                chat_completion = vars(query_response)['response']
                print(chat_completion)
                slack_instance.post_reply_message(channel_id, ts, f"{chat_completion}")
                return jsonify({"msg": chat_completion})
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                return jsonify({"msg": "An error occurred"}), 500
    else:
        return jsonify({"msg": "Invalid content"}), 400

@app.route("/delete-index/<int:id>", methods=["DELETE"])
def delete_index(id):
    return jsonify({"msg": "delete_index method"})

def lambda_handler(event, context):
    result = awsgi.response(app, event, context)
    print(result)
    return result