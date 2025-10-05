"""
Laucher module.
It asks for inpunt based on s3 buckets, and run some experiment method.
and get the list of all object in the bucket chosen.
"""

import os
from src.files.s3_ops import S3Ops

# DEFAULT VALUES

# endpoint to access my Buckets
#   s3 - for AWS S3 Buckets;
#   https://s3.cubbit.eu - for Cubbit S3 Archives
# It gives preference to the environment variable S3_ENDPOINT (if exists)
DEFAULT_S3_ENDPOINT: str = "s3"

# Server Region
# It gives preference to the environment variable S3_REGION (if exists)
#   eu-west-1 - for Cubbit S3 Archives
DEFAULT_S3_REGION: str = "eu-central-1"


class ArgumentQuestion:
    """
    Class to represent a single question or argument to ask.
    It is used to ask for input to the user or read it from environemnt variables.
    """

    question: str = None
    key: str = None
    default: any = None

    def __init__(self, _question: str = None, _key: str = None, _default: any = None):
        self.question = _question
        self.key = _key
        self.default = _default


class ArgumentsLoader:
    """
    Launcher class to run various experiments chooing bucket and objects
    """

    s3: S3Ops = None
    s3_endpoint: str = None
    s3_region: str = None

    def __init__(self, *, _s3_endpoint: str = None, _s3_region: str = None, _s3: S3Ops = None):

        #Step 1: Get the S3 data from the environment variables (if not passed as argument)
        if _s3_endpoint is None:
            _s3_endpoint = os.environ.get("S3_ENDPOINT", None)
        if _s3_region is None:
            _s3_region = os.environ.get("S3_REGION", None)
        print(f'Environ Endpoint: {_s3_endpoint}; Region: {_s3_region}')


        #Step 2: Get the S3 data from default variable
        if _s3_endpoint is None:
            _s3_endpoint = DEFAULT_S3_ENDPOINT
        if _s3_region is None:
            _s3_region = DEFAULT_S3_REGION
        self.s3_endpoint = _s3_endpoint
        self.s3_region = _s3_region
        print(f'Final Endpoint: {_s3_endpoint}; Region: {_s3_region}')

        #Step 3: Get the S3 data from the user (if not passed as argument)
        self.ask_for_s3_data(**{"s3_endpoint": _s3_endpoint, "s3_region": _s3_region})

        self.s3 = S3Ops(_s3_endpoint, _s3_region)

    def ask_for_s3_data(self, **s3_args) -> None:
        '''
        Ask the user for S3 data if not provided in the environment variables.
        '''
        if s3_args["s3_region"] is None or s3_args["s3_region"] == DEFAULT_S3_REGION:
            msg = f'Which region do you want to use? (default: {DEFAULT_S3_REGION}): '
            self.s3_region = input(msg)
            if self.s3_region == '':
                self.s3_region = DEFAULT_S3_REGION
        if s3_args["s3_endpoint"] is None or s3_args["s3_endpoint"] == DEFAULT_S3_ENDPOINT:
            msg = f'Which S3 endpoint do you want to use? (default: {DEFAULT_S3_ENDPOINT}): '
            self.s3_endpoint = input(msg)
            if self.s3_endpoint == '':
                self.s3_endpoint = DEFAULT_S3_ENDPOINT

    def get_bucket(self) -> str:
        """Main entry point of the script"""

        if self.s3 is None:
            print("Error: S3 client is not initialized")
            return
        response = self.s3.list_buckets()

        if response is None:
            answer = input(
                "S3 client is not initialized. Do you want to set the right S3 data?"
            )
            if answer.capitalize() == "Y":
                self.ask_for_s3_data()
                self.s3 = S3Ops(self.s3_endpoint, self.s3_region)
                response = self.s3.list_buckets()
            else:
                return None

        if response is None:
            return None

        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            print("S3 buckets listed successfully.")
        else:
            print(f'Error: {response["ResponseMetadata"]["HTTPStatusCode"]}')
            return

        bucket_list = self.s3.print_bucket_names(response)
        if bucket_list:
            selected_num = self._get_valid_bucket_number(len(bucket_list))
            selected_bucket = bucket_list[selected_num - 1]["Name"]
            print(f"You selected bucket: {selected_bucket}")

            return selected_bucket

        print("No buckets found")
        return None

    def get_arguments(self, list_of_args: list) -> dict:
        """
        Get arguments from the command line or Environment Variable.

        Args:
            list_of_args (list): List of arguments to get

        Returns:
            dict: Dictionary of arguments
        """
        args = dict()
        for arg in list_of_args:
            if isinstance(arg, ArgumentQuestion):
                _val = os.environ.get(arg.key.upper(), None)
                if _val is None:
                    args[arg.key] = input(
                        f"Enter {arg.question} (default: {arg.default}): "
                    )
                else:
                    args[arg.key] = _val
                    print(
                        f"Using environment variable {arg.key.upper()} for {arg.question}: {_val}"
                    )
            else:
                args[arg] = input(f"Enter {arg}: ")
        return args

    def _get_valid_bucket_number(self, max_buckets: int) -> int:
        """
        Get and validate user input for bucket selection.

        Args:
            max_buckets (int): Maximum number of buckets to choose from

        Returns:
            int: Validated bucket number
        """
        while True:
            try:
                value = input("Which bucket do you want to list? (Enter a number): ")
                bucket_num = int(value)
                if 1 <= bucket_num <= max_buckets:
                    return bucket_num
                print(f"Please enter a number between 1 and {max_buckets}")
            except ValueError:
                print("Please enter a valid integer")
