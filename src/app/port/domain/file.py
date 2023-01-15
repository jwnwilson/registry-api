from tempfile import SpooledTemporaryFile

from pydantic import BaseModel


class FileDTO(BaseModel):
    file: SpooledTemporaryFile
    filename: str
    content_type: str

    class Config:
        arbitrary_types_allowed = True
