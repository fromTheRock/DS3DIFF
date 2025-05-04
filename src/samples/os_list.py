'''
Module to work with files in filesytem folders
'''
import os
import sys
from stat import S_ISDIR, S_ISREG
import src.files.os_dir as os_dir

def walktree(top, callback):
    '''recursively descend the directory tree rooted at top,
       calling the callback function for each regular file'''

    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.lstat(pathname).st_mode
        if S_ISDIR(mode):
            # It's a directory, recurse into it
            walktree(pathname, callback)
        elif S_ISREG(mode):
            # It's a file, call the callback function
            callback(pathname)
        else:
            # Unknown file type, print a message
            print('Skipping %s' % pathname)

def extract_file_data(path: str, list_files: list) -> list:
    '''Returna a list of files in JSon format
    '''
    f_json = []
    for fl in list_files:
        pathname = os.path.join(path, fl)
        # get file data
        mode = os.lstat(pathname).st_mode

        # If it's a directory, recurse into it
        if S_ISDIR(mode):
            continue
        # If it's a regular file...
        if S_ISREG(mode):
            #f_stat = os.stat(pathname)
            f_json.append(os_dir.get_file_data(pathname))

    return f_json


def main() -> list:
    '''Prints a list of files in directory received as argument
    '''
    # sys.argv[0] is the script name
    # sys.argv[1:] contains the arguments
    if len(sys.argv) < 2:
        print("Argument required:")
        print(f"{sys.argv[0]} <PATH TO LIST>")
        return None

    path = sys.argv[1]

    list_files = os.listdir(path)

    f_json = extract_file_data(path, list_files)

    return f_json

if __name__ == "__main__":  
    files_json = main()

    for file in files_json:
        print (file)
