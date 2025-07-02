'''
Utility Module to scan directories on local file system.
'''
import os

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
