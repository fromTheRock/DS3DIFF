"""Entry Point of the application:
- Asks for a S3 Bucketn (the S3 EntryPoint is stored in a environment variable)
- Asks for a local folder path
- Do comparation and shows the different files.
TODO:
- Add a easy way to merge different files
"""

from pathlib import Path
from rich.console import Console

from src.files.s3_ops import S3Ops
from src.config import Config

from src.arguments_loader import ArgumentsLoader as Loader
from src.arguments_loader import ArgumentQuestion

# constants
OS_FOLDER = "LOCAL_FOLDER"
S3_FOLDER = "S3_PREFIX"

# Initialize global variables
dict_os = dict()
s3: S3Ops = None
cfg: Config = None


#def compare_dir(bucket: str, dir: str):
#    """Compare a bucket folder wit ao os folder on the local PC"""
#    dir_s3 = s3.list_file_metadata(bucket)
#
#    # path_os = os.path.join(get_module_path, 'os_fixture')
#    list_files_s3 = os.listdir(dir)
#
#    f_json = os_dir.extract_file_data(dir, list_files_s3, sys.maxsize)
#
#    # Test the os_dir function with the current directory
#    print(f"s3 dir: {dir_s3}")
#    print(f"os dir: {f_json}")
#
#    for file in f_json:
#        print(f"os file: {file}")
#
#        file_s3 = list_files_s3[file]
#        print(f"s3 file: {file_s3}")


# def cb_add_files(pathname: str):
#    file_metadata = os_dir.get_file_data(pathname)
#
#    file_metadata.etag = s3_ops.calculate_s3_etag(pathname)
#    os_dic[pathname] = file_metadata
#    print (f"pathname: {pathname}")


def main():
    """Main entry point of the script"""
    loader = Loader()
    questions = [
        ArgumentQuestion("Directory?", OS_FOLDER),
        ArgumentQuestion("S3 root path?", S3_FOLDER),
    ]

    selected_bucket = loader.get_bucket()
    if selected_bucket is None:
        print("No buckets found")
        return
    args = loader.get_arguments(questions)

    if args is None:
        print("No arguments provided")
        return
    if args[OS_FOLDER] is None:
        print("No directory to compare")
        return
    if args[S3_FOLDER] is None:
        reply = input("No S3 written. Should I use the same local directory?")
        if reply is None or reply.capitalize() == "N":
            return

    # Convert string to Path object
    os_path = Path(args[OS_FOLDER])

    # For S3 paths (always use forward slashes)
    if args[S3_FOLDER] is None:
        s3_path = Path(os_path).as_posix()
    else:
        s3_path = args[S3_FOLDER]

    output = loader.s3.compare_directory_with_s3_prefix(
        bucket_name=selected_bucket,
        s3_prefix=s3_path,
        local_dir_path=os_path
    )
    con = Console()
    con.print(output)


if __name__ == "__main__":
    main()
