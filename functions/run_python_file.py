# run_python_file.py
import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    print(f"RUN_PYTHON_FILE {file_path}")
    print(f"{working_directory=}, {file_path=}, {args=}")
    absolute_full_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not absolute_full_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(absolute_full_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        if args:
            completed_process = subprocess.run(
                ["python", absolute_full_path, " ".join(args)],
                text=True,
                timeout=30,
                capture_output=True,
            )
        else:
            completed_process = subprocess.run(
                ["python", absolute_full_path],
                text=True,
                timeout=30,
                capture_output=True,
            )
    except Exception as exception:
        return f"Error: executing Python file: {exception}"
    result = f'STDOUT: {completed_process.stdout}, STDERR: {completed_process.stderr}. The "completed_process" object has a stdout and stderr attribute.'
    if completed_process.returncode != 0:
        result += f"Process exited with code {completed_process.returncode}"
    if not completed_process.stdout:
        result += " No output produced."
    return result


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes python file within the working directory and return the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
