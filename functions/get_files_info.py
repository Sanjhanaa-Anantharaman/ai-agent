import os
import google.genai.types as types
def get_files_info(working_directory, directory="."):
    working_dir_path = os.path.abspath(working_directory)
    target_dir_path = os.path.normpath(os.path.join(working_dir_path, directory))
    valid_target_dir = os.path.commonpath([working_dir_path, target_dir_path]) == working_dir_path
    if not valid_target_dir:
        err = Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        return str(err)
    if not os.path.isdir(target_dir_path):
        err = Exception(f'Error: {directory} is not a directory')
        return str(err)
    list_of_files = os.listdir(target_dir_path)
    result = []
    for file in list_of_files:
        try: 
            file_size = os.path.getsize(os.path.join(target_dir_path, file))
            is_dir = os.path.isdir(os.path.join(target_dir_path, file)) 
            result.append(f"- {file}: file_size={file_size} bytes, is_dir={is_dir}")
        except Exception as err:
            error = "Error: " + str(err)
            return error
    return "\n".join(result)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)