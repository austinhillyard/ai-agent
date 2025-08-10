import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):

    # Get full absolute path given directory and working directory
    full_path = os.path.abspath(os.path.normpath(os.path.join(working_directory, directory)))
    # Convert working directory into absolute path.
    abs_working_directory = os.path.abspath(working_directory)
    
    try :
        # Initailize output string and read directory contents
        output = ""
        dir_contents = os.listdir(full_path)
        output += f"Result for {"current" if directory == '.' else f"'{directory}'"} directory:\n"

        # Check if full path is inside workspace, or even a directory.
        if not full_path.startswith(abs_working_directory):
            output += f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            return output
        if not os.path.isdir(full_path):
            output += f'Error: "{directory}" is not a directory'
            return output
        
        # Iterate through directory and print it's details
        for item in dir_contents:
            item_path = full_path + '/' + item
            output += f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}\n"

        return output
    except Exception as e:
        print(f"Error: Unexpected error: {str(e)}")
