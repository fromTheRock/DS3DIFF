from rich import print as rprint

from src.files.s3_ops import S3Ops
from src.config import Config


def main() -> None:
    '''Main entry point of the script'''

    cfg = Config()
    s3 = S3Ops(cfg)
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
