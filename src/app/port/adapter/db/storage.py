import uuid
from abc import ABC
from typing import List, Optional

from pydantic import BaseModel

from ..ports.user import UserData


class StorageData(BaseModel):
    path: str


class UploadUrlData(BaseModel):
    upload_url: str
    fields: dict


class StorageAdapter(ABC):
    def __init__(self) -> None:
        pass

    def generate_key(self, user_data: UserData, object_path: str) -> str:
        """
        Generate a unique key for the user in format:

        /<user_org_id>/<user_id>/<object_path or uuid>
        """
        object_path = object_path or str(uuid.uuid4())
        return f"{user_data.organisation_id}/{user_data.user_id}/{object_path}"

    def get_url(self, key: str) -> str:
        raise NotImplementedError

    def get_public_url(self, key: str) -> str:
        raise NotImplementedError

    def create_folder(self, path: str):
        raise NotImplementedError

    def list(self, path: str) -> List[str]:
        raise NotImplementedError

    def upload_url(self, path: str) -> UploadUrlData:
        raise NotImplementedError

    def save(self, source_file_path: str, target_file_path: str) -> StorageData:
        raise NotImplementedError

    def load(self, source_file_path: str, target_file_path: str) -> StorageData:
        raise NotImplementedError
