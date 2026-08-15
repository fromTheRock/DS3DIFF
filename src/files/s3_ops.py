"""
Module containing the utility class for working with boto3 S3 funcions

I like have a utility class that work with Config class to use
the right parameters to the boto3 funtions
"""

from typing import Dict, Any, Tuple, List
import hashlib
import os

import boto3
from botocore.exceptions import ClientError

from src.files.file_metadata import DifferentFileMetadata, FileMetadata
class S3Ops:
    """Utility class for S3 operations"""

    def __init__(self, _s3_endpoint: str, _s3_region: str):
        """
        Initialize the S3Ops class.

        Args:
            _s3_endpoint (str): The S3 endpoint URL. Defaults to None.
            _s3_region (str): The S3 region of the server.

        """
        self.s3_bucket_name: str = None

        self.s3_endpoint: str = _s3_endpoint
        self.s3_region: str = _s3_region

        self.s3_client: boto3.client = self.get_s3_client()

    def get_s3_client(self) -> boto3.client:
        """
        Create and return an S3 client with the endpoint specified in S3Ops object.

        Returns:
        - boto3.client: Configured S3 client;
        - None: if the client can not connect to the S3 endpoint configured
        """
        try:
            self.s3_client = boto3.client(
                "s3", endpoint_url=self.s3_endpoint, region_name=self.s3_region
            )
            return self.s3_client
        except ClientError as e:
            print(
                f'''Error creating S3 client for endpoint {self.s3_endpoint} \
                    and region {self.s3_region}'''
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
        _region = self.s3_region
        return self.s3_client.list_buckets(BucketRegion=_region)
        # return self.s3_client.list_buckets()

    #TODO: Add list_files with paginator:
    #paginator = self.s3_client.get_paginator("list_objects_v2")
    #for page in paginator.paginate(Bucket=bucket_name, Prefix=s3_prefix):
    #    if "Contents" in page:
    #        for obj in page["Contents"]:
    #            key = obj["Key"]
    #            # Skip "directory" objects (empty objects with trailing slash)
    #            if not key.endswith("/"):
    #                s3_objects[key] = obj["ETag"].strip('"')
    def list_files(self, _bucket_name: str, _prefix: str | None = None) -> Dict[str, Any]:
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
        if _prefix is None:
            return self.s3_client.list_objects_v2(Bucket=_bucket_name)
        return self.s3_client.list_objects_v2(Bucket=_bucket_name, Prefix=_prefix)

    @staticmethod
    def print_bucket_names(_buckets: Dict[str, Any]) -> None:
        """
        Print the names of S3 buckets with numbers.

        Args:
            buckets (Dict[str, Any]): Dictionary containing bucket information
        Returns:
            list: List of bucket names
        """
        bucket_list = _buckets["Buckets"]
        print("Available buckets:")
        for i, bucket in enumerate(bucket_list, 1):
            print(f"{i}: {bucket['Name']}")
        return bucket_list

    def _list_file_metadata(
        self, _list_objects: Dict[str, Any]) -> Dict[str, FileMetadata]:
        """
        Internal use only. Use list_file_metadata(bucket) instead.
        Returns a dictionary of object file metadata from the output of list_files()
        """
        file_dict = dict()

        if "Contents" not in _list_objects:
            return file_dict
        for obj in _list_objects["Contents"]:
            file_name = obj["Key"]
            file_size = obj["Size"]
            file_last_modified = obj["LastModified"]
            file_tag = obj["ETag"].strip('"')

            file_metadata = FileMetadata(
                file_name, file_name, file_size, None, file_last_modified, file_tag
            )
            file_dict[file_name] = file_metadata

            #Debug print generate confusing list
            #print(file_metadata)

        return file_dict

    def list_file_metadata(self, _bucket_name: str,
                           _prefix: str | None = None) -> Dict[str, FileMetadata]:
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
        list_objects = self.list_files(_bucket_name, _prefix)
        return self._list_file_metadata(list_objects)

    def get_s3_object_info(self, _bucket_name: str, _s3_key: str) -> dict:
        """
        Get comprehensive information about an S3 object including ETag and LastModified.

        Args:
            bucket_name: Name of the S3 bucket
            s3_key: Key (path) of the S3 object

        Returns:
            Dictionary containing S3 object metadata or None if not found
        """
        try:
            s3_object = self.s3_client.head_object(Bucket=_bucket_name, Key=_s3_key)
            return {
                "ETag": s3_object["ETag"].strip('"'),
                "LastModified": s3_object["LastModified"],
                "ContentLength": s3_object["ContentLength"],
                "Metadata": s3_object["Metadata"],
                # Real files in a DS3 buckets does not have CustomLastModified
                # "CustomLastModified": (
                #     datetime.datetime.fromisoformat(
                #         s3_object["Metadata"]["last-modified"]
                #     )
                #     if "Metadata" in s3_object
                #     and "last-modified" in s3_object["Metadata"]
                #     else None
                # ),
            }
        except Exception:
            return None

    def calculate_s3_etag(
        self, _file_path: str, _chunk_size: int = 8 * 1024 * 1024
    ) -> str:
        """
        Calculate the S3 ETag for a file, supporting both single-part and multipart uploads.

        Args:
            file_path: Path to the local file
            chunk_size: Size of each chunk in bytes (default: 8MB, S3's default chunk size)

        Returns:
            The calculated ETag string (without quotes)
        """
        file_size = os.path.getsize(_file_path)

        # For small files (single part), just return the MD5
        if file_size <= _chunk_size:
            with open(_file_path, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()

        # For multipart uploads
        md5s: List[bytes] = []
        with open(_file_path, "rb") as f:
            while True:
                data = f.read(_chunk_size)
                if not data:
                    break
                md5s.append(hashlib.md5(data).digest())

        # Combine the MD5 hashes and add the number of parts
        combined_md5 = hashlib.md5(b"".join(md5s)).hexdigest()
        part_count = len(md5s)

        return f"{combined_md5}-{part_count}"

    def compare_files_using_etag(
        self,
        _bucket_name: str,
        _s3_key: str,
        _local_file_path: str,
        _chunk_size: int = 8 * 1024 * 1024,
    ) -> Tuple[str, str, bool]:
        """
        Compare a local file with its S3 counterpart using ETags, supporting multipart uploads.

        Args:
            bucket_name: Name of the S3 bucket
            s3_key: Key (path) of the S3 object
            local_file_path: Path to the local file
            chunk_size: Size of each chunk in bytes (default: 8MB, S3's default chunk size)

        Returns:
            Tuple containing:
            - S3 object's ETag (without quotes)
            - Local file's calculated ETag
            - Boolean indicating if the files are identical (True) or different (False)
        """
        try:
            # Get S3 object's ETag
            s3_object = self.s3_client.head_object(Bucket=_bucket_name, Key=_s3_key)
            s3_etag = s3_object["ETag"].strip('"')  # Remove surrounding quotes

            # Calculate local file's ETag
            local_etag = self.calculate_s3_etag(_local_file_path, _chunk_size)

            # Compare ETags
            files_match = s3_etag == local_etag

            return s3_etag, local_etag, files_match

        except Exception as e:
            raise Exception(f"Error comparing files using multipart ETag: {e}")

    def calculate_directory_etag(
        self, _directory_path: str, _chunk_size: int = 8 * 1024 * 1024
    ) -> str:
        """
        Calculate a composite ETag for a directory by combining ETags of all files within it.

        Args:
            directory_path: Path to the local directory
            chunk_size: Size of each chunk in bytes for file ETag calculations

        Returns:
            A composite ETag string representing the directory
        """
        if not os.path.isdir(_directory_path):
            raise ValueError(f"{_directory_path} is not a directory")

        # Get all files in the directory (recursively)
        all_files = []
        for root, _, files in os.walk(_directory_path):
            for file in files:
                all_files.append(os.path.join(root, file))

        # Sort files for consistent results
        all_files.sort()

        # Calculate ETag for each file and combine them
        file_etags = []
        for file_path in all_files:
            # Get relative path for consistent hashing regardless of directory location
            rel_path = os.path.relpath(file_path, _directory_path)
            file_etag = self.calculate_s3_etag(file_path, _chunk_size)
            file_etags.append(f"{rel_path}:{file_etag}")

        # Create a composite hash from all file ETags
        combined_string = ",".join(file_etags)
        return hashlib.md5(combined_string.encode()).hexdigest()

    def compare_directory_with_s3_prefix(
        self,
        _bucket_name: str,
        _s3_prefix: str,
        _local_dir_path: str,
        _chunk_size: int = 8 * 1024 * 1024,
    ) -> Dict[str, FileMetadata]:
        """
        Compare a local directory with objects under an S3 prefix.

        Args:
            bucket_name: Name of the S3 bucket
            s3_prefix: Prefix (path) in S3 to compare with
            local_dir_path: Path to the local directory
            chunk_size: Size of each chunk in bytes for ETag calculations

        Returns:
            Dictionary with comparison results including:
            - directory_etag: Composite ETag for the local directory
            - matching_files: List of files that match between local and S3
            - different_files: List of files with different ETags
            - missing_in_s3: Files in local directory not found in S3
            - missing_locally: Files in S3 not found in local directory
        """
        if not os.path.isdir(_local_dir_path):
            raise ValueError(f"{_local_dir_path} is not a directory")

        # Ensure s3_prefix ends with '/' if not empty
        if _s3_prefix and not _s3_prefix.endswith("/"):
            _s3_prefix += "/"

        # Get all S3 objects under the prefix
        s3_objects = self.list_file_metadata(_bucket_name, _s3_prefix)

        # Get all local files
        local_files : Dict[str, str] = {}
        for root, _, files in os.walk(_local_dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, _local_dir_path)
                # Convert Windows path separators to forward slashes for S3 compatibility
                rel_path = rel_path.replace("\\", "/")
                s3_key = _s3_prefix + rel_path
                local_files[s3_key] = file_path

        # Compare files
        matching_files : List[FileMetadata] = []
        different_files : List[DifferentFileMetadata] = []
        missing_in_s3 : List[FileMetadata] = []
        missing_locally : List[FileMetadata] = []

        # Check local files against S3
        for s3_key, local_path in local_files.items():
            if s3_key in [k for k in s3_objects if not k.endswith("/")]:
                local_etag = self.calculate_s3_etag(local_path, _chunk_size)
                if local_etag == s3_objects[s3_key].etag:
                    file_s3 = s3_objects[s3_key]
                    file_s3.last_modification_date = os.path.getmtime
                    matching_files.append(file_s3)
                else:
                    different_files.append(
                        DifferentFileMetadata.from_filemetadata(
                            s3_objects[s3_key],
                            os.path.getsize(local_path),
                            os.path.getmtime(local_path),
                            local_etag))
            else:
                file_os = FileMetadata(local_path, 
                                       os.path.basename(local_path),
                                       os.path.getsize(local_path),
                                       os.path.getctime(local_path),
                                       os.path.getmtime(local_path),
                                       local_etag)
                missing_in_s3.append(file_os)

        # Check for files in S3 but not locally
        for s3_key in s3_objects:
            if s3_key not in local_files:
                missing_locally.append(s3_key)

        # Calculate directory composite ETag
        directory_etag = self.calculate_directory_etag(_local_dir_path, _chunk_size)

        return {
            "directory_etag": directory_etag,
            "matching_files": matching_files,
            "different_files": different_files,
            "missing_in_s3": missing_in_s3,
            "missing_locally": missing_locally,
        }
