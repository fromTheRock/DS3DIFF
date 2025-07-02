import os
import os_dir

import src.files.os_dir
import src.files.s3_ops
import src.files.file_metadata

from test_s3_ops import set_aws_credentials, moto_server, s3_client, get_s3_ops
from test_os_dir import get_module_path

def test_compare_file(get_s3_ops, get_module_path):
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
