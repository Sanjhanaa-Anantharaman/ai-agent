import subprocess
import os
import google.genai.types as types
def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_path, file_path))
        valid_target_file = os.path.commonpath([working_dir_path, target_file_path]) == working_dir_path
        if not valid_target_file:
            err = Exception(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
            return str(err)
        if not os.path.isfile(target_file_path):
            err = Exception(f'Error: "{file_path}" does not exist or is not a regular file')
            return str(err)
        if not target_file_path.endswith(".py"):
            err = Exception(f'Error: "{file_path}" is not a Python file')
            return str(err)
        command = ["python", target_file_path]
        if args:
            command.extend(args)
        process = subprocess.run(command, capture_output=True, text=True, timeout=30, cwd=working_dir_path)
        res = ''
        if process.returncode != 0:
            res += f"STDOUT: {process.stdout.strip()}\nSTDERR: {process.stderr.strip()}\n"   
            res += f"Process exited with code {process.returncode}"
        elif not process.stdout and not process.stderr:
            res += "No output produced"
        else:
            res += f"STDOUT: {process.stdout.strip()}\nSTDERR: {process.stderr.strip()}"   
        return res.strip()
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file relative to the working directory with optional command-line arguments, capturing and returning the output or any errors that occur during execution",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the Python file during execution",
            ),
        },
        required=["file_path", "args"],
    ),
)