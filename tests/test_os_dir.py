'''
Pytest module
* test the os_dir module 
* use the  os_fixture folder with sample files

import os_dir

def test_os_dir():
' ' '
    ' ' '
    Test the os_dir module
    # Test the os_dir function with the current directory
    assert os_dir.os_dir('.') == os_dir.os.listdir('.')
    '''