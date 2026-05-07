import os
from google.genai import types


def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = (
        os.path.commonpath([target_file, working_dir_abs]) == working_dir_abs
    )

    if not valid_target_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    os.makedirs(os.path.dirname(target_file), exist_ok=True)

    try:
        with open(target_file, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: some kind of error with writing to the file occured. Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to the given file the content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Filepath to write the content, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written to the given file",
            ),
        },
        required=["file_path", "content"],
    ),
)
