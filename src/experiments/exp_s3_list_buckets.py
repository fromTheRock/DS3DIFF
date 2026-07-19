from rich import print as rprint

from src.arguments_loader import ArgumentsLoader


def main() -> None:
    '''Main entry point of the script'''

    rprint("Usage:\n")
    rprint("py ./src/experiments/exp_s3_list_buckets.py\n")
    rprint("- It asks for s3 connection parameters (endpoint and region),\n") 
    rprint("  if not provided in environment variable\n")
    rprint("- It prints all the tata returned by [italic]list_buckets[/italic] S3 function \n")

    loader = ArgumentsLoader()
    s3 = loader.s3

    if s3.s3_client is None:
        rprint('Error: S3 client is not initialized')
        return

    response = s3.list_buckets()
    #rprint(response)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        rprint('S3 buckets listed successfully.')
        rprint(f'HTTP Status Code: {response["ResponseMetadata"]["HTTPStatusCode"]}')
        #rprint(f'Request ID: {response["ResponseMetadata"]["RequestId"]}')
        rprint(f'HTTP Headers: {response["ResponseMetadata"]["HTTPHeaders"]}')
        rprint(f'Retry Attempts: {response["ResponseMetadata"]["RetryAttempts"]}')
        rprint(f'Bucket Owner: {response["Owner"]["DisplayName"]}')
        rprint(f'Bucket Owner ID: {response["Owner"]["ID"]}')
        #rprint(f'Bucket Owner Type: {response["Owner"]["Type"]}')
        rprint(f'Bucket Owner Display Name: {response["Owner"]["DisplayName"]}')
    else:
        rprint(f'Error: {response["ResponseMetadata"]["HTTPStatusCode"]}')
        return

    rprint("Final Result:")
    rprint(f'Buckets: {response["Buckets"]}')

if __name__ == "__main__":
    main()
