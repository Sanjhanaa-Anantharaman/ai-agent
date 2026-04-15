import os
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
    