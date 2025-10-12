"""
Pytest Module
Check the comparation between the s3_fixture and s3_fixture
"""
import os
import sys

from src.files.s3_ops import S3Ops
from test_s3_ops import set_aws_credentials, moto_server, s3_client, get_s3_ops
from test_os_dir import get_module_path

import src.files.os_dir as os_dir

def test_compare_file(get_s3_ops: S3Ops, get_module_path: str):
    s3_ops = get_s3_ops

    file_s3 = s3_ops.list_file_metadata("bucket1")['sample-1.txt']
    path_os = os.path.join(get_module_path,
                             'os_fixture/sample-1.txt')
    file_os = os_dir.get_file_data(path_os)

    # Test the os_dir function with the current directory
    print (f"s3 file: {file_s3}")
    print (f"os file: {file_os}")
    assert file_s3 is not None
    assert file_s3.name == file_os.name
    assert file_s3.size == file_os.size
    assert file_s3.last_modification_date >= file_os.last_modification_date
    assert file_s3.etag == s3_ops.calculate_s3_etag(path_os)

def test_compare_dir(get_s3_ops: S3Ops, get_module_path: str):
    s3_ops = get_s3_ops

    bucket = 'bucket1'
    s3_path = ''

    path_os = os.path.join(get_module_path, 'os_fixture')

    res = s3_ops.compare_directory_with_s3_prefix(
        bucket_name=bucket,
        s3_prefix=s3_path,
        local_dir_path=path_os
    )

    assert res is not None
    assert len(res["matching_files"]) == 4
    assert len(res["missing_in_s3"]) == 2 #json/ and sample-8.txt
    assert len(res["missing_locally"]) == 1 #sample-2.txt