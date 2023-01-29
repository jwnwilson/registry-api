from typing import Optional

from pydantic import BaseModel


class UserData(BaseModel):
    user_id: str
    organisation_id: Optional[str] = None
