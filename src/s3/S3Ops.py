import boto3
import os
import sys
import S3connectionData as S3connData
from typing import Dict, Any

class S3Ops:
    """Utility class for S3 operations"""

    @staticmethod
    def getS3Client(endpoint_url: str) -> boto3.client:
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

    @staticmethod
    def listBuckets(cls, endpoint_url: str, region: str) -> Any:
        """
        Get list of S3 buckets.
        
        Args:
            endpoint_url (str): The S3 endpoint URL
            
        Returns:
            Dict[str, Any]: Response containing bucket information
        """
        #s3_client = cls.getS3Client(endpoint_url)
        return cls.list_buckets(BucketRegion=region)

    #@classmethod
    @staticmethod
    def listFiles(cls, endpoint_url: str, bucket_name: str) -> Dict[str, Any]:
        """
        Get list of files in a S3 bucket.

        Args:
            endpoint_url (str): The S3 endpoint URL
            bucket_name (str): The name of the S3 bucket

        Returns:
            Dict[str, Any]: Response containing file information
        """
        #s3_client = cls.getS3Client(endpoint_url)
        return cls.list_objects_v2(Bucket=bucket_name)


    @staticmethod
    def getValidBucketNumber(max_buckets: int) -> int:
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

    @staticmethod
    def printBucketNames(buckets: Dict[str, Any]) -> None:
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

    @staticmethod
    def getConnectionData() -> tuple[str, str]:
        """
        Get connection data from environment variables.

        Returns:
            tuple[str, str]: the connection data: Endpoint, Region
        """
        cdEndPnt = S3connData.endpoint
        cdRegion = S3connData.region
        cdEndPnt = os.environ.get("S3_ENDPOINT", cdEndPnt)
        cdRegion = os.environ.get("S3_REGION", cdRegion)

        return cdEndPnt, cdRegion

def main() -> None:
    """Main entry point of the script"""
    endpoint, region = S3Ops.getConnectionData()
    client = S3Ops.getS3Client(endpoint)
    response = S3Ops.listBuckets(client, endpoint, region)
    #print(response)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print('S3 buckets listed successfully.')
    else:
        print(f'Error: {response["ResponseMetadata"]["HTTPStatusCode"]}')
        return
    print(f'Buckets: {response["Buckets"]}')

if __name__ == "__main__":
    main()
