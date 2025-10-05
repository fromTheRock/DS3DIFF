'''Prints a S3 object metadata
'''
from rich import inspect

from src.files.s3_ops import S3Ops
from src.arguments_loader import ArgumentQuestion as Question
from src.arguments_loader import ArgumentsLoader as Loader

OBJ_SELECTED = "S3_OBJECT"
questions = list()
questions.append(Question("Object to read?", OBJ_SELECTED))

def main() -> None:
    '''Main entry point of the script
    '''

    loader = Loader()
    s3 = loader.s3
    if s3.s3_client is None:
        print('Error: S3 client is not initialized')
        return

    selected_bucket = loader.get_bucket()
    if selected_bucket is None:
        print('No buckets found')
        return
    args = loader.get_arguments(questions)
    selected_file = args[OBJ_SELECTED]


    metadata = s3.get_s3_object_info(bucket_name=selected_bucket, s3_key=selected_file)
    print(f'Bucket: {selected_bucket}, file: {selected_file}')
    print(f'File Metadata: {metadata}')
    inspect(metadata, methods=True)

if __name__ == "__main__":
    main()
    