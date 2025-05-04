'''
Pytest module
* test the os_dir module 
* use the  os_fixture folder with sample files
'''
import os
import pytest
import src.files.os_dir as os_dir

@pytest.fixture(scope="function")
def get_module_path():
    '''
    Get the path of the current module
    '''
    yield os.path.dirname(os.path.abspath(__file__))


def test_os_dir(get_module_path):
    '''
    Test the os_dir module
    '''
    print (f'  Module Path {get_module_path}')
    filepath1 = os.path.join(get_module_path, 'os_fixture/sample-1.txt')
    print (f'  File Path 1 {filepath1}')
    # Test the os_dir function with the current directory
    assert os_dir.get_file_data(filepath1) is not None
    assert os_dir.get_file_data(filepath1).get_size() == "1.12 KB"
