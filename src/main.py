from dotenv import load_dotenv
import os
import openai


def main():
    print("Enter a value (press Ctrl+C to exit)")
    conversation_buffer = []
    while True:
        try:
            load_dotenv()
            openai.api_key = os.getenv("OPENAI_API_KEY")
            input_value = input("input : ").strip()
            conversation_buffer.append(input_value)
            chat_completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "\n\n".join(conversation_buffer)}],
                max_tokens=300,
            )
            response = chat_completion["choices"][0]["message"]["content"]
            print("output:", response)
        except KeyboardInterrupt:
            print("\nExiting...")
            break


if __name__ == "__main__":
    main()
