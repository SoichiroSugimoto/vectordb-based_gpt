import logging
import os
import constants as const

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackClient:
    def __init__(self, slack_bot_token, received_data):
        self.client = WebClient(token=slack_bot_token)
        self.content = received_data['event']['text']
        if 'thread_ts' in received_data['event']:
            self.ts = received_data['event']['thread_ts']
        else:
            self.ts = received_data['event']['ts']
        self.channel_id = received_data['event']['channel']
        elements = received_data['event']['blocks'][0]['elements'][0]['elements']
        self.texts = [element['text'] for element in elements if element['type'] == 'text']
        self.logger = logging.getLogger(__name__)

    def get_conversation_as_array(self, ts):
        try:
            result = self.client.conversations_replies(
                channel=self.channel_id,
                ts=ts
            )
            if len(result['messages']) <= 1:
                return ''
            else:
                conversation_data = []
                for message in result['messages']:
                    data_list = message['blocks'][0]['elements'][0]['elements']
                    for item in data_list:
                        if 'type' in item and item['type'] == 'text':
                            text = item['text']
                    if not text.startswith(const.MESSAGE_PLEASE_WAITING):
                        if 'bot_id' in message.keys():
                            conversation_data.append({'role': 'Back-Office Expert', 'content': text})
                        else:
                            conversation_data.append({'role': 'Client', 'content': text})
                print(conversation_data)
                return str(conversation_data)

        except SlackApiError as e:
            self.logger.error(f"Error posting message: {e}")

    def post_reply_message(self, channel_id, parent_ts, message_text):
        try:
            result = self.client.chat_postMessage(
                channel=channel_id,
                thread_ts=parent_ts,
                text=message_text
            )
            self.logger.info(result)

        except SlackApiError as e:
            self.logger.error(f"Error posting message: {e}")
