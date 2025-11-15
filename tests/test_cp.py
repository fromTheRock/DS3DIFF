"""
Run the tests for upload and downlad using pytest:
    pytest test_cp.py -v
"""
import os
import pytest
from src.files.s3_ops import S3Ops
from test_s3_ops import set_aws_credentials, moto_server, s3_client, get_s3_ops
from test_os_dir import get_module_path

import src.files.os_dir as os_dir

# def test_upload_file (set_aws_credentials, moto_server, s3_client, get_module_path):
#     """
#     Test upload file from os fixture directory to s3 bucket
#     """
#     # Test S3Ops.upload_file()
#     s3_ops = S3Ops(_s3_endpoint = ENV_S3_ENDPOINT, _s3_region = ENV_S3_REGION)

#     # Verify s3 connection
#     assert s3_ops is not None
#     assert s3_ops.s3_client is not None

#     dest = os.path.join(get_module_path, "os_fixture/sample-B.txt")
#     file_dict = s3_client.upload_file("bucket1", "sample-B.txt", dest)

#     print(file_dict)

#     # Verify upload
#     assert file_dict is not None

def test_download_file (get_s3_ops: S3Ops, get_module_path: str):
    """
    Test download file from s3 bucket to os fixture directory
    """
    # Test S3Ops.download_file()
    s3_ops = get_s3_ops

    # Verify s3 connection
    assert s3_ops is not None
    assert s3_ops.s3_client is not None

    dest = os.path.join(get_module_path, "os_fixture/sample-2.txt")
    print (f'  Downloading file to {dest}')
    s3_ops.s3_client.download_file("bucket1", "sample-2.txt", dest)

    # Test the os_dir function with the current directory
    file_md = os_dir.get_file_data(dest) 
    print (f'  File downladed: {file_md}')

    # Verify upload
    assert file_md is not None
    assert file_md.name == "sample-2.txt"

if __name__ == "__main__":
    pytest.main()
