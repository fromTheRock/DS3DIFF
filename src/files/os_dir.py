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
    return FileMetadata(file_path, file_name, file_stats.st_size,
                        file_stats.st_ctime, file_stats.st_mtime)


def extract_file_data(path: str, list_files: list, deph: int) -> list[FileMetadata]:
    '''Returns a list of files in JSon format
    '''
    _file_metadata = []
    for fl in list_files:
        pathname = os.path.join(path, fl)
        # get file data
        mode = os.lstat(pathname).st_mode

        # If it's a directory, recurse into it
        if S_ISDIR(mode):
            if deph > 0:
                _file_metadata.append(extract_file_data(pathname, os.listdir(pathname), deph - 1))
            continue
        # If it's a regular file...
        if S_ISREG(mode):
            #f_stat = os.stat(pathname)
            _file_metadata.append(get_file_data(pathname))

    return _file_metadata

def check_and_delete(path: str) -> bool:
    '''
    Delete a file from the file system if it exists.
    
    Args:
        path (str): The path to the file to delete
        
    Returns:
        bool: True if file was deleted, False if file did not exist
    '''
    try:
        if os.path.exists(path):
            os.remove(path)
            return True
        return False
    except OSError:
        return False