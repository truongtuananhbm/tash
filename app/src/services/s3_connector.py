"""Define S3torage."""
import io
import logging
from typing import Optional

import boto3
from botocore.client import Config
from botocore.exceptions import NoCredentialsError


class S3Storage:
    """Define S3torage."""

    def __init__(self, s3_host: str, s3_public_key: str, s3_secret_key: str, s3_bucket: str, s3_region: str):
        """Define init."""
        self.s3_bucket = s3_bucket
        session = boto3.Session(aws_access_key_id=s3_public_key, aws_secret_access_key=s3_secret_key)
        self.client = session.client("s3",
                                     endpoint_url=s3_host,
                                     region_name=s3_region,
                                     config=Config(signature_version='s3v4'))

    def upload_file(self, local_file_path, s3_file_path):
        """Define upload file."""
        try:
            self.client.upload_file(local_file_path, self.aws_bucket_name, s3_file_path)
            print("Upload Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False

    def download_file(self, s3_file_path, local_file_path):
        """Define download file."""
        try:
            self.client.download_file(self.aws_bucket_name, s3_file_path, local_file_path)
            print("Download Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False

    def put_object(self, object_name: str, data: bytes) -> None:
        """Define put object."""
        self.client.upload_fileobj(
            io.BytesIO(data),
            Bucket=self.s3_bucket, Key=object_name)
        logging.info(f"Push {object_name} to bucket {self.s3_bucket} done")

    def get_object(self, object_name: str) -> Optional[bytes]:
        """Define get object."""
        file_obj = self.client.get_object(Bucket=self.s3_bucket, Key=object_name)
        file_content = file_obj["Body"].read()
        logging.info(f"Get object {object_name} from bucket {self.s3_bucket} done")
        return bytes(file_content)
