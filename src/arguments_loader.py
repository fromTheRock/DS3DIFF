"""
Laucher module.
It asks for inpunt based on s3 buckets, and run some experiment method.
and get the list of all object in the bucket chosen.
"""

import os
from argparse import ArgumentParser
from src.files.s3_ops import S3Ops

# DEFAULT VALUES

# endpoint to access my Buckets
#   s3 - for AWS S3 Buckets;
#   https://s3.cubbit.eu - for Cubbit S3 Archives
# It gives preference to the enARGnt variable S3_ENDPOINT (if exists)
DEFAULT_S3_ENDPOINT: str = "s3"
ARG_S3_ENDPOINT: str = "S3_ENDPOINT"


# Server Region
# It gives preference to the environment variable S3_REGION (if exists)
#   eu-west-1 - for Cubbit S3 Archives
DEFAULT_S3_REGION: str = "eu-central-1"
ARG_S3_REGION: str = "S3_REGION"



class ArgumentQuestion:
    """
    Class to represent a single question or argument to ask.
    It is used to ask for input to the user or read it from environemnt variables.
    """

    def __init__(self, question: str = None, key: str = None, default: any = None, \
                 *, clarg_flag: str = None, clarg_action: str | list[type[str]] = None):
        self.question: str = question
        self.key: str = key
        self.default: any = default
        self.clarg_flag: str | list[type[str]] = clarg_flag
        self.clarg_action: str = clarg_action


class ArgumentsLoader:
    """
    Launcher class to load arguments from varous source (CLI Argument, OS Variable or Default value)
    """

    def __init__(self, *, use_s3: bool = True, questions: list = None, \
                 s3_endpoint: str = None, s3_region: str = None, s3: S3Ops = None):

        self.s3: S3Ops = s3
        self.s3_endpoint: str = s3_endpoint
        self.s3_region: str = s3_region
        self.questions: list = questions if questions is not None else []
        self.arguments: dict = {}

        if use_s3:
            if s3 is not None:
                self.s3 = s3
                self.s3_endpoint = s3.s3_endpoint
                self.s3_region = s3.s3_region

            #Step 2: Load argument to parse command line arguments
            if self.s3_endpoint is None:
                msg = f'Which S3 endpoint do you want to use? (default: {DEFAULT_S3_ENDPOINT}): '
                self.questions.append(
                    ArgumentQuestion(
                        question=msg,
                        key=ARG_S3_ENDPOINT,
                        default=DEFAULT_S3_ENDPOINT,
                        clarg_flag=["-e","--endpoint"]
                        #clarg_action=None
                    )
                )
            if self.s3_region is None:
                self.questions.append(
                    ArgumentQuestion(
                        question=f'Which region do you want to use? (default: {DEFAULT_S3_REGION}): ',
                        key=ARG_S3_REGION,
                        default=DEFAULT_S3_REGION,
                        clarg_flag=["-r", "--region"]
                        #clarg_action=None
                    )
                )

        if self.questions is not None and len(self.questions) > 0:
            self.arguments = self._get_arguments(self.questions)

        #Final chance: Get the S3 data from default constant
        if use_s3:
            if self.s3_endpoint is None:
                self.s3_endpoint = s3_endpoint = self.arguments[ARG_S3_ENDPOINT]
            if self.s3_region is None:
                self.s3_region = s3_region = self.arguments[ARG_S3_REGION]
            print(f'Final Endpoint: {self.s3_endpoint}; Region: {self.s3_region}')

            self.s3 = S3Ops(s3_endpoint, s3_region)

    def get_bucket(self) -> str:
        """
        Scan the available S3 Buckets and asks to the user wich Bucket to use.
        
        :param self: Description
        :return: Name of the selected Bucket
        :rtype: str
        """

        if self.s3 is None:
            print("Error: S3 client is not initialized")
            return
        response = self.s3.list_buckets()

        if response is None:
            answer = input(
                "S3 client is not initialized. Do you want to set the right S3 data?"
            )
            if answer.capitalize() == "Y":
                #self.ask_for_s3_data()
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

    def _get_arguments(self, list_of_args: list) -> dict:
        """
        Get arguments either from the command line, from Environment Variable 
        or ask the input to the user.

        Args:
            list_of_args (list): List of arguments to get

        Returns:
            dict: Dictionary of arguments
        """

        use_argparse = False
        cl_parser = ArgumentParser()
        args = dict()
        for arg in list_of_args:
            if isinstance(arg, ArgumentQuestion):
                if arg.clarg_flag is not None:
                    use_argparse = True
                    if arg.clarg_action is not None:
                        cl_parser.add_argument(*arg.clarg_flag, \
                                            action=arg.clarg_action, required=False)
                    else:
                        cl_parser.add_argument(*arg.clarg_flag, required=False)

        if use_argparse:
            cl_args = cl_parser.parse_args()
            if 'help' in cl_args and cl_args['help'] is not None:
                cl_parser.print_help()
                return None

        for arg in list_of_args:
            if isinstance(arg, ArgumentQuestion):
                #Step 1: find if the argument is passed as command line argument
                if use_argparse:
                    if arg.key and arg.key in args.keys():
                        args[arg.key] = cl_args[arg.key]
                        continue

                #Step 2: use the OS Environment Variable
                _val = os.environ.get(arg.key.upper(), None)
                if _val is not None:
                    print(
                        f"Using environment variable {arg.key.upper()} for {arg.question}: {_val}"
                    )

                #Step 3: ask argument to the user
                if _val is None:
                    #try 3: ask the user for the argument
                    _val = input(
                        f"Enter {arg.question} (default: {arg.default}): "
                    )

                #Step 4: get default
                if _val is None:
                    args[arg.key] = arg.default
                else:
                    args[arg.key] = _val

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
