import os

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