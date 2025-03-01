import boto3
import os
import sys
from typing import Dict, Any

class S3Ops:
    """Utility class for S3 operations"""

    @staticmethod
    def get_s3_client(endpoint_url: str) -> boto3.client:
        """
        Create and return an S3 client with the specified endpoint.
        
        Args:
            endpoint_url (str): The S3 endpoint URL
            
        Returns:
            boto3.client: Configured S3 client
        """
        if endpoint_url is None:
            return boto3.client('s3')
        return boto3.client('s3', endpoint_url=endpoint_url)

    @classmethod
    def list_buckets(cls, endpoint_url: str) -> Any:
        """
        Get list of S3 buckets.
        
        Args:
            endpoint_url (str): The S3 endpoint URL
            
        Returns:
            Dict[str, Any]: Response containing bucket information
        """
        s3_client = cls.get_s3_client(endpoint_url)
        return s3_client.list_buckets()

    @classmethod
    def list_files(cls, endpoint_url: str, bucket_name: str) -> Dict[str, Any]:
        """
        Get list of files in a S3 bucket.

        Args:
            endpoint_url (str): The S3 endpoint URL
            bucket_name (str): The name of the S3 bucket

        Returns:
            Dict[str, Any]: Response containing file information
        """
        s3_client = cls.get_s3_client(endpoint_url)
        return s3_client.list_objects_v2(Bucket=bucket_name)


def get_valid_bucket_number(max_buckets: int) -> int:
    """
    Get and validate user input for bucket selection.
    
    Args:
        max_buckets (int): Maximum number of buckets to choose from
        
    Returns:
        int: Validated bucket number
    """
    while True:
        try:
            value = input('Which bucket do you want to list? (Enter a number): ')
            bucket_num = int(value)
            if 1 <= bucket_num <= max_buckets:
                return bucket_num
            else:
                print(f'Please enter a number between 1 and {max_buckets}')
        except ValueError:
            print('Please enter a valid integer')

def print_bucket_names(buckets: Dict[str, Any]) -> None:
    """
    Print the names of S3 buckets with numbers.
    
    Args:
        buckets (Dict[str, Any]): Dictionary containing bucket information
    Returns:
        list: List of bucket names
    """
    bucket_list = buckets['Buckets']
    print('Available buckets:')
    for i, bucket in enumerate(bucket_list, 1):
        print(f"{i}: {bucket['Name']}")
    return bucket_list

def main() -> None:
    """Main entry point of the script"""
    endpoint = os.environ.get("S3_ENDPOINT", "")
    response = S3Ops.list_buckets(endpoint)
    #print(response)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print('S3 buckets listed successfully.')
        print(f'HTTP Status Code: {response["ResponseMetadata"]["HTTPStatusCode"]}')
        print(f'Request ID: {response["ResponseMetadata"]["RequestId"]}')
        print(f'HTTP Headers: {response["ResponseMetadata"]["HTTPHeaders"]}')
        print(f'Retry Attempts: {response["ResponseMetadata"]["RetryAttempts"]}')
        print(f'Bucket Owner: {response["Owner"]["DisplayName"]}')
        print(f'Bucket Owner ID: {response["Owner"]["ID"]}')
        print(f'Bucket Owner Type: {response["Owner"]["Type"]}')
        print(f'Bucket Owner Display Name: {response["Owner"]["DisplayName"]}')
    else:
        print(f'Error: {response["ResponseMetadata"]["HTTPStatusCode"]}')
        return
    
    bucket_list = print_bucket_names(response)
    if bucket_list:
        selected_num = get_valid_bucket_number(len(bucket_list))
        selected_bucket = bucket_list[selected_num - 1]['Name']
        print(f"You selected bucket: {selected_bucket}")
        
        print(bucket_list(response, selected_bucket))
    else:
        print("No buckets found")

if __name__ == "__main__":
    main()
