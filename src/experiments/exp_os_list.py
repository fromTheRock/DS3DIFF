'''
Module to work with files in filesytem folders
'''
import contextlib
import os

from rich.console import Console
#from rich import inspect

from src.arguments_loader import ArgumentQuestion
from src.arguments_loader import ArgumentsLoader
from src.files.os_dir import extract_file_data
from src.files.os_dir import FileMetadata

LIST_FOLDER = "LIST_FOLDER"
con = Console()



def main() -> list[FileMetadata]:
    '''Prints a list of files in directory received as argument
    '''

    con.clear()

    with contextlib.suppress(KeyboardInterrupt):
        #Asks for the path to list without loading the S3 objects
        _question = [ ArgumentQuestion("Root Path to scan:", LIST_FOLDER) ]
        loader = ArgumentsLoader(questions =_question, use_s3=False)

        path = loader.arguments[LIST_FOLDER]

        list_files = os.listdir(path)

        f_json = extract_file_data(path, list_files, 0)

        return f_json

if __name__ == "__main__":
    files_json = main()

    if files_json is None:
        exit(1)

    for file in files_json:
        con.print(file)
        #inspect(file, methods=False)
        con.print("\n")
