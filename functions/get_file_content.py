import os 
from config import MAX_CHARS
import google.genai.types as types
def get_file_content(working_directory, file_path):
    working_dir_path = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_dir_path, file_path))
    valid_target_file = os.path.commonpath([working_dir_path, target_file_path]) == working_dir_path
    if not valid_target_file:
        err = Exception(f'Error: Cannot list "{file_path}" as it is outside the permitted working directory')
        return str(err)
    if not os.path.isfile(target_file_path):
        err = Exception(f'Error: File not found or is not a regular file: "{file_path}"')
        return str(err)
    with open(target_file_path, 'r') as file:
        try:
            content = file.read(MAX_CHARS)
            if file.read(1):
                content+= f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        except Exception as err:
            error = "Error: " + str(err)
            return error
    return content

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specified file relative to the working directory, with a maximum character limit to prevent excessive output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read content from, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)