import os, subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file specified, with optional arguments. Any STDOUT and STDERR is captures and returned as a string. If no arguments are specified the user, assume none are required",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to run in python, relative to the working directory. A required parameter.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
                description="A list of strings of optional arguments to run with the specified file. By default an empty list. Any arguments are appended after the file name in the command line",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    # Get full absolute path given directory and working directory
    full_path = os.path.abspath(os.path.normpath(os.path.join(working_directory, file_path)))
    # Convert working directory into absolute path.
    abs_working_directory = os.path.abspath(working_directory)

    # Check if full path is inside workspace, or even a file.
    if not full_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        args = ['python', full_path] + args
        output = subprocess.run(args, timeout=30, capture_output=True)
        stdout = output.stdout
        stderr = output.stderr

        if output.returncode != 0:
            return f"Process exited with code {output.returncode}"

        if len(stdout) == 0 and len(stderr) == 0:
            return f"No output produced"
        
        return f"""STDOUT: {stdout}\nSTDERR: {stderr}"""
    except Exception as err:
        return f"Error: executing Python file: {err}"