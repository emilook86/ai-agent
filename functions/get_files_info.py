import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = (
        os.path.commonpath([target_dir, working_dir_abs]) == working_dir_abs
    )

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside permitted working directory.'

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory.'

    files_info = []
    for entry in os.listdir(target_dir):
        entry_path = os.path.join(target_dir, entry)
        files_info.append(
            f"  - {entry}: file_size={os.path.getsize(entry_path)}, is_dir={os.path.isdir(entry_path)}"
        )
    result = "Result for current directory:\n" + "\n".join(files_info)
    return result


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
