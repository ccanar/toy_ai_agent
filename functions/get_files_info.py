# get_files_info.py
import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    # print(f"{working_directory=}, {directory=}")
    absolute_full_path = os.path.abspath(os.path.join(working_directory, directory))
    # print(f"{full_path=}")
    contents = os.listdir(absolute_full_path)

    # print(
    #     "Is directory outside working_directory: ",
    #     not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)),
    # )
    if not absolute_full_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # print("Is 'directory' not a directory: ", not os.path.isdir(full_path))
    if not os.path.isdir(absolute_full_path):
        return f'Error: "{directory}" is not a directory'

    try:
        files_info = []
        for item in contents:
            path_to_item = os.path.join(absolute_full_path, item)
            # print(f"{path_to_item=}")
            file_size = 0
            is_dir = os.path.isdir(path_to_item)
            file_size = os.path.getsize(path_to_item)
            files_info.append(f" - {item}: {file_size=} bytes, {is_dir=}")
    except Exception as exception:
        return f"Error listing filses: {exception}"
    return "\n".join(files_info)


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            )
        },
    ),
)
