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

    _question = [ ArgumentQuestion("Root Bucket Path to scan:", LIST_FOLDER) ]
    loader = ArgumentsLoader(questions =_question)
    _s3 = loader.s3
    if _s3.s3_client is None:
        print('Error: S3 client is not initialized')
        return
    _prefix = loader.arguments[LIST_FOLDER]
    _bucket = loader.get_bucket()

    rprint(_s3.list_file_metadata(_bucket, _prefix))

if __name__ == "__main__":
    main()
