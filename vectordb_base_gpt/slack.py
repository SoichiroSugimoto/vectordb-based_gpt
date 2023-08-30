import logging
import os

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class Slack:
    def __init__(self, slack_bot_token):
        self.client = WebClient(token=slack_bot_token)
        self.logger = logging.getLogger(__name__)

    def get_thread_text_array(self, channel_id, ts):
        try:
            result = self.client.conversations_replies(
                channel=channel_id,
                ts=ts
            )
            thread_text_array = []
            self.logger.info(result)
            for message in vars(result)['_initial_data']['messages']:
                thread_text_array.append(message['text'])
            return thread_text_array

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
