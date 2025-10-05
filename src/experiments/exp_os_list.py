'''
Module to work with files in filesytem folders
'''
import os

from rich.console import Console

from src.arguments_loader import ArgumentQuestion
from src.arguments_loader import ArgumentsLoader
from src.files.os_dir import extract_file_data

LIST_FOLDER = "LIST_FOLDER"
con = Console()



def main() -> list:
    '''Prints a list of files in directory received as argument
    '''

    con.clear()

    #Asks for the path to list without loading the S3 objects
    loader = ArgumentsLoader()
    _question = [ ArgumentQuestion("Root Path to scan:", LIST_FOLDER) ]
    args = loader.get_arguments(_question)

    path = args[LIST_FOLDER]

    list_files = os.listdir(path)

    f_json = extract_file_data(path, list_files, 0)

    return f_json

if __name__ == "__main__":
    files_json = main()

    if files_json is None:
        exit(1)

    for file in files_json:
        con.print(file)
        con.print("\n")
