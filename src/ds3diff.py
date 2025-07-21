""" Entry Point of the application:
- Asks for a S3 Bucketn (the S3 EntryPoint is stored in a environment variable)
- Asks for a local folder path
- Do comparation and shows the different files.
TODO: 
- Add a easy way to merge different files
"""

from src.files.s3_ops import S3Ops
from src.config import Config
import src.files.file_metadata

from src.arguments_loader import ArgumentsLoader as Loader
from src.arguments_loader import ArgumentQuestion

FOLDER = "ROOT_FOLDER"
dict_os = dict()

def test_compare_dir():
    s3_ops = get_s3_ops

    os_dic = dict()

    dir_s3 = s3_ops.list_file_metadata("bucket1")
    s3_data = os.path.join(get_module_path,
                             'os_fixture')
    os_dir.walktree(path_os, cb_add_files, 0)


    # Test the os_dir function with the current directory
    print (f"s3 dir: {dir_s3}")
    print (f"os dir: {dir_os}")
    assert len(os_dic) == len(dir_s3)

    for key in os_dic:
        file_s3 = dir_s3[key]
        file_os = os_dic[key]
        print (f"s3 file: {file_s3}")
        print (f"os file: {file_os}")
        assert file_s3 is not None
        assert file_s3.name == file_os.name
        assert file_s3.size == file_os.size
        assert file_s3.last_modification_date >= file_os.last_modification_date
        assert file_s3.etag == file_os.etag

def cb_add_files(pathname: str):
    file_metadata = os_dir.get_file_data(pathname)
    
    file_metadata.etag = s3_ops.calculate_s3_etag(pathname)
    os_dic[pathname] = file_metadata
    print (f"pathname: {pathname}")

def main():
    '''Main entry point of the script
    '''

    cfg = Config()
    s3 = S3Ops(cfg)
    if s3.s3_client is None:
        print('Error: S3 client is not initialized')
        return

    loader = Loader(cfg, s3)
    questions = [
        ArgumentQuestion("Directory?", FOLDER)
    ]

    selected_bucket = loader.get_bucket()
    if selected_bucket is None:
        print('No buckets found')
        return
    args = loader.get_arguments(questions)
    #dir = args[FOLDER]

if __name__ == "__main__":
    main()