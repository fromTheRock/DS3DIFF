import os
import sys
import datetime
from stat import *
        
class FileData:
    '''Base object representina a filesyssemt object
    '''
    path = ""
    name = ""
    extension = ""
    size = 0
    creationDate = None
    lastModificationDate = None
    def __init__(self, path: str, name: str, size: int, creationDate: int, lastModificationDate: int) -> None:
        self.path = path
        self.name = name
        _, file_extension = os.path.splitext(name)
        self.extension =  file_extension[1:] if file_extension else ""
        self.size = size
        self.creationDate = datetime.datetime.fromtimestamp(creationDate, tz=datetime.timezone.utc)
        self.lastModificationDate = datetime.datetime.fromtimestamp(lastModificationDate, tz=datetime.timezone.utc)

    def getSize(self) -> str:
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
        #return f"Path: {self.path}, Name: {self.name}, Extension: {self.extension}, Size: {self.size}, Creation Date: {self.creationDate}, Last Modification Date: {self.lastModificationDate}"
        return f"{self.path}, Size: {self.getSize()}, Creation Date: {self.creationDate}, Last Modification Date: {self.lastModificationDate}"


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

def extractFileData(path: str, listFiles: list) -> list:
    filesJson = []
    for file in listFiles:
        pathname = os.path.join(path, file)
        # get file data
        mode = os.lstat(pathname).st_mode

        # If it's a directory, recurse into it
        if S_ISDIR(mode):
            continue
        # If it's a regular file...
        elif S_ISREG(mode):
            fStat = os.stat(pathname)
            filesJson.append(FileData(os.path.join(path,file), file, fStat.st_size, fStat.st_birthtime, fStat.st_mtime))

    return filesJson


def main() -> list:
    # sys.argv[0] is the script name
    # sys.argv[1:] contains the arguments
    if len(sys.argv) < 2:
        print("Argument required:")
        print(f"{sys.argv[0]} <PATH TO LIST>")
        return

    path = sys.argv[1]

    listFiles = os.listdir(path)

    filesJson = extractFileData(path, listFiles)

    return filesJson

if __name__ == "__main__":
    
    filesJson = main()

    for f in filesJson:
        print (f)
