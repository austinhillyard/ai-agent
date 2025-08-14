import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites and existing python file, or if the file does not exist, creates a new file with the specified content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory. A required parameter. If it does not exist it will create the file first.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    # Get full absolute path given directory and working directory
    full_path = os.path.abspath(os.path.normpath(os.path.join(working_directory, file_path)))
    # Convert working directory into absolute path.
    abs_working_directory = os.path.abspath(working_directory)

    # Check if full path is inside workspace, or even a file.
    if not full_path.startswith(abs_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    bytes_written = 0
    try:
        with open(full_path, "w+") as file:
            bytes_written = file.write(content)
            file.close()

        return f'Successfully wrote to "{file_path}" ({bytes_written} characters written)'
    except Exception as err:
        return f'Error: "{err}"'