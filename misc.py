import os

def delete_file_if_exists(file_name):
    """
    Deletes a file if it exists.

    :param file_name: The path to the file to be deleted.
    """
    # Checks if the file exists at the specified path
    if os.path.exists(file_name):
        # Removes the file
        os.remove(file_name)
        # Informs the user that the file was successfully deleted
        print(f"{file_name} has been deleted.")
    else:
        # Informs the user that the file does not exist
        print(f"The file {file_name} does not exist.")
