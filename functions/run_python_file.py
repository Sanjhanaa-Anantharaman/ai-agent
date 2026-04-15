import os
def run_python_file(working_directory, file_path, args=None):
    working_dir_path = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_dir_path, file_path))
    valid_target_file = os.path.commonpath([working_dir_path, target_file_path]) == working_dir_path
    if not valid_target_file:
        err = Exception(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        return str(err)
    if not os.path.isfile(target_file_path):
        err = Exception(f'Error: "{file_path}" does not exist or is not a regular file')
        return str(err)
    if valid_target_file[-1:-4] != '.py':
        err = Exception(f'Error: "{file_path}" is not a Python file')
        return str(err)
    command = ["python", target_file_path]
    if args:
        command.extend(args)
    process = subproces.run(command, capture_output=True, text=True, timeout=30)
    