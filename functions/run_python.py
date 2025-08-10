import os, subprocess

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