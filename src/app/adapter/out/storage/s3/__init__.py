import logging
import os
from typing import List

import boto3

from hex_lib.ports.storage import StorageAdapter, StorageData, UploadUrlData
from hex_lib.ports.user import UserData

ENVIRONMENT = os.environ.get("ENVIRONMENT", "")
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "eu-west-1")
logger = logging.getLogger(__name__)


class S3Adapter(StorageAdapter):
    def __init__(self, config: dict, user: UserData, upload_prefix: str) -> None:
        self.bucket_name = config["bucket"]
        self.s3 = boto3.resource("s3")
        self.client = boto3.client("s3")
        self.bucket = self.s3.Bucket(self.bucket_name)
        self.user = user

        self.url_prefix = (
            f"https://{self.bucket_name}.s3-{AWS_DEFAULT_REGION}.amazonaws.com/"
        )
        self.upload_prefix = upload_prefix
        self.upload_user_access_id = (
            f"/{self.upload_prefix}/upload_access_id_{ENVIRONMENT}"
        )
        self.upload_user_secret_key = (
            f"/{self.upload_prefix}/upload_secret_key_{ENVIRONMENT}"
        )
        self.public_url_timeout = 3600

    def _get_upload_client(self):
        client = boto3.client("ssm")
        access_id = client.get_parameter(
            Name=self.upload_user_access_id, WithDecryption=True
        )
        secret_key = client.get_parameter(
            Name=self.upload_user_secret_key, WithDecryption=True
        )
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=access_id["Parameter"]["Value"],
            aws_secret_access_key=secret_key["Parameter"]["Value"],
        )

        return s3_client

    def get_url(self, key: str) -> str:
        return self.url_prefix + key

    def get_key(self, url: str) -> str:
        key = url.replace(self.url_prefix, "")
        return key

    def get_public_url(self, storage_path: str) -> str:
        key = self.generate_key(self.user, storage_path)
        public_url: str = self._get_upload_client().generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket_name, "Key": key},
            ExpiresIn=self.public_url_timeout,
        )
        return public_url

    def create_folder(self, path):
        path = self.generate_key(self.user, path)
        self.client.put_object(Bucket=self.bucket_name, Body="", Key=path)

    def upload_url(self, path: str) -> UploadUrlData:
        path = self.generate_key(self.user, path)
        upload_data = self._get_upload_client().generate_presigned_post(
            Bucket=self.bucket_name, Key=path, ExpiresIn=self.public_url_timeout
        )
        return UploadUrlData(
            upload_url=upload_data["url"], fields=upload_data["fields"]
        )

    def list(
        self, path: str, include_files=True, include_folders=True, as_urls=False
    ) -> List[str]:
        prefix = self.generate_key(self.user, path)
        objs = self.client.list_objects_v2(
            Bucket=self.bucket_name, Prefix=prefix, Delimiter="/"
        )
        results: List[str] = []
        if include_files:
            results = results + [obj["Key"] for obj in objs.get("Contents", [])]
        if include_folders:
            results = results + [
                obj["Prefix"] for obj in objs.get("CommonPrefixes", [])
            ]
        if as_urls:
            results = [self.get_url(r) for r in results]
        return sorted(results)

    def save(self, source_path: str, target_path: str) -> StorageData:
        target_path = self.generate_key(self.user, target_path)
        logger.info(
            f"Saving file: {source_path} to s3 bucket: {self.bucket_name}, key: {target_path}"
        )
        self.bucket.upload_file(source_path, target_path)
        return StorageData(path=self.get_url(target_path))

    def load(self, source_path: str, target_path: str):
        logger.info(
            f"Loading file: {source_path} from s3 bucket: {self.bucket_name}, to path: {target_path}"
        )
        target_dir = "/".join(target_path.split("/")[:-1])
        os.makedirs(target_dir, exist_ok=True)
        self.client.download_file(self.bucket_name, source_path, target_path)
