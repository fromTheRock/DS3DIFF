"""
Module containing the utility class for working with boto3 S3 funcions

I like have a utility class that work with Config class to use
the right parameters to the boto3 funtions
"""

import datetime
from typing import Dict, Any, Tuple, Optional
from pathlib import Path
import hashlib

import boto3
from botocore.exceptions import ClientError

from src import config
from src.config import Config
from src.files.file_metadata import FileMetadata


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

    def get_s3_client(self) -> boto3.client:
        """
        Create and return an S3 client with the endpoint specified in S3Ops object.

        Returns:
        - boto3.client: Configured S3 client;
        - None: if the client can not connect to the S3 endpoint configured
        """
        if self.cfg is None:
            return boto3.client("s3", config.DEFAULT_S3_ENDPOINT)

        try:
            self.s3_client = boto3.client(
                "s3", endpoint_url=self.cfg.s3_endpoint, region_name=self.cfg.s3_region
            )
            return self.s3_client
        except ClientError as e:
            print(
                f"Error creating S3 client for endpoint {self.cfg.s3_endpoint} and region {self.cfg.s3_region}"
            )
            print(f"  get_s3_client Error: {str(e)}")
            self.s3_client = None
            return None
        except Exception as e:
            print(f"Generic Error creating S3 client: {str(e)}")
            self.s3_client = None
            return None

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
        # return self.s3_client.list_buckets()

    def list_files(self, bucket_name: str) -> Dict[str, Any]:
        """
        Get the data returned by in a S3 bucket.

        Args:
            bucket_name (str): The name of the S3 bucket

        Returns:
            Dict[str, Any]: Response containing file information in AWS format
        """
        # s3_client = cls.get_s3_client(endpoint_url)
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
        bucket_list = buckets["Buckets"]
        print("Available buckets:")
        for i, bucket in enumerate(bucket_list, 1):
            print(f"{i}: {bucket['Name']}")
        return bucket_list

    def _list_file_metadata(
        self, list_objects: Dict[str, Any]
    ) -> Dict[str, FileMetadata]:
        """
        Internal use only. Use list_file_metadata(bucket) instead.
        Returns a dictionary of object file metadata from the output of list_files()
        """
        file_dict = dict()

        for obj in list_objects["Contents"]:
            file_name = obj["Key"]
            file_size = obj["Size"]
            file_last_modified = obj["LastModified"]

            file_metadata = FileMetadata(
                file_name, file_name, file_size, None, file_last_modified
            )
            file_dict[file_name] = file_metadata

            print(file_metadata)

        return file_dict

    def list_file_metadata(self, bucket_name: str) -> Dict[str, FileMetadata]:
        """
        Get the data returned by in a S3 bucket.

        Args:
            bucket_name (str): The name of the S3 bucket

        Returns:
            Dict[str, FileMetadata]: list of objects FileMetadata
        """
        # s3_client = cls.get_s3_client(endpoint_url)
        if self.s3_client is None:
            return None
        list_objects = self.list_files(bucket_name)
        return self._list_file_metadata(list_objects)

    def compare_files_using_etag(
        self, bucket_name: str, s3_key: str, local_file_path: Path
    ) -> Tuple[str, str, bool]:
        """
        Compare a local file with its S3 counterpart using ETags.

        Args:
            bucket_name: Name of the S3 bucket
            s3_key: Key (path) of the S3 object
            local_file_path: Path to the local file

        Returns:
            Tuple containing:
            - S3 object's ETag (without quotes)
            - Local file's calculated MD5 hash
            - Boolean indicating if the files are identical (True) or different (False)
        """
        try:
            # Get S3 object's ETag
            s3_object = self.s3_client.head_object(Bucket=bucket_name, Key=s3_key)
            s3_etag = s3_object["ETag"].strip('"')  # Remove surrounding quotes

            # Calculate MD5 hash of local file
            with open(local_file_path, "rb") as f:
                local_md5 = hashlib.md5(f.read()).hexdigest()

            # Compare ETags (they match if the files are identical)
            files_match = s3_etag == local_md5

            return s3_etag, local_md5, files_match

        except Exception as e:
            raise Exception(f"Error comparing files using ETag: {e}")

    def get_s3_object_info(self, bucket_name: str, s3_key: str) -> dict:
        """
        Get comprehensive information about an S3 object including ETag and LastModified.

        Args:
            bucket_name: Name of the S3 bucket
            s3_key: Key (path) of the S3 object

        Returns:
            Dictionary containing S3 object metadata or None if not found
        """
        try:
            s3_object = self.s3_client.head_object(Bucket=bucket_name, Key=s3_key)
            return {
                "ETag": s3_object["ETag"].strip('"'),
                "LastModified": s3_object["LastModified"],
                "ContentLength": s3_object["ContentLength"],
                "Metadata": s3_object["Metadata"],
                "CustomLastModified": (
                    datetime.datetime.fromisoformat(
                        s3_object["Metadata"]["last-modified"]
                    )
                    if "Metadata" in s3_object
                    and "last-modified" in s3_object["Metadata"]
                    else None
                ),
            }
        except Exception:
            return None

    def get_s3_file_modified_date(
        self, bucket_name: str, s3_key: str
    ) -> Optional[datetime.datetime]:
        """
        Get the last modified date of an S3 object.

        Args:
            bucket_name: Name of the S3 bucket
            s3_key: Key (path) of the S3 object

        Returns:
            The last modified date of the S3 object or None if not found
        """
        try:
            s3_object = self.s3_client.head_object(Bucket=bucket_name, Key=s3_key)

            # Try to get the last modified date from metadata first (our custom field)
            if "Metadata" in s3_object and "last-modified" in s3_object["Metadata"]:
                return datetime.datetime.fromisoformat(
                    s3_object["Metadata"]["last-modified"]
                )

            # Fall back to S3's LastModified
            return s3_object["LastModified"]

        except Exception:
            return None


def main() -> None:
    """Main entry point of the script"""
    cfg = Config()
    s3 = S3Ops(cfg)
    if s3.s3_client is None:
        print("Error: S3 client is not initialized")
        return
    response = s3.list_buckets()

    # print(response)
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        print("S3 buckets listed successfully.")
    else:
        print(f'Error: {response["ResponseMetadata"]["HTTPStatusCode"]}')
        return
    print(f'Buckets: {response["Buckets"]}')


if __name__ == "__main__":
    main()
