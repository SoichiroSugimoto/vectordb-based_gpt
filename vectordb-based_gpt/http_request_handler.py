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


def validate_request(req, required_params):
    missing_params = [param for param in required_params if param not in req]
    if missing_params:
        return False, f"Missing required parameters: {', '.join(missing_params)}"
    empty_params = [param for param in required_params if not req[param]]
    if empty_params:
        return False, f"Empty or None values for parameters: {', '.join(empty_params)}"
    return True, ""


def group_by_namespace(dynamodb_data):
    result = []
    namespace_to_index = {}
    for item in dynamodb_data:
        namespace = item['category_id'].split('#')[0]
        pinecone_id = item['pinecone_id']
        if namespace in namespace_to_index:
            index = namespace_to_index[namespace]
            result[index]['pinecone_ids'].append(pinecone_id)
        else:
            new_dict = {'namespace': namespace, 'pinecone_ids': [pinecone_id]}
            result.append(new_dict)
            namespace_to_index[namespace] = len(result) - 1
    return (result)


def get_category_id_with_pinecone_id(dynamodb_data, pinecone_id):
    for item in dynamodb_data:
        if item['pinecone_id'] == pinecone_id:
            return (item['category_id'])
    return (None)


def handle_slack_chat(received_data, accessibility_ids=None):
    slack_instance = slack.SlackClient(os.getenv("SLACK_BOT_TOKEN"), received_data)
    slack_instance.post_reply_message(
        slack_instance.channel_id, 
        slack_instance.ts,
        const.MESSAGE_PLEASE_WAITING + f" \n\n>>>{slack_instance.content}"
    )
    conversation_data = slack_instance.get_conversation_as_array(slack_instance.ts)
    query_text = const.FORMATTED_PROMPT_TEXT % (slack_instance.texts[0], conversation_data)
    query_engine = retriever.create_query_engine(accessibility_ids)
    query_response = query_engine.query(query_text)
    chat_completion = vars(query_response)['response']
    if chat_completion is None:
        chat_completion = const.MESSAGE_ANSWER_UNGENERATED
    slack_instance.post_reply_message(slack_instance.channel_id, slack_instance.ts, f"{chat_completion}")
    return (chat_completion)


def handle_chat(chat_content, accessibility_ids=None):
    query_engine = retriever.create_query_engine(accessibility_ids)
    query_response = query_engine.query(chat_content)
    chat_completion = vars(query_response)['response']
    if chat_completion is None:
        chat_completion = const.MESSAGE_ANSWER_UNGENERATED
    return (chat_completion)


app = Flask(__name__)


@app.route("/vector-data-list", methods=["GET"])
def get_vector_data_list():
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
            namespace_groups = group_by_namespace(records)
            for namespace_group in namespace_groups:
                vector_data = pinecone_instance.fetch_vector_data_with_id(
                    namespace_group['pinecone_ids'], 
                    namespace=namespace_group['namespace'])
                for pinecone_id in namespace_group['pinecone_ids']:
                    category_id = get_category_id_with_pinecone_id(
                        records, pinecone_id)
                    parsed_vector_data = json.loads(
                        vector_data
                        ['vectors'][pinecone_id]['metadata']['_node_content'])
                    text = parsed_vector_data['text']
                    index_data.append({
                        'category_id': category_id,
                        'pinecone_id': pinecone_id,
                        'text': text})
        print(index_data)
        return (json.dumps(index_data))
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return jsonify({"msg": f"An error occurred. {e}"}), 500


@app.route("/vector-data", methods=["GET"])
def get_vector_data():
    return jsonify({"msg": "get_index method"})


@app.route("/store-article/<string:accessibility_ids>", methods=["POST"])
def store_article(accessibility_ids):
    try:
        req = request.args
        required_params = ["text", "title"]
        is_valid, validation_msg = validate_request(req, required_params)
        if not is_valid:
            return jsonify({"msg": validation_msg}), 400
        text = req.get("text")
        title = req.get("title")
        article_summary = f"Article about {title}"
        print(article_summary)
        storer.create_index_from_string(
            article_summary, text, accessibility_ids.split(',')[0])
        return jsonify({"msg": "Article stored successfully"}), 200
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return jsonify({"msg": "An error occurred"}), 500


@app.route("/slack-chat", methods=["POST"])
def slack_chat_query():
    try:
        received_data = request.json
        if 'type' in received_data and received_data['type'] == 'url_verification':
            return json.dumps({'challenge': received_data['challenge']})
        elif request.headers['X-Slack-Retry-Num'] == '1':
            chat_completion = handle_slack_chat(received_data)
            return jsonify({"msg": chat_completion})
        else:
            return jsonify({"msg": "Retry"})
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return jsonify({"msg": "An error occurred"}), 500


@app.route("/slack-chat/<string:accessibility_ids>", methods=["POST"])
def slack_chat_query_with_accessibility_ids(accessibility_ids):
    try:
        received_data = request.json
        if 'type' in received_data and received_data['type'] == 'url_verification':
            return json.dumps({'challenge': received_data['challenge']})
        elif request.headers['X-Slack-Retry-Num'] == '1':
            chat_completion = handle_slack_chat(received_data, accessibility_ids.split(','))
            return jsonify({"msg": chat_completion})
        else:
            return jsonify({"msg": "Retry"})
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return jsonify({"msg": "An error occurred"}), 500
    

@app.route("/chat/<string:accessibility_ids>", methods=["POST"])
def chat_query_with_accessibility_ids(accessibility_ids):
    try:
        req = request.args
        required_params = ["chat_content"]
        is_valid, validation_msg = validate_request(req, required_params)
        if not is_valid:
            return jsonify({"msg": validation_msg}), 400
        chat_content = req.get("chat_content")
        chat_completion = handle_chat(chat_content, accessibility_ids.split(','))
        return jsonify({"chat_completion": chat_completion}), 200
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return jsonify({"msg": "An error occurred"}), 500


@app.route("/vector-data", methods=["DELETE"])
def delete_vector_data():
    try:
        req = request.args
        required_params = ["category_id"]
        is_valid, validation_msg = validate_request(req, required_params)
        if not is_valid:
            return jsonify({"msg": validation_msg}), 400
        category_id = req.get("category_id")
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
        dynamodb_response = article_table.delete_item(
            partition_key_value=category_id, sort_key_value=0)
        pinecone_response = pinecone_instance.delete_vector_data_with_id(
            category_id, namespace=str(category_id).split('#')[0])
        return jsonify({"msg": f"{dynamodb_response}  {pinecone_response}"}), 200
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return jsonify({"msg": "An error occurred"}), 500


def lambda_handler(event, context):
    result = awsgi.response(app, event, context)
    print(result)
    return result
