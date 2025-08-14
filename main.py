import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

def main():
    # Verbose flag for command line
    verbose = False

    usage_text = 'Usage: main.py "{You prompt here}" --verbose\n--verbose flag is optional'
    # Parse arguments
    # Check for verbose flag
    if len(sys.argv) == 3 and sys.argv[2] == '--verbose':
        verbose = True
    # Exit on improper argument list
    elif len(sys.argv) < 2 or len(sys.argv) >= 3:
        print(usage_text)
        sys.exit(1)

    user_prompt = sys.argv[1]

    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments. Arguments are not required. Run the file without arguments by default instead of asking for additional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
Once you are done, simply write your response in your response.text field. Unless specified, refrain from writing new files.
"""

    # Load API key and Client
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # Create messages variable that stores user prompt
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    iterations = 0
    while iterations < 20:
        iterations += 1
        try:

            # Get response
            response = client.models.generate_content(
                model="gemini-2.0-flash-001", 
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
                
            )
            
            # Add candidate messages to messages list
            for candidate in response.candidates:
                messages.append(candidate.content)

            # Function calls from AI model
            if response.function_calls and len(response.function_calls) > 0:
                # Loop through function calls
                for function_call_part in response.function_calls:
                    # call function
                    function_call_result = call_function(function_call_part, verbose)
                    # Check if we have a response, otherwise through an error
                    if not function_call_result.parts[0].function_response.response:
                        raise Exception("Expected 'function_call_result.parts[0].function_response.response', got none")
                    # Print that response if verbose option exists
                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                    # Add function response to messages list
                    messages.append(types.Content(
                        role="user", 
                        parts=[types.Part(text=str(function_call_result.parts[0].function_response.response['result']))]
                    ))

            # If plain text response, treat as end of loop, and print response.
            elif response.text:
                print(f"Final response:\n{response.text}")
                break           

        except Exception as err:
            print(f"Error: {err}")
            break


def call_function(function_call_part: types.FunctionCall, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"- Calling function: {function_call_part.name}")

    # Map of functions we can call
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    # Call function if found
    if function_call_part.name in function_map:
        result = function_map[function_call_part.name]("./calculator", **function_call_part.args)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": result},
                )
            ],
        )
    # Return unknown function error.
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

if __name__ == "__main__":
    main()
