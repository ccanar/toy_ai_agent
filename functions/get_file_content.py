# get_file_content.py
import os
from google.genai import types

from config import FILE_READ_CHARACTER_LIMIT


def get_file_content(working_directory, file_path):
    absolute_full_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not absolute_full_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(absolute_full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(absolute_full_path, "r") as file:
            file_content_string = file.read(FILE_READ_CHARACTER_LIMIT)
            # print(f"{len(file_content_string)=}")
            if os.path.getsize(absolute_full_path) > FILE_READ_CHARACTER_LIMIT:
                file_content_string += f'[...File "{file_path}" truncated at {FILE_READ_CHARACTER_LIMIT} characters].'
                # print(f"{len(file_content_string)=}")
        return file_content_string

    except Exception as exception:
        return f'Error reading the file "{file_path}": {exception}'


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {FILE_READ_CHARACTER_LIMIT} characters of the content from a specified file within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            )
        },
        required=["file_path"],
    ),
)
