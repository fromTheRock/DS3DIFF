'''Prints a S3 object metadata
'''
import sys

from src.config import Config
from src.files.s3_ops import S3Ops


def main(selected_bucket: str, selected_file: str) -> None:
    '''Main entry point of the script
    '''

    cfg = Config()
    s3 = S3Ops(cfg)
    if s3.s3_client is None:
        print('Error: S3 client is not initialized')
        return

    metadata = s3.get_s3_object_info(bucket_name=selected_bucket, s3_key=selected_file)
    print(f'Bucket: {selected_bucket}, file: {selected_file}')
    print(f'File Metadata: {metadata}')

if __name__ == "__main__":
    # sys.argv[0] is the script name
    # sys.argv[1:] contains the arguments
    if len(sys.argv) < 3:
        print("Argument required:")
        print(f"{sys.argv[0]} <bucket> <file s3 key>")
    else:
        selected_bucket = sys.argv[1]
        print(f"You selected bucket: {selected_bucket}")

        selected_file = sys.argv[2]
        print(f"You selected file: {selected_file}")

        main(selected_bucket, selected_file)
