import pkg_resources
import os
import logging
import json
import retriever
import constants as const
from tools.slack_client import SlackClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle_slack_chat(received_data):
    slack_instance = SlackClient(os.getenv("SLACK_BOT_TOKEN"), received_data)
    conversation_data = slack_instance.get_conversation_as_array(slack_instance.ts)
    query_text = const.FORMATTED_PROMPT_TEXT % (slack_instance.texts[0], conversation_data)
    query_engine = retriever.create_query_engine()
    query_response = query_engine.query(query_text)
    chat_response = retriever.get_chat_response(query_response)
    if chat_response is None:
        chat_completion = os.getenv("MESSAGE_ANSWER_UNGENERATED")
    else:
        reference_urls = retriever.get_reference_urls(query_response)
        chat_completion = chat_response + "\n\n" + const.REFERENCE_GUIDE_TEXT + "\n" + reference_urls.replace('- ', '• ')
    slack_instance.post_reply_message(slack_instance.channel_id, slack_instance.ts, f"{chat_completion}")
    return (chat_completion)

def handle_slack_request(request):
    try:
        request_headers = request.get('headers')
        request_body = json.loads(request.get('body'))
        # for Slack URL Verification
        if request_body.get('type') == 'url_verification':
            return {
                'statusCode': 200,
                'body': json.dumps( {'challenge': request_body.get('challenge') } )
            }
        elif request_headers.get('X-Slack-Retry-Num') == '1': # handle Slack response retry
            chat_completion = handle_slack_chat(request_body)
            return json.dumps({"msg": chat_completion}), 200
        else:
            return json.dumps({"msg": "Retry"}), 208
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return json.dumps({"msg": "An error occurred"}), 500


def lambda_handler(event, context):
    result = handle_slack_request(event)
    return result
