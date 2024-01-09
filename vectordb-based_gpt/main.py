from dotenv import load_dotenv
import os
import sys
import openai
import retriever
# from storer import LocalFileReader

# Purpose: This is the main entry point for the application of local usage.
def main():
    query_engine = retriever.create_query_engine(1)
    print("Enter a value (press Ctrl+C to exit)")
    conversation_buffer = []
    while True:
        try:
            input_value = input("input : ").strip()
            conversation_buffer.append(input_value)
            content = "\n\n".join(conversation_buffer)
            chat_completion = query_engine.query(content)
            reference_urls = retriever.get_reference_urls(chat_completion)
            print("output:", vars(chat_completion)['response'] + "\n" + reference_urls)
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {type(e).__name__}, {e}")
            break

if __name__ == "__main__":
    main()
