import boto3
import os
import sys
import S3connectionData as S3connData
from typing import Dict, Any

class S3Ops:
    """Utility class for S3 operations"""

    s3Endpoint: str = None
    s3Region: str = None
    s3Client: boto3.client = None
    s3_bucket_name: str = None

    def __init__(self, endpoint_url: str = None, region: str = None):
        """
        Initialize the S3Ops class.

        Args:
            endpoint_url (str, optional): The S3 endpoint URL. Defaults to None.
        """
        if endpoint_url is None and region is None:
            epnt, reg = self.getConnectionData()
        if endpoint_url is None:
            endpoint_url = self.s3Endpoint = epnt
        if region is None:
            region = reg
        self.s3Endpoint = endpoint_url
        self.s3Region = region

        self.s3Client = self.getS3Client()

    #@classmethod
    #@staticmethod
    def getS3Client(self) -> boto3.client:
        """
        Create and return an S3 client with the endpoint specified in S3Ops object.
            
        Returns:
            boto3.client: Configured S3 client
        """
        if self.s3Endpoint is None:
            self.s3Endpoint = 's3'
            return boto3.client('s3',
                                self.s3Endpoint)
        
        self.s3Client =  boto3.client('s3', 
                                      endpoint_url=self.s3Endpoint, 
                                      region_name=self.s3Region)
        #boto3.client('s3', endpoint_url=self.s3Endpoint)
        return self.s3Client

    def listBuckets(self) -> Any:
        """
        Get list of S3 buckets.
        
        Returns:
            Dict[str, Any]: Response containing bucket information
        """
        if self.s3Client is None:
            return None
        return self.s3Client.list_buckets(BucketRegion=self.s3Region)

    def listFiles(self, bucket_name: str) -> Dict[str, Any]:
        """
        Get list of files in a S3 bucket.

        Args:
            endpoint_url (str): The S3 endpoint URL
            bucket_name (str): The name of the S3 bucket

        Returns:
            Dict[str, Any]: Response containing file information
        """
        #s3_client = cls.getS3Client(endpoint_url)
        if self.s3Client is None:
            return None
        return self.s3Client.list_objects_v2(Bucket=bucket_name)


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

    s3 = S3Ops()
    response = s3.listBuckets()

    #print(response)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print('S3 buckets listed successfully.')
    else:
        print(f'Error: {response["ResponseMetadata"]["HTTPStatusCode"]}')
        return
    print(f'Buckets: {response["Buckets"]}')

if __name__ == "__main__":
    main()
