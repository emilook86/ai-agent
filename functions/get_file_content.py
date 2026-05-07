import os
from config import MAX_CHARS
from google.genai import types


def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = (
        os.path.commonpath([target_file, working_dir_abs]) == working_dir_abs
    )

    if not valid_target_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
            return file_content_string
    except Exception as e:
        return f"Error: some kind of error with reading the file occured. Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads file content in a specified directory, relative to the working directory. It reads the first MAX_CHARS characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Filepath to be read, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)
