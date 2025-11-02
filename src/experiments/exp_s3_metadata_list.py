'''
Sample module that ask for the bucket to open
and get the list of all object in the bucket chosen.
'''
from rich import print as rprint

from src.arguments_loader import ArgumentsLoader 
from src.arguments_loader import ArgumentQuestion 

LIST_FOLDER = "LIST_FOLDER"

def main() -> None:
    '''Main entry point of the script'''

    loader = ArgumentsLoader()
    _question = [ ArgumentQuestion("Root Path to scan:", LIST_FOLDER) ]
    args = loader.get_arguments(_question)
    prefix = args[LIST_FOLDER]

    _s3 = loader.s3
    _bucket = loader.get_bucket()

    rprint(_s3.list_file_metadata(_bucket, prefix))

if __name__ == "__main__":
    main()
