import os
import google.genai.types as types
def write_file(working_directory, file_path, content):
    working_dir_path = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_dir_path, file_path))
    valid_target_file = os.path.commonpath([working_dir_path, target_file_path]) == working_dir_path
    if not valid_target_file:
        err = Exception(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        return str(err)
    if os.path.isdir(target_file_path):
        err = Exception(f'Error: Cannot write to "{file_path}" as it is a directory')
        return str(err)
    os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
    try:
        with open(target_file_path, 'w') as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as err:
        error = "Error: " + str(err)
        return error

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes specified content to a file at a given path relative to the working directory, creating any necessary directories and ensuring the target path is valid and not a directory itself",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write content to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the specified file",
            ),
        },
        required=["file_path", "content"],
    ),
)