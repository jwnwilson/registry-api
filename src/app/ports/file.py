from pydantic import BaseModel
from io import FileIO


class FileDTO(BaseModel):
    file: FileIO
    filename: str
    content_type: str

    class Config:
        arbitrary_types_allowed  = True
