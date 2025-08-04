import os
from config import MAX_FILE_READ_LENGTH

def get_file_content(working_directory, file_path):
    # Get full absolute path given directory and working directory
    full_path = os.path.abspath(os.path.normpath(os.path.join(working_directory, file_path)))
    # Convert working directory into absolute path.
    abs_working_directory = os.path.abspath(working_directory)

    # Check if full path is inside workspace, or even a file.
    if not full_path.startswith(abs_working_directory):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    # Read up to max length of file
    try:
        with open(full_path, "r") as file:
            file_content = file.read(MAX_FILE_READ_LENGTH)
            # Append message if file is max length
            if len(file_content) >= MAX_FILE_READ_LENGTH:
                file_content += f'[...File "{file_path}" truncated at 10000 characters]'

            return file_content
    except Exception as e:
        return f"Error: {e}"