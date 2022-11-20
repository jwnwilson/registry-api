from pydantic import BaseModel
from tempfile import SpooledTemporaryFile


class FileDTO(BaseModel):
    file: SpooledTemporaryFile
    filename: str
    content_type: str

    class Config:
        arbitrary_types_allowed  = True
