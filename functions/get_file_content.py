import os 
from config import MAX_CHARS
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