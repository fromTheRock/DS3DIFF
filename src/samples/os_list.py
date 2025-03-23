import os
import sys
import datetime
from stat import S_ISDIR, S_ISREG

class FileData:
    '''Base object representina a filesyssemt object
    '''
    path = ""
    name = ""
    extension = ""
    size = 0
    creation_date = None
    last_modification_date = None

    def __init__(self, path: str, name: str, size: int, 
                 creation_date: int, last_modification_date: int) -> None:
        self.path = path
        self.name = name
        _, file_extension = os.path.splitext(name)
        self.extension =  file_extension[1:] if file_extension else ""
        self.size = size
        self.creation_date = datetime.datetime.fromtimestamp(creation_date, tz=datetime.timezone.utc)
        self.last_modification_date = datetime.datetime.fromtimestamp(last_modification_date, tz=datetime.timezone.utc)

    def get_size(self) -> str:
        if self.size < 1024:
            return f"{self.size} B"
        elif self.size < 1024 * 1024:
            return f"{self.size / 1024:.2f} KB"
        elif self.size < 1024 * 1024 * 1024:
            return f"{self.size / (1024 * 1024):.2f} MB"
        elif self.size < 1024 * 1024 * 1024 * 1024:
            return f"{self.size / (1024 * 1024 * 1024):.2f} GB"
        else:
            return f"{self.size / (1024 * 1024 * 1024 * 1024):.2f} TB"

    def __str__(self):
        #return f"Path: {self.path}, Name: {self.name}, Extension: {self.extension}, Size: {self.size}, Creation Date: {self.creation_date}, Last Modification Date: {self.last_modification_date}"
        return f"{self.path}, Size: {self.get_size()}, Creation Date: {self.creation_date}, Last Modification Date: {self.last_modification_date}"


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
        elif S_ISREG(mode):
            fStat = os.stat(pathname)
            f_json.append(FileData(os.path.join(path,fl),
                        fl, fStat.st_size, 
                        fStat.st_birthtime, fStat.st_mtime))

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
