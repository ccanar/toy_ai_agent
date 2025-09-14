# write_file.py
import os

from google.genai import types


def write_file(working_directory, file_path, content):
    absolute_full_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not absolute_full_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        if not os.path.exists(absolute_full_path):
            os.makedirs(os.path.dirname(absolute_full_path), exist_ok=True)
    except Exception as exception:
        return f"Error: {exception} creating a directory"

    try:
        with open(absolute_full_path, "w") as file:
            file.write(content)
    except Exception as exception:
        return f"Error: writing to file {exception}"
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes specified content to the file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)
