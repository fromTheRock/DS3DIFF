'''
Utility Module to scan directories on local file system.
'''
import os
from stat import S_ISDIR, S_ISREG

from src.files.file_metadata import FileMetadata

def get_file_data(path: str) -> FileMetadata:
    '''
    Get file data from the file system.

    Args:
        path (str): The path to the file

    Returns:
        FileMetadata: The file data object
    '''
    file_stats = os.stat(path)
    file_name = os.path.basename(path)
    file_path = os.path.dirname(path)
    return FileMetadata(file_path, file_name, file_stats.st_size, file_stats.st_ctime, file_stats.st_mtime)


def extract_file_data(path: str, list_files: list, deph: int) -> list:
    '''Returns a list of files in JSon format
    '''
    f_json = []
    for fl in list_files:
        pathname = os.path.join(path, fl)
        # get file data
        mode = os.lstat(pathname).st_mode

        # If it's a directory, recurse into it
        if S_ISDIR(mode):
            if deph > 0:
                f_json.append(extract_file_data(pathname, os.listdir(pathname), deph - 1))
            continue
        # If it's a regular file...
        if S_ISREG(mode):
            #f_stat = os.stat(pathname)
            f_json.append(get_file_data(pathname))

    return f_json
