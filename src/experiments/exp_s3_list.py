'''
Sample module that ask for the bucket to open
and get the list of all object in the bucket chosen.
'''
from rich import print as rprint

from src.arguments_loader import ArgumentsLoader as Loader

def main() -> None:
    '''Main entry point of the script'''

    rprint("Usage:\n")
    rprint("py ./src/experiments/exp_s3_list.py\n")
    rprint("- It asks for s3 connection parameters (if not provided in environment variables)")
    rprint("- You can chose from a list of available buchets")
    rprint("- It prints a JSon with all the data contained in the bucket \n")

    loader = Loader()
    s3 = loader.s3
    if s3.s3_client is None:
        rprint('Error: S3 client is not initialized')
        return

    selected_bucket = loader.get_bucket()
    if selected_bucket is None:
        rprint('No buckets found')
        return

    rprint(s3.list_files(selected_bucket))

if __name__ == "__main__":
    main()
