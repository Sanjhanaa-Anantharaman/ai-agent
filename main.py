import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found in environment variables.")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt", )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client=genai.Client(api_key=api_key)
    response = client.models.generate_content(model='gemini-flash-lite-latest', contents=messages) #This is a GenerateContentResponse object
    if args.verbose:
        if response.usage_metadata:
            print("User prompt: ", args.user_prompt)
            print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
            print("Response tokens: ", response.usage_metadata.candidates_token_count)
        else:
            raise RuntimeError("Response was not generated successfully.")
    print(response.text)

if __name__ == "__main__":
    main()
