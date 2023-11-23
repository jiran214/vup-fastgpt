from typing import List, Optional

from pydantic import BaseModel
from scipy import spatial


class Record(BaseModel):
    event: dict
    prompt: str
    speech: str
    action: Optional[str] = None
    time: str