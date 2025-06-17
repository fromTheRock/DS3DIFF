'''
Sample module that ask for the bucket to open
and get the list of all object in the bucket chosen.
'''
from rich import print as rprint

from src.config import Config
from src.files.s3_ops import S3Ops
from src.arguments_loader import ArgumentsLoader as Loader

def main() -> None:
    '''Main entry point of the script'''

    cfg = Config()
    s3 = S3Ops(cfg)
    if s3.s3_client is None:
        rprint('Error: S3 client is not initialized')
        return
    loader = Loader(cfg, s3)

    selected_bucket = loader.get_bucket()
    if selected_bucket is None:
        rprint('No buckets found')
        return

    rprint(s3.list_files(selected_bucket))

if __name__ == "__main__":
    main()
