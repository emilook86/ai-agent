import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_functions import available_functions, call_functions
import sys
from config import MAX_LOOPS


def main():

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("The API Key is not there.")

    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(MAX_LOOPS):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )

        for candidate in response.candidates:
            messages.append(candidate.content)

        if response.usage_metadata is None:
            raise RuntimeError("There is no token usage metadata in the response.")

        input_tokens = response.usage_metadata.prompt_token_count
        output_tokens = response.usage_metadata.candidates_token_count

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {input_tokens}")
            print(f"Response tokens: {output_tokens}")

        if response.function_calls:
            function_responses = []
            for function_call in response.function_calls:
                if args.verbose:
                    print(
                        f"Calling function: {function_call.name}({function_call.args})"
                    )
                function_call_result = call_functions(function_call, args.verbose)
                if function_call_result.parts is None:
                    raise Exception(
                        "The calling function result should have nonempty parts property"
                    )
                if function_call_result.parts[0].function_response is None:
                    raise Exception(
                        "The first element of parts atrribute should have nonempty response object"
                    )
                result_response = function_call_result.parts[
                    0
                ].function_response.response
                if result_response is None:
                    raise Exception("The actual response is empty")
                function_responses.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {result_response}")

            messages.append(types.Content(role="user", parts=function_responses))
        else:
            print(f"Response:\n{response.text}")
            return

    print("The maximum number of iterations was hit.")
    sys.exit("The maximum number of iterations was hit.")


if __name__ == "__main__":
    main()
