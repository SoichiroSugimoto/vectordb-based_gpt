from dotenv import load_dotenv
import os
import openai
import retriever


def main():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    query_engine = retriever.create_query_engine()
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
