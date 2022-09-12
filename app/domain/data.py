import logging
import re
import uuid
from typing import List

import requests
from hex_lib.ports.db import DbAdapter
from hex_lib.ports.storage import StorageAdapter
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)


def get_file_name(url, response) -> str:
    fname = ""
    if "Content-Disposition" in response.headers.keys():
        fname = re.findall("filename=(.+)", response.headers["Content-Disposition"])[0]
    else:
        fname = url.split("/")[-1]

    return fname


def download_file(url, file_name=None) -> str:
    file_data = requests.get(url)
    file_name = file_name or get_file_name(url, file_data)
    file_path = f"/tmp/{file_name}"
    # save html template
    with open(file_path, "w") as fh:
        fh.write(file_data.text)

    return file_path


class BaseEntity:
    def __init__(
        self,
        db_adapter: DbAdapter,
        storage_adapter: StorageAdapter,
    ):
        self.db_adapter = db_adapter
        self.storage_adapter = storage_adapter


class DataEntity(BaseEntity):
    def list(self) -> List[str]:
        """List data"""
        folders: List[str] = self.storage_adapter.list(
            "/", include_files=False
        )
        return [f.split("/")[1] for f in folders]
