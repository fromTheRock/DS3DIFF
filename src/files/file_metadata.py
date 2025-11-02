"""
Class with Main data used to identify a single file,
Used to check differences between files stored in different archives
"""

import os
import datetime

class S3Consts:
    """Constannts for dict file metadata containter"""
    #list_objects_v2 - output dict keys
    F_DICT_KEY = 'Key'
    F_DICT_LAST_MODIFIED = 'LastModified'
    F_DICT_ETAG = 'ETag'
    F_DICT_SIZE = 'Size'
    F_DICT_STORAGE_CLASS = 'StorageClass'
    F_DICT_OWNER = 'Owner'

class FileMetadata:
    """Base object representing the file metadata from the filesysstem"""

    def __init__(self,
        _path: str, _name: str, _size: int,
        _creation_date, _last_modification_date,
        etag: str = None,
    ) -> None:
        self.path = _path
        self.name = _name
        self.full_path = os.path.join(_path, _name)
        _, file_extension = os.path.splitext(_name)
        self.extension = file_extension[1:] if file_extension else ""
        self.size = _size if _size else None
        self.etag = etag

        if _creation_date is None:
            self.creation_date = None
        elif isinstance(_creation_date, datetime.datetime):
            self.creation_date = _creation_date
        elif isinstance(_creation_date, (float, int)):
            self.creation_date = datetime.datetime.fromtimestamp(
                _creation_date, tz=datetime.timezone.utc
            )
        else:
            try:
                # To parse a datetime string, use datetime.strptime() with appropriate format string
                # Example: datetime.datetime.strptime(creation_date_str, '%Y-%m-%d %H:%M:%S')
                self.creation_date = datetime.datetime.strptime(
                    _creation_date.__str__, "%Y-%m-%d %H:%M:%S"
                )
            except ValueError:
                self.creation_date = None

        if _last_modification_date is None:
            self.last_modification_date = None
        if isinstance(_last_modification_date, datetime.datetime):
            self.last_modification_date = _last_modification_date
        elif isinstance(_last_modification_date, (float, int)):
            self.last_modification_date = datetime.datetime.fromtimestamp(
                _last_modification_date, tz=datetime.timezone.utc
            )
        else:
            try:
                # To parse a datetime string, use datetime.strptime() with appropriate format string
                # Example: datetime.datetime.strptime(creation_date_str, '%Y-%m-%d %H:%M:%S')
                self.last_modification_date = datetime.datetime.strptime(
                    _last_modification_date.__str__, "%Y-%m-%d %H:%M:%S"
                )
            except ValueError:
                self.last_modification_date = None

    def get_size(self) -> str:
        """
        Returns the size approssimated string in KB, MB etc...
        """
        if self.size < 1024:
            return f"{self.size} B"
        elif self.size < 1024 * 1024:
            return f"{self.size / 1024:.2f} KB"
        elif self.size < 1024 * 1024 * 1024:
            return f"{self.size / (1024 * 1024):.2f} MB"
        elif self.size < 1024 * 1024 * 1024 * 1024:
            return f"{self.size / (1024 * 1024 * 1024):.2f} GB"
        else:
            return f"{self.size / (1024 * 1024 * 1024 * 1024):.2f} TB"

    def __str__(self):
        return f'''{{"{S3Consts.F_DICT_KEY}": "{self.full_path}",
        "{S3Consts.F_DICT_LAST_MODIFIED}": "{self.last_modification_date}",
        "{S3Consts.F_DICT_ETAG}": "{self.etag}",
        "{S3Consts.F_DICT_SIZE}": "{self.size}"}}'''

    def __repr__(self):
        return f'''{{"path": "{self.full_path}", \
            "name": "{self.name}", \
            "extension": "{self.extension}", \
            "creation_date": {self.creation_date}, \
            "etag": "{self.etag}", \
            "size": {self.get_size()}, \
            "last_modification_date": {self.last_modification_date}}}'''

    def __eq__(self, other):
        """
        Define equality comparison between two FileMetadata objects.
        Two files are considered equal if they have the same path, name, and size.

        Args:
            other: Another FileMetadata object to compare with

        Returns:
            bool: True if the objects are equal, False otherwise
        """
        if not isinstance(other, FileMetadata):
            return False

        return (
            self.name == other.name
            and self.size == other.size
            and self.last_modification_date == other.last_modification_date
            and (
                self.creation_date is None
                or other.creation_date is None
                or self.creation_date == other.creation_date
            )
        )
