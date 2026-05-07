import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = (
        os.path.commonpath([target_file, working_dir_abs]) == working_dir_abs
    )

    if not valid_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    try:
        command = ["python", target_file]
        if args is not None:
            command.extend(args)

        completed_process = subprocess.run(
            command, capture_output=True, text=True, timeout=30
        )
        output_string = ""
        if not completed_process.stdout and not completed_process.stderr:
            output_string += "No output produced"
        if completed_process.stdout:
            output_string += f"STDOUT: {completed_process.stdout}"
        if completed_process.stderr:
            output_string += f"STDERR: {completed_process.stderr}"
        if completed_process.returncode != 0:
            output_string += f"Process exited with code {completed_process.returncode}"
        return output_string

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run python file from the file_path with the given optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Filepath of a python script to be executed, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional arguments provided to the python script",
            ),
        },
        required=["file_path"],
    ),
)
