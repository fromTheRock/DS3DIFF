"""
Module containing the utility class for working with boto3 S3 funcions

I like have a utility class that work with Config class to use 
the right parameters to the boto3 funtions
"""
from typing import Dict, Any
import boto3
from src.config import Config

class S3Ops:
    """Utility class for S3 operations"""

    cfg: Config = None
    s3_client: boto3.client = None
    s3_bucket_name: str = None

    def __init__(self, _cfg: Config):
        """
        Initialize the S3Ops class.

        Args:
            endpoint_url (str, optional): The S3 endpoint URL. Defaults to None.
        """
        self.cfg = _cfg
        self.s3_client = self.get_s3_client()

    #@classmethod
    #@staticmethod
    def get_s3_client(self) -> boto3.client:
        """
        Create and return an S3 client with the endpoint specified in S3Ops object.
            
        Returns:
            boto3.client: Configured S3 client
        """
        if self.cfg is None:
            return boto3.client('s3', 's3')
        self.s3_client =  boto3.client('s3',
                                      endpoint_url=self.cfg.s3_endpoint,
                                      region_name=self.cfg.s3_region)
        return self.s3_client

    def list_buckets(self) -> Any:
        """
        Get list of S3 buckets. 
        
        Returns:
            Dict[str, Any]: Response containing bucket information
        """
        if self.s3_client is None:
            return None
        _region = self.cfg.s3_region
        return self.s3_client.list_buckets(BucketRegion=_region)
        #return self.s3_client.list_buckets()

    def list_files(self, bucket_name: str) -> Dict[str, Any]:
        """
        Get list of files in a S3 bucket.

        Args:
            endpoint_url (str): The S3 endpoint URL
            bucket_name (str): The name of the S3 bucket

        Returns:
            Dict[str, Any]: Response containing file information
        """
        #s3_client = cls.get_s3_client(endpoint_url)
        if self.s3_client is None:
            return None
        return self.s3_client.list_objects_v2(Bucket=bucket_name)


    @staticmethod
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
    cfg = Config()
    s3 = S3Ops(cfg)
    response = s3.list_buckets()

    #print(response)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print('S3 buckets listed successfully.')
    else:
        print(f'Error: {response["ResponseMetadata"]["HTTPStatusCode"]}')
        return
    print(f'Buckets: {response["Buckets"]}')

if __name__ == "__main__":
    main()
