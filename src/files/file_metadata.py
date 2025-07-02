"""
Class with Main data used to identify a single file,
Used to check differences between files stored in different archives
"""

import os
import datetime


class FileMetadata:
    """Base object representing the file metadata from the filesysstem"""

    path = ""
    name = ""
    extension = ""
    size = 0
    creation_date = None
    last_modification_date = None
    etag = None

    def __init__(
        self,
        path: str,
        name: str,
        size: int,
        creation_date,
        last_modification_date,
        etag: str = None,
    ) -> None:
        self.path = path
        self.name = name
        _, file_extension = os.path.splitext(name)
        self.extension = file_extension[1:] if file_extension else ""
        self.size = size if size else None
        self.etag = etag

        if creation_date is None:
            self.creation_date = None
        elif isinstance(creation_date, datetime.datetime):
            self.creation_date = creation_date
        elif isinstance(creation_date, (float, int)):
            self.creation_date = datetime.datetime.fromtimestamp(
                creation_date, tz=datetime.timezone.utc
            )
        else:
            try:
                # To parse a datetime string, use datetime.strptime() with appropriate format string
                # Example: datetime.datetime.strptime(creation_date_str, '%Y-%m-%d %H:%M:%S')
                self.creation_date = datetime.datetime.strptime(
                    creation_date.__str__, "%Y-%m-%d %H:%M:%S"
                )
            except ValueError:
                self.creation_date = None

        if last_modification_date is None:
            self.last_modification_date = None
        if isinstance(last_modification_date, datetime.datetime):
            self.last_modification_date = last_modification_date
        elif isinstance(last_modification_date, (float, int)):
            self.last_modification_date = datetime.datetime.fromtimestamp(
                last_modification_date, tz=datetime.timezone.utc
            )
        else:
            try:
                # To parse a datetime string, use datetime.strptime() with appropriate format string
                # Example: datetime.datetime.strptime(creation_date_str, '%Y-%m-%d %H:%M:%S')
                self.last_modification_date = datetime.datetime.strptime(
                    last_modification_date.__str__, "%Y-%m-%d %H:%M:%S"
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
        return f"""{self.name}, Size: {self.get_size()}, \
            Creation Date: {self.creation_date}, \
            Last Modification Date: {self.last_modification_date}"""

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
