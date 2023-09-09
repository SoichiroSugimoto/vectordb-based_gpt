from dotenv import load_dotenv
import os
import sys
import openai
import retriever

try:
    accessibility_ids = [sys.argv[1]]
except IndexError:
    accessibility_ids = ["001"]


def main():
    query_engine = retriever.create_query_engine(accessibility_ids)
    print("Enter a value (press Ctrl+C to exit)")
    conversation_buffer = []
    while True:
        try:
            input_value = input("input : ").strip()
            conversation_buffer.append(input_value)
            content = "\n\n".join(conversation_buffer)
            chat_completion = query_engine.query(content)
            print("output:", chat_completion)
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print("Error:", e)
            break


if __name__ == "__main__":
    main()
