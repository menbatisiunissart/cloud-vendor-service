"""Type hints for commonly used AWS instances that are dynamically defined."""
from typing import Optional
import abc

class S3Client(abc.ABC):
    """Typing stub for the S3 client.

    The S3 client is created dynamically at runtime, so it is impossible to write type
    hints for an instance of it without defining this stub class.
    """

    @abc.abstractmethod
    def download_file(self, bucket_name: str, object_name: str, file_name: str, /):
        """Download a file from S3.

        :param bucket_name: The bucket name on S3.
        :param object_name: The path to the file relative to the bucket in S3.
        :param file_name: The local path to save the file to.
        """



    def upload_file(self, file_name: str, bucket: str, object_name: Optional[str]=None, /):
        """Upload a file to S3.

        :param file_name: The local path to the file.
        :param bucket: The bucket to store the file in.
        :param object_name: The path to the object on S3, relative to the bucket.
        """
