'''
Laucher module. 
It asks for inpunt based on s3 buckets, and run some experiment method.
and get the list of all object in the bucket chosen.
'''
import os
from src.config import Config
from src.files.s3_ops import S3Ops

class ArgumentQuestion:

    def __init__(self, _question: str = None, _key: str = None, _default: any = None):
        self.question = _question
        self.key = _key
        self.default = _default

class ArgumentsLoader:
    '''
    Launcher class to run various experiments chooing bucket and objects
    '''
    s3: S3Ops = None

    def __init__(self, _cfg: Config = None, _s3: S3Ops = None):
        if _cfg is None:
            _cfg = Config()
        if _s3 is None and _cfg is not None:
            self.s3 = S3Ops(_cfg)
        else:
            self.s3 = _s3

    def get_bucket(self) -> str:
        '''Main entry point of the script'''

        if self.s3 is None:
            print('Error: S3 client is not initialized')
            return
        response = self.s3.list_buckets()

        if response is None:
            answer = input('S3 client is not initialized. Do you want to set the right S3 data?')
            if answer.capitalize() == 'Y':
                _cfg = self.s3.cfg
                _cfg.ask_for_s3_data()
                self.s3 = S3Ops(_cfg)
                response = self.s3.list_buckets()
            else:
                return None
        
        if response is None:
            return None
        
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print('S3 buckets listed successfully.')
        else:
            print(f'Error: {response["ResponseMetadata"]["HTTPStatusCode"]}')
            return

        bucket_list = self.s3.print_bucket_names(response)
        if bucket_list:
            selected_num = self._get_valid_bucket_number(len(bucket_list))
            selected_bucket = bucket_list[selected_num - 1]['Name']
            print(f"You selected bucket: {selected_bucket}")

            return selected_bucket

        print("No buckets found")
        return None

    def get_arguments(self, list_of_args: list) -> dict:
        '''
        Get arguments from the command line or Environment Variable.

        Args:
            list_of_args (list): List of arguments to get

        Returns:
            dict: Dictionary of arguments
        '''
        args = dict()
        for arg in list_of_args:
            if isinstance(arg, ArgumentQuestion):
                _val = os.environ.get(arg.key.upper(), None)
                if (_val is None):
                    args[arg.key] = input(f'Enter {arg.question} (default: {arg.default}): ')
                else:
                    args[arg.key] = _val
                    print(f'Using environment variable {arg.key.upper()} for {arg.question}: {_val}')
            else:
                args[arg] = input(f'Enter {arg}: ')
        return args

    def _get_valid_bucket_number(self, max_buckets: int) -> int:
        '''
        Get and validate user input for bucket selection.
        
        Args:
            max_buckets (int): Maximum number of buckets to choose from
            
        Returns:
            int: Validated bucket number
        '''
        while True:
            try:
                value = input('Which bucket do you want to list? (Enter a number): ')
                bucket_num = int(value)
                if 1 <= bucket_num <= max_buckets:
                    return bucket_num
                print(f'Please enter a number between 1 and {max_buckets}')
            except ValueError:
                print('Please enter a valid integer')
