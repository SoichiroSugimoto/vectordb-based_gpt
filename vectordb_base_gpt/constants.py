import os
from dotenv import load_dotenv

load_dotenv('.env')

default_formatted_prompt_text = "Language: JP, \
    Requested-Role: Back-Office Expert, \
    Question: %s, \
    History: %s, \
    Reference URL: Required for completion (Provide Specific Source), \
    No Reference: Skip"
if os.getenv('FORMATTED_PROMPT_TEXT') is None or \
        os.getenv('FORMATTED_PROMPT_TEXT').count("%s") != 2:
    FORMATTED_PROMPT_TEXT = default_formatted_prompt_text
else:
    FORMATTED_PROMPT_TEXT = os.environ['FORMATTED_PROMPT_TEXT']
MESSAGE_PLEASE_WAITING = "The message has been received. \
    \nPlease wait while we generate your answer: "
MESSAGE_ANSWER_UNGENERATED = "Sorry, I don't know the answer."
